# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="OrzMC",
    version="1.0.23",
    description="A project for deployment of minecraft game.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="王志舟<wangzhizhou>",
    author_email="824219521@qq.com",
    maintainer='王志舟',
    maintainer_email='824219521@qq.com',
    url="https://github.com/OrzGeeker/OrzMC.git",
    packages=setuptools.find_packages(),
    platforms = ['all'],
    keywords='minecraft python',
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux"
    ),
    python_requires='>=2.7, <4',
    install_requires=[
        'requests',
        'progressbar2',
        'twine',
        'beautifulsoup4'
    ],
    entry_points = {
        'console_scripts': [
            'orzmc = OrzMC:start'
        ]
    }
)