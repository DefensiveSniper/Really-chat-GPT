# Really-chat-GPT
**真正意义上的chat**
# 原理
Azure语音识别后转文本，文本发送至AI模型得到response，response交给TTS模型生成音频播放
目前TTS模型仅有openai、讯飞以及azure
**推荐使用azure的tts，因为可以支持流式合成，即实时合成语音**
# 功能
划线部分偏离项目初衷
1. ~~`alt+c` - 切换模型~~
2. `alt+b` - 截取屏幕，下一次的语音交互在此基础上
3. ~~`alt+r` - 读取文件、图片~~
4. ~~`alt+p` - 图片生成，通过语音交互~~
5. `menu` - 语音交互
6. `esc` - 结束程序
# 使用
1. `demo.py`**为最新更新**,
2. `demo_only_chat.py`**已经没有进行维护，可能需要自行调整**
