# !/usr/bin/env bash
# -*- coding: utf-8 -*-

access_token=$(curl --location 'https://bots.qq.com/app/getAppAccessToken' --header 'Content-Type: application/json' --data '{"appId": "102813326", "clientSecret": "XOF6xphZRJB3vohaTMF82wqkeYSNID83"}' | jq '.access_token')
access_token="${access_token//\"}"
echo "access_token: ${access_token}"

content_type_header='Content-Type: application/json'
echo "content_type_header: ${content_type_header}"

authorization_header="Authorization: QQBot ${access_token}"
echo "authorization_header: ${authorization_header}"

curl \
    --location 'https://api.sgroup.qq.com/users/@me' \
    --header "${content_type_header}" \
    --header "${authorization_header}" \
    | jq

curl \
    --location 'https://api.sgroup.qq.com/users/@me/guilds' \
    --header "${content_type_header}" \
    --header "${authorization_header}" \
    | jq

curl --location 'https://api.sgroup.qq.com/guilds/4678868088901888449/channels' \
    --header "${content_type_header}" \
    --header "${authorization_header}" \
    | jq    

curl --location 'https://api.sgroup.qq.com/channels/716172984' \
    --header "${content_type_header}" \
    --header "${authorization_header}" \
    | jq    


curl --location 'https://api.sgroup.qq.com/channels/716172984/messages' \
    --header "${content_type_header}" \
    --header "${authorization_header}" \
    -X POST \
    --data '{
    "msg_type": 0,
    "content": "test message from qq bot"
    }' | jq