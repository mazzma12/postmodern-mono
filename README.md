# postmodern-mono

## Important notes
### Syncing
You must always sync with:
```bash
uv sync --all-packages
```

### Pyright
You'll need to add the following to every `pyproject.toml`:
```toml
[tool.pyright]
venvPath = ".."
venv = ".venv"
strict = ["**/*.py"]
pythonVersion = "3.13"
extraPaths = ["../"]
```

## Docker
The Dockerfile is at [myserver/Dockerfile](./myserver/Dockerfile).

Build the Docker image:
```bash
docker build --tag=postmodern-mono -f myserver/Dockerfile .
```

And run it:
```bash
docker run --rm -it postmodern-mono
```
