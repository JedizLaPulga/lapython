from setuptools import setup, find_packages

setup(
    name="cppfunctional",
    version="0.1.0",
    author="JedizLaPulga",
    author_email="jedizlapulga@gmail.com",
    description="C++ style functional utilities (Function, ReferenceWrapper) for Python",
    long_description="Implementation of std::function, std::ref, std::cref and other functional utilities.",
    long_description_content_type="text/markdown",
    url="https://github.com/JedizLaPulga/lapython",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["cppbase"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Introduction :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
