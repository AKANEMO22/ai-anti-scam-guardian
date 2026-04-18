Param()

Write-Host "Setup lanes: installing Python dependencies for api-gateway, agentic-core, and storage" -ForegroundColor Cyan

python -V
python -m pip install --upgrade pip

try {
    Write-Host "Installing api-gateway requirements..."
    python -m pip install -r ..\lane-api-gateway\python-api-gateway\requirements.txt
} catch {
    Write-Host "Failed installing api-gateway requirements: $_" -ForegroundColor Red
}

try {
    Write-Host "Installing agentic-core requirements..."
    python -m pip install -r ..\lane-agentic-core\python-agentic-core\requirements.txt
} catch {
    Write-Host "Failed installing agentic-core requirements: $_" -ForegroundColor Red
}

try {
    Write-Host "Installing storage requirements (may fail for faiss on Windows)..."
    python -m pip install -r ..\lane-storage\python-storage\requirements.txt
} catch {
    Write-Host "Storage requirements install failed. If the failure is due to faiss, see the README or use WSL/Conda:" -ForegroundColor Yellow
    Write-Host "  - On Windows: install Anaconda, create conda env, then 'conda install -c pytorch faiss-cpu' or use WSL" -ForegroundColor Yellow
}

Write-Host "Done. If any step failed, read the printed hints above." -ForegroundColor Green
