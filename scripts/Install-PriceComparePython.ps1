[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$target = 'D:\Tools\Python\3.14'
$installer = 'D:\Installers\Python\python-3.14.8-amd64.exe'
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
if ($env:COMPUTERNAME -ine '398F536' -or -not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'This helper requires administrator elevation on 398F536. Run Initialize-PriceCompare.ps1 as ordinary developer; it requests elevation for this helper only.'
}
$python = Join-Path $target 'python.exe'
$records = Join-Path 'D:\Installers\Python' ('install-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $records -Force | Out-Null
$exitCode = $null
try {
    if ((Get-FileHash -LiteralPath $installer -Algorithm SHA256).Hash -ne '759BE887B96E736A3CA886DAF8D575F18FCAE1A09EFAB6902F42D59E8999F8EF') { throw 'Python installer SHA256 was not verified.' }
    $signature = Get-AuthenticodeSignature -LiteralPath $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation') { throw 'Python installer signature was not verified.' }
    # Read policy metadata only. Never relax policy or delete a failed installation.
    $policy = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Installer' -ErrorAction SilentlyContinue
    $disableMsi = $policy.DisableMSI
    [pscustomobject]@{Computer=$env:COMPUTERNAME;Account=$identity.Name;DisableMSI=$disableMsi;Target=$target;TargetExists=(Test-Path -LiteralPath $target)} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $records 'preflight.json') -Encoding utf8
    if ($disableMsi -eq 2) { throw 'Windows Installer policy disables all installations. Policy was not changed.' }
    if (Test-Path -LiteralPath $python -PathType Leaf) { throw 'Python executable already exists; use ordinary project initialization to validate it. No reinstallation attempted.' }
    $log = Join-Path $records 'python-installer.log'
    $arguments = @('/passive','/norestart','/log',('"' + $log + '"'),'InstallAllUsers=1','TargetDir=D:\Tools\Python\3.14','Include_launcher=0','InstallLauncherAllUsers=0','PrependPath=0','AppendPath=0','Include_test=0','Include_doc=0','Include_pip=1','Include_tcltk=0','AssociateFiles=0','Shortcuts=0')
    $process = Start-Process -FilePath $installer -ArgumentList $arguments -WindowStyle Hidden -Wait -PassThru
    $exitCode = $process.ExitCode
    if ($exitCode -notin @(0,3010)) { throw ('Python installer failed with exit code ' + $exitCode) }
    $version = @(& $python -c 'import sys; print(sys.version.split()[0]); print(sys.maxsize > 2**32)')
    if ($LASTEXITCODE -ne 0 -or $version.Count -ne 2 -or $version[0] -ne '3.14.8' -or $version[1] -ne 'True') { throw 'Installed Python 3.14.8 x64 verification failed.' }
    [pscustomobject]@{Computer=$env:COMPUTERNAME;Python=$python;Version=$version[0];InstallAllUsers=$true;InstallerExitCode=$exitCode;RestartRequired=($exitCode -eq 3010);PolicyChanged=$false;CompletedAtUtc=(Get-Date).ToUniversalTime().ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $records 'result.json') -Encoding utf8
    exit 0
} catch {
    [pscustomobject]@{Message=$_.Exception.Message;InstallerExitCode=$exitCode;PolicyChanged=$false;Records=$records} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $records 'failure.json') -Encoding utf8
    Write-Error ('Python installation stopped. Records: ' + $records) -ErrorAction Continue
    exit 1
}
