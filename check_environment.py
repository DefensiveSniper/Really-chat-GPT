"""
This module checks the environment for necessary configurations and settings.
该模块检查环境是否有必要的配置和设置。
"""
import os

def check_environment():
    print(os.environ.get('OPENAI_API_KEY'))
    print(os.environ.get('SPEECH_KEY'))
    print(os.environ.get('SPEECH_REGION'))
