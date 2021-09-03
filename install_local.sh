#!/usr/bin/env bash
#-*- coding: utf-8 -*-

rm -rf ./dist/* && echo "removed"
pipenv run python setup.py release
echo "generated new dist"
python3 -m pip install ./dist/*.whl
echo "install completed"

