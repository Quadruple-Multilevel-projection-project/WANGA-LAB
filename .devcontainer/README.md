# WANGA-LAB Codespace

This directory defines the reproducible GitHub Codespaces development environment for WANGA-LAB.

## Environment

- Python 3.12 on the Dev Containers Bookworm image.
- GitHub CLI.
- VS Code Python, Pylance, and GitHub Actions extensions.
- Project and development dependencies installed after container creation.
- pytest configured to run the repository test suite.

## Security boundary

Do not commit or hard-code API keys or other credentials. In particular, `GOOGLE_API_KEY` and other provider credentials must remain in the Codespaces secret store or another approved secret mechanism and should be scoped only to the process that requires them.

## Validation

After the Codespace is created:

```bash
python --version
python -m pytest -q
git status
```

The Codespace configuration does not grant repository permissions, create GitHub Teams, or establish provider credentials.
