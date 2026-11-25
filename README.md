### Requirements

- Python >=3.10

### INSTALL virtualenv (if not installed yet)
`sudo apt update`
`sudo apt upgrade`
`sudo apt install python3.12-venv`

### CREATE VIRTUAL ENV (if not created yet)
From `infra/`, run:
`make venv`

This creates `apivenv` in the project root.

### INSTALL PYTHON BACKEND DEPENDENCIES (if not installed yet)
`pip3 install -r requirements.txt`

### RUN

Use makefile targets to run the API:
`cd infra`
`make rundev`

then:
`make runmock`


### RUN BOTH APIS

From `infra/`, run: 
`make envrun`

This ensures the virtual environment exists,
then starts `rundev` and `runmock` in separate windows of a `lookmix-api` tmux
session. Use `Ctrl-b` followed by `n` or `p` to switch windows, and `Ctrl-b`
followed by `d` to detach while leaving both APIs running. Reattach with
`tmux attach -t lookmix-api`.

#### TROUBLESHOOTING 

In case of below error:

"Building wheel for aioquic (pyproject.toml) did not run successfully. │ exit code: 1 ╰─> [63 lines of output] /tmp/pip-build-env-ibyh3fhh/overlay/lib/python3.12/site-packages/setuptools/dist.py:765: SetuptoolsDeprecationWarning: License classifiers are deprecated. !!"

run:

`sudo apt install build-essential libssl-dev libffi-dev python3-dev`

then, reopen the terminal and install requirements again.

In case of below error:

"Building wheel for Pillow (pyproject.toml) did not run successfully. │ exit code: 1 ╰─> [211 lines of output] /tmp/pip-build-env-lvowkurw/overlay/lib/python3.12/site-packages/setuptools/dist.py:765: SetuptoolsDeprecationWarning: License classifiers are deprecated. !!"

run:

`sudo apt install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev`

then, reopen the terminal and install requirements again