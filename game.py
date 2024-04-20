# flappy bird #
import pygame
import random
import os

# Constants 常量
W, H = 288, 512  # 背景图尺寸
FPS = 30         # 游戏帧率

# Setup 设置
pygame.init()
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption('Flappy bird——code by Muhao')  # 标题栏命名
CLOCK = pygame.time.Clock()

# Materials 素材
IMAGES = {}
for image in os.listdir('assets/sprites'):
    name, extension = os.path.splitext(image)
    path = os.path.join('assets/sprites', image)
    IMAGES[name] = pygame.image.load(path)

FLOOR_Y = H - IMAGES['floor'].get_height()  # 地板高度

AUDIO = {}
for audio in os.listdir('assets/audio'):
    name, extension = os.path.splitext(audio)
    path = os.path.join('assets/audio', audio)
    AUDIO[name] = pygame.mixer.Sound(path)


def main():
    while True:
        AUDIO['start'].play()
        IMAGES['bgpic'] = IMAGES[random.choice(
            ['background-day', 'background-night'])]
        color = random.choice(['bluebird', 'redbird', 'yellowbird'])
        IMAGES['birds'] = [IMAGES[color + '-upflap'],
                           IMAGES[color + '-midflap'], IMAGES[color + '-downflap']]
        pipe = IMAGES[random.choice(['pipe-green', 'pipe-red'])]
        IMAGES['pipes'] = [pipe, pygame.transform.flip(pipe, False, True)]
        menu_window()
        result = game_window()
        end_window(result)


def menu_window():

    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0

    guide_x = (W - IMAGES['guide'].get_width()) / 2
    guide_y = (FLOOR_Y - IMAGES['guide'].get_height()) / 2
    bird_x = W * 0.2
    bird_y = (H - IMAGES['birds'][0].get_height()) / 2
    bird_y_vel = 1  # 小鸟Y轴方向速度
    bird_y_range = [bird_y - 8, bird_y + 8]

    idx = 0
    repeat = 5  # 每repeat帧添加一个动画
    frames = [0] * repeat + [1] * repeat + [2] * repeat + [1] * repeat

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        # 地板坐标移动
        floor_x -= 4
        if floor_x <= - floor_gap:
            floor_x = 0

        # 小鸟Y轴坐标移动
        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1  # 改变小鸟Y轴速度方向

        # 小鸟翅膀动画
        idx += 1
        idx %= len(frames)

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        SCREEN.blit(IMAGES['guide'], (guide_x, guide_y))
        SCREEN.blit(IMAGES['birds'][frames[idx]], (bird_x, bird_y))
        pygame.display.update()
        CLOCK.tick(FPS)


def game_window():

    score = 0

    AUDIO['flap'].play()
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0

    bird = Bird(W * 0.2, H * 0.4)

    n_pairs = 4
    distance = 150  # 左右水管间距
    pipe_gap = 150  # 上下水管间距
    pipe_group = pygame.sprite.Group()
    for i in range(n_pairs):
        pipe_y = random.randint(int(H * 0.3), int(H * 0.6))
        pipe_up = Pipe(W + i * distance, pipe_y, True)
        pipe_down = Pipe(W + i * distance, pipe_y - pipe_gap, False)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)

    while True:
        # 默认翅膀没有扇动
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flap = True
                    AUDIO['flap'].play()

        floor_x -= 4
        if floor_x <= - floor_gap:
            floor_x = 0

        bird.update(flap)
        # 如果小鸟飞出屏幕或者飞到地板，触发撞击和死亡音效
        if bird.rect.y > FLOOR_Y or bird.rect.y < 0 or pygame.sprite.spritecollideany(
                bird, pipe_group):
            AUDIO['hit'].play()
            AUDIO['die'].play()
            result = {'bird': bird, 'pipe_group': pipe_group, 'score': score}
            return result

        first_pipe_up = pipe_group.sprites()[0]
        first_pipe_down = pipe_group.sprites()[1]
        if first_pipe_up.rect.right < 0:
            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(
                first_pipe_up.rect.x +
                n_pairs *
                distance,
                pipe_y,
                True)
            new_pipe_down = Pipe(
                first_pipe_down.rect.x +
                n_pairs *
                distance,
                pipe_y -
                pipe_gap,
                False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()

        pipe_group.update()

        if bird.rect.left + first_pipe_up.x_vel < first_pipe_up.rect.centerx < bird.rect.left:
            score += 1
            AUDIO['score'].play()

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))

        show_score(score)

        SCREEN.blit(bird.imge, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)


def end_window(result):
    gameover_x = (W - IMAGES['gameover'].get_width()) / 2
    gameover_y = (H - IMAGES['gameover'].get_height()) / 2

    bird = result['bird']
    pipe_group = result['pipe_group']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        bird.go_die()

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, FLOOR_Y))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        show_score(result['score'])
        SCREEN.blit(bird.imge, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)


def show_score(score):
    score_str = str(score)
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1
    x = (W - n * w) / 2
    y = H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))
        x += w


class Bird:
    def __init__(self, x, y):
        self.frames = [0] * 5 + [1] * 5 + [2] * 5 + [1] * 5
        self.idx = 0
        self.imges = IMAGES['birds']
        self.imge = self.imges[self.frames[self.idx]]
        self.rect = self.imge.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = -10
        self.max_y_vel = 10
        self.gravity = 1  # 重力加速度
        self.rotate = 45  # 旋转角度
        self.max_rotate = -20  # 最大旋转角度
        self.rotate_vel = -3

        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45

    def update(self, flap=False):

        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap
        # 更新Y轴速度
        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)
        # 更新Y轴坐标
        self.rect.y += self.y_vel
        # 更新角度
        self.rotate = max(self.rotate + self.rotate_vel, self.max_rotate)

        self.idx += 1
        self.idx %= len(self.frames)
        self.imge = IMAGES['birds'][self.frames[self.idx]]
        self.imge = pygame.transform.rotate(self.imge, self.rotate)

    def go_die(self):
        if self.rect.y < FLOOR_Y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.imge = self.imges[self.frames[self.idx]]
            self.imge = pygame.transform.rotate(self.imge, self.rotate)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards=True):
        pygame.sprite.Sprite.__init__(self)
        if upwards:
            self.image = IMAGES['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        else:
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
        self.x_vel = -4

    def update(self):
        self.rect.x += self.x_vel


main()
