from setuptools import setup, find_packages

setup(
    name="cpptuple",
    version="0.1.0",
    author="JedizLaPulga",
    author_email="jedizlapulga@gmail.com",
    description="A C++ style mutable tuple implementation for Python",
    long_description="A mutable tuple implementation mimicking std::tuple from C++.",
    long_description_content_type="text/markdown",
    url="https://github.com/JedizLaPulga/lapython",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["cppbase"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
