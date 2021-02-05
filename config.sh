#!/usr/bin/env bash
#-*- utf-8 -*-


brew --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # https://brew.sh
    sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # uninstall homebrew
    # sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"

    if [ $(uname) == 'Linux' ]; then
        # 替换brew.git
        cd "$(brew --repo)"
        git remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git

        # 替换homebrew-core.git
        cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
        git remote set-url origin https://mirrors.aliyun.com/homebrew/homebrew-core.git

        # 替换homebrew-bottles访问地址
        export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles
        echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles' >> ~/.bashrc
    fi
fi

pipenv --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # https://github.com/pypa/pipenv
    brew install pipenv
fi

git --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # https://git-scm.com/
    brew install git
fi

hugo version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # https://gohugo.io/
    brew install hugo
fi

pipenv --three  install     \
                install     \
                setuptools  \
                wheel       \
                twine       \
                -e .        \
                && pipenv shell