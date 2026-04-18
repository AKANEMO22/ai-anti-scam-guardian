#!/usr/bin/env python3
"""
generate_tflite.py

Simple utility to create placeholder .tflite files (zero-filled or random) for local testing.

Usage examples:
  python scripts/generate_models/generate_tflite.py --output lane-end-user/core/ml/src/main/assets/scam_detector_en.tflite --size-mb 5
  python scripts/generate_models/generate_tflite.py -o assets/my_model.tflite -s 100 --random --force

Note: By default the script refuses to create files larger than 500MB unless `--force` is provided.
"""
import argparse
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Generate placeholder .tflite files.")
    p.add_argument("--output", "-o", default="lane-end-user/core/ml/src/main/assets/scam_detector_en.tflite",
                   help="Output file path (will create parent dirs)")
    p.add_argument("--size-mb", "-s", type=int, default=5,
                   help="Size in megabytes to create (default 5MB)")
    p.add_argument("--random", action="store_true", help="Fill with random bytes instead of zeros (slower)")
    p.add_argument("--force", action="store_true", help="Allow sizes greater than the safe default limit")
    return p.parse_args()


def generate_file(path: str, size_bytes: int, random_fill: bool = False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    chunk = 1024 * 1024
    written = 0
    with open(path, "wb") as f:
        if random_fill:
            import os
            while written < size_bytes:
                to_write = min(chunk, size_bytes - written)
                f.write(os.urandom(to_write))
                written += to_write
        else:
            zero_chunk = b"\0" * chunk
            while written < size_bytes:
                to_write = min(chunk, size_bytes - written)
                if to_write == chunk:
                    f.write(zero_chunk)
                else:
                    f.write(zero_chunk[:to_write])
                written += to_write


def main():
    args = parse_args()
    safe_limit_mb = 500
    if args.size_mb > safe_limit_mb and not args.force:
        print(f"Refusing to create files >{safe_limit_mb}MB without --force. Use --force to override.", file=sys.stderr)
        sys.exit(2)

    size_bytes = args.size_mb * 1024 * 1024
    print(f"Generating {args.size_mb} MB file at {args.output} (random={args.random})")
    try:
        generate_file(args.output, size_bytes, args.random)
    except Exception as e:
        print("Error while generating file:", e, file=sys.stderr)
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
