from pagermaid import log
from pagermaid.enums import Client, Message
from pagermaid.utils import client
from pagermaid.listener import listener
import json

## Nolan 杂货铺公益API
API = 'http://api.nolanstore.top/JComExchange'

@listener(is_plugin=False, outgoing=True, command="code",
          description="\n解析京东APP口令，支持特价版和京喜",
          parameters="<口令>")

async def code(message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.arguments
    if not text:
        return await message.edit("**❌ 请输入要解析的口令或回复一条消息**")
    else:
        await message.edit("🕙 正在全力解析中，请稍后...")

    try:
        data = (await client.post(f"{API}", json={"code": text}))
    except:
        return await message.edit("**❌ 请检查网络连接或接口状态**")

    try:
        data = data.json()
        if (data["code"] == '0'):
            data = data["data"]

            push_msg = f"**【活动标题】** {data['title']}\n**【用户昵称】** {data['userName']}\n**【用户头像】** [点此查看]({data['headImg']})\n**【活动链接】** __{data['jumpUrl']}__"
            await log("code => 解析成功")

        elif (data["code"] == '400'):
            push_msg = "❌ 口令不存在，请检查是否正确！"
            await log("code => 口令不存在")

        else:
            push_msg = "口令不存在或解析失败，请检查口令是否正确！\n\n接口返回数据：\n" + str(json.dumps(data, indent=4, ensure_ascii=False))
            await log("code => 接口返回异常 " + str(data))

    except Exception as e:
        errorMsg = f"code => 第{e.__traceback__.tb_lineno}行：{e}"
        await log("code => 处理接口回传数据时遇到了错误 " + errorMsg)
        push_msg = "❌ 处理接口回传数据时遇到了错误"

    await message.edit(push_msg, disable_web_page_preview=True)
