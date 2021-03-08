```bash
pip install --user --upgrade pip

# ---- Windows -----

# On powershell
pip install pyenv-win --target $HOME\\.pyenv

# With Chocolatey
choco install pyenv-win

# Warning: Check if not got any error
pyenv rehash

# ---- Pyenv: Python versions manager -----

cd [project-folder]

# Loads local version from .python-version file
pyenv local

# PS: Latest 3.8.x Python version available in Pyenv for Windows
pyenv install 3.8.2

python --version


# ---- Virtual Environments ----

python -m venv venv

# Activate
.\venv\Scripts\activate.bat

pip install -r .\requirements.txt
```

### Integrate .NET and Python: Strategies

1. IronPython = Interpreter para gerar Python em IL (Intermediate Language)
2. Biblioteca = CLI assincrona
3. Backend Web Python: http://aaaaaa.py => {aaa:bbbb} (C#)
4. Service Tray Python => C#
