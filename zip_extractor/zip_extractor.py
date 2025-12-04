# zip_extractor/zip_extractor.py
#!/usr/bin/env python3
"""
Self-contained single script version – just copy & run anywhere.
"""
import zipfile
import argparse
from pathlib import Path


def extract(zip_path: str, dest: str = None, password: str = None, overwrite: bool = False):
    zip_path = Path(zip_path)
    dest = Path(dest or zip_path.stem)
    dest.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        if password:
            zf.setpassword(password.encode())

        for member in zf.infolist():
            target_path = dest / member.filename
            if not overwrite and target_path.exists():
                print(f"Skipping existing: {target_path}")
                continue
            zf.extract(member, dest)

    print(f"Extracted {zip_path.name} → {dest.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple cross-platform ZIP extractor")
    parser.add_argument("zipfile", help="Path to .zip file")
    parser.add_argument("-d", "--dest", help="Destination folder")
    parser.add_argument("-p", "--password", help="Password for encrypted zip")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()
    extract(args.zipfile, args.dest, args.password, args.overwrite)