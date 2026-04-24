#!/usr/bin/env bash
# -*- coding: utf-8 -*-

set -euo pipefail

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "缺少依赖命令: $1" >&2
        exit 1
    fi
}

require_env() {
    local var_name="$1"
    if [ -z "${!var_name:-}" ]; then
        echo "请先设置环境变量 ${var_name}" >&2
        exit 1
    fi
}

require_command curl
require_command jq
require_env QQBOT_APP_ID
require_env QQBOT_CLIENT_SECRET

# QQBOT_APP_ID:
#   QQ 机器人应用的 AppID，由 QQ Bot 平台分配。
#   必填，格式为纯数字字符串。
#   示例值: 102813326
app_id="${QQBOT_APP_ID:-}"

# QQBOT_CLIENT_SECRET:
#   QQ 机器人应用的密钥，用于换取 access_token。
#   必填，内容通常是一串字母数字组合。
#   示例值: your_client_secret_here
client_secret="${QQBOT_CLIENT_SECRET:-}"

# QQBOT_GUILD_ID:
#   目标频道服务器（guild）的 ID，用于查询子频道列表和成员列表。
#   选填，未设置时使用当前脚本内的默认 guild。
#   示例值: 4678868088901888449
guild_id="${QQBOT_GUILD_ID:-4678868088901888449}"

# QQBOT_CHANNEL_ID:
#   目标子频道（channel）的 ID，用于查询频道信息和发送频道消息。
#   选填，未设置时使用当前脚本内的默认 channel。
#   示例值: 716172984
channel_id="${QQBOT_CHANNEL_ID:-716172984}"

# QQBOT_DM_GUILD_ID:
#   DMS 会话对应的 guild ID，用于向私聊会话发送 DMS 消息。
#   选填，未设置时使用当前脚本内的默认值。
#   示例值: 4678868088901888449
dm_guild_id="${QQBOT_DM_GUILD_ID:-4678868088901888449}"

# QQBOT_PRIVATE_USER_ID:
#   私信目标用户的 ID，用于调用用户私信消息接口。
#   选填，未设置时使用当前脚本内的默认用户 ID。
#   示例值: 1F57730D6ADC5F5CD417D5614A52F2CF
private_user_id="${QQBOT_PRIVATE_USER_ID:-1F57730D6ADC5F5CD417D5614A52F2CF}"

# QQBOT_MEMBER_LIMIT:
#   查询频道成员列表时的分页条数上限。
#   选填，必须为纯数字。
#   示例值: 20
member_limit="${QQBOT_MEMBER_LIMIT:-20}"

# QQBOT_TEST_MESSAGE:
#   测试发送消息时使用的文本内容。
#   选填，可填写任意文本；脚本会自动进行 JSON 转义。
#   示例值: hello from qq bot
test_message="${QQBOT_TEST_MESSAGE:-test message from qq bot}"

if ! [[ "${app_id}" =~ ^[0-9]+$ ]]; then
    echo "QQBOT_APP_ID 格式不正确，期望为纯数字" >&2
    exit 1
fi

if ! [[ "${member_limit}" =~ ^[0-9]+$ ]]; then
    echo "QQBOT_MEMBER_LIMIT 格式不正确，期望为纯数字" >&2
    exit 1
fi

fetch_access_token() {
    echo "==> 获取 access_token" >&2
    if ! curl --fail --silent --show-error --location 'https://bots.qq.com/app/getAppAccessToken' \
        --header 'Content-Type: application/json' \
        --data "{\"appId\": \"${app_id}\", \"clientSecret\": \"${client_secret}\"}" \
        | jq -r '.access_token'; then
        echo "请求失败: 获取 access_token" >&2
        exit 1
    fi
}

qq_api_request() {
    local api_name="$1"
    local method="$2"
    local url="$3"
    local request_body="${4:-}"
    local curl_args=(
        --fail
        --silent
        --show-error
        --location
        "$url"
        --header
        "$content_type_header"
        --header
        "$authorization_header"
        --request
        "$method"
    )

    echo "==> ${api_name}" >&2

    if [ -n "${request_body}" ]; then
        curl_args+=(--data "$request_body")
    fi

    if ! curl "${curl_args[@]}" | jq; then
        echo "接口请求失败: ${api_name}" >&2
        exit 1
    fi
}

build_text_message_payload() {
    local message="$1"
    jq -cn --arg content "$message" '{msg_type: 0, content: $content}'
}

access_token="$(fetch_access_token)"

if [ -z "${access_token}" ] || [ "${access_token}" = "null" ]; then
    echo "获取 access_token 失败" >&2
    exit 1
fi

content_type_header='Content-Type: application/json'
authorization_header="Authorization: QQBot ${access_token}"

qq_api_request "获取机器人信息" "GET" 'https://api.sgroup.qq.com/users/@me'
qq_api_request "获取机器人所属频道列表" "GET" 'https://api.sgroup.qq.com/users/@me/guilds'
qq_api_request "获取频道子频道列表" "GET" "https://api.sgroup.qq.com/guilds/${guild_id}/channels"
qq_api_request "获取频道成员列表" "GET" "https://api.sgroup.qq.com/guilds/${guild_id}/members?limit=${member_limit}"
qq_api_request "获取子频道信息" "GET" "https://api.sgroup.qq.com/channels/${channel_id}"
message_payload="$(build_text_message_payload "${test_message}")"
qq_api_request "发送私信消息" "POST" "https://api.sgroup.qq.com/v2/users/${private_user_id}/messages" "${message_payload}"
qq_api_request "发送频道消息" "POST" "https://api.sgroup.qq.com/channels/${channel_id}/messages" "${message_payload}"
qq_api_request "发送 DMS 消息" "POST" "https://api.sgroup.qq.com/dms/${dm_guild_id}/messages" "${message_payload}"
