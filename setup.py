import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wava",
    version="0.1.0",
    author="Riccardo Magliocchetti",
    author_email="riccardo.magliocchetti@gmail.com",
    description="A website availability checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "validators",
    ],
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest",
    ],
    entry_points={"console_scripts": ["wavacheck=wava.checker.cli:main"]},
)
