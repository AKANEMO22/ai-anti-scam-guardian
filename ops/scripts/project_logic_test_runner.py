from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

CODE_EXTENSIONS = {".py", ".kt", ".kts", ".java", ".dart"}
EXCLUDED_DIRS = {
    ".git",
    ".gradle",
    "build",
    "apk-output",
    "__pycache__",
    ".idea",
    ".venv",
    "venv",
    "node_modules",
}

COMMON_SYMBOLS = {
    "main",
    "build",
    "copy",
    "run",
    "test",
    "create",
    "update",
    "delete",
    "get",
    "set",
    "list",
    "map",
    "init",
}

TEXT_STUB_PATTERNS = [
    r"NotImplementedError",
    r"UnimplementedError",
    r"UnsupportedOperationException",
    r"\bTODO\s*[:(]",
    r"\breturn\s+null\b",
    r"throw\s+NotImplementedError",
    r"throw\s+UnimplementedError",
    r"throw\s+UnsupportedOperationException",
]

FUNCTION_PATTERNS = {
    ".kt": [
        re.compile(r"\bfun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("),
    ],
    ".kts": [
        re.compile(r"\bfun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("),
    ],
    ".java": [
        re.compile(
            r"\b(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?"
            r"(?:[A-Za-z_][A-Za-z0-9_<>,?.\[\]]*\s+)+([A-Za-z_][A-Za-z0-9_]*)\s*\("
        ),
    ],
    ".dart": [
        re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\("),
    ],
}


@dataclass
class FunctionRecord:
    symbol: str
    file_path: str
    language: str
    start_line: int
    end_line: int
    is_stub: bool
    stub_reason: str | None


@dataclass
class FileResult:
    path: str
    status: str
    language: str
    functions_total: int
    functions_stubbed: int
    issues: list[str]


@dataclass
class DependencyIssue:
    symbol: str
    definition_file: str
    caller_file: str
    caller_line: int


@dataclass
class ParseIssue:
    file_path: str
    message: str


def _is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def discover_code_files(repo_root: Path, scopes: list[str]) -> list[Path]:
    roots: list[Path]
    if scopes:
        roots = [(repo_root / scope).resolve() for scope in scopes]
    else:
        roots = [repo_root]

    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            if _is_excluded(file_path.relative_to(repo_root)):
                continue
            if file_path.suffix.lower() in CODE_EXTENSIONS:
                files.append(file_path)

    # Deduplicate when multiple scopes overlap.
    unique = sorted(set(files))
    return unique


def discover_all_files(repo_root: Path, scopes: list[str]) -> list[Path]:
    roots: list[Path]
    if scopes:
        roots = [(repo_root / scope).resolve() for scope in scopes]
    else:
        roots = [repo_root]

    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            if _is_excluded(file_path.relative_to(repo_root)):
                continue
            files.append(file_path)

    return sorted(set(files))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def _strip_docstring(stmts: list[ast.stmt]) -> list[ast.stmt]:
    if not stmts:
        return stmts
    first = stmts[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return stmts[1:]
    return stmts


def _is_raise_not_implemented(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or stmt.exc is None:
        return False

    exc = stmt.exc
    if isinstance(exc, ast.Name):
        return exc.id in {"NotImplementedError", "NotImplemented"}
    if isinstance(exc, ast.Call):
        if isinstance(exc.func, ast.Name):
            return exc.func.id in {"NotImplementedError", "NotImplemented"}
    return False


def _is_return_none(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Return):
        return False
    return stmt.value is None or (isinstance(stmt.value, ast.Constant) and stmt.value.value is None)


def _python_function_stub(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[bool, str | None]:
    body = _strip_docstring(node.body)
    if not body:
        return True, "empty-body"

    if all(isinstance(stmt, ast.Pass) for stmt in body):
        return True, "pass-only"

    if all(_is_raise_not_implemented(stmt) for stmt in body):
        return True, "raise-not-implemented"

    if all(_is_return_none(stmt) for stmt in body):
        return True, "return-none-only"

    if len(body) == 1 and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        if body[0].value.value is Ellipsis:
            return True, "ellipsis-only"

    return False, None


def parse_python_functions(file_path: Path, text: str, rel_path: str) -> tuple[list[FunctionRecord], list[ParseIssue]]:
    records: list[FunctionRecord] = []
    parse_issues: list[ParseIssue] = []

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        parse_issues.append(ParseIssue(file_path=rel_path, message=f"SyntaxError: {exc}"))
        return records, parse_issues

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        start_line = int(getattr(node, "lineno", 1))
        end_line = int(getattr(node, "end_lineno", start_line))
        is_stub, reason = _python_function_stub(node)

        records.append(
            FunctionRecord(
                symbol=node.name,
                file_path=rel_path,
                language="python",
                start_line=start_line,
                end_line=end_line,
                is_stub=is_stub,
                stub_reason=reason,
            )
        )

    return records, parse_issues


def _find_brace_block(text: str, from_index: int) -> tuple[int, int] | None:
    open_index = text.find("{", from_index)
    if open_index == -1:
        return None

    depth = 0
    for index in range(open_index, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return open_index, index

    return None


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _is_text_block_stub(block_text: str) -> tuple[bool, str | None]:
    for pattern in TEXT_STUB_PATTERNS:
        if re.search(pattern, block_text):
            return True, f"matched:{pattern}"

    # Remove comments and whitespace to detect effectively-empty function blocks.
    compact = re.sub(r"//.*", "", block_text)
    compact = re.sub(r"/\*.*?\*/", "", compact, flags=re.DOTALL)
    compact = re.sub(r"\s+", "", compact)

    if compact in {"{}", "{;}", "{return;}"}:
        return True, "empty-block"

    return False, None


def parse_brace_language_functions(file_path: Path, text: str, rel_path: str) -> tuple[list[FunctionRecord], list[ParseIssue]]:
    records: list[FunctionRecord] = []
    parse_issues: list[ParseIssue] = []

    suffix = file_path.suffix.lower()
    patterns = FUNCTION_PATTERNS.get(suffix, [])

    for pattern in patterns:
        for match in pattern.finditer(text):
            symbol = match.group(1)

            # Dart regex is broad. Skip control keywords and language primitives.
            if suffix == ".dart" and symbol in {"if", "for", "while", "switch", "catch", "return", "throw"}:
                continue

            block = _find_brace_block(text, match.end())
            if block is None:
                continue

            block_start, block_end = block
            start_line = _line_number(text, match.start())
            end_line = _line_number(text, block_end)
            block_text = text[block_start : block_end + 1]
            is_stub, reason = _is_text_block_stub(block_text)

            records.append(
                FunctionRecord(
                    symbol=symbol,
                    file_path=rel_path,
                    language=suffix.lstrip("."),
                    start_line=start_line,
                    end_line=end_line,
                    is_stub=is_stub,
                    stub_reason=reason,
                )
            )

    return records, parse_issues


def parse_file_functions(repo_root: Path, file_path: Path, text: str) -> tuple[list[FunctionRecord], list[ParseIssue]]:
    rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")

    if file_path.suffix.lower() == ".py":
        return parse_python_functions(file_path, text, rel_path)

    return parse_brace_language_functions(file_path, text, rel_path)


def collect_references(
    symbol: str,
    definition_file: str,
    definition_line: int,
    file_text_map: dict[str, str],
) -> list[tuple[str, int]]:
    if len(symbol) < 4 or symbol.lower() in COMMON_SYMBOLS:
        return []

    pattern = re.compile(rf"\b{re.escape(symbol)}\s*\(")
    references: list[tuple[str, int]] = []

    for file_path, text in file_text_map.items():
        lines = text.splitlines()
        for match in pattern.finditer(text):
            line = _line_number(text, match.start())
            line_text = lines[line - 1] if line - 1 < len(lines) else ""

            # Skip function declarations to reduce false positives.
            if re.search(
                rf"\b(def|fun|class|interface|object)\b[^\n]*\b{re.escape(symbol)}\s*\(",
                line_text,
            ):
                continue

            if file_path == definition_file and line == definition_line:
                continue

            references.append((file_path, line))

    return references


def build_file_results(
    file_list: list[str],
    records: list[FunctionRecord],
    parse_issues: list[ParseIssue],
) -> list[FileResult]:
    issues_by_file: dict[str, list[str]] = {path: [] for path in file_list}
    funcs_by_file: dict[str, list[FunctionRecord]] = {path: [] for path in file_list}

    for issue in parse_issues:
        issues_by_file.setdefault(issue.file_path, []).append(issue.message)

    for record in records:
        funcs_by_file.setdefault(record.file_path, []).append(record)
        if record.is_stub:
            issues_by_file.setdefault(record.file_path, []).append(
                f"stub-function:{record.symbol} ({record.stub_reason})"
            )

    results: list[FileResult] = []
    for path in file_list:
        funcs = funcs_by_file.get(path, [])
        issues = issues_by_file.get(path, [])
        status = "DONE" if not issues else "NOT_DONE"

        suffix = Path(path).suffix.lower().lstrip(".")
        results.append(
            FileResult(
                path=path,
                status=status,
                language=suffix,
                functions_total=len(funcs),
                functions_stubbed=sum(1 for item in funcs if item.is_stub),
                issues=issues,
            )
        )

    return sorted(results, key=lambda item: item.path)


def run_logic_check(repo_root: Path, scopes: list[str]) -> dict[str, object]:
    all_files = discover_all_files(repo_root, scopes)
    code_files = [path for path in all_files if path.suffix.lower() in CODE_EXTENSIONS]
    file_text_map: dict[str, str] = {}
    parse_issues: list[ParseIssue] = []
    records: list[FunctionRecord] = []

    for file_path in code_files:
        rel = str(file_path.relative_to(repo_root)).replace("\\", "/")
        text = read_text(file_path)
        file_text_map[rel] = text

        parsed_records, parsed_issues = parse_file_functions(repo_root, file_path, text)
        records.extend(parsed_records)
        parse_issues.extend(parsed_issues)

    dependency_issues: list[DependencyIssue] = []
    symbol_definitions: dict[str, list[FunctionRecord]] = {}
    for record in records:
        symbol_definitions.setdefault(record.symbol, []).append(record)

    for record in records:
        if not record.is_stub:
            continue

        # Only evaluate dependency usage when symbol definition is unique.
        if len(symbol_definitions.get(record.symbol, [])) != 1:
            continue

        references = collect_references(
            symbol=record.symbol,
            definition_file=record.file_path,
            definition_line=record.start_line,
            file_text_map=file_text_map,
        )
        for caller_file, caller_line in references:
            dependency_issues.append(
                DependencyIssue(
                    symbol=record.symbol,
                    definition_file=record.file_path,
                    caller_file=caller_file,
                    caller_line=caller_line,
                )
            )

    code_file_list = list(file_text_map.keys())
    file_results = build_file_results(
        file_list=code_file_list,
        records=records,
        parse_issues=parse_issues,
    )

    # Explicitly include non-code files as skipped so report covers whole project scope.
    code_set = set(code_file_list)
    for file_path in all_files:
        rel = str(file_path.relative_to(repo_root)).replace("\\", "/")
        if rel in code_set:
            continue
        file_results.append(
            FileResult(
                path=rel,
                status="SKIPPED_NON_CODE",
                language=file_path.suffix.lower().lstrip("."),
                functions_total=0,
                functions_stubbed=0,
                issues=[],
            )
        )

    file_results = sorted(file_results, key=lambda item: item.path)

    functions_total = len(records)
    functions_stubbed = sum(1 for record in records if record.is_stub)
    functions_implemented = functions_total - functions_stubbed

    summary = {
        "projectFilesTotal": len(all_files),
        "codeFilesScanned": len(code_file_list),
        "nonCodeFilesSkipped": len(all_files) - len(code_file_list),
        "filesScanned": len(file_results),
        "functionsTotal": functions_total,
        "functionsImplemented": functions_implemented,
        "functionsStubbed": functions_stubbed,
        "dependencyFailures": len(dependency_issues),
        "syntaxErrors": len(parse_issues),
        "fileDone": sum(1 for item in file_results if item.status == "DONE"),
        "fileNotDone": sum(1 for item in file_results if item.status == "NOT_DONE"),
        "fileSkipped": sum(1 for item in file_results if item.status == "SKIPPED_NON_CODE"),
    }

    overall_pass = (
        summary["syntaxErrors"] == 0
        and summary["functionsStubbed"] == 0
        and summary["dependencyFailures"] == 0
    )

    payload = {
        "checkedAt": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "scope": scopes if scopes else ["ALL_PROJECT"],
        "pass": overall_pass,
        "passCriteria": {
            "syntaxErrors": 0,
            "functionsStubbed": 0,
            "dependencyFailures": 0,
        },
        "summary": summary,
        "syntaxIssues": [asdict(issue) for issue in parse_issues],
        "dependencyIssues": [asdict(issue) for issue in dependency_issues],
        "files": [asdict(item) for item in file_results],
    }

    return payload


def render_console(payload: dict[str, object], max_file_lines: int = 20) -> None:
    summary = payload["summary"]

    print("=== Project Logic Test Summary ===")
    print(f"Scope: {', '.join(payload['scope'])}")
    print(f"PASS: {payload['pass']}")
    print(f"Project files total: {summary['projectFilesTotal']}")
    print(f"Code files scanned: {summary['codeFilesScanned']}")
    print(f"Non-code files skipped: {summary['nonCodeFilesSkipped']}")
    print(f"Files in report: {summary['filesScanned']}")
    print(f"Functions total: {summary['functionsTotal']}")
    print(f"Functions implemented: {summary['functionsImplemented']}")
    print(f"Functions stubbed: {summary['functionsStubbed']}")
    print(f"Dependency failures: {summary['dependencyFailures']}")
    print(f"Syntax errors: {summary['syntaxErrors']}")
    print(f"File DONE: {summary['fileDone']}")
    print(f"File NOT_DONE: {summary['fileNotDone']}")
    print(f"File SKIPPED_NON_CODE: {summary['fileSkipped']}")

    files = payload["files"]
    not_done = [item for item in files if item["status"] == "NOT_DONE"]
    if not_done:
        print("--- NOT_DONE Files (top) ---")
        for item in not_done[:max_file_lines]:
            print(f"[NOT_DONE] {item['path']}")
            for issue in item["issues"][:3]:
                print(f"  - {issue}")

    dep_issues = payload["dependencyIssues"]
    if dep_issues:
        print("--- Dependency Failures (top) ---")
        for issue in dep_issues[:max_file_lines]:
            print(
                f"- symbol={issue['symbol']} def={issue['definition_file']} "
                f"caller={issue['caller_file']}:{issue['caller_line']}"
            )


def write_report(report_dir: Path, report_name: str, payload: dict[str, object]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = str(payload["checkedAt"])
    latest_path = report_dir / report_name
    history_path = report_dir / f"logic_status_{timestamp}.json"

    latest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    history_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return latest_path


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Logic-focused project test runner: scan all code files, detect stubbed functions, "
            "and fail when stubbed functions are referenced by other files."
        )
    )
    parser.add_argument("--repo-root", help="Repository root path", default=None)
    parser.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Relative folder scope (can be repeated). Example: --scope lane-storage",
    )
    parser.add_argument("--report-dir", required=True, help="Directory to write report JSON files")
    parser.add_argument("--report-name", default="latest_report.json", help="Latest report file name")
    parser.add_argument(
        "--strict-exit",
        action="store_true",
        help="Exit with code 1 when overall PASS is false",
    )
    parser.add_argument(
        "--max-file-lines",
        type=int,
        default=20,
        help="Max NOT_DONE and dependency lines to print in console",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    script_path = Path(__file__).resolve()
    default_repo_root = script_path.parents[2]
    repo_root = Path(args.repo_root).resolve() if args.repo_root else default_repo_root

    payload = run_logic_check(repo_root=repo_root, scopes=args.scope)
    render_console(payload, max_file_lines=args.max_file_lines)

    report_path = write_report(Path(args.report_dir).resolve(), args.report_name, payload)
    print(f"Report written: {report_path}")

    if args.strict_exit and not payload["pass"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
