#!/usr/bin/env bash
#-*- utf-8 -*-

pkill -9 hugo
hugo -s swiftui server -D --bind "0.0.0.0" &
sleep 2s
open http://localhost:1313