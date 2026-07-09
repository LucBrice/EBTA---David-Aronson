param(
    [string]$DriveLetter = "N",
    [string]$VenvRelativePath = "Implementation\.venv-nautilus",
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$implementationRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
$repoRoot = Split-Path -Parent $implementationRoot
$target = (Resolve-Path -LiteralPath $repoRoot).Path
$drive = "$DriveLetter`:"
$requirementsPath = Join-Path $scriptDir "requirements.txt"

if (-not (Test-Path -LiteralPath $requirementsPath)) {
    throw "Missing requirements file: $requirementsPath"
}

$existing = (& subst) | Where-Object { $_ -like "$drive\*" }
if ($existing) {
    $existingTarget = ($existing -replace "^[A-Z]:\\: => ", "").Trim()
    if ($existingTarget -eq $target) {
        # Mapping already matches the reproducible short-drive convention.
    } elseif ($existingTarget.StartsWith($target, [System.StringComparison]::OrdinalIgnoreCase)) {
        & subst $drive /D
        & subst $drive $target
    } else {
        throw "$drive is already mapped to another path: $existing"
    }
} else {
    & subst $drive $target
}

$venvPath = Join-Path $drive $VenvRelativePath
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonExe)) {
    python -m venv $venvPath
}

if (-not $SkipInstall) {
    & $pythonExe -m pip install --upgrade pip
    & $pythonExe -m pip install -r $requirementsPath
}

& $pythonExe -c "import nautilus_trader, sys; from nautilus_trader.backtest.engine import BacktestEngine; from nautilus_trader.config import BacktestEngineConfig, LoggingConfig; engine = BacktestEngine(config=BacktestEngineConfig(logging=LoggingConfig(log_level='ERROR'))); print('nautilus_trader', nautilus_trader.__version__); print(sys.executable); print(type(engine.cache).__name__); engine.dispose()"
