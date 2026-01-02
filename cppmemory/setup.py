from setuptools import setup, find_packages

setup(
    name="cppmemory",
    version="0.1.0",
    author="JedizLaPulga",
    author_email="jedizlapulga@gmail.com",
    description="C++ style smart pointers (shared_ptr, unique_ptr) for Python",
    long_description="Implementation of std::shared_ptr, std::unique_ptr, and std::weak_ptr semantics in Python.",
    long_description_content_type="text/markdown",
    url="https://github.com/JedizLaPulga/lapython",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["cppbase"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
