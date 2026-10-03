# Work on the new server

Use the ordinary `398F536\developer` RDP session. Git, PowerShell 7 and desktop
sign-in have already been verified during Portal migration.

## Clone and prepare

Clone the private repository once into a new folder:

```powershell
& 'D:\Tools\Git\cmd\git.exe' clone https://github.com/reiner-ruebel/price-compare.git D:\Dev\price-compare
& 'D:\Tools\PowerShell\7\pwsh.exe' -NoProfile -File 'D:\Dev\price-compare\scripts\Initialize-PriceCompare.ps1' -IncludeBrowser
```

If Git requests authentication, use its normal browser sign-in. Do not paste a
token into the command, URL, repository or chat. If the destination already
exists, stop and inspect its contents rather than deleting/replacing it.

Setup uses the [official Python 3.14.8 Windows installer](https://www.python.org/downloads/release/python-3148/),
checks its published SHA256 and Python Software Foundation signature, and
requests administrator approval to install for all users under
`D:\Tools\Python\3.14` if that executable is absent. Only the Python installation
helper is elevated; dependencies, browser preparation and tests run as developer.
It does not change system/user Python PATH, file associations or another runtime.
Project dependencies go into `D:\Dev\price-compare\.venv`; pip/Chromium caches
go under `D:\UserData\developer\Caches`. It runs offline tests and no live quotes.

### Recovery from Python exit code 1625

The first non-elevated per-user attempt on 398F536 returned 1625 on 3 October
2026. Microsoft defines this as installation forbidden by system policy; the
specific server policy was not supplied. Its DisableMSI policy documentation
distinguishes blocked non-elevated per-user installation from allowed elevated
or per-machine installation for value 1. The updated setup uses the official
installer's `InstallAllUsers=1` route without changing policy.

In ordinary developer PowerShell, update the clean clone and rerun setup:

```powershell
& 'D:\Tools\Git\cmd\git.exe' -C 'D:\Dev\price-compare' pull --ff-only
& 'D:\Tools\PowerShell\7\pwsh.exe' -NoProfile -File 'D:\Dev\price-compare\scripts\Initialize-PriceCompare.ps1' -IncludeBrowser
```

Approve the administrator prompt with the server administrator account. Do not
run the whole project setup in an administrator shell. The helper rechecks the
existing download's hash/signature, records policy metadata, and saves installer
logs/results under `D:\Installers\Python\install-*`. It does not remove partial
files or change policy. If policy prohibits all installations, it stops and
retains a failure record.

Sources: [Microsoft error codes](https://learn.microsoft.com/en-us/windows/win32/msi/error-codes),
[DisableMSI policy](https://learn.microsoft.com/en-us/windows/win32/msi/disablemsi),
[Python installer options](https://docs.python.org/3.14/using/windows.html#installing-without-ui).

### Verified server setup

The operator reported successful setup on 3 October 2026 at 16:10:27 UTC
(18:10:27 Berlin time), after the installer recovery:

| Item | Reported result |
| --- | --- |
| Computer/account | `398F536`, `398F536\developer` |
| Project | `D:\Dev\price-compare` |
| Python | `3.14.8`, `D:\Tools\Python\3.14\python.exe` |
| Project interpreter | `D:\Dev\price-compare\.venv\Scripts\python.exe` |
| pip cache | `D:\UserData\developer\Caches\pip` |
| Browser prepared/cache | `True`, `D:\UserData\developer\Caches\playwright` |
| Offline tests | 17 passed; no broken requirements |
| Insurer requests / Portal or SQL changed | `False` / `False` |
| Setup records | `D:\Dev\price-compare\.local\setup-20261003-181027` |

This verifies project setup from the operator's supplied summary. Desktop
project access and the requested market-wide assessment implementation remain
to be verified/delivered. Do not repeat installation or cloning for this state.

## Attach the local folder

In ChatGPT Desktop on the new server, add a local project/open folder and select
`D:\Dev\price-compare`. In **Edit project**, make that root folder **Primary**.
Start a chat from that project; confirm it is using **This computer/local**.
The local project provides access to the folder and discovers its `AGENTS.md`.
These steps follow [official OpenAI project documentation](https://learn.chatgpt.com/docs/projects).

If a command reports another working directory or access denied, attach/select
the actual repository folder and retry a small read/write check there. Do not
grant broad access to all of D: or reuse the unrelated ServerSetup folder.

## First project prompt

Read `AGENTS.md`, `README.md` and `docs/current-task.md`. Work in this local
repository on 398F536. First verify the working directory, Python virtual
environment and offline tests. Then build the internal assessment tool and
initial evidence-backed report described in the task brief: portal access by
Python or Python+Playwright, competitor coverage by portal, direct-insurer access,
and a strict score for expected future robustness. Use the existing research as
dated historical evidence; do not claim its old observations are current. Confirm
the target market/product/list and approved cases before live quote submissions.
Public research, schemas, offline fixtures and the first report may proceed in
parallel with that clarification. Keep private inputs and session captures out
of Git. Do not touch Portal, SQL, VPN configuration or backup tasks.

The existing Lemonade prototype's offline tests establish implementation behavior,
not current insurer availability. Its live code runs only with an explicit
`--confirm-test-submission` flag; do not add that flag during project setup.

## Local/private material

The complete pre-consolidation folder is preserved in a protected notebook
archive. Personal/business input CSV, `my-approved-case.json`, old session captures,
browser outputs and virtual environments were not put in GitHub. If needed for
an approved next task, transfer only the required input through the agreed private
channel into ignored `data/local/` on the new server. Old browser sessions and
virtual environments are not portable setup dependencies.

## Portal remains a separate migration task

The encrypted Portal checkpoint upload/download/hash proof succeeded on
3 October 2026: snapshot `d170c2ce3e9cf2d0a857d82b391d9ae9`, 6,513 total files.
The next Portal backup step is an isolated SQL restore from the downloaded files,
then recurring full/log backups. Continue that work in the original migration chat
after this project is available on the new server.
