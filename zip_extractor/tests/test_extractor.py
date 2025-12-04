# tests/test_extractor.py
import shutil
from pathlib import Path
import pytest
import zipfile
from zip_extractor.extractor import extract_zip

TEST_DIR = Path(__file__).parent
TMP_DIR = TEST_DIR / "tmp_extract"


@pytest.fixture(autouse=True)
def cleanup():
    # Setup: clean before each test
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir()
    yield
    # Teardown: clean after each test
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)


def test_extract_normal_zip():
    extracted = extract_zip(TEST_DIR / "sample.zip", extract_to=TMP_DIR / "normal")
    assert extracted.exists()
    assert (extracted / "hello.txt").read_text().strip() == "Hello from the test"


def test_extract_with_custom_output():
    custom = TMP_DIR / "mydata"
    extracted = extract_zip(TEST_DIR / "sample.zip", extract_to=custom)
    assert extracted == custom.resolve()
    assert (custom / "hello.txt").is_file()


def test_password_protected():
    extracted = extract_zip(
        TEST_DIR / "sample_encrypted.zip",
        extract_to=TMP_DIR / "protected",
        password=b"secret123"
    )
    assert (extracted / "hello.txt").exists()


def test_wrong_password_raises():
    with pytest.raises(zipfile.BadZipFile):
        extract_zip(
            TEST_DIR / "sample_encrypted.zip",
            password=b"wrong"
        )


def test_zip_slip_protection():
    # Create malicious zip with ../../etc/passwd-like entry
    bad_zip = TEST_DIR / "malicious.zip"
    with zipfile.ZipFile(bad_zip, "w") as zf:
        zf.writestr("../../evil.txt", "hacked")

    with pytest.raises(ValueError, match="Unsafe zip entry"):
        extract_zip(bad_zip)
    bad_zip.unlink()  # cleanup