# grokpediapy

A tiny, safe retrieval library skeleton for demos and local testing.

Usage

- Install in editable mode for development:

```powershell
python -m pip install -e .
```

- Quick CLI:

```powershell
python -m grokpediapy.cli "your query here"
# or, after installation:
grokpediapy "your query here"
```

Python API

```python
from grokpediapy import fetch
result = fetch("hello world")
print(result)
```

Notes

This project provides a deterministic local stub in `core.py`. Replace the retrieval logic with secure, networked retrieval code as needed.