#!/usr/bin/env bash

TITLE="jokermc"

function exec() {
	/usr/bin/screen -p 0 -S $TITLE -X eval 'stuff "title @a times 10 100 10"\\015'
	/usr/bin/screen -p 0 -S $TITLE -X eval 'stuff "title @a title {\\"text\\":\\"温馨提示\\",\\"color\\":\\"white\\",\\"bold\\":\\"true\\"}"\\015'
	/usr/bin/screen -p 0 -S $TITLE -X eval 'stuff "title @a subtitle {\\"text\\":\\"各位冒险家们注意早点休息啦!\\",\\"color\\":\\"yellow\\",\\"bold\\":\\"true\\"}"\\015'
}

exec