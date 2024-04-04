from random import randint, choice

import pgzrun


WIDTH = 1024
HEIGHT = 768
TITLE = "DINO JUMP"

BACKGROUNDS = [
    "#004400",
    "#000066",
    "#663300",
    "#223366",
    "#660022",
    "#002244",
    "#330044",
    "#224433",
    "#004466",
]


class Dino:
    GRAVITY = 1

    def __init__(self):
        self.actor = Actor("dino")
        self.x: int
        self.y: int
        self.speed: int
        self.bottom: int
        self.score: int
        self.background: str

        self.reset()
        self.place()

    def reset(self):
        self.x = WIDTH // 8
        self.y = HEIGHT - self.actor.height
        self.bottom = self.y
        self.speed = 0
        self.score = 0
        self.background: str = choice(BACKGROUNDS)

    def place(self):
        self.actor.topleft = self.x, self.y

    def update(self):
        self.speed += self.GRAVITY
        self.y += self.speed
        if self.y >= self.bottom:
            self.y = self.bottom
            self.speed = 0
        self.place()

    def jump(self):
        if self.y >= self.bottom:
            self.speed = -35 * self.GRAVITY
            sounds.mario.play()
        self.place()

    def collisions(self):
        for cactus in cactuses:
            if dino.actor.colliderect(cactus.actor):
                self.score = 0
                sounds.mario.stop()
                sounds.eep.play()
                cactus.reset()
                cactus.reset_x()

    def update_score(self):
        for cactus in cactuses:
            if (self.x > cactus.x + cactus.width) and not cactus.passed:
                cactus.passed = True
                self.score += 1
                if self.score >= 3 and (self.score % 3) == 0:
                    self.background = choice(BACKGROUNDS)

    def draw_score(self):
        screen.draw.text(
            str(self.score),
            (WIDTH // 10, HEIGHT // 10),
            color="white",
            owidth=1,
            fontsize=100,
        )


class Cactus:

    def __init__(self, x):
        self.actor = Actor("cactus")
        self.x = x
        self.y: int
        self.speed: int
        self.color: str
        self.reset()
        self.place()

    def reset(self):
        self.speed = WIDTH // 100
        self.y = HEIGHT - self.actor.height
        self.passed = False
        self.width = self.actor.width

    def place(self):
        self.actor.topleft = self.x, self.y

    def reset_x(self):
        self.x = 2 * WIDTH + randint(0, WIDTH // 10)
        for cactus in cactuses:
            if cactus is self:
                continue
            if abs(cactus.x - self.x) < 1600:
                self.x = cactus.x + 1600

    def update(self):
        self.x -= self.speed
        if self.x < -self.actor.width:
            self.reset_x()
            self.passed = False
        self.place()

    def draw(self):
        self.actor.draw()


class Cloud:
    def __init__(self, x, y):
        self.actor = Actor("cloud")
        self.actor.topleft = x, y

    def draw(self):
        self.actor.draw()

    def update(self):
        x, y = self.actor.topleft
        x = x - 0.3
        if x < -self.actor.width:
            x = 2000
        self.actor.topleft = x, y


class Clouds:
    def __init__(self):
        self.clouds = [Cloud(200 * i, 100 + 100 * (i % 2)) for i in range(20)]

    def draw(self):
        for cloud in self.clouds:
            cloud.draw()

    def update(self):
        for cloud in self.clouds:
            cloud.update()


class Road:
    MAX = 3 * WIDTH
    SP_WIDTH = 32

    def __init__(self):
        self.actors = [Actor("road") for _ in range(self.MAX // self.SP_WIDTH)]
        for index, actor in enumerate(self.actors):
            actor.topleft = self.SP_WIDTH * index, HEIGHT + 16

    def draw(self):
        for actor in self.actors:
            actor.draw()

    def update(self):
        for actor in self.actors:
            x, y = actor.topleft
            x -= 1
            if x < -self.SP_WIDTH:
                x = self.MAX
            actor.topleft = x, y


def check_keys():
    if keyboard.ESCAPE or keyboard.Q:
        exit()
    if keyboard.SPACE:
        dino.jump()


def draw_floor():
    screen.draw.filled_rect(Rect((0, HEIGHT), (WIDTH * 5, HEIGHT)), "#565656")


def draw_jump_marker():
    screen.draw.filled_rect(Rect((dino.x + 500, HEIGHT - 30), (30, 30)), "red")


def update():
    check_keys()
    dino.update()
    dino.collisions()
    dino.update_score()
    for cactus in cactuses:
        cactus.update()
    road.update()
    clouds.update()


def draw():
    screen.fill(dino.background)
    draw_floor()
    clouds.draw()

    dino.actor.draw()
    for cactus in cactuses:
        cactus.draw()
    draw_jump_marker()
    dino.draw_score()
    road.draw()


dino = Dino()
cactuses = [Cactus(2000), Cactus(3600)]
clouds = Clouds()
road = Road()


pgzrun.go()
