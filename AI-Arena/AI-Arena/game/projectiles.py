import math
import pygame as pg


class Bullet:

    def __init__(
        self,
        position,
        direction,
        weapon,
        player_stats,
        play_area
    ):
        self.position = pg.Vector2(
            position
        )

        self.direction = pg.Vector2(
            direction
        )

        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        self.speed = (
            weapon["bullet_speed"]
            * player_stats["projectile_speed_multiplier"]
        )

        self.damage = (
            weapon["damage"]
            * player_stats["damage_multiplier"]
        )

        self.range = weapon["range"]

        self.radius = weapon[
            "bullet_radius"
        ]

        self.distance_traveled = 0

        self.play_area = play_area

        self.alive = True

    def update(
        self,
        dt,
        walls
    ):

        if not self.alive:
            return

        movement = (
            self.direction
            * self.speed
            * dt
        )

        distance = movement.length()

        steps = max(
            1,
            math.ceil(distance / 5)
        )

        step = movement / steps

        for _ in range(steps):

            self.position += step

            self.distance_traveled += (
                step.length()
            )

            if not self.play_area.collidepoint(
                round(self.position.x),
                round(self.position.y)
            ):

                self.alive = False
                return

            for wall in walls:

                if wall.collidepoint(
                    round(self.position.x),
                    round(self.position.y)
                ):

                    self.alive = False
                    return

            if (
                self.distance_traveled
                >= self.range
            ):

                self.alive = False
                return

    def draw(self, screen):

        if not self.alive:
            return

        pg.draw.circle(
            screen,
            (255, 220, 80),
            (
                round(self.position.x),
                round(self.position.y)
            ),
            self.radius
        )


class EnemyProjectile:

    def __init__(
        self,
        position,
        direction,
        damage,
        speed,
        max_range,
        radius,
        color,
        play_area
    ):

        self.position = pg.Vector2(
            position
        )

        self.direction = pg.Vector2(
            direction
        )

        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        self.damage = damage
        self.speed = speed
        self.max_range = max_range
        self.radius = radius
        self.color = color

        self.distance_traveled = 0

        self.play_area = play_area

        self.alive = True

    def update(
        self,
        dt,
        walls,
        player
    ):

        if not self.alive:
            return

        movement = (
            self.direction
            * self.speed
            * dt
        )

        distance = movement.length()

        steps = max(
            1,
            math.ceil(distance / 5)
        )

        step = movement / steps

        for _ in range(steps):

            self.position += step

            self.distance_traveled += (
                step.length()
            )

            if not self.play_area.collidepoint(
                round(self.position.x),
                round(self.position.y)
            ):

                self.alive = False
                return

            projectile_rect = pg.Rect(
                int(
                    self.position.x
                    - self.radius
                ),
                int(
                    self.position.y
                    - self.radius
                ),
                self.radius * 2,
                self.radius * 2
            )

            for wall in walls:

                if projectile_rect.colliderect(
                    wall
                ):

                    self.alive = False
                    return

            if (
                self.distance_traveled
                >= self.max_range
            ):

                self.alive = False
                return

            closest_x = max(
                player.left,
                min(
                    self.position.x,
                    player.right
                )
            )

            closest_y = max(
                player.top,
                min(
                    self.position.y,
                    player.bottom
                )
            )

            distance_to_player = math.hypot(
                self.position.x - closest_x,
                self.position.y - closest_y
            )

            if (
                distance_to_player
                <= self.radius
            ):

                self.alive = False
                return

    def draw(self, screen):

        if not self.alive:
            return

        pg.draw.circle(
            screen,
            self.color,
            (
                round(self.position.x),
                round(self.position.y)
            ),
            self.radius
        )