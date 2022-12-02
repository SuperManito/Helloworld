'''
活动线报人形 PagerMaid-Pyro Bot 监控插件（一键命令版）
Author: SuperManito
Version: 2.0
Modified: 2022-12-02

友情提示：如果阁下喜欢用记事本编辑此脚本，那么如果报错了请不要在群里问，容易挨打

工作原理: 
监控本群线报Bot发送的消息，将二次处理后的命令发送至用户容器Bot通过 /cmd 指令运行，群线报自带去重功能，目前默认30分钟内不会重复，0~2点会动态调整为1时

配置方法:
自行使用带有语法检测的专业代码编辑器进行配置，首先需要定义你的容器 Bot id (user_id)，监控脚本自行定义，默认附带了几个，注意看注释内容

'''

from pagermaid import bot, log
from pagermaid.single_utils import sqlite
from pagermaid.enums import Client, Message
from pagermaid.utils import lang, client
from pagermaid.listener import listener
from datetime import datetime

from asyncio import sleep
import re, os, time

## ⚠ 容器Bot id
ID_BOT = 1234567890
## 调试模式
DEBUG_MODE = False

## 处理命令
async def filters(text):

    def getSqlite(value):
        return sqlite.get(f"forwardMark." + value)

    # 初始化一些变量
    is_lzkj = is_lzkjdz = is_cjhy = is_cjhydz = is_txzj = enable_proxy = False # 过滤标记
    NowHour = os.popen("echo -n $(TZ=UTC-8 date +%H)").read() # 读取当前北京时间的小时数

    # ⚠ 用户需知:
    # 1. return False 或返回空值为不执行任何命令即不监控对应线报
    # 2. 注意代码格式与缩进，建议使用带有语法检测的专业代码编辑器
    # 3. 你需要了解各个脚本所对应的活动玩法以及活动域名，不要盲目设置监控，不建议监控任何开卡
    # 4. 在 try 作用域下代码报错会自动向你的bot发送错误信息，但是不一定会影响监控的正常运行

    try:

        ## 定义你的运行账号（凌晨线报较多，合理安排运行账号，你也可以自定义此可选参数变量）
        if NowHour in ['23', '00', '01', '02']:
            LZKJ_RUNS = " -c 1-2"
            CJHY_RUNS = " -c 1-2"
            TXZJ_RUNS = " -c 1-2"
            ADDCARTS_RUNS = " -c 1"
        else:
            LZKJ_RUNS = " -c 1-4"
            CJHY_RUNS = " -c 1-4"
            TXZJ_RUNS = " -c 1-4"
            ADDCARTS_RUNS = " -c 1"


        ## 定义针对对应类型的脚本是否启用 HTTP/HTTPS 全局代理（--agent）
        LZKJ_PROXY = False
        LZKJDZ_PROXY = False
        CJHY_PROXY = False
        CJHYDZ_PROXY = False
        TXZJ_PROXY = False


        ## 常规脚本匹配
        if "task env edit " in text:
            ## 匹配脚本名
            script = re.search(r'KingRan_KR/(.*?)\b ', text, re.M | re.I)[1]

            # 脚本类型屏蔽标记判断（勿动）
            if 'https://lzkj' in text:
                is_lzkj = True
                if 'https://lzkjdz' in text:
                    is_lzkjdz = True
            elif 'https://cjhy' in text:
                is_cjhy = True
                if 'https://cjhydz' in text:
                    is_cjhydz = True
            elif 'https://txzj' in text:
                is_txzj = True

            # 注释：
            # text += xxx   可以理解为追加 xxx 内容
            # text = text   执行原命令（即执行所有账号）

            # 脚本类型：
            # lzkj 域名活动为超级无线
            # cjhy 域名活动为超级会员
            # txzj 域名活动为收藏大师

            match script:

                # 店铺抽奖 · 超级无线/超级会员
                case 'jd_luck_draw.js':
                    text += LZKJ_RUNS if is_lzkj else CJHY_RUNS

                # 加购有礼 · 超级无线/超级会员
                case 'jd_wxCollectionActivity.js':
                    text += ADDCARTS_RUNS

                # 关注店铺有礼 · 超级无线/超级会员
                case 'jd_wxShopFollowActivity.js':
                    text += LZKJ_RUNS if is_lzkj else CJHY_RUNS

                # 店铺礼包 · 超级无线/超级会员
                case 'jd_wxShopGift.js':
                    text += LZKJ_RUNS if is_lzkj else CJHY_RUNS

                # 知识超人 · 超级无线/超级会员
                case 'jd_wxKnowledgeActivity.js':
                    text += LZKJ_RUNS if is_lzkj else CJHY_RUNS

                # 店铺抽奖中心 · 超级无线
                case 'jd_drawCenter.js':
                    text += LZKJ_RUNS
                    is_lzkj = True # 用于屏蔽标记判断（勿动）

                # 读秒拼手速 · 超级无线
                case 'jd_wxSecond.js':
                    text += LZKJ_RUNS
                    is_lzkj = is_lzkjdz = True # 用于屏蔽标记判断（勿动）

                # 无线游戏 · 超级无线
                case 'jd_wxgame.js':
                    text += LZKJ_RUNS
                    is_lzkj = True # 用于屏蔽标记判断（勿动）

                # 集卡有礼 · 超级无线
                case 'jd_wxCollectCard.js':
                    text += LZKJ_RUNS
                    is_lzkj = is_lzkjdz = True # 用于屏蔽标记判断（勿动）

                # 粉丝互动 · 超级无线
                case 'jd_wxFansInterActionActivity.js':
                    text += LZKJ_RUNS
                    is_lzkj = is_lzkjdz = True # 用于屏蔽标记判断（勿动）

                # 分享有礼 · 超级无线
                case 'jd_wxShareActivity.js':
                    text = text
                    is_lzkj = is_lzkjdz = True # 用于屏蔽标记判断（勿动）

                # 组队瓜分奖品 · 超级无线
                case 'jd_zdjr.js':
                    text = text

                # 组队瓜分奖品 · 超级会员
                case 'jd_cjzdgf.js':
                    text = text

                # 加购有礼 · 收藏大师
                case 'jd_txzj_cart_item.js':
                    text += ADDCARTS_RUNS

                # 关注商品有礼 · 收藏大师
                case 'jd_txzj_collect_item.js':
                    text += TXZJ_RUNS

                # 关注店铺有礼 · 收藏大师
                case 'jd_txzj_collect_shop.js':
                    text += TXZJ_RUNS

                # 幸运抽奖 · 收藏大师
                case 'jd_txzj_lottery.js':
                    text += TXZJ_RUNS

                # 购物车锦鲤 · 超级无线
                # case 'jd_wxCartKoi.js':
                #     text += ADDCARTS_RUNS
                #     is_lzkj = True

                # 微定制瓜分京豆 · 超级会员
                # case 'jd_wdz.js':
                #     text = text
                #     is_cjhy = True

                # 大牌集合 · 京耕
                # case 'jd_opencardDPLHTY.js':
                #     text = text

                # joyjd抽奖机
                # case 'jd_lottery.js':
                #     text = text

                # joyjd开卡
                # case 'jd_joyopen.js':
                #     text = text

                case _:
                    await debugMode("未匹配到对应监控脚本")
                    return False

        else:
            return False

        ## 监控屏蔽和脚本代理（勿动）
        if is_lzkj:
            if getSqlite("disable_lzkj"):
                await debugMode("超级无线活动已被屏蔽")
                return False
            if LZKJ_PROXY:
                enable_proxy = True
        elif is_lzkjdz:
            if getSqlite("disable_lzkjdz"):
                await debugMode("超级无线（定制）活动已被屏蔽")
                return False
            if LZKJDZ_PROXY:
                enable_proxy = True
        elif is_cjhy:
            if getSqlite("disable_cjhy"):
                await debugMode("超级会员活动已被屏蔽")
                return False
            if CJHY_PROXY:
                enable_proxy = True
        elif is_cjhydz:
            if getSqlite("disable_cjhydz"):
                await debugMode("超级会员（定制）活动已被屏蔽")
                return False
            if CJHYDZ_PROXY:
                enable_proxy = True
        elif is_txzj:
            if getSqlite("disable_txzj"):
                await debugMode("收藏大师活动已被屏蔽")
                return False
            if TXZJ_PROXY:
                enable_proxy = True

        ## 设置一些脚本运行参数
        if " now" in text:
            # 迅速模式
            text += " -r"
            # 脚本 HTTP/HTTPS 全局代理
            if enable_proxy:
                text += " -a"

        text = "/cmd " + text
        return text

    except Exception as e:
        errorMsg = f"❌ 第{e.__traceback__.tb_lineno}行：{e}"
        await log(errorMsg)
        await bot.send_message(int(ID_BOT), "❌ 阁下修改的脚本报错了！\n\n错误内容：" + errorMsg)
        return False






