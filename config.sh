#!/usr/bin/env bash
#-*- utf-8 -*-


brew --version > /dev/null 2>&1
if [ $? -ne 0 ]; then

    case $(uname) in
        'Linux')
            # ubuntu 安装homebrew
            sudo apt-get install linuxbrew-wrapper
        ;;
        'Darwin')
            # https://brew.sh
            sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            # uninstall homebrew
            # sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
        ;;
        *)
            echo 'unknown platform and os'
        ;;
    esac
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