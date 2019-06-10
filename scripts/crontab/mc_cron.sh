#!/usr/bin/env bash

TITLE="jokermc"

function exec() {
	/usr/bin/screen -p 0 -S $TITLE -X eval 'stuff "title @a actionbar {\\"text\\":\\"请各位冒险家们合理安排游戏时间， 注意早点休息哦～～～\\",\\"color\\":\\"yellow\\",\\"bold\\":\\"true\\"}"\\015'
}

exec