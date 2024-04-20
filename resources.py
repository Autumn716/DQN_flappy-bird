# resources.py

import pygame
import os

# 定义资源目录路径
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

# 初始化资源字典
IMAGES = {}
AUDIO = {}


def load_resources():
    # 加载所有图像资源
    for image in os.listdir(os.path.join(ASSETS_PATH, 'sprites')):
        name, extension = os.path.splitext(image)
        path = os.path.join(ASSETS_PATH, 'sprites', image)
        IMAGES[name] = pygame.image.load(path)

    # 加载所有音频资源
    for audio in os.listdir(os.path.join(ASSETS_PATH, 'audio')):
        name, extension = os.path.splitext(audio)
        path = os.path.join(ASSETS_PATH, 'audio', audio)
        AUDIO[name] = pygame.mixer.Sound(path)


def get_image(name):

    return IMAGES.get(name)


def get_audio(name):

    return AUDIO.get(name)

