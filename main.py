# main.py

import pygame
from resources import load_resources, get_image, get_audio

# 初始化pygame
pygame.init()

# 设置游戏窗口
SCREEN_WIDTH, SCREEN_HEIGHT = 288, 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Test')

# 加载资源
load_resources()

# 获取资源进行测试
bird_image = get_image('bluebird-upflap')
start_sound = get_audio('start')

# 设置帧率
FPS = 30
clock = pygame.time.Clock()

# 游戏主循环
running = True
while running:
    # 检查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 渲染背景
    screen.fill((255, 255, 255))  # 使用白色填充屏幕作为背景
    screen.blit(bird_image, (50, 100))  # 绘制小鸟图像

    # 更新游戏窗口
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

    # 测试音频播放
    if start_sound:
        start_sound.play()


# 退出游戏
pygame.quit()

