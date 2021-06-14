# -*- coding: utf-8 -*-
import setuptools
import sys

setuptools.setup(
    name="OrzMC",
    version="1.0.102",
    description="A project for deployment of minecraft game.",
    long_description=open('README.md', encoding = 'UTF-8').read(),
    long_description_content_type="text/markdown",
    author="王志舟<wangzhizhou>",
    author_email="824219521@qq.com",
    maintainer='王志舟',
    maintainer_email='824219521@qq.com',
    url="https://github.com/OrzGeeker/OrzMC.git",
    packages=setuptools.find_packages(),
    platforms = ['all'],
    keywords='minecraft python',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3, <4',
    install_requires=[
        'requests',
        'twine',
        'beautifulsoup4',
        'pyyaml',
        'rich'
    ],
    entry_points = {
        'console_scripts': [
            'orzmc = OrzMC:start',
            'orzmc-rsync = OrzMC:rsync_server_core_data',
            'orzmc-jdk = OrzMC:install_jdk',
            'orzmc-jdk-remove = OrzMC:uninstall_jdk'
        ]
    }
)
