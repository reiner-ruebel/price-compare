# Price compare

Internal research and tooling for insurance price-comparison access. The immediate
deliverable is an evidence-backed report showing which comparison portals and
direct competitors can supply data, what competitor coverage each portal offers,
and how robust future collection appears. The tool stays internal; share its
results with the owner.

Start with [the current task brief](docs/current-task.md). The existing UK Lemonade
collector is a working **single-case prototype**, not the requested market-wide
assessment tool. Its two successful journeys were observed on 7 September 2026;
they do not establish present access or future reliability.

## Project contents

- `worker/`: one canonical Lemonade collector, offline tests, optional browser
  observer, and explicit-file package builder.
- `docs/`: investigation findings, feasibility review, owner notes, current task
  and migration instructions.
- `research/docs/` and `research/matrix/`: earlier UK/Ireland pricing research,
  worker design, workbench proposals and effort/decision-paper drafts.
- `research/deliverables/`: previously delivered decision-paper PDF.
- `reference/`: original exploratory Lemonade and HUK code retained for reading.
  These files can submit applications and are not the normal entry points.

The working collector, tests and research copies were compared by SHA256 before
consolidation. Identical delivery/extracted copies have one canonical source.
Original environments, run captures, copied Portal/Notion reference material,
owner-local cases and inputs are retained in a separate protected local archive,
outside this Git repository.

## New-server setup

Clone this private repository into `D:\Dev\price-compare`, then run in ordinary
developer PowerShell:

```powershell
& 'D:\Tools\PowerShell\7\pwsh.exe' -NoProfile -File 'D:\Dev\price-compare\scripts\Initialize-PriceCompare.ps1' -IncludeBrowser
```

If Python is absent, the script requests administrator approval to install it
for all users under `D:\Tools\Python\3.14`. The remaining setup runs as developer:
it creates the project's `.venv`, installs the pinned dependencies, puts
browser/cache files on D:, and runs the offline tests. It does not contact an
insurer or start a live quote journey. Windows installation policy is not changed.

For a notebook with an existing Python installation:

```powershell
pwsh -NoProfile -File .\scripts\Initialize-PriceCompare.ps1 -PythonPath 'C:\Python314\python.exe'
```

See [desktop handover](docs/new-server-handover.md). Add the **repository root** as
the primary local project folder in the desktop app, so it discovers `AGENTS.md`
and durable task context.

## Work safely with project data

Put real owner cases and business inputs under ignored `data/local/`; put local
results/session captures under ignored `worker/runs/` or `artifacts/`. Preserve
their copies through the agreed private transfer/backup workflow. Do not commit
cookies, session tokens, browser profiles, credentials or original private run
captures. A private GitHub repository still needs this boundary.

Offline test command:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s .\worker -p test_collect_quote.py -v
```

Live submissions require the owner's case-specific authorization. Setup and
offline validation provide no authorization to submit applications, agree to
terms, make purchases or run a batch of quotes.
