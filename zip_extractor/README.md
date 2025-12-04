# Zip Extractor 🗜️

A clean, secure, cross-platform ZIP extraction tool in Python.

## Features
- Single-file mode or full modular package
- Password-protected ZIP support
- Zip-slip attack protection
- Overwrite control
- Beautiful CLI with `click`
- 100% pure Python (works on Windows/macOS/Linux)

## Quick Start (single file)
```bash
python zip_extractor.py myfile.zip -d ./output --password secret