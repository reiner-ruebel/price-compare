[CmdletBinding()]
param([string]$PythonPath='D:\Tools\Python\3.14\python.exe',[switch]$IncludeBrowser)
$ErrorActionPreference='Stop'
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
    if(([Security.Principal.WindowsPrincipal]::new($identity)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){throw 'Use ordinary developer PowerShell for this per-user installation.'}
    $installerRoot='D:\Installers\Python'
    New-Item -ItemType Directory -Path $installerRoot -Force | Out-Null
    $installer=Join-Path $installerRoot 'python-3.14.8-amd64.exe'
    if(-not(Test-Path -LiteralPath $installer)){Write-Output 'Downloading the official Python 3.14.8 installer...';Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.14.8/python-3.14.8-amd64.exe' -OutFile $installer}
    if((Get-FileHash -LiteralPath $installer).Hash -ne '759BE887B96E736A3CA886DAF8D575F18FCAE1A09EFAB6902F42D59E8999F8EF'){throw 'Python installer differs from the published SHA256; it was not run.'}
    $signature=Get-AuthenticodeSignature -LiteralPath $installer
    if($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation'){throw 'Python installer signature was not verified; it was not run.'}
    if(Test-Path -LiteralPath 'D:\Tools\Python\3.14'){throw 'Python target folder exists without the expected executable; no overwrite. Report this before retrying.'}
    Write-Output 'Installing Python for developer under D:\Tools\Python\3.14...'
    $process=Start-Process -FilePath $installer -ArgumentList @('/passive','InstallAllUsers=0','TargetDir=D:\Tools\Python\3.14','Include_launcher=0','InstallLauncherAllUsers=0','PrependPath=0','AppendPath=0','Include_test=0','Include_doc=0','Include_pip=1','Include_tcltk=0','AssociateFiles=0','Shortcuts=0') -WindowStyle Hidden -Wait -PassThru
    if($process.ExitCode -notin @(0,3010)){throw ('Python installer failed with exit code '+$process.ExitCode+'. Keep the installer; do not substitute another path.')}
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
