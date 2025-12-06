from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cpparray",
    version="0.1.0",
    author="JedizLaPulga",
    author_email="jedizlapulga@gmail.com",
    description="A C++ style fixed-size std::array implementation for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JedizLaPulga/lapython",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Introduction :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
