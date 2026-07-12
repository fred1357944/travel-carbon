# Contributing to travel-carbon

Thanks for considering a contribution. This project is a small research-software package for Taiwan HEI Scope 3 Category 6 distance-based travel estimates.

## Development setup

```bash
git clone https://github.com/fred1357944/travel-carbon.git
cd travel-carbon
python3 -m pip install -e ".[dev]"
pytest -q
```

## What to work on

- Gazetteer fixes (coordinates, aliases, district maps) with tests
- Distance/OSRM reliability (mocked network tests preferred)
- Factor profiles and documentation honesty
- Evaluation harness improvements
- GUI/package integration tests

Please avoid committing real reimbursement Excel files or personal data.

## Pull requests

1. Open an issue describing the change when non-trivial.
2. Keep PRs focused; include or update tests.
3. Run `pytest -q` before push.
4. Do not claim MOENV statutory compliance for screening km factors without source tables.

## Support expectations

- Best-effort responses via GitHub Issues on the public repository.
- No guaranteed SLA; this is a volunteer / research-tooling project.
- Security or privacy concerns: open a private security advisory if available, otherwise a minimal public issue without personal data.

## Code of conduct

Be respectful in issues and PRs. Harassment or personal data dumps will be removed.
