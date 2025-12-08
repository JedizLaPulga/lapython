from setuptools import setup, find_packages

setup(
    name="cppflat_set",
    version="0.1.0",
    description="A Python implementation of C++23 std::flat_set",
    author="LaPython Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["cppbase"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
