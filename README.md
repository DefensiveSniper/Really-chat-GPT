# Really-chat-GPT
**简易的python请求OPENAI API（CHATGPT）语音聊天**
# 原理
Azure语音识别后转文本，文本发送至openai得到response，response交给TTS模型生成音频播放
目前TTS模型仅有openai和讯飞
# 功能
划线部分偏离项目初衷
 ~~`alt+c` - 切换模型~~
`alt+b` - 截取屏幕，下一次的语音交互在此基础上
~~`alt+r` - 读取文件、图片~~
~~`alt+p` - 图片生成，通过语音交互~~
`menu` - 语音交互
`esc` - 结束程序
# 使用
`demo.py`中包含划线功能，但没有讯飞TTS，上述说过偏离主题
`demo_only_chat.py`为最新更新，支持两种TTS以及**聊天记忆**，并且可以保存聊天内容
