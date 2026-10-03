[CmdletBinding()]
param([string]$PythonPath='D:\Tools\Python\3.14\python.exe',[switch]$IncludeBrowser)
$ErrorActionPreference='Stop'
if($env:COMPUTERNAME -ieq '398F536') {
    $identity=[Security.Principal.WindowsIdentity]::GetCurrent()
    if([Environment]::UserName -ne 'developer' -or ([Security.Principal.WindowsPrincipal]::new($identity)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){throw 'On 398F536, use ordinary developer PowerShell for this project setup.'}
}
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not (Test-Path -LiteralPath (Join-Path $root 'worker\requirements.txt') -PathType Leaf)) {throw 'Run from the complete price-compare repository.'}
function Invoke-PriceCompareCommand {
    param([string]$Executable,[string[]]$Arguments)
    & $Executable @Arguments
    if($LASTEXITCODE -ne 0){throw 'Price-compare setup/validation command failed. No insurer request was made by setup.'}
}
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    if ($env:COMPUTERNAME -ine '398F536' -or [Environment]::UserName -ne 'developer' -or $PythonPath -ne 'D:\Tools\Python\3.14\python.exe') {throw 'Supply -PythonPath with an existing Python 3.12+ executable; automatic installation is limited to developer on 398F536.'}
    $identity=[Security.Principal.WindowsIdentity]::GetCurrent()
    if(([Security.Principal.WindowsPrincipal]::new($identity)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){throw 'Use ordinary developer PowerShell; Python installation requests separate elevation.'}
    $installerRoot='D:\Installers\Python'
    New-Item -ItemType Directory -Path $installerRoot -Force | Out-Null
    $installer=Join-Path $installerRoot 'python-3.14.8-amd64.exe'
    if(-not(Test-Path -LiteralPath $installer)){Write-Output 'Downloading the official Python 3.14.8 installer...';Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.14.8/python-3.14.8-amd64.exe' -OutFile $installer}
    if((Get-FileHash -LiteralPath $installer).Hash -ne '759BE887B96E736A3CA886DAF8D575F18FCAE1A09EFAB6902F42D59E8999F8EF'){throw 'Python installer differs from the published SHA256; it was not run.'}
    $signature=Get-AuthenticodeSignature -LiteralPath $installer
    if($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation'){throw 'Python installer signature was not verified; it was not run.'}
    $helper=Join-Path $PSScriptRoot 'Install-PriceComparePython.ps1'
    if(-not(Test-Path -LiteralPath $helper -PathType Leaf)){throw 'Python installer helper is missing; update the complete repository.'}
    Write-Output 'Approve the administrator prompt for Python installation on D:. Project dependencies and tests will continue as developer.'
    $powershell=Join-Path $PSHOME $(if($PSVersionTable.PSEdition -eq 'Desktop'){'powershell.exe'}else{'pwsh.exe'})
    $process=Start-Process -FilePath $powershell -Verb RunAs -ArgumentList @('-NoProfile','-File',('"'+$helper+'"')) -WindowStyle Hidden -Wait -PassThru
    if($process.ExitCode -ne 0 -or -not(Test-Path -LiteralPath $PythonPath -PathType Leaf)){throw 'Python administrator installation did not complete. Keep D:\Installers\Python\install-* logs and failure.json; no policy was changed. Do not rerun the whole project setup elevated.'}
}
$probe=@(& $PythonPath -c 'import sys; print(sys.version.split()[0]); print(int(sys.version_info >= (3,12))); print(sys.maxsize > 2**32)')
if($LASTEXITCODE -ne 0 -or $probe.Count -ne 3 -or $probe[1] -ne '1' -or $probe[2] -ne 'True'){throw 'Expected Python 3.12+ x64 executable was not verified.'}
$venv=Join-Path $root '.venv';$venvPython=Join-Path $venv 'Scripts\python.exe'
if (-not(Test-Path -LiteralPath $venvPython)) {
    if(Test-Path -LiteralPath $venv){throw 'Incomplete project virtual environment exists; no overwrite. Report its path.'}
    Invoke-PriceCompareCommand $PythonPath @('-m','venv',$venv)
}
$cache=$(if($env:COMPUTERNAME -ieq '398F536'){'D:\UserData\developer\Caches\pip'}else{Join-Path $root '.local\pip-cache'})
New-Item -ItemType Directory -Path $cache -Force | Out-Null
Invoke-PriceCompareCommand $venvPython @('-m','pip','install','--cache-dir',$cache,'--disable-pip-version-check','-r',(Join-Path $root 'worker\requirements.txt'))
if($IncludeBrowser){
    $browserCache=$(if($env:COMPUTERNAME -ieq '398F536'){'D:\UserData\developer\Caches\playwright'}else{Join-Path $root '.local\playwright'})
    New-Item -ItemType Directory -Path $browserCache -Force | Out-Null
    $env:PLAYWRIGHT_BROWSERS_PATH=$browserCache
    if($env:COMPUTERNAME -ieq '398F536'){[Environment]::SetEnvironmentVariable('PLAYWRIGHT_BROWSERS_PATH',$browserCache,'User')}
    Invoke-PriceCompareCommand $venvPython @('-m','pip','install','--cache-dir',$cache,'--disable-pip-version-check','-r',(Join-Path $root 'worker\requirements-browser.txt'))
    Invoke-PriceCompareCommand $venvPython @('-m','playwright','install','chromium')
    Invoke-PriceCompareCommand $venvPython @('-c','from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); page=b.new_page(); page.set_content("<title>Offline browser check</title>"); assert page.title()=="Offline browser check"; b.close(); p.stop(); print("Offline Chromium launch passed")')
}
Write-Output 'Running the offline worker tests; no insurer or portal is contacted...'
Invoke-PriceCompareCommand $venvPython @('-m','unittest','discover','-s',(Join-Path $root 'worker'),'-p','test_collect_quote.py','-v')
Invoke-PriceCompareCommand $venvPython @('-m','pip','check')
$records=Join-Path $root ('.local\setup-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $records -Force | Out-Null
$result=[pscustomobject]@{Computer=$env:COMPUTERNAME;Account=[Security.Principal.WindowsIdentity]::GetCurrent().Name;Project=$root;BasePython=$PythonPath;PythonVersion=$probe[0];ProjectPython=$venvPython;PipCache=$cache;BrowserPrepared=[bool]$IncludeBrowser;BrowserCache=$(if($IncludeBrowser){$browserCache}else{$null});OfflineTestsPassed=$true;InsurerRequestsMade=$false;PortalOrSqlChanged=$false;Records=$records;CompletedAtUtc=(Get-Date).ToUniversalTime().ToString('o')}
$result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $records 'result.json') -Encoding utf8
$result | Format-List
Write-Output 'Project setup and offline validation passed. Open this repository root as a local desktop project. Start a fresh desktop chat so newly saved browser-cache settings reach it.'
