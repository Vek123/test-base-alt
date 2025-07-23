# Test Base ALT

[![Flake Black Pytest](https://github.com/Vek123/test-base-alt/actions/workflows/python-app.yml/badge.svg)](https://github.com/Vek123/test-base-alt/actions/workflows/python-app.yml)

Test case from **Base ALT** company. This is application was created to get information about Base ALT's repository.

## Requirements

- `python==3.12`

```bash
sudo apt-get update
sudo apt-get install python
```

- `Git`

```bash
sudo apt-get install git
```

## Preparing to lunch

- Clone repository

```bash
git clone https://github.com/Vek123/test-base-alt.git
cd test-base-alt
```

- Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install pip dependencies

```bash
pip install -r requirements.txt
```

## How to run CLI?

```bash
python3 repo_info_cli.py # to get help info about CLI
```

## How to build tool?

- Install `pyinstaller`

```bash
pip install pyinstaller
```

- Build tool

```bash
pyinstaller repo_info_cli.py --onefile --name="repo-info"
```

- Check the `dist` folder, it should contain an executable file with name `repo-info`.

- To use it from anywhere in Linux you need to move it to the system `bin` folder.

```bash
sudo mv repo-info /bin/
```

- Now, you need just write `repo-info` command to use it.

## Running tests

```bash
pytest
```
