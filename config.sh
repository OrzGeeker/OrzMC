#!/usr/bin/env bash
#-*- utf-8 -*-

function config_python_env {
    pipenv --three  install     \
                    install     \
                    setuptools  \
                    wheel       \
                    twine       \
                    -e .        \
                    && pipenv shell
}

function config_darwin {

    brew --version > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        # https://brew.sh
        sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        # uninstall homebrew
        # sudo echo '^M' | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
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

    config_python_env
}

function config_ubuntu {
    sudo apt-get install -y \
        git                 \
        pipenv              \
        hugo

    config_python_env
}

function main {
    case $(uname) in
        'Linux')
            LINUX_TYPE=$(echo $(cat /etc/issue) | cut -d ' ' -f 1)
            if [ "$LINUX_TYPE" = 'Ubuntu' ]; then
                config_ubuntu
            fi
            ;;
        'Darwin')
            config_darwin
            ;;
        *)
            echo 'unknown platform and os'
            ;;
    esac
}

main