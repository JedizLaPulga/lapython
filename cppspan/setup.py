from setuptools import setup, find_packages

setup(
    name="cppspan-jediz",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        # "cppbase-jediz>=0.1.0" # Local dependency typically, but good to list
    ],
    python_requires=">=3.7",
)
