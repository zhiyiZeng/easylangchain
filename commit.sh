#!/bin/bash

# 检查是否提供了提交消息
if [ -z "$1" ]; then
    echo "请提供提交消息。"
    echo "用法: ./git_push.sh \"你的提交消息\""
    exit 1
fi

# Git 操作
git add .
git commit -m "$1"
git push

echo "代码已成功提交并推送。"
