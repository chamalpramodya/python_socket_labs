# Python Socket Labs

## Objective
Master raw TCP/UDP sockets, concurrency, framing, and diagnostics.

## Repo Layout
D:.
├───.github
│   └───workflows
├───docs
│   ├───diagrams
│   └───wireshark
├───infra
├───src
└───tests


##
Why did we create a virtual environment (Step 2)?

A virtual environment (venv) is important because:

Isolation – It keeps your project’s dependencies separate from your system Python packages. This prevents version conflicts.

Reproducibility – You can freeze the exact package versions in requirements.txt and recreate the environment on another machine.

Clean removal – If you delete the venv folder, your global Python stays untouched.

Industry best practice – Every Python project typically uses a venv (or similar tools like pipenv or poetry).

Without a virtual environment, if you install packages globally, you risk breaking other projects or your system packages.