## ⚠⚠⚠
## ⬇️ 不懂勿动 ⬇️

## 监控群组ID
ID_FROM = -1001615491008
## 监控消息发送者（由用户id组成的数组）
ID_ARRAY = [5116402142]

@listener(is_plugin=False, outgoing=True, command="forward",
          description='\n线报监控插件（群用户公开版）',
          parameters="`"
                     "\n\n**开启监控**:\n `,forward enable`"
                     "\n\n**关闭监控**:\n `,forward disable`"
                     "\n\n**设置标记**:\n `,forward set <字符串>`"
                     "\n\n**移除标记**:\n `,forward unset <字符串>\n")
async def forward(message: Message):
    errMsg = "出错了呜呜呜 ~ 无法识别的来源对话。"

    if ID_BOT == '1234567890':
        await message.edit("⚠ 请先在此脚本中定义你的容器 BOT id 后才能使用哦~")
        await sleep(5)
        await message.delete()
        return

    ## 开启监控
    if message.parameter[0] == "enable":
        # 检查来源频道/群组
        try:
            channel = await bot.get_chat(ID_FROM)
        except Exception as e:
            errorMsg = f"第{e.__traceback__.tb_lineno}行：{e}"
            await message.edit(f"{errMsg}\n\n{errorMsg}")
            return

        # 记录id至数据库
        if not sqlite.get(f"forward.{channel.id}"):
            sqlite[f"forward.{channel.id}"] = ID_BOT
        else:
            await message.edit('❌ 插件正在运行中，无需再次启用')
            await sleep(5)
            await message.delete()
            return

        # 返回消息
        await message.edit(f"**已启用公共线报消息监控 ✅**")
        await bot.send_message(int(ID_BOT), "**监控已启用 ▶️**")
        await log(f"线报监控已启用")
        await sleep(5)
        await message.delete()

        ## 删除消息 
        await sleep(5)
        await message.delete()


    ## 关闭监控
    elif message.parameter[0] == "disable":
        # 检查来源频道/群组
        try:
            channel = await bot.get_chat(ID_FROM)
        except Exception as e:
            errorMsg = f"第{e.__traceback__.tb_lineno}行：{e}"
            await message.edit(f"{errMsg}\n\n{errorMsg}")
            return

        # 从数据库移除id
        try:
            del sqlite[f"forward.{channel.id}"]
        except:
            await message.edit('❌ 目标对话没有启用监控')
            await sleep(5)
            await message.delete()
            return

        # 返回消息
        await message.edit(f"已停用消息监控插件 ❌")
        await bot.send_message(int(ID_BOT), "**监控已关闭 🚫**")
        await log(f"线报监控已关闭")

        ## 删除消息 
        await sleep(5)
        await message.delete()


    ## 设置标记
    elif (message.parameter[0] == "set") and (len(message.parameter) == 2):
        keys = message.parameter[1]

        if sqlite.get(f"forwardMark.{keys}"):
            await message.edit(f"❌ 已在数据库中设置当前标记（无法添加）")
        else:
            sqlite[f"forwardMark.{keys}"] = ID_BOT
            await message.edit(f"已设置 __{keys}__ 用户监控标记 ✅")

        ## 删除消息 
        await sleep(5)
        await message.delete()


    ## 移除标记
    elif (message.parameter[0] == "unset") and (len(message.parameter) == 2):
        keys = message.parameter[1]

        if sqlite.get(f"forwardMark.{keys}"):
            del sqlite[f"forwardMark.{keys}"]
            await message.edit(f"已移除 __{keys}__ 用户监控标记 ❎")
        else:
            await message.edit(f"❌ 未在数据库中设置当前标记（无法移除）")

        ## 删除消息 
        await sleep(5)
        await message.delete()


    else:
        return await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")


