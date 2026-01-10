## Session 1 — Project Setup & Tooling Foundations

### Concepts Learned

- Python virtual environments isolate dependencies per project
- On macOS, `python3` is used to create venvs, not `python`
- The name of a virtual environment (e.g., `popenv`) is arbitrary
- Jupyter notebooks (`.ipynb`) are JSON files and must be created via Jupyter
- Jupyter creates `.ipynb_checkpoints` as auto-save backups
- Code quality tools serve different purposes:
  - Black → formatting
  - Ruff → linting and bug detection
  - Pytest → testing framework

### Why This Matters

A clean environment and repository structure prevent hidden bugs, reduce confusion, and make the project reproducible and professional.

### What I Did

- Created and activated a virtual environment
- Set up a clean project structure
- Installed and configured Black, Ruff, and Pytest
- Installed Jupyter inside the venv and created a valid notebook
- Cleaned up auto-generated files using `.gitignore`
- Fixed tooling warnings to keep the repo future-proof
