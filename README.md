### Requirements

- Python =3.10

### INSTALL virtualenv (if not installed yet)
`sudo apt update`
`sudo apt upgrade`
`sudo apt install python3.12-venv`

### CREATE VIRTUAL ENV (if not created yet)
`python3.12 -m venv apivenv`

### ACTIVATE VIRTUAL ENV
`. apivenv/bin/activate`

### INSTALL PYTHON BACKEND DEPENDENCIES (if not installed yet)
`pip3 install -r requirements.txt`

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