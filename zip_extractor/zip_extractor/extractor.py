# zip_extractor/extractor.py
import zipfile
from pathlib import Path
from typing import Union, List, Optional


def extract_zip(
    zip_path: Union[str, Path],
    extract_to: Optional[Union[str, Path]] = None,
    password: Optional[bytes] = None,
    overwrite: bool = False,
) -> Path:
    """
    Extract a zip file to a destination folder.

    Args:
        zip_path: Path to the .zip file
        extract_to: Destination directory (defaults to same name without .zip)
        password: Optional password (as bytes) for encrypted archives
        overwrite: If True, overwrite existing files without asking

    Returns:
        Path to the extracted directory
    """
    zip_path = Path(zip_path).expanduser().resolve()
    if not zip_path.is_file():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")

    if extract_to is None:
        extract_to = zip_path.parent / zip_path.stem
    else:
        extract_to = Path(extract_to).expanduser().resolve()

    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        if password:
            zf.setpassword(password)

        # Check for dangerous paths (zip slip protection)
        for member in zf.infolist():
            if member.filename.startswith('/') or '..' in member.filename.split('/'):
                raise ValueError(f"Unsafe zip entry detected: {member.filename}")

        if not overwrite:
            # Simulate extraction to check for conflicts
            conflicts = [
                extract_to / member.filename
                for member in zf.infolist()
                if (extract_to / member.filename).exists()
            ]
            if conflicts:
                raise FileExistsError(
                    f"Files already exist (use --overwrite): {conflicts[:5]}..."
                )

        zf.extractall(extract_to)

    return extract_to.resolve()