from setuptools import setup, find_packages

setup(
    name="cppchrono",
    version="0.1.0",
    author="JedizLaPulga",
    author_email="jedizlapulga@gmail.com",
    description="C++ style time library for Python",
    long_description="Implementation of std::chrono Duration, TimePoint, and Clocks.",
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
