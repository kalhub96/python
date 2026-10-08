import pygame as pg


class Player:
    def __init__(self, position, width, height, stats):
        self.rect = pg.Rect(
            0,
            0,
            width,
            height
        )

        self.rect.center = position

        self.pos = pg.Vector2(
            self.rect.center
        )

        self.stats = stats
        self.health = stats["max_health"]
        self.damage_cooldown = 0.0

    @property
    def center(self):
        return self.rect.center

    @center.setter
    def center(self, value):
        self.rect.center = value
        self.pos.update(self.rect.center)

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value
        self.pos.update(self.rect.center)

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value
        self.pos.update(self.rect.center)

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, value):
        self.rect.left = value
        self.pos.update(self.rect.center)

    @property
    def right(self):
        return self.rect.right

    @right.setter
    def right(self, value):
        self.rect.right = value
        self.pos.update(self.rect.center)

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, value):
        self.rect.top = value
        self.pos.update(self.rect.center)

    @property
    def bottom(self):
        return self.rect.bottom

    @bottom.setter
    def bottom(self, value):
        self.rect.bottom = value
        self.pos.update(self.rect.center)

    def colliderect(self, other):
        return self.rect.colliderect(other)