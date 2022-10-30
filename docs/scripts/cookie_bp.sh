#!/bin/bash
## 账号批量管理工具脚本
## Author: SuperManito
## Modified: 2022-04-03

## 执行位置判定
if [ ${WORK_DIR} ]; then
    . ${WORK_DIR}/shell/share.sh
else
    echo -e "\n[\033[31mERROR\033[0m] 请进入容器内执行此脚本！\n"
    exit
fi

## 使用帮助
function Help() {
    echo -e "\n${GREEN}使用方法${PLAIN}：\n\n 批量添加/更新 ${BLUE}bash $0 add${PLAIN}\n\n  批 量 删 除  ${BLUE}bash $0 del${PLAIN}\n"
}

## 检查面板状态
function Check_Panel_Status() {
    pm2 list | sed "/─/d" | perl -pe "{s| ||g; s#│#|#g}" | sed "1d" >$FilePm2List
    cat $FilePm2List | awk -F '|' '{print$3}' | grep "web_server" -wq
    if [ $? -eq 0 ]; then
        if [[ $(cat $FilePm2List | grep "web_server" -w | awk -F '|' '{print$10}') != "online" ]]; then
            echo -e "\n$ERROR 请先启动控制面板！\n"
            ExitStatus
        fi
    else
        echo -e "\n$ERROR 请先启动控制面板！\n"
        exit
    fi
    [ -f $FilePm2List ] && rm -rf $FilePm2List
}

## 获取面板 OpenApiToken
function Get_OpenApiToken() {
    cat $FileAuth | jq | grep "openApiToken" -q
    if [ $? -eq 0 ]; then
        OpenApiToken=$(cat $FileAuth | jq .openApiToken | sed "s/\"//g")
    else
        echo -e "\n$ERROR 检测到当前仍在使用旧版 ${BLUE}OpenApiToken${PLAIN} ，请先重置控制面板登录认证信息！\n"
        exit
    fi
}

## 获取文件内容请单
function Get_List() {
    local FileListCK=$ConfigDir/cookie.txt
    if [ -s $FileListCK ]; then
        List=(
            $(cat $FileListCK | sed "/^[#/]/d" | perl -pe "{s|Cookie[0-9]{1,3}=||g; s|export JD_COOKIE=||g; s|[ #\"\']||g}")
        )
    else
        echo -e "\n$ERROR 请先将CK写入至 ${BLUE}$ConfigDir/cookie.txt${PLAIN} 文件中，一行一个，支持任意格式，但尽量不要带有特殊符号例如中文汉字\n"
        exit
    fi
}

function Main() {
    local pin key ck
    Check_Panel_Status
    Get_OpenApiToken
    Get_List

    case $1 in
    add)
        echo -e "\n$WORKING 检测到 ${BLUE}${#List[@]}${PLAIN} 个账号数据，开始批量添加/更新...\n"
        for ((i = 0; i <= $((${#List[@]} - 1)); i++)); do
            echo "${List[i]}" | grep "pt_key=.*;" -q
            if [ $? -eq 0 ]; then
                pin="$(echo ${List[i]} | perl -pe "{s|.*pt_pin=([^; ]+)(?=;?).*|\1|}")"
                key="$(echo ${List[i]} | perl -pe "{s|.*pt_key=([^; ]+)(?=;?).*|\1|}")"
                ck="pt_key=${key};pt_pin=${pin};"

                curl -s -L -X POST "http://127.0.0.1:5678/openApi/updateCookie" \
                    -H "api-token: ${OpenApiToken}" \
                    -H "Content-Type: application/json" \
                    --data-raw "{\"cookie\": \"${ck}\"}"
                echo ''
            else
                continue
            fi
        done
        echo -e "\n$COMPLETE 批量添加/更新完成\n"
        ;;
    del)
        echo -e "\n$WORKING 检测到 ${BLUE}${#List[@]}${PLAIN} 个账号数据，开始批量删除...\n"
        for ((i = 0; i <= $((${#List[@]} - 1)); i++)); do
            pin="$(echo ${List[i]} | perl -pe "{s|.*pt_pin=([^; ]+)(?=;?).*|\1|}")"
            curl -s -L -X POST "http://127.0.0.1:5678/openApi/cookie/delete" \
                -H "api-token: ${OpenApiToken}" \
                -H "Content-Type: application/json" \
                --data-raw "{\"ptPins\": \"${pin}\"}"
            echo ''
        done
        echo -e "\n$COMPLETE 批量删除完成\n"
        ;;
    esac
}

case $# in
1)
    case $1 in
    add | del)
        Main "$1"
        ;;
    *)
        Help
        echo -e "$ERROR 不能这么用哦～\n"
        exit
        ;;
    esac
    ;;
*)
    Help
    ;;
esac