@listener(is_plugin=False, incoming=True, ignore_edited=True)
async def forward_message(message: Message):
    try:
        if not sqlite.get(f"forward.{message.chat.id}"):
            return
        # await bot.send_message(int(ID_BOT), str(message))

        # 定义监控范围（由消息发送者id组成的数组），忽略匿名管理员
        if message.from_user:
            from_user = message.from_user
            ## 判断是否在监控名单中
            if from_user.id not in ID_ARRAY:
                return
        else:
            # 匿名管理员
            return

        ## 匹配带有执行命令的消息且原消息不能为空
        text = message.text.markdown
        if text != '' and '`' in text:
            text = text.split('`')[1]
        else:
            await debugMode("线报内容的语法格式不符合要求")
            return

        ## 去解析命令
        results = await filters(text)
        await log(f"forward 监控到新消息：{str(text)}") # 打印日志
        if not results:
            await debugMode("线报经过函数处理后返回为空")
            return

        if results != '':
            await bot.send_message(int(ID_BOT), results)

    except Exception as e:
        errorMsg = f"❌ 第{e.__traceback__.tb_lineno}行：{e}"
        await log(errorMsg)
        await bot.send_message(int(ID_BOT), "❌ 脚本报错了！\n\n错误内容：" + errorMsg)
        return False


async def debugMode(msg):
    if DEBUG_MODE:
        timeStr = str(datetime.fromtimestamp(int(time.time())))
        await bot.send_message(int(ID_BOT), timeStr + f"\n🔧 debug: {msg}")

## ⬆️ 不懂勿动 ⬆️