import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "ba ga ya lu"
import pygame

# 初始化 pygame 的混音器模块
pygame.mixer.init()

def play_mp3(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
