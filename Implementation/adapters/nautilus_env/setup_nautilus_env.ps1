param(
    [string]$DriveLetter = "N",
    [string]$PackageVersion = "1.230.0"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = (Resolve-Path -LiteralPath $scriptDir).Path
$drive = "$DriveLetter`:"
$venvPath = "$drive\venv"
$pythonExe = "$venvPath\Scripts\python.exe"

$existing = (& subst) | Where-Object { $_ -like "$drive\*" }
if ($existing) {
    if ($existing -notlike "*$target") {
        throw "$drive is already mapped to another path: $existing"
    }
} else {
    & subst $drive $target
}

if (-not (Test-Path -LiteralPath $pythonExe)) {
    python -m venv $venvPath
}

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install "nautilus_trader==$PackageVersion"
& $pythonExe -c "import nautilus_trader, sys; print('nautilus_trader', nautilus_trader.__version__); print(sys.executable)"
