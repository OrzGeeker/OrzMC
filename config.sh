#!/usr/bin/env bash
#-*- utf-8 -*-


brew --version > /dev/null 2>&1
if [ $? -ne 0 ]; then

    case $(uname) in
        'Linux')
            # ubuntu 
            sudo apt-get install linuxbrew-wrapper

            # 替换brew.git
            HOMEBREW_REPO_DIR="$(brew --repo)"
            if [ -d "$HOMEBREW_REPO_DIR" ]; then
                cd $HOMEBREW_REPO_DIR
                git remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git
                cd -
            fi

            # 替换homebrew-core.git
            HOMEBREW_CORE_DIR="$(brew --repo)/Library/Taps/homebrew/homebrew-core"
            if [ -d "$HOMEBREW_CORE_DIR" ]; then
                cd $HOMEBREW_CORE_DIR
                git remote set-url origin https://mirrors.aliyun.com/homebrew/homebrew-core.git
                cd -
            fi

            # 替换homebrew-bottles访问地址
            HOMEBREW_BOTTLE='export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles'
            BASHRC='~/.bashrc'
            cat $BASHRC | grep "$HOMEBREW_BOTTLE" > /dev/null 2>&1
            if [ $? -ne 0 ]; then
                echo ""$HOMEBREW_BOTTLE"" >> $BASHRC
                source $BASHRC
            fi
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