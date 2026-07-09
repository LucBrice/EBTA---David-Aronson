param(
    [string]$DriveLetter = "N",
    [string]$VenvRelativePath = "Implementation\.venv-nautilus",
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $scriptDir "setup_env.ps1") -DriveLetter $DriveLetter -VenvRelativePath $VenvRelativePath -SkipInstall:$SkipInstall
