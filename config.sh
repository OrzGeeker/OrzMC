#!/usr/bin/env bash
#-*- utf-8 -*-


brew --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # https://brew.sh
    sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # uninstall homebrew
    # sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
fi

pipenv --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    brew install pipenv
fi

git --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    brew install git
fi
