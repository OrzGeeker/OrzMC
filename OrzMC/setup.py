import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OrzMC",
    version="0.0.1",
    author="wangzhizhou",
    author_email="824219521@qq.com",
    description="A project for deployment of minecraft game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OrzGeeker/OrzMC.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ),
)