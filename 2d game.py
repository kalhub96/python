import pygame as pg
import random
import math


# ============================================================
# INITIALIZATION
# ============================================================

pg.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TOP_BAR_HEIGHT = 70

screen = pg.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pg.display.set_caption("AI Arena")

clock = pg.time.Clock()


PLAY_AREA = pg.Rect(
    0,
    TOP_BAR_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT - TOP_BAR_HEIGHT
)


# ============================================================
# GAME SETTINGS
# ============================================================

level = 1
wave_number = 1

GAME_STATE_PREP = "prep"
GAME_STATE_ACTIVE = "active"
GAME_STATE_COMPLETE = "complete"
GAME_STATE_UPGRADE = "upgrade"
GAME_STATE_GAME_OVER = "game_over"

GAME_STATE_HOME = "home"
GAME_STATE_SHOP = "shop"

game_state = GAME_STATE_HOME

WAVE_COMPLETE_TIME = 2.0
wave_complete_timer = 0.0
wave_complete_number = 0


# ============================================================
# AI SEARCH SETTINGS
# ============================================================

SEARCH_RADIUS = 180
SEARCH_TIME = 6.0
SEARCH_POINT_REACHED_DISTANCE = 15

AI_CHASE = "chase"
AI_SEARCH = "search"
AI_IDLE = "idle"


# ============================================================
# AI ATTACKER LOCATION SETTINGS
# ============================================================

ATTACKER_ESTIMATE_DISTANCE = 300
ATTACKER_MEMORY_TIME = 8.0

# How far an enemy searches around the estimated attacker.
ATTACKER_SEARCH_RADIUS = 180


# ============================================================
# AI COMMUNICATION SETTINGS
# ============================================================

COMMUNICATION_RANGE = 450
COMMUNICATION_COOLDOWN = 0.8
COMMUNICATION_MEMORY_TIME = 8.0
COMMUNICATION_DISPLAY_TIME = 0.35

MESSAGE_PLAYER_SPOTTED = "player_spotted"
MESSAGE_PLAYER_LOST = "player_lost"
MESSAGE_UNDER_ATTACK = "under_attack"
MESSAGE_ATTACK_LOCATION = "attack_location"


# ============================================================
# PLAYER SETTINGS
# ============================================================

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

PLAYER_DAMAGE_MULTIPLIER = 0.6
PLAYER_DAMAGE_COOLDOWN = 0.5

player_damage_timer = 0.0


# ============================================================
# PLAYER BASE STATS
# ============================================================

PLAYER_BASE_STATS = {
    "max_health": 100,
    "move_speed": 300,
    "damage_multiplier": 1.0,
    "fire_rate_multiplier": 1.0,
    "damage_reduction": 0.0,
    "vision_range": 300,
    "projectile_speed_multiplier": 1.0,
}

player_stats = PLAYER_BASE_STATS.copy()

player_health = player_stats["max_health"]


# ============================================================
# SAFE ZONE
# ============================================================

SAFE_ZONE = pg.Rect(
    30,
    TOP_BAR_HEIGHT + 30,
    220,
    180
)


# ============================================================
# PLAYER WEAPON
# ============================================================

WEAPON = {
    "name": "Pistol",
    "damage": 25,
    "fire_rate": 0.25,
    "bullet_speed": 850,
    "range": 700,
    "bullet_radius": 5
}

weapon_fire_timer = 0.0


# ============================================================
# PLAYER UPGRADES
# ============================================================

PLAYER_UPGRADES = {

    "vitality": {
        "name": "Vitality",
        "description": "+20 maximum HP and restore 20 HP",
        "icon": "HP",
        "effect": "MAX HP +20"
    },

    "speed": {
        "name": "Speed",
        "description": "+30 movement speed",
        "icon": "SPD",
        "effect": "MOVE SPEED +30"
    },

    "damage": {
        "name": "Damage",
        "description": "Increase weapon damage by 15%",
        "icon": "DMG",
        "effect": "DAMAGE +15%"
    },

    "fire_rate": {
        "name": "Fire Rate",
        "description": "Increase weapon fire rate by 10%",
        "icon": "FR",
        "effect": "FIRE RATE +10%"
    },

    "armor": {
        "name": "Armor",
        "description": "Reduce incoming damage by 10%",
        "icon": "ARM",
        "effect": "DAMAGE TAKEN -10%"
    },

    "vision": {
        "name": "Vision",
        "description": "+40 player vision range",
        "icon": "VIS",
        "effect": "VISION +40"
    },

    "projectile_speed": {
        "name": "Projectile Speed",
        "description": "Increase bullet speed by 15%",
        "icon": "PS",
        "effect": "BULLET SPEED +15%"
    }
}


# ============================================================
# ENEMY TYPES
# ============================================================

ENEMY_TYPES = {

    "grunt": {
        "health": 100,
        "speed": 120,
        "damage": 10,
        "color": (220, 60, 60),
        "size": 40,
        "shape": "square"
    },

    "runner": {
        "health": 25,
        "speed": 250,
        "damage": 15,
        "color": (255, 180, 40),
        "size": 30,
        "shape": "triangle"
    },

    "tank": {
        "health": 300,
        "speed": 50,
        "damage": 20,
        "color": (120, 120, 120),
        "size": 60,
        "shape": "hexagon"
    },

    "shooter": {
        "health": 75,
        "speed": 100,
        "damage": 15,
        "color": (80, 150, 255),
        "size": 35,
        "shape": "circle"
    },

    "splitter": {
        "health": 50,
        "speed": 150,
        "damage": 15,
        "color": (180, 80, 220),
        "size": 40,
        "shape": "diamond"
    },
    
    "witch": {
        "health": 60,
        "speed": 140,
        "damage": 30,
        "color": (120, 50, 220),
        "size": 34,
        "shape": "witch"
    },

    "boss": {
        "health": 1000,
        "speed": 75,
        "damage": 75,
        "color": (255, 50, 180),
        "size": 80,
        "shape": "octagon"
    } 
    
}


# ============================================================
# ENEMY WEAPONS
# ============================================================

ENEMY_WEAPONS = {

    "grunt": {
        "type": "melee",
        "damage": 10,
        "fire_rate": 0.5,
        "range": 65
    },

    "runner": {
        "type": "melee",
        "damage": 15,
        "fire_rate": 0.35,
        "range": 70
    },

    "shooter": {
        "type": "ranged",
        "damage": 12,
        "fire_rate": 0.8,
        "range": 500,
        "projectile_speed": 600,
        "projectile_range": 500,
        "projectile_radius": 4,
        "projectile_color": (80, 150, 255)
    },

    "tank": {
        "type": "ranged",
        "damage": 40,
        "fire_rate": 2.5,
        "range": 350,
        "projectile_speed": 450,
        "projectile_range": 350,
        "projectile_radius": 10,
        "projectile_color": (170, 170, 170)
    },

    "splitter": {
        "type": "ranged",
        "damage": 20,
        "fire_rate": 1.2,
        "range": 450,
        "projectile_speed": 550,
        "projectile_range": 450,
        "projectile_radius": 6,
        "projectile_color": (180, 80, 220)
    },
    
    "witch": {
        "type": "ranged",
        "damage": 30,
        "fire_rate": 1.5,
        "range": 500,
        "projectile_speed": 500,
        "projectile_range": 500,
        "projectile_radius": 8,
        "projectile_color": (180, 70, 255)
    },

    "boss": {
        "type": "ranged",
        "damage": 60,
        "fire_rate": 1.8,
        "range": 600,
        "projectile_speed": 500,
        "projectile_range": 600,
        "projectile_radius": 12,
        "projectile_color": (255, 50, 180),
        "projectile_count": 3,
        "spread": 12
    }
}


# ============================================================
# ENEMY SPAWN PROBABILITY
# ============================================================

WAVE_SPAWN_WEIGHTS = {
    1: {"grunt": 100},
    2: {"grunt": 70, "runner": 30},
    3: {"grunt": 60, "runner": 25, "shooter": 12, "witch": 3},
    4: {"grunt": 55, "runner": 20, "shooter": 15, "tank": 10},
    5: {"grunt": 45, "runner": 20, "shooter": 15, "tank": 10, "splitter": 6, "witch": 4},
    6: {"grunt": 25, "runner": 20, "shooter": 15, "tank": 15, "splitter": 21, "witch": 2, "boss": 2}
}

WAVE_ENEMY_COUNTS = {
    1: 5,
    2: 10,
    3: 15,
    4: 20,
    5: 30,
    6: 40
}


def choose_enemy_type():
    weights = WAVE_SPAWN_WEIGHTS.get(
        wave_number,
        {"grunt": 100}
    )

    return random.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=1
    )[0]

# ============================================================
# DROP ITEM CHANCE
# ============================================================

ITEM_TYPE  = {
    "health": {
        "chance": 0.40,
        "value": 60,
    },
    
    "coin": {
        "chance": 0.50,
        "value": 10,
    },
    
    "ammo": {
        "chance": 0.10,
        "value": 20,
    },
}
 
# ============================================================
# ITEM CLASS
# ============================================================ 

class Item:
    def __init__(self, item_type, position):
        self.type = item_type
        self.pos = pg.Vector2(position)
        self.size = 20
    
    def draw(self,screen):
        if self.type == "health":
            pg.draw.circle(
                screen, (50, 220, 80), 
                (int(self.pos.x), int(self.pos.y)),
                self.size // 2
            )
        
        elif self.type == "coin":
            pg.draw.circle(
                screen, (255, 220,50), 
                (int(self.pos.x),int(self.pos.y)),
                self.size // 2
            )

        elif self.type == "ammo":
            pg.draw.rect(
                screen, (80, 150, 255),(
                    int(self.pos.x - 8),
                    int(self.pos.y - 8),
                    16,
                    16
                )
            )
    
# ============================================================
# SPAWN DELAYS
# ============================================================

SPAWN_DELAY = {
    "grunt": 0.3,
    "runner": 0.5,
    "shooter": 1.5,
    "tank": 4.0,
    "splitter": 2.0,
    "witch": 2.0,
    "boss": 10.0
}

# ============================================================
# ENEMY DROP CHANCES
# ============================================================

ENEMY_DROPS = {
    "grunt": {"chance": 0.20, "items": ["coin"]},
    "runner": {"chance": 0.15, "items": ["coin", "ammo"]},
    "shooter": {"chance": 0.25, "items": ["coin", "ammo"]},
    "tank": {"chance": 0.50, "items": ["coin", "health"]},
    "splitter": {"chance": 0.40, "items": ["coin", "ammo"]},
    "witch": {"chance": 0.75, "items": ["coin", "health"]},
    "boss": {"chance": 1.00, "items": ["coin", "health", "ammo"]}
}


def drop_item(enemy):
    drop_data = ENEMY_DROPS.get(enemy.type)

    if not drop_data:
        return

    if random.random() > drop_data["chance"]:
        return

    item_type = random.choice(drop_data["items"])

    items.append(
        Item(item_type, enemy.rect.center)
    )

# ============================================================
# PLAYER
# ============================================================

player = pg.Rect(
    0,
    0,
    PLAYER_WIDTH,
    PLAYER_HEIGHT
)

player.center = SAFE_ZONE.center

player_pos = pg.Vector2(
    player.center
)


# ============================================================
# GLOBAL OBJECT LISTS
# ============================================================

bullets = []
enemies = []
enemy_projectiles = []
items = []

upgrade_choices = []
upgrade_selection_rects = []


# ============================================================
# AI MESSAGE
# ============================================================

class AIMessage:

    def __init__(
        self,
        message_type,
        position,
        sender,
        timestamp,
        confidence=1.0
    ):

        self.message_type = message_type
        self.position = pg.Vector2(position)
        self.sender = sender
        self.timestamp = timestamp
        self.confidence = confidence


# ============================================================
# PLAYER DAMAGE
# ============================================================

def damage_player(amount):

    global player_health
    global player_damage_timer
    global game_state

    if game_state == GAME_STATE_GAME_OVER:
        return

    if player_damage_timer > 0:
        return

    damage = (
        amount
        * PLAYER_DAMAGE_MULTIPLIER
        * (1 - player_stats["damage_reduction"])
    )

    player_health -= damage

    player_damage_timer = PLAYER_DAMAGE_COOLDOWN

    if player_health <= 0:

        player_health = 0

        game_state = GAME_STATE_GAME_OVER


# ============================================================
# GENERATE UPGRADE CHOICES
# ============================================================

def generate_upgrade_choices():

    global upgrade_choices
    global upgrade_selection_rects

    available_upgrades = list(
        PLAYER_UPGRADES.keys()
    )

    upgrade_choices = random.sample(
        available_upgrades,
        min(3, len(available_upgrades))
    )

    upgrade_selection_rects = []


# ============================================================
# APPLY UPGRADE
# ============================================================

def apply_upgrade(upgrade_id):

    global player_health

    if upgrade_id == "vitality":

        player_stats["max_health"] += 20

        player_health = min(
            player_health + 20,
            player_stats["max_health"]
        )

    elif upgrade_id == "speed":

        player_stats["move_speed"] += 30

    elif upgrade_id == "damage":

        player_stats["damage_multiplier"] += 0.15

    elif upgrade_id == "fire_rate":

        player_stats["fire_rate_multiplier"] += 0.10

    elif upgrade_id == "armor":

        player_stats["damage_reduction"] = min(
            0.75,
            player_stats["damage_reduction"] + 0.10
        )

    elif upgrade_id == "vision":

        player_stats["vision_range"] += 40

    elif upgrade_id == "projectile_speed":

        player_stats["projectile_speed_multiplier"] += 0.15

    print(
        f"Upgrade selected: "
        f"{PLAYER_UPGRADES[upgrade_id]['name']}"
    )


# ============================================================
# CHOOSE UPGRADE
# ============================================================

def choose_upgrade(index):

    global game_state
    global wave_number
    global upgrade_choices
    global upgrade_selection_rects

    if not (
        0 <= index < len(upgrade_choices)
    ):
        return

    selected_upgrade = upgrade_choices[index]

    apply_upgrade(
        selected_upgrade
    )

    upgrade_choices = []
    upgrade_selection_rects = []

    enemy_projectiles.clear()
    bullets.clear()

    if wave_number < len(WAVE_SPAWN_WEIGHTS):
        wave_number += 1
    else:
        wave_number = 1

    game_state = GAME_STATE_PREP

# ============================================================
# WALL GENERATION
# ============================================================

def generate_walls(amount=10):
    
    walls = []
    
    MIN_WALL_WIDTH = 80 
    MAX_WALL_WIDTH = 180
    
    MIN_WALL_HEIGHT = 50
    MAX_WALL_HEIGHT = 120
    
    MIN_WALL_GAP = 45
    
    for _ in range(amount):
        
        placed = False
        
        for _ in range(200):
            
            width = random.randint(
                MIN_WALL_WIDTH,
                MAX_WALL_WIDTH
            )
            
            height = random.randint(
                MIN_WALL_HEIGHT,
                MAX_WALL_HEIGHT
            )
            
            x = random.randint(
                PLAY_AREA.left + 30,
                PLAY_AREA.right - width - 30
            )
            
            y = random.randint(
                PLAY_AREA.top + 30,
                PLAY_AREA.bottom - height - 30
            )
            
            wall = pg.Rect(
                x, 
                y, 
                width, 
                height
            )
            
            # --------------------------------------------
            # Keep safe zone clear
            # --------------------------------------------
            
            if wall.colliderect(
                SAFE_ZONE
            ):
                continue
            
            # --------------------------------------------
            # Keep player clear
            # --------------------------------------------
            
            if wall.colliderect(
                player
            ):
                continue
            
            # --------------------------------------------
            # Keep a minimum gap between walls
            # --------------------------------------------
            
            padded_wall = wall.inflate(
                MIN_WALL_GAP * 2,
                MIN_WALL_GAP * 2
            )
            
            if any(
                padded_wall.colliderect(
                    existing_wall
                )
                for existing_wall in walls
            ):
                continue
            
            walls.append(
                wall
            )
            
            placed = True
            break
        
        if not placed:
            break
        
        return walls

# ============================================================
# COLLISION MOVEMENT
# ============================================================

def move_horizontal(
    entity,
    dx,
    walls
):

    entity.x += round(dx)

    for wall in walls:

        if entity.colliderect(wall):

            if dx > 0:
                entity.right = wall.left

            elif dx < 0:
                entity.left = wall.right


def move_vertical(
    entity,
    dy,
    walls
):

    entity.y += round(dy)

    for wall in walls:

        if entity.colliderect(wall):

            if dy > 0:
                entity.bottom = wall.top

            elif dy < 0:
                entity.top = wall.bottom


def keep_inside_play_area(
    entity,
    play_area
):

    if entity.left < play_area.left:
        entity.left = play_area.left

    if entity.right > play_area.right:
        entity.right = play_area.right

    if entity.top < play_area.top:
        entity.top = play_area.top

    if entity.bottom > play_area.bottom:
        entity.bottom = play_area.bottom


# ============================================================
# NAVIGATION
# ============================================================

GRID_SIZE = 40


def world_to_grid(position):

    return (
        int(
            (
                position[0]
                - PLAY_AREA.left
            ) // GRID_SIZE
        ),
        int(
            (
                position[1]
                - PLAY_AREA.top
            ) // GRID_SIZE
        )
    )


def grid_to_world(grid_position):

    x, y = grid_position

    return pg.Vector2(
        PLAY_AREA.left
        + x * GRID_SIZE
        + GRID_SIZE / 2,

        PLAY_AREA.top
        + y * GRID_SIZE
        + GRID_SIZE / 2
    )


def create_navigation_grid(
    walls,
    enemy_size
):

    grid_width = math.ceil(
        PLAY_AREA.width
        / GRID_SIZE
    )

    grid_height = math.ceil(
        PLAY_AREA.height
        / GRID_SIZE
    )

    grid = []

    clearance = enemy_size / 2

    for y in range(grid_height):

        row = []

        for x in range(grid_width):

            cell_center = grid_to_world(
                (x, y)
            )

            blocked = False

            for wall in walls:

                expanded_wall = wall.inflate(
                    clearance * 2,
                    clearance * 2
                )

                if expanded_wall.collidepoint(
                    round(cell_center.x),
                    round(cell_center.y)
                ):

                    blocked = True
                    break

            row.append(
                not blocked
            )

        grid.append(row)

    return grid


def get_neighbors(
    node,
    grid
):

    x, y = node

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]

    neighbors = []

    if not grid:
        return neighbors

    grid_height = len(grid)
    grid_width = len(grid[0])

    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        if not (
            0 <= nx < grid_width
            and
            0 <= ny < grid_height
        ):
            continue

        if not grid[ny][nx]:
            continue

        if dx != 0 and dy != 0:

            if not grid[y][nx]:
                continue

            if not grid[ny][x]:
                continue

        neighbors.append(
            (nx, ny)
        )

    return neighbors


def heuristic(a, b):

    return max(
        abs(a[0] - b[0]),
        abs(a[1] - b[1])
    )


def a_star(
    start,
    goal,
    grid
):

    if not grid:
        return []

    grid_height = len(grid)
    grid_width = len(grid[0])

    if not (
        0 <= start[0] < grid_width
        and
        0 <= start[1] < grid_height
    ):
        return []

    if not (
        0 <= goal[0] < grid_width
        and
        0 <= goal[1] < grid_height
    ):
        return []

    if not grid[start[1]][start[0]]:
        return []

    if not grid[goal[1]][goal[0]]:
        return []

    open_set = {start}

    came_from = {}

    g_score = {
        start: 0
    }

    f_score = {
        start: heuristic(
            start,
            goal
        )
    }

    while open_set:

        current = min(
            open_set,
            key=lambda node:
                f_score.get(
                    node,
                    float("inf")
                )
        )

        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.append(start)

            path.reverse()

            return path

        open_set.remove(current)

        for neighbor in get_neighbors(
            current,
            grid
        ):

            dx = abs(
                neighbor[0] - current[0]
            )

            dy = abs(
                neighbor[1] - current[1]
            )

            movement_cost = (
                math.sqrt(2)
                if dx == 1 and dy == 1
                else 1
            )

            tentative_g_score = (
                g_score[current]
                + movement_cost
            )

            if tentative_g_score < g_score.get(
                neighbor,
                float("inf")
            ):

                came_from[neighbor] = current

                g_score[neighbor] = (
                    tentative_g_score
                )

                f_score[neighbor] = (
                    tentative_g_score
                    + heuristic(
                        neighbor,
                        goal
                    )
                )

                open_set.add(
                    neighbor
                )

    return []


# ============================================================
# VISION
# ============================================================

def is_player_in_fov(
    enemy,
    player_pos
):

    enemy_center = pg.Vector2(
        enemy.rect.center
    )

    direction_to_player = (
        player_pos
        - enemy_center
    )

    distance = (
        direction_to_player.length()
    )

    if distance > enemy.vision_range:
        return False

    if distance == 0:
        return True

    direction_to_player.normalize_ip()

    facing = pg.Vector2(
        enemy.facing_direction
    )

    if facing.length_squared() == 0:
        return False

    facing.normalize_ip()

    dot = max(
        -1,
        min(
            1,
            facing.dot(
                direction_to_player
            )
        )
    )

    angle = math.degrees(
        math.acos(dot)
    )

    return angle <= (
        enemy.vision_angle / 2
    )


def has_line_of_sight(
    enemy,
    player_pos,
    walls
):

    start = pg.Vector2(
        enemy.rect.center
    )

    end = pg.Vector2(
        player_pos
    )

    distance = start.distance_to(end)

    if distance == 0:
        return True

    direction = (
        end - start
    ).normalize()

    step_size = 5

    steps = int(
        distance / step_size
    )

    for i in range(steps + 1):

        point = (
            start
            + direction
            * i
            * step_size
        )

        for wall in walls:

            if wall.collidepoint(
                round(point.x),
                round(point.y)
            ):

                return False

    return True


# ============================================================
# PLAYER BULLET
# ============================================================

class Bullet:

    def __init__(
        self,
        position,
        direction
    ):

        self.position = pg.Vector2(
            position
        )

        self.direction = pg.Vector2(
            direction
        )

        if self.direction.length_squared() > 0:

            self.direction.normalize_ip()
        
        weapon = get_current_weapon()

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

            if not PLAY_AREA.collidepoint(
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


# ============================================================
# ENEMY PROJECTILE
# ============================================================

class EnemyProjectile:

    def __init__(
        self,
        position,
        direction,
        damage,
        speed,
        max_range,
        radius,
        color
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

            if not PLAY_AREA.collidepoint(
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

                damage_player(
                    self.damage
                )

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


# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(
        self,
        enemy_type,
        x,
        y,
        player_position=None
    ):

        self.type = enemy_type

        self.weapon = ENEMY_WEAPONS[
            self.type
        ]

        self.weapon_fire_timer = 0.0

        self.facing_direction = pg.Vector2(
            1,
            0
        )

        data = ENEMY_TYPES[
            enemy_type
        ]

        self.rect = pg.Rect(
            x,
            y,
            data["size"],
            data["size"]
        )

        self.health = data["health"]
        self.max_health = data["health"]

        self.speed = data["speed"]
        self.damage = data["damage"]

        self.color = data["color"]
        self.shape = data["shape"]

        # ----------------------------------------------------
        # Vision
        # ----------------------------------------------------

        self.vision_range = 300
        self.vision_angle = 90

        self.can_see_player = False

        # ----------------------------------------------------
        # Normal player memory
        # ----------------------------------------------------

        self.last_seen_position = None
        self.last_seen_time = 0

        # ----------------------------------------------------
        # Attacker memory
        # ----------------------------------------------------

        self.last_attacker_position = None
        self.attacker_confidence = 0.0
        self.attacker_direction = None
        self.attacker_memory_timer = 0.0

        # ----------------------------------------------------
        # Communication memory
        # ----------------------------------------------------

        self.last_known_player_position = None
        self.last_known_player_time = 0
        self.last_known_player_confidence = 0.0

        self.last_message_sender = None

        self.communication_cooldown = random.uniform(
            0,
            COMMUNICATION_COOLDOWN
        )

        self.communication_flash_timer = 0.0
        self.communication_flash_position = None

        # ----------------------------------------------------
        # AI state
        # ----------------------------------------------------

        self.ai_state = AI_IDLE

        self.search_timer = 0.0
        self.search_target = None

        # ----------------------------------------------------
        # Path
        # ----------------------------------------------------

        self.path = []
        self.path_index = 0

        self.path_update_timer = 0
        self.path_update_interval = 0.25

        if player_position is not None:

            direction = (
                pg.Vector2(player_position)
                - pg.Vector2(self.rect.center)
            )

            if direction.length_squared() > 0:

                self.facing_direction = (
                    direction.normalize()
                )

    # ========================================================
    # WEAPON TIMER
    # ========================================================

    def update_weapon_timer(self, dt):

        if self.weapon_fire_timer > 0:

            self.weapon_fire_timer -= dt

            self.weapon_fire_timer = max(
                0,
                self.weapon_fire_timer
            )

    # ========================================================
    # COMMUNICATION TIMER
    # ========================================================

    def update_communication_timer(self, dt):

        if self.communication_cooldown > 0:

            self.communication_cooldown -= dt

            self.communication_cooldown = max(
                0,
                self.communication_cooldown
            )

        if self.communication_flash_timer > 0:

            self.communication_flash_timer -= dt

            self.communication_flash_timer = max(
                0,
                self.communication_flash_timer
            )

    # ========================================================
    # SEND COMMUNICATION
    # ========================================================

    def send_message(
        self,
        message_type,
        enemies,
        position=None,
        confidence=None
    ):

        if self.communication_cooldown > 0:
            return

        if position is None:

            if self.last_known_player_position is None:
                return

            position = self.last_known_player_position

        if confidence is None:
            confidence = self.last_known_player_confidence

        now = pg.time.get_ticks() / 1000.0

        message = AIMessage(
            message_type,
            position,
            self,
            now,
            confidence
        )

        sender_position = pg.Vector2(
            self.rect.center
        )

        for other_enemy in enemies:

            if other_enemy is self:
                continue

            other_position = pg.Vector2(
                other_enemy.rect.center
            )

            distance = sender_position.distance_to(
                other_position
            )

            if distance > COMMUNICATION_RANGE:
                continue

            other_enemy.receive_message(
                message
            )

        self.communication_cooldown = (
            COMMUNICATION_COOLDOWN
        )

        self.communication_flash_timer = (
            COMMUNICATION_DISPLAY_TIME
        )

        self.communication_flash_position = (
            pg.Vector2(position)
        )

    # ========================================================
    # RECEIVE COMMUNICATION
    # ========================================================

    def receive_message(self, message):

        if message.sender is self:
            return

        now = pg.time.get_ticks() / 1000.0

        message_age = (
            now - message.timestamp
        )

        if message_age > COMMUNICATION_MEMORY_TIME:
            return

        # ----------------------------------------------------
        # PLAYER LOCATION MESSAGE
        # ----------------------------------------------------

        if message.message_type in (
            MESSAGE_PLAYER_SPOTTED,
            MESSAGE_PLAYER_LOST,
            MESSAGE_UNDER_ATTACK
        ):

            if self.last_known_player_position is not None:

                existing_age = (
                    now
                    - self.last_known_player_time
                )

                existing_quality = (
                    self.last_known_player_confidence
                    * max(
                        0,
                        1
                        - (
                            existing_age
                            / COMMUNICATION_MEMORY_TIME
                        )
                    )
                )

                new_quality = (
                    message.confidence
                    * max(
                        0,
                        1
                        - (
                            message_age
                            / COMMUNICATION_MEMORY_TIME
                        )
                    )
                )

                if new_quality < existing_quality:
                    return

            self.last_known_player_position = pg.Vector2(
                message.position
            )

            self.last_known_player_time = (
                message.timestamp
            )

            self.last_known_player_confidence = (
                message.confidence
            )

            self.last_message_sender = (
                message.sender
            )

            self.communication_flash_timer = (
                COMMUNICATION_DISPLAY_TIME
            )

            self.communication_flash_position = (
                pg.Vector2(
                    message.position
                )
            )

            if not self.can_see_player:

                self.last_seen_position = pg.Vector2(
                    message.position
                )

                self.ai_state = AI_SEARCH

                self.search_timer = SEARCH_TIME

                self.search_target = None

                self.path = []
                self.path_index = 0
                self.path_update_timer = 0

            return

        # ----------------------------------------------------
        # ATTACK LOCATION MESSAGE
        # ----------------------------------------------------

        if message.message_type == MESSAGE_ATTACK_LOCATION:

            # Do not replace direct visual information.
            if self.can_see_player:
                return

            self.last_attacker_position = (
                pg.Vector2(
                    message.position
                )
            )

            self.attacker_confidence = (
                message.confidence * 0.85
            )

            self.attacker_memory_timer = (
                ATTACKER_MEMORY_TIME
            )

            self.last_message_sender = (
                message.sender
            )

            self.communication_flash_timer = (
                COMMUNICATION_DISPLAY_TIME
            )

            self.communication_flash_position = (
                pg.Vector2(
                    message.position
                )
            )

            # Use attacker location as search center.
            self.last_seen_position = (
                pg.Vector2(
                    message.position
                )
            )

            self.ai_state = AI_SEARCH

            self.search_timer = SEARCH_TIME

            self.search_target = None

            self.path = []
            self.path_index = 0
            self.path_update_timer = 0

    # ========================================================
    # BROADCAST PLAYER SPOTTED
    # ========================================================

    def broadcast_player_spotted(self, enemies):

        if self.last_seen_position is None:
            return

        self.last_known_player_position = pg.Vector2(
            self.last_seen_position
        )

        self.last_known_player_time = (
            pg.time.get_ticks() / 1000.0
        )

        self.last_known_player_confidence = 1.0

        self.send_message(
            MESSAGE_PLAYER_SPOTTED,
            enemies,
            self.last_seen_position,
            1.0
        )

    # ========================================================
    # REGISTER ATTACK
    # ========================================================

    def register_attack(
        self,
        bullet,
        enemies
    ):
        """
        The enemy was hit by a player bullet.

        The bullet direction tells the enemy the direction
        the attacker was located in.

        The enemy does NOT know the exact player position.
        It only gets an estimated location.
        """

        direction = pg.Vector2(
            bullet.direction
        )

        if direction.length_squared() == 0:
            return

        direction.normalize_ip()

        enemy_position = pg.Vector2(
            self.rect.center
        )

        # The player is somewhere behind the bullet.
        estimated_position = (
            enemy_position
            - direction
            * ATTACKER_ESTIMATE_DISTANCE
        )

        # Keep estimate inside play area.
        estimated_position.x = max(
            PLAY_AREA.left,
            min(
                estimated_position.x,
                PLAY_AREA.right
            )
        )

        estimated_position.y = max(
            PLAY_AREA.top,
            min(
                estimated_position.y,
                PLAY_AREA.bottom
            )
        )

        self.last_attacker_position = (
            estimated_position.copy()
        )

        self.attacker_direction = (
            direction.copy()
        )

        # Bullet direction gives medium confidence.
        self.attacker_confidence = 0.7

        self.attacker_memory_timer = (
            ATTACKER_MEMORY_TIME
        )

        # Search around estimated position.
        self.last_seen_position = (
            estimated_position.copy()
        )

        self.ai_state = AI_SEARCH

        self.search_timer = SEARCH_TIME

        self.search_target = None

        self.path = []
        self.path_index = 0
        self.path_update_timer = 0

        # Communicate estimated attacker location.
        self.broadcast_attack_location(
            enemies
        )

    # ========================================================
    # BROADCAST ATTACK LOCATION
    # ========================================================

    def broadcast_attack_location(
        self,
        enemies
    ):

        if self.last_attacker_position is None:
            return

        if self.attacker_confidence <= 0:
            return

        self.send_message(
            MESSAGE_ATTACK_LOCATION,
            enemies,
            self.last_attacker_position,
            self.attacker_confidence
        )

    # ========================================================
    # UPDATE VISION
    # ========================================================

    def update_vision(
        self,
        player_pos,
        walls,
        enemies
    ):

        previously_visible = (
            self.can_see_player
        )

        in_fov = is_player_in_fov(
            self,
            player_pos
        )

        visible = (
            in_fov
            and
            has_line_of_sight(
                self,
                player_pos,
                walls
            )
        )

        # ----------------------------------------------------
        # PLAYER VISIBLE
        # ----------------------------------------------------

        if visible:

            self.can_see_player = True

            self.last_seen_position = (
                pg.Vector2(
                    player_pos
                )
            )

            now = pg.time.get_ticks() / 1000.0

            self.last_seen_time = now

            self.last_known_player_position = (
                pg.Vector2(
                    player_pos
                )
            )

            self.last_known_player_time = now

            self.last_known_player_confidence = 1.0

            # Visual confirmation overrides estimate.
            self.last_attacker_position = (
                pg.Vector2(
                    player_pos
                )
            )

            self.attacker_confidence = 1.0

            self.attacker_memory_timer = (
                ATTACKER_MEMORY_TIME
            )

            self.ai_state = AI_CHASE

            self.search_timer = 0
            self.search_target = None

            if (
                not previously_visible
                or
                self.communication_cooldown <= 0
            ):

                self.broadcast_player_spotted(
                    enemies
                )

        # ----------------------------------------------------
        # PLAYER NOT VISIBLE
        # ----------------------------------------------------

        else:

            self.can_see_player = False

            if (
                previously_visible
                and
                self.last_seen_position is not None
            ):

                self.ai_state = AI_SEARCH

                self.search_timer = SEARCH_TIME

                self.search_target = None

                self.path = []
                self.path_index = 0

                self.last_known_player_position = (
                    pg.Vector2(
                        self.last_seen_position
                    )
                )

                self.last_known_player_time = (
                    pg.time.get_ticks()
                    / 1000.0
                )

                self.last_known_player_confidence = 0.8

                self.send_message(
                    MESSAGE_PLAYER_LOST,
                    enemies,
                    self.last_seen_position,
                    0.8
                )

    # ========================================================
    # UPDATE ATTACKER MEMORY
    # ========================================================

    def update_attacker_memory(self, dt):

        if self.attacker_memory_timer <= 0:
            return

        self.attacker_memory_timer -= dt

        self.attacker_memory_timer = max(
            0,
            self.attacker_memory_timer
        )

        # Memory becomes less reliable over time.
        if ATTACKER_MEMORY_TIME > 0:

            self.attacker_confidence *= max(
                0,
                1
                - (
                    dt
                    / ATTACKER_MEMORY_TIME
                )
            )

        if self.attacker_memory_timer <= 0:

            self.last_attacker_position = None

            self.attacker_direction = None

            self.attacker_confidence = 0.0

    # ========================================================
    # GENERATE SEARCH POINT
    # ========================================================

    def generate_search_point(
        self,
        walls
    ):

        # Prefer attacker position if available.
        if self.last_attacker_position is not None:

            center = pg.Vector2(
                self.last_attacker_position
            )

            search_radius = (
                ATTACKER_SEARCH_RADIUS
            )

        elif self.last_seen_position is not None:

            center = pg.Vector2(
                self.last_seen_position
            )

            search_radius = SEARCH_RADIUS

        else:

            return None

        for _ in range(50):

            angle = random.uniform(
                0,
                math.tau
            )

            radius = random.uniform(
                50,
                search_radius
            )

            point = (
                center
                + pg.Vector2(
                    math.cos(angle),
                    math.sin(angle)
                )
                * radius
            )

            test_rect = pg.Rect(
                0,
                0,
                self.rect.width,
                self.rect.height
            )

            test_rect.center = (
                round(point.x),
                round(point.y)
            )

            if not PLAY_AREA.contains(
                test_rect
            ):
                continue

            if any(
                test_rect.colliderect(wall)
                for wall in walls
            ):
                continue

            return point

        return None

    # ========================================================
    # CALCULATE PATH
    # ========================================================

    def calculate_path(
        self,
        target_position,
        navigation_grid
    ):

        start = world_to_grid(
            self.rect.center
        )

        goal = world_to_grid(
            target_position
        )

        if not navigation_grid:

            self.path = []
            self.path_index = 0

            return

        grid_height = len(
            navigation_grid
        )

        grid_width = len(
            navigation_grid[0]
        )

        if not (
            0 <= start[0] < grid_width
            and
            0 <= start[1] < grid_height
        ):

            self.path = []
            self.path_index = 0

            return

        if not (
            0 <= goal[0] < grid_width
            and
            0 <= goal[1] < grid_height
        ):

            self.path = []
            self.path_index = 0

            return

        if not navigation_grid[
            start[1]
        ][
            start[0]
        ]:

            self.path = []
            self.path_index = 0

            return

        if not navigation_grid[
            goal[1]
        ][
            goal[0]
        ]:

            possible_goals = []

            for radius in range(1, 4):

                for dx in range(
                    -radius,
                    radius + 1
                ):

                    for dy in range(
                        -radius,
                        radius + 1
                    ):

                        gx = goal[0] + dx
                        gy = goal[1] + dy

                        if not (
                            0 <= gx < grid_width
                            and
                            0 <= gy < grid_height
                        ):
                            continue

                        if navigation_grid[gy][gx]:

                            possible_goals.append(
                                (gx, gy)
                            )

                if possible_goals:
                    break

            if possible_goals:

                goal = random.choice(
                    possible_goals
                )

            else:

                self.path = []
                self.path_index = 0

                return

        self.path = a_star(
            start,
            goal,
            navigation_grid
        )

        self.path_index = (
            1
            if len(self.path) > 1
            else 0
        )

    # ========================================================
    # FOLLOW PATH
    # ========================================================

    def follow_path(
        self,
        target_position,
        navigation_grids,
        walls,
        dt
    ):

        self.path_update_timer -= dt

        navigation_grid = (
            navigation_grids.get(
                self.type
            )
        )

        if navigation_grid is None:
            return

        if (
            self.path_update_timer <= 0
            or
            not self.path
            or
            self.path_index >= len(
                self.path
            )
        ):

            self.calculate_path(
                target_position,
                navigation_grid
            )

            self.path_update_timer = (
                self.path_update_interval
            )

        if not self.path:
            return

        if self.path_index >= len(
            self.path
        ):
            return

        enemy_pos = pg.Vector2(
            self.rect.center
        )

        target = grid_to_world(
            self.path[
                self.path_index
            ]
        )

        direction = target - enemy_pos

        if direction.length_squared() == 0:

            self.path_index += 1

            return

        direction.normalize_ip()

        self.facing_direction = (
            direction.copy()
        )

        movement = (
            direction
            * self.speed
            * dt
        )

        move_horizontal(
            self.rect,
            movement.x,
            walls
        )

        move_vertical(
            self.rect,
            movement.y,
            walls
        )

        enemy_pos = pg.Vector2(
            self.rect.center
        )

        if (
            enemy_pos.distance_to(target)
            < SEARCH_POINT_REACHED_DISTANCE
        ):

            self.path_index += 1

    # ========================================================
    # ENEMY SHOOTING
    # ========================================================

    def try_fire(
        self,
        player_pos
    ):

        weapon = self.weapon

        if weapon["type"] != "ranged":
            return

        if self.weapon_fire_timer > 0:
            return

        direction = (
            pg.Vector2(player_pos)
            - pg.Vector2(
                self.rect.center
            )
        )

        if direction.length_squared() == 0:
            return

        direction.normalize_ip()

        self.facing_direction = (
            direction.copy()
        )

        origin = (
            pg.Vector2(
                self.rect.center
            )
            + direction
            * (
                self.rect.width / 2
                + 6
            )
        )

        projectile_count = weapon.get(
            "projectile_count",
            1
        )

        spread = weapon.get(
            "spread",
            0
        )

        if projectile_count == 1:

            angles = [0]

        else:

            angles = [
                -spread / 2
                + i
                * (
                    spread
                    / (
                        projectile_count - 1
                    )
                )
                for i in range(
                    projectile_count
                )
            ]

        for angle in angles:

            shot_direction = (
                direction.rotate(angle)
            )

            enemy_projectiles.append(
                EnemyProjectile(
                    origin,
                    shot_direction,
                    weapon["damage"],
                    weapon["projectile_speed"],
                    weapon["projectile_range"],
                    weapon["projectile_radius"],
                    weapon["projectile_color"]
                )
            )

        self.weapon_fire_timer = (
            weapon["fire_rate"]
        )

    # ========================================================
    # MELEE ATTACK
    # ========================================================

    def melee_attack(
        self,
        player_pos
    ):

        weapon = self.weapon

        if weapon["type"] != "melee":
            return False

        if self.weapon_fire_timer > 0:
            return False

        distance = (
            pg.Vector2(
                self.rect.center
            ).distance_to(
                pg.Vector2(player_pos)
            )
        )

        if (
            distance <= weapon["range"]
            and
            self.can_see_player
        ):

            damage_player(
                weapon["damage"]
            )

            self.weapon_fire_timer = (
                weapon["fire_rate"]
            )

            return True

        return False

    # ========================================================
    # SEARCH
    # ========================================================

    def search_for_player(
        self,
        navigation_grids,
        walls,
        dt
    ):

        if (
            self.last_seen_position is None
            and
            self.last_attacker_position is None
        ):

            self.ai_state = AI_IDLE

            return

        self.search_timer -= dt

        if self.search_timer <= 0:

            self.ai_state = AI_IDLE

            self.search_target = None
            self.path = []
            self.path_index = 0

            return

        if self.search_target is None:

            self.search_target = (
                self.generate_search_point(
                    walls
                )
            )

            self.path = []
            self.path_index = 0
            self.path_update_timer = 0

        if self.search_target is None:
            return

        self.follow_path(
            self.search_target,
            navigation_grids,
            walls,
            dt
        )

        enemy_pos = pg.Vector2(
            self.rect.center
        )

        if (
            enemy_pos.distance_to(
                self.search_target
            )
            < SEARCH_POINT_REACHED_DISTANCE
        ):

            self.search_target = None
            self.path = []
            self.path_index = 0

    # ========================================================
    # AI UPDATE
    # ========================================================

    def update_ai(
        self,
        player_pos,
        navigation_grids,
        walls,
        dt
    ):

        self.update_weapon_timer(dt)

        self.update_attacker_memory(dt)

        # ----------------------------------------------------
        # CHASE / COMBAT
        # ----------------------------------------------------

        if self.ai_state == AI_CHASE:

            weapon = self.weapon

            distance = (
                pg.Vector2(
                    self.rect.center
                ).distance_to(
                    pg.Vector2(player_pos)
                )
            )

            # ------------------------------------------------
            # RANGED
            # ------------------------------------------------

            if weapon["type"] == "ranged":

                if (
                    self.can_see_player
                    and
                    distance <= weapon["range"]
                ):

                    direction = (
                        pg.Vector2(player_pos)
                        - pg.Vector2(
                            self.rect.center
                        )
                    )

                    if direction.length_squared() > 0:

                        direction.normalize_ip()

                        self.facing_direction = (
                            direction.copy()
                        )

                    self.try_fire(
                        player_pos
                    )

                else:

                    self.follow_path(
                        player_pos,
                        navigation_grids,
                        walls,
                        dt
                    )

            # ------------------------------------------------
            # MELEE
            # ------------------------------------------------

            else:

                if (
                    self.can_see_player
                    and
                    distance <= weapon["range"]
                ):

                    attacked = self.melee_attack(
                        player_pos
                    )

                    if attacked:
                        return

                self.follow_path(
                    player_pos,
                    navigation_grids,
                    walls,
                    dt
                )

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        elif self.ai_state == AI_SEARCH:

            self.search_for_player(
                navigation_grids,
                walls,
                dt
            )

        # ----------------------------------------------------
        # IDLE
        # ----------------------------------------------------

        elif self.ai_state == AI_IDLE:

            if random.random() < 0.01:

                angle = random.uniform(
                    0,
                    math.tau
                )

                self.facing_direction = pg.Vector2(
                    math.cos(angle),
                    math.sin(angle)
                )

    # ========================================================
    # DRAW
    # ========================================================

    def draw(
        self,
        screen
    ):

        center = self.rect.center
        size = self.rect.width
        half = size / 2

        # ----------------------------------------------------
        # Body
        # ----------------------------------------------------

        if self.shape == "square":

            pg.draw.rect(
                screen,
                self.color,
                self.rect
            )

        elif self.shape == "circle":

            pg.draw.circle(
                screen,
                self.color,
                center,
                size // 2
            )

        elif self.shape == "triangle":

            points = [
                (
                    center[0],
                    center[1] - half
                ),
                (
                    center[0] - half,
                    center[1] + half
                ),
                (
                    center[0] + half,
                    center[1] + half
                )
            ]

            pg.draw.polygon(
                screen,
                self.color,
                points
            )

        elif self.shape == "diamond":

            points = [
                (
                    center[0],
                    center[1] - half
                ),
                (
                    center[0] + half,
                    center[1]
                ),
                (
                    center[0],
                    center[1] + half
                ),
                (
                    center[0] - half,
                    center[1]
                )
            ]

            pg.draw.polygon(
                screen,
                self.color,
                points
            )

        elif self.shape == "hexagon":

            points = []

            radius = half

            for i in range(6):

                angle = (
                    math.radians(
                        60 * i
                    )
                    - math.pi / 2
                )

                points.append(
                    (
                        center[0]
                        + math.cos(angle)
                        * radius,

                        center[1]
                        + math.sin(angle)
                        * radius
                    )
                )

            pg.draw.polygon(
                screen,
                self.color,
                points
            )

        elif self.shape == "octagon":

            points = []

            radius = half

            for i in range(8):

                angle = (
                    math.radians(
                        45 * i
                    )
                    - math.pi / 2
                )

                points.append(
                    (
                        center[0]
                        + math.cos(angle)
                        * radius,

                        center[1]
                        + math.sin(angle)
                        * radius
                    )
                )

            pg.draw.polygon(
                screen,
                self.color,
                points
            )

        elif self.shape == "witch":

            # Purple circular body.
            pg.draw.circle(
                screen,
                self.color,
                center,
                size // 2
            )

            # Dark witch hat.
            hat_points = [
                (center[0], center[1] - half - 8),
                (center[0] - half, center[1] - 2),
                (center[0] + half, center[1] - 2)
            ]
            pg.draw.polygon(
                screen,
                (35, 20, 45),
                hat_points
            )

            # Glowing-looking eyes.
            eye_y = center[1] - 2
            pg.draw.circle(screen, (255, 120, 220), (center[0] - 6, eye_y), 3)
            pg.draw.circle(screen, (255, 120, 220), (center[0] + 6, eye_y), 3)

        # ----------------------------------------------------
        # Health bar
        # ----------------------------------------------------

        bar_width = size
        bar_height = 5

        bar_x = self.rect.left
        bar_y = self.rect.top - 9

        health_ratio = (
            self.health
            / self.max_health
        )

        health_ratio = max(
            0,
            min(
                1,
                health_ratio
            )
        )

        pg.draw.rect(
            screen,
            (50, 50, 50),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            )
        )

        if health_ratio > 0:

            pg.draw.rect(
                screen,
                (60, 220, 80),
                (
                    bar_x,
                    bar_y,
                    int(
                        bar_width
                        * health_ratio
                    ),
                    bar_height
                )
            )

        # ----------------------------------------------------
        # Facing direction
        # ----------------------------------------------------

        direction = pg.Vector2(
            self.facing_direction
        )

        if direction.length_squared() > 0:

            direction.normalize_ip()

            end = (
                pg.Vector2(center)
                + direction
                * (size * 0.7)
            )

            pg.draw.line(
                screen,
                (255, 255, 255),
                center,
                (
                    round(end.x),
                    round(end.y)
                ),
                3
            )

        # ----------------------------------------------------
        # Vision indicator
        # ----------------------------------------------------

        if self.can_see_player:

            pg.draw.circle(
                screen,
                (255, 255, 255),
                center,
                5
            )

        # ----------------------------------------------------
        # Search indicator
        # ----------------------------------------------------

        elif self.ai_state == AI_SEARCH:

            pg.draw.circle(
                screen,
                (255, 200, 50),
                center,
                5
            )

        # ----------------------------------------------------
        # Attacker direction indicator
        # ----------------------------------------------------

        if (
            self.ai_state == AI_SEARCH
            and
            self.last_attacker_position is not None
        ):

            attacker_position = (
                self.last_attacker_position
            )

            pg.draw.line(
                screen,
                (255, 120, 60),
                center,
                (
                    round(attacker_position.x),
                    round(attacker_position.y)
                ),
                2
            )

            pg.draw.circle(
                screen,
                (255, 120, 60),
                (
                    round(attacker_position.x),
                    round(attacker_position.y)
                ),
                7,
                2
            )

        # ----------------------------------------------------
        # Communication indicator
        # ----------------------------------------------------

        if self.communication_flash_timer > 0:

            pg.draw.circle(
                screen,
                (80, 220, 255),
                center,
                size // 2 + 8,
                2
            )

# ============================================================
# MAP CONNECTIVITY
# ============================================================

def is_grid_connected(grid, start):
    
    if not grid:
        return False
    
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    start_x, start_y = start
    
    if not (
        0 <= start_x < grid_width
        and
        0 <= start_y < grid_height
    ):
        
        return False
    
    if not grid[start_y][start_x]:
        return False
    
    visited = set()
    stack = [start]
    
    while stack:
        
        current = stack.pop()
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor in get_neighbors(
            current,
            grid
        ):
            
            if neighbor not in visited:
                stack.append(neighbor)
    
    # Count every walkable cell
    walkable_cell = 0
    
    for row in grid:
        for cell in row:
            if cell:
                walkable_cell += 1
    
    return len(visited) == walkable_cell

# ============================================================
# SPAWN ENEMY
# ============================================================

def spawn_enemy(
    enemy_type,
    player_rect,
    walls
):

    data = ENEMY_TYPES[
        enemy_type
    ]

    size = data["size"]

    for _ in range(200):

        x = random.randint(
            PLAY_AREA.left + 20,
            PLAY_AREA.right
            - size
            - 20
        )

        y = random.randint(
            PLAY_AREA.top + 20,
            PLAY_AREA.bottom
            - size
            - 20
        )

        enemy_rect = pg.Rect(
            x,
            y,
            size,
            size
        )

        if enemy_rect.colliderect(
            SAFE_ZONE
        ):
            continue

        if any(
            enemy_rect.colliderect(wall)
            for wall in walls
        ):
            continue

        if enemy_rect.colliderect(
            player_rect
        ):
            continue

        # Prevent enemies from spawning on top of existing enemies.
        # A small padding keeps newly spawned enemies from touching
        # or immediately overlapping each other.
        spawn_padding = 5
        padded_enemy_rect = enemy_rect.inflate(
            spawn_padding * 2,
            spawn_padding * 2
        )

        if any(
            padded_enemy_rect.colliderect(enemy.rect)
            for enemy in enemies
            if enemy.health > 0
        ):
            continue

        # ----------------------------------------------------
        # Reject unreachable / enclosed spawn locations
        # ----------------------------------------------------
        # A spawn can avoid every wall and still be trapped
        # inside a closed group of walls. Use the enemy's
        # size-aware A* grid to verify that it can reach the
        # player's current position before accepting the spawn.
        navigation_grid = navigation_grids.get(
            enemy_type
        )

        if navigation_grid is None:
            continue

        spawn_cell = world_to_grid(
            enemy_rect.center
        )

        player_cell = world_to_grid(
            player_rect.center
        )

        if not a_star(
            spawn_cell,
            player_cell,
            navigation_grid
        ):
            continue

        return Enemy(
            enemy_type,
            x,
            y,
            pg.Vector2(
                player_rect.center
            )
        )

    return None


# ============================================================
# WAVE SYSTEM
# ============================================================

spawn_queue = []
spawn_timer = 0.0


def build_wave_spawn_queue():

    queue = []

    enemy_count = WAVE_ENEMY_COUNTS.get(
        wave_number,
        5
    )

    for _ in range(enemy_count):
        queue.append(choose_enemy_type())

    random.shuffle(queue)

    return queue



def start_wave():

    global spawn_queue
    global spawn_timer
    global game_state

    spawn_queue = build_wave_spawn_queue()

    spawn_timer = 0.0

    game_state = GAME_STATE_ACTIVE


def spawn_next_wave_enemy():

    global spawn_queue

    if not spawn_queue:
        return

    enemy_type = spawn_queue[0]

    enemy = spawn_enemy(
        enemy_type,
        player,
        walls
    )

    if enemy is not None:

        enemies.append(
            enemy
        )

        spawn_queue.pop(0)


# ============================================================
# WORLD + NAVIGATION GRIDS
# ============================================================

def generate_valid_world(
    wall_amount=10,
    max_attempts=100
):
    
    for attempt in range(max_attempts):
        
        candidate_walls = generate_walls(
            wall_amount
        )
        
        candidate_grids = {}
        
        valid = True
        
        # Build a navigation grid for every enemy type
        for enemy_type, data in ENEMY_TYPES.items():
            
            grid = create_navigation_grid(
                candidate_walls,
                data["size"]
            )
            
            candidate_grids[
                enemy_type
            ] = grid
            
            player_grid = world_to_grid(
                player.center
            )
            
            if not is_grid_connected(
                grid,
                player_grid
            ):
                
                valid = False
                break
            
            if valid:
                
                return(
                    candidate_walls,
                    candidate_grids
                )
    # Fallback
    print(
        "WARNING: Could not generate a fully connected map."
    )
    
    fallback_wall = generate_walls(
        wall_amount
    )
    
    fallback_grids = {}
    
    for enemy_type, data in ENEMY_TYPES.items():
        
        fallback_grids[
            enemy_type
        ] = create_navigation_grid(
            fallback_wall,
            data["size"]
        )
    
    return (
        fallback_wall,
        fallback_grids
    )
    
walls, navigation_grids = generate_valid_world(
    10
)

# ============================================================
# MAP DRAWING
# ============================================================

def draw_map(screen):

    screen.fill(
        (25, 25, 30)
    )

    pg.draw.rect(
        screen,
        (35, 35, 42),
        PLAY_AREA
    )

    for wall in walls:

        pg.draw.rect(
            screen,
            (80, 80, 90),
            wall
        )

        pg.draw.rect(
            screen,
            (110, 110, 120),
            wall,
            2
        )


# ============================================================
# TOP BAR
# ============================================================

def draw_top_bar(screen):

    pg.draw.rect(
        screen,
        (25, 25, 30),
        (
            0,
            0,
            SCREEN_WIDTH,
            TOP_BAR_HEIGHT
        )
    )

    pg.draw.line(
        screen,
        (60, 60, 70),
        (
            0,
            TOP_BAR_HEIGHT - 1
        ),
        (
            SCREEN_WIDTH,
            TOP_BAR_HEIGHT - 1
        ),
        2
    )

    title_font = pg.font.SysFont(
        None,
        30
    )

    info_font = pg.font.SysFont(
        None,
        22
    )

    level_text = title_font.render(
        f"LEVEL {level}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        level_text,
        (20, 10)
    )

    wave_text = info_font.render(
        f"WAVE {wave_number} / {len(WAVE_SPAWN_WEIGHTS)}",
        True,
        (200, 200, 200)
    )

    screen.blit(
        wave_text,
        (20, 40)
    )

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    health_x = 220
    health_y = 18
    health_width = 300
    health_height = 30

    health_label = info_font.render(
        "HP",
        True,
        (255, 255, 255)
    )

    screen.blit(
        health_label,
        (
            health_x,
            health_y + 3
        )
    )

    bar_x = health_x + 45
    bar_y = health_y

    pg.draw.rect(
        screen,
        (60, 60, 65),
        (
            bar_x,
            bar_y,
            health_width,
            health_height
        ),
        border_radius=6
    )

    health_ratio = (
        player_health
        / player_stats["max_health"]
    )

    health_ratio = max(
        0,
        min(
            1,
            health_ratio
        )
    )

    current_width = int(
        health_width
        * health_ratio
    )

    if health_ratio > 0.6:

        health_color = (
            50,
            200,
            80
        )

    elif health_ratio > 0.3:

        health_color = (
            240,
            190,
            50
        )

    else:

        health_color = (
            220,
            50,
            50
        )

    if current_width > 0:

        pg.draw.rect(
            screen,
            health_color,
            (
                bar_x,
                bar_y,
                current_width,
                health_height
            ),
            border_radius=6
        )

    pg.draw.rect(
        screen,
        (180, 180, 190),
        (
            bar_x,
            bar_y,
            health_width,
            health_height
        ),
        2,
        border_radius=6
    )

    hp_text = info_font.render(
        f"{int(player_health)} / "
        f"{player_stats['max_health']}",
        True,
        (255, 255, 255)
    )

    hp_rect = hp_text.get_rect(
        center=(
            bar_x + health_width // 2,
            bar_y + health_height // 2
        )
    )

    screen.blit(
        hp_text,
        hp_rect
    )

    # --------------------------------------------------------
    # Coins
    # --------------------------------------------------------
    
    coin_x = SCREEN_WIDTH - 300
    coin_y = 35
    
    pg.draw.circle(
        screen,
        (255, 205, 60),
        (coin_x, coin_y),
        14
    )
    
    pg.draw.circle(
        screen,
        (180, 130, 20),
        (coin_x, coin_y),
        10,
        2
    )
    
    coin_text = info_font.render(
        f"Coins: {player_coins}",
        True,
        (255, 230, 100)
    )
    
    screen.blit(
        coin_text,
        (
            coin_x + 22,
            coin_y - 10
        )
    )

    
    # --------------------------------------------------------
    # Weapon
    # --------------------------------------------------------

    weapon_text = info_font.render(
        f"WEAPON: {get_current_weapon()['name']}",
        True,
        (230, 230, 230)
    )

    screen.blit(
        weapon_text,
        (570, 15)
    )

    # --------------------------------------------------------
    # Enemies
    # --------------------------------------------------------

    enemies_left = (
        len(enemies)
        + len(spawn_queue)
    )

    enemy_text = info_font.render(
        f"ENEMIES: {enemies_left}",
        True,
        (230, 230, 230)
    )

    screen.blit(
        enemy_text,
        (570, 42)
    )

    # --------------------------------------------------------
    # State
    # --------------------------------------------------------

    if game_state == GAME_STATE_PREP:

        state_text = "PRESS SPACE TO START"

    elif game_state == GAME_STATE_ACTIVE:

        if spawn_queue:
            state_text = "WAVE ACTIVE"
        else:
            state_text = "CLEAR ENEMIES"

    elif game_state == GAME_STATE_COMPLETE:

        state_text = "WAVE COMPLETE"

    elif game_state == GAME_STATE_UPGRADE:

        state_text = "CHOOSE UPGRADE"

    else:

        state_text = "GAME OVER"

    state_surface = info_font.render(
        state_text,
        True,
        (255, 255, 255)
    )

    state_rect = state_surface.get_rect(
        midright=(
            SCREEN_WIDTH - 20,
            TOP_BAR_HEIGHT // 2
        )
    )

    screen.blit(
        state_surface,
        state_rect
    )


# ============================================================
# PLAYER VISION DISPLAY
# ============================================================

def draw_player_vision(screen):

    if game_state not in (
        GAME_STATE_PREP,
        GAME_STATE_ACTIVE
    ):
        return

    vision_surface = pg.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pg.SRCALPHA
    )

    pg.draw.circle(
        vision_surface,
        (100, 180, 255, 35),
        player.center,
        player_stats["vision_range"],
        2
    )

    screen.blit(
        vision_surface,
        (0, 0)
    )


# ============================================================
# COMMUNICATION DEBUG
# ============================================================

def draw_communication_debug(screen):

    for enemy in enemies:

        if (
            enemy.communication_flash_timer
            <= 0
        ):
            continue

        if enemy.last_message_sender is not None:

            sender = enemy.last_message_sender

            if sender in enemies:

                pg.draw.line(
                    screen,
                    (80, 220, 255),
                    sender.rect.center,
                    enemy.rect.center,
                    2
                )

        if (
            enemy.communication_flash_position
            is not None
        ):

            position = (
                enemy.communication_flash_position
            )

            pg.draw.circle(
                screen,
                (80, 220, 255),
                (
                    round(position.x),
                    round(position.y)
                ),
                8,
                2
            )


# ============================================================
# WAVE COMPLETE
# ============================================================

def draw_wave_complete(screen):

    overlay = pg.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pg.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 120)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title_font = pg.font.SysFont(
        None,
        60
    )

    text = title_font.render(
        f"WAVE {wave_complete_number} COMPLETE",
        True,
        (100, 255, 150)
    )

    rect = text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
    )

    screen.blit(
        text,
        rect
    )


# ============================================================
# UPGRADE SCREEN
# ============================================================

def draw_upgrade_screen(screen):

    global upgrade_selection_rects

    upgrade_selection_rects = []

    overlay = pg.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pg.SRCALPHA
    )

    overlay.fill(
        (5, 5, 10, 225)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title_font = pg.font.SysFont(
        None,
        56
    )

    subtitle_font = pg.font.SysFont(
        None,
        28
    )

    card_title_font = pg.font.SysFont(
        None,
        30
    )

    body_font = pg.font.SysFont(
        None,
        20
    )

    small_font = pg.font.SysFont(
        None,
        18
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    title = title_font.render(
        f"WAVE {wave_complete_number} COMPLETE",
        True,
        (255, 255, 255)
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            115
        )
    )

    screen.blit(
        title,
        title_rect
    )

    subtitle = subtitle_font.render(
        "CHOOSE 1 UPGRADE",
        True,
        (180, 180, 200)
    )

    subtitle_rect = subtitle.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            165
        )
    )

    screen.blit(
        subtitle,
        subtitle_rect
    )

    # --------------------------------------------------------
    # Cards
    # --------------------------------------------------------

    card_width = 330
    card_height = 300
    gap = 25

    total_width = (
        card_width * 3
        + gap * 2
    )

    start_x = (
        SCREEN_WIDTH
        - total_width
    ) // 2

    card_y = 220

    mouse_pos = pg.mouse.get_pos()

    for index, upgrade_id in enumerate(
        upgrade_choices
    ):

        rect = pg.Rect(
            start_x
            + index * (
                card_width + gap
            ),
            card_y,
            card_width,
            card_height
        )

        upgrade_selection_rects.append(
            rect
        )

        hovered = rect.collidepoint(
            mouse_pos
        )

        if hovered:

            card_color = (
                55,
                50,
                75
            )

            border_color = (
                190,
                150,
                255
            )

        else:

            card_color = (
                35,
                35,
                45
            )

            border_color = (
                90,
                90,
                105
            )

        pg.draw.rect(
            screen,
            card_color,
            rect,
            border_radius=16
        )

        pg.draw.rect(
            screen,
            border_color,
            rect,
            3,
            border_radius=16
        )

        data = PLAYER_UPGRADES[
            upgrade_id
        ]

        # ----------------------------------------------------
        # Number
        # ----------------------------------------------------

        number_text = card_title_font.render(
            str(index + 1),
            True,
            (255, 220, 100)
        )

        screen.blit(
            number_text,
            (
                rect.x + 20,
                rect.y + 18
            )
        )

        # ----------------------------------------------------
        # Icon
        # ----------------------------------------------------

        icon_rect = pg.Rect(
            rect.centerx - 42,
            rect.y + 25,
            84,
            70
        )

        pg.draw.rect(
            screen,
            (25, 25, 35),
            icon_rect,
            border_radius=12
        )

        pg.draw.rect(
            screen,
            (110, 100, 140),
            icon_rect,
            2,
            border_radius=12
        )

        icon_text = card_title_font.render(
            data["icon"],
            True,
            (210, 180, 255)
        )

        icon_text_rect = icon_text.get_rect(
            center=icon_rect.center
        )

        screen.blit(
            icon_text,
            icon_text_rect
        )

        # ----------------------------------------------------
        # Name
        # ----------------------------------------------------

        name_text = card_title_font.render(
            data["name"],
            True,
            (255, 255, 255)
        )

        name_rect = name_text.get_rect(
            centerx=rect.centerx,
            y=rect.y + 115
        )

        screen.blit(
            name_text,
            name_rect
        )

        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        description = data[
            "description"
        ]

        description_text = body_font.render(
            description,
            True,
            (190, 190, 205)
        )

        description_rect = description_text.get_rect(
            centerx=rect.centerx,
            y=rect.y + 165
        )

        screen.blit(
            description_text,
            description_rect
        )

        # ----------------------------------------------------
        # Effect
        # ----------------------------------------------------

        effect_text = body_font.render(
            data["effect"],
            True,
            (100, 255, 150)
        )

        effect_rect = effect_text.get_rect(
            centerx=rect.centerx,
            y=rect.y + 205
        )

        screen.blit(
            effect_text,
            effect_rect
        )

        # ----------------------------------------------------
        # Click hint
        # ----------------------------------------------------

        click_text = small_font.render(
            f"PRESS {index + 1}",
            True,
            (140, 140, 155)
        )

        click_rect = click_text.get_rect(
            centerx=rect.centerx,
            y=rect.bottom - 40
        )

        screen.blit(
            click_text,
            click_rect
        )

    # --------------------------------------------------------
    # Current stats
    # --------------------------------------------------------

    stats_text = small_font.render(
        f"HP {int(player_health)}/"
        f"{int(player_stats['max_health'])}   "
        f"SPD {int(player_stats['move_speed'])}   "
        f"DMG x{player_stats['damage_multiplier']:.2f}   "
        f"FIRE x{player_stats['fire_rate_multiplier']:.2f}   "
        f"ARMOR {int(player_stats['damage_reduction'] * 100)}%   "
        f"VISION {int(player_stats['vision_range'])}",
        True,
        (170, 170, 185)
    )

    stats_rect = stats_text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            570
        )
    )

    screen.blit(
        stats_text,
        stats_rect
    )

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    footer = body_font.render(
        "Click an upgrade or press 1 / 2 / 3",
        True,
        (230, 230, 240)
    )

    footer_rect = footer.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            625
        )
    )

    screen.blit(
        footer,
        footer_rect
    )


# ============================================================
# GAME OVER
# ============================================================

def draw_game_over(screen):

    overlay = pg.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pg.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 190)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title_font = pg.font.SysFont(
        None,
        80
    )

    info_font = pg.font.SysFont(
        None,
        32
    )

    game_over_text = title_font.render(
        "GAME OVER",
        True,
        (255, 60, 60)
    )

    game_over_rect = (
        game_over_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50
            )
        )
    )

    screen.blit(
        game_over_text,
        game_over_rect
    )

    restart_text = info_font.render(
        "Press R to restart",
        True,
        (255, 255, 255)
    )

    restart_rect = (
        restart_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 40
            )
        )
    )

    screen.blit(
        restart_text,
        restart_rect
    )


# ============================================================
# SHOOT
# ============================================================

def shoot():

    mouse_position = pg.Vector2(
        pg.mouse.get_pos()
    )

    direction = (
        mouse_position
        - pg.Vector2(
            player.center
        )
    )

    if direction.length_squared() == 0:
        return

    direction.normalize_ip()

    weapon = get_current_weapon()

    projectile_count = weapon.get(
        "projectile_count",
        1
    )

    spread = weapon.get(
        "spread",
        0
    )

    if projectile_count == 1:
        angles = [0]
    else:
        angles = [
            -spread / 2
            + i * (
                spread / (projectile_count - 1)
            )
            for i in range(projectile_count)
        ]

    for angle in angles:

        shot_direction = direction.rotate(
            angle
        )

        bullet_start = (
            pg.Vector2(
                player.center
            )
            + shot_direction * 30
        )

        bullets.append(
            Bullet(
                bullet_start,
                shot_direction
            )
        )


# ============================================================

# ============================================================

def reset_game():

    global player_health
    global player_damage_timer
    global weapon_fire_timer
    global wave_number
    global game_state
    global wave_complete_timer
    global spawn_queue
    global spawn_timer
    global player_stats
    global upgrade_choices
    global upgrade_selection_rects
    global wave_complete_number

    player_stats = PLAYER_BASE_STATS.copy()

    player_health = player_stats[
        "max_health"
    ]

    player_damage_timer = 0
    weapon_fire_timer = 0

    wave_number = 1

    game_state = GAME_STATE_PREP

    wave_complete_timer = 0

    spawn_queue = []
    spawn_timer = 0

    items.clear()
    enemy_projectiles.clear()
    bullets.clear()

    upgrade_choices = []
    upgrade_selection_rects = []

    wave_complete_number = 0

    enemies.clear()
    bullets.clear()
    enemy_projectiles.clear()

    player.center = SAFE_ZONE.center

    player_pos.update(
        player.center
    )
    
# ============================================================
# HOME / SHOP / COINS
# ============================================================




player_coins = 0

owned_weapons = {"pistol"}
equipped_weapon = "pistol"

WAVE_REWARDS = {
    1: 10,
    2: 15,
    3: 25,
    4: 40,
    5: 60,
    6: 100,
}

PLAYER_WEAPONS = {

    "pistol": {
        "name": "Pistol",
        "damage": 25,
        "fire_rate": 0.25,
        "bullet_speed": 850,
        "range": 700,
        "bullet_radius": 5,
        "cost": 0,
    },

    "smg": {
        "name": "SMG",
        "damage": 12,
        "fire_rate": 0.08,
        "bullet_speed": 900,
        "range": 500,
        "bullet_radius": 4,
        "cost": 100,
    },

    "shotgun": {
        "name": "Shotgun",
        "damage": 15,
        "fire_rate": 0.8,
        "bullet_speed": 700,
        "range": 400,
        "bullet_radius": 5,
        "projectile_count": 6,
        "spread": 30,
        "cost": 150,
    },

    "rifle": {
        "name": "Rifle",
        "damage": 40,
        "fire_rate": 0.45,
        "bullet_speed": 1100,
        "range": 900,
        "bullet_radius": 4,
        "cost": 250,
    },
}


def buy_weapon(weapon_id):

    global player_coins

    if weapon_id not in PLAYER_WEAPONS:
        return

    if weapon_id in owned_weapons:
        return

    weapon = PLAYER_WEAPONS[weapon_id]

    if player_coins >= weapon["cost"]:

        player_coins -= weapon["cost"]

        owned_weapons.add(
            weapon_id
        )


def equip_weapon(weapon_id):

    global equipped_weapon

    if weapon_id in owned_weapons:

        equipped_weapon = weapon_id


def get_current_weapon():

    return PLAYER_WEAPONS[
        equipped_weapon
    ]

# ============================================================
# HOME SCREEN
# ============================================================

HOME_PLAY_RECT = pg.Rect(
    SCREEN_WIDTH // 2 - 180,
    280,
    360,
    70
)

HOME_WEAPONS_RECT = pg.Rect(
    SCREEN_WIDTH // 2 - 180,
    370,
    360,
    70
)


def draw_home_screen(screen):

    screen.fill(
        (8, 7, 11)
    )

    title_font = pg.font.SysFont(
        None,
        80
    )

    big_font = pg.font.SysFont(
        None,
        36
    )

    small_font = pg.font.SysFont(
        None,
        24
    )

    # Title

    title = title_font.render(
        "AI ARENA",
        True,
        (242, 238, 248)
    )

    title_rect = title.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            130
        )
    )

    screen.blit(
        title,
        title_rect
    )

    # Equipped weapon

    weapon = get_current_weapon()

    weapon_text = small_font.render(
        f"EQUIPPED: {weapon['name']}",
        True,
        (180, 180, 200)
    )

    weapon_rect = weapon_text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            200
        )
    )

    screen.blit(
        weapon_text,
        weapon_rect
    )

    # Coins

    coin_text = big_font.render(
        f"COINS: {player_coins}",
        True,
        (255, 215, 80)
    )

    coin_rect = coin_text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            240
        )
    )

    screen.blit(
        coin_text,
        coin_rect
    )

    mouse_pos = pg.mouse.get_pos()

    # --------------------------------------------------------
    # PLAY
    # --------------------------------------------------------

    play_hover = HOME_PLAY_RECT.collidepoint(
        mouse_pos
    )

    pg.draw.rect(
        screen,
        (55, 40, 75)
        if play_hover
        else (35, 30, 45),
        HOME_PLAY_RECT,
        border_radius=12
    )

    pg.draw.rect(
        screen,
        (190, 150, 255)
        if play_hover
        else (90, 80, 110),
        HOME_PLAY_RECT,
        2,
        border_radius=12
    )

    play_text = big_font.render(
        "PLAY",
        True,
        (255, 255, 255)
    )

    screen.blit(
        play_text,
        play_text.get_rect(
            center=HOME_PLAY_RECT.center
        )
    )

    # --------------------------------------------------------
    # WEAPONS
    # --------------------------------------------------------

    weapons_hover = (
        HOME_WEAPONS_RECT.collidepoint(
            mouse_pos
        )
    )

    pg.draw.rect(
        screen,
        (55, 40, 75)
        if weapons_hover
        else (35, 30, 45),
        HOME_WEAPONS_RECT,
        border_radius=12
    )

    pg.draw.rect(
        screen,
        (190, 150, 255)
        if weapons_hover
        else (90, 80, 110),
        HOME_WEAPONS_RECT,
        2,
        border_radius=12
    )

    weapons_text = big_font.render(
        "WEAPONS",
        True,
        (255, 255, 255)
    )

    screen.blit(
        weapons_text,
        weapons_text.get_rect(
            center=HOME_WEAPONS_RECT.center
        )
    )

# ============================================================
# WEAPON SHOP
# ============================================================

SHOP_WEAPON_RECTS = []


def draw_weapon_shop(screen):

    global SHOP_WEAPON_RECTS

    SHOP_WEAPON_RECTS = []

    screen.fill(
        (8, 7, 11)
    )

    title_font = pg.font.SysFont(
        None,
        55
    )

    card_font = pg.font.SysFont(
        None,
        30
    )

    info_font = pg.font.SysFont(
        None,
        21
    )

    small_font = pg.font.SysFont(
        None,
        18
    )

    title = title_font.render(
        "WEAPON SHOP",
        True,
        (242, 238, 248)
    )

    screen.blit(
        title,
        title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                70
            )
        )
    )

    coins = info_font.render(
        f"COINS: {player_coins}",
        True,
        (255, 215, 80)
    )

    screen.blit(
        coins,
        (
            SCREEN_WIDTH - 180,
            35
        )
    )

    mouse_pos = pg.mouse.get_pos()

    weapons = list(
        PLAYER_WEAPONS.keys()
    )

    card_width = 260
    card_height = 330
    gap = 25

    total_width = (
        len(weapons)
        * card_width
        + (len(weapons) - 1)
        * gap
    )

    start_x = (
        SCREEN_WIDTH - total_width
    ) // 2

    for index, weapon_id in enumerate(
        weapons
    ):

        weapon = PLAYER_WEAPONS[
            weapon_id
        ]

        rect = pg.Rect(
            start_x
            + index
            * (card_width + gap),
            140,
            card_width,
            card_height
        )

        SHOP_WEAPON_RECTS.append(
            rect
        )

        hovered = rect.collidepoint(
            mouse_pos
        )

        owned = (
            weapon_id
            in owned_weapons
        )

        equipped = (
            weapon_id
            == equipped_weapon
        )

        if equipped:

            card_color = (
                45,
                65,
                50
            )

            border_color = (
                100,
                255,
                150
            )

        elif hovered:

            card_color = (
                55,
                45,
                75
            )

            border_color = (
                190,
                150,
                255
            )

        else:

            card_color = (
                30,
                30,
                40
            )

            border_color = (
                80,
                80,
                95
            )

        pg.draw.rect(
            screen,
            card_color,
            rect,
            border_radius=15
        )

        pg.draw.rect(
            screen,
            border_color,
            rect,
            3,
            border_radius=15
        )

        # Weapon name

        name = card_font.render(
            weapon["name"],
            True,
            (255, 255, 255)
        )

        screen.blit(
            name,
            name.get_rect(
                centerx=rect.centerx,
                y=rect.y + 25
            )
        )

        # Stats

        damage = info_font.render(
            f"Damage: {weapon['damage']}",
            True,
            (210, 210, 220)
        )

        fire_rate = info_font.render(
            f"Fire rate: {weapon['fire_rate']:.2f}s",
            True,
            (210, 210, 220)
        )

        bullet_speed = info_font.render(
            f"Bullet speed: {weapon['bullet_speed']}",
            True,
            (210, 210, 220)
        )

        weapon_range = info_font.render(
            f"Range: {weapon['range']}",
            True,
            (210, 210, 220)
        )

        screen.blit(
            damage,
            (
                rect.x + 25,
                rect.y + 90
            )
        )

        screen.blit(
            fire_rate,
            (
                rect.x + 25,
                rect.y + 125
            )
        )

        screen.blit(
            bullet_speed,
            (
                rect.x + 25,
                rect.y + 160
            )
        )

        screen.blit(
            weapon_range,
            (
                rect.x + 25,
                rect.y + 195
            )
        )

        # Status

        if equipped:

            status = "EQUIPPED"

            status_color = (
                100,
                255,
                150
            )

        elif owned:

            status = "CLICK TO EQUIP"

            status_color = (
                180,
                180,
                200
            )

        elif player_coins >= weapon["cost"]:

            status = f"BUY  -  {weapon['cost']} COINS"

            status_color = (
                255,
                215,
                80
            )

        else:

            status = f"LOCKED  -  {weapon['cost']} COINS"

            status_color = (
                220,
                90,
                90
            )

        status_text = small_font.render(
            status,
            True,
            status_color
        )

        screen.blit(
            status_text,
            status_text.get_rect(
                centerx=rect.centerx,
                y=rect.bottom - 55
            )
        )

    # Back button

    back_rect = pg.Rect(
        30,
        30,
        120,
        45
    )

    pg.draw.rect(
        screen,
        (35, 30, 45),
        back_rect,
        border_radius=8
    )

    back_text = small_font.render(
        "BACK",
        True,
        (255, 255, 255)
    )

    screen.blit(
        back_text,
        back_text.get_rect(
            center=back_rect.center
        )
    )

    return back_rect



# ============================================================
# MAIN LOOP
# ============================================================

running = True


while running:

    dt = clock.tick(60) / 1000.0

    dt = min(
        dt,
        0.05
    )

    # ========================================================
    # PLAYER TIMERS
    # ========================================================

    if player_damage_timer > 0:

        player_damage_timer -= dt

        player_damage_timer = max(
            0,
            player_damage_timer
        )

    if weapon_fire_timer > 0:

        weapon_fire_timer -= dt

        weapon_fire_timer = max(
            0,
            weapon_fire_timer
        )

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pg.event.get():

        if event.type == pg.QUIT:

            running = False

        # ----------------------------------------------------
        # Mouse
        # ----------------------------------------------------

        elif event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:
                
                # ====================================================
                # HOME
                # ====================================================
                
                if game_state == GAME_STATE_HOME:
                    
                    if HOME_PLAY_RECT.collidepoint(
                        event.pos
                    ):
                        
                        reset_game()
                        
                        game_state = GAME_STATE_PREP
                    
                    elif HOME_WEAPONS_RECT.collidepoint(
                        event.pos
                    ):
                        game_state = GAME_STATE_SHOP
                        
                # ====================================================
                # SHOP
                # ====================================================
                
                elif game_state == GAME_STATE_SHOP:
                    
                    back_rect = pg.Rect(
                        30,
                        30,
                        120,
                        45
                    )
                    
                    if back_rect.collidepoint(
                        event.pos
                    ):
                        
                        game_state = GAME_STATE_HOME
                    
                    else: 
                        
                        for index, rect in enumerate(
                            SHOP_WEAPON_RECTS
                        ):
                            
                            if rect.collidepoint(
                                event.pos
                            ):
                                
                                weapon_ids = list(
                                    PLAYER_WEAPONS.keys()
                                )
                                
                                weapon_id = (
                                    weapon_ids[index]
                                )
                                
                                if weapon_id in owned_weapons:
                                    
                                    equip_weapon(
                                        weapon_id
                                    )
                                    
                                else:
                                    buy_weapon(
                                        weapon_id
                                    )
                                    
                                    break
                
                # ====================================================
                # UPGRADE
                # ====================================================

                elif game_state == GAME_STATE_UPGRADE:

                    for index, rect in enumerate(
                        upgrade_selection_rects
                    ):

                        if rect.collidepoint(
                            event.pos
                        ):

                            choose_upgrade(
                                index
                            )

                            break
                    
        # ----------------------------------------------------
        # Keyboard
        # ----------------------------------------------------

        elif event.type == pg.KEYDOWN:

            # Start wave.
            if (
                event.key == pg.K_SPACE
                and
                game_state == GAME_STATE_PREP
            ):

                start_wave()

            # Upgrade selection.
            elif (
                game_state == GAME_STATE_UPGRADE
                and
                event.key in (
                    pg.K_1,
                    pg.K_2,
                    pg.K_3
                )
            ):

                choose_upgrade(
                    event.key - pg.K_1
                )

            # Restart.
            elif (
                event.key == pg.K_r
                and
                game_state == GAME_STATE_GAME_OVER
            ):

                reset_game()
                
                game_state = GAME_STATE_HOME

    # ========================================================
    # GAME UPDATE
    # ========================================================

    if game_state != GAME_STATE_GAME_OVER:

        # ====================================================
        # PLAYER MOVEMENT
        # ====================================================

        if game_state in (
            GAME_STATE_PREP,
            GAME_STATE_ACTIVE
        ):

            keys = pg.key.get_pressed()

            direction = pg.Vector2(
                keys[pg.K_d] - keys[pg.K_a],
                keys[pg.K_s] - keys[pg.K_w]
            )

            if direction.length_squared() > 0:

                direction.normalize_ip()

                movement = (
                    direction
                    * player_stats["move_speed"]
                    * dt
                )

            else:

                movement = pg.Vector2(
                    0,
                    0
                )

            move_horizontal(
                player,
                movement.x,
                walls
            )

            move_vertical(
                player,
                movement.y,
                walls
            )

            keep_inside_play_area(
                player,
                PLAY_AREA
            )

            player_pos.update(
                player.center
            )

        # ====================================================
        # ITEM PICKUP
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            for item in items[:]:

                if player_pos.distance_to(item.pos) <= 30:

                    if item.type == "health":
                        player_health = min(
                            player_health + 25,
                            player_stats["max_health"]
                        )

                    elif item.type == "coin":
                        player_coins += 10

                    elif item.type == "ammo":
                        # Reserved for the future ammo system.
                        pass

                    items.remove(item)

        # ====================================================
        # PLAYER SHOOTING
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            mouse_buttons = pg.mouse.get_pressed()

            if (
                mouse_buttons[0]
                and weapon_fire_timer <= 0
            ):

                shoot()

                weapon = get_current_weapon()
                
                weapon_fire_timer = (
                    weapon["fire_rate"]
                    / player_stats[
                        "fire_rate_multiplier"
                    ]
                )

        # ====================================================
        # WAVE SYSTEM
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            if spawn_queue:

                spawn_timer -= dt

                if spawn_timer <= 0:

                    enemy_type = (
                        spawn_queue[0]
                    )

                    before_count = (
                        len(spawn_queue)
                    )

                    spawn_next_wave_enemy()

                    after_count = (
                        len(spawn_queue)
                    )

                    if after_count < before_count:

                        spawn_timer = (
                            SPAWN_DELAY[
                                enemy_type
                            ]
                        )

                    else:

                        spawn_timer = 0.1

            elif not enemies:

                game_state = (
                    GAME_STATE_COMPLETE
                )

                wave_complete_timer = (
                    WAVE_COMPLETE_TIME
                )

                wave_complete_number = (
                    wave_number
                )

                player_coins += WAVE_REWARDS.get(
                    wave_number,
                    0
                )

                enemy_projectiles.clear()
                bullets.clear()

        # ====================================================
        # WAVE COMPLETE
        # ====================================================

        elif game_state == GAME_STATE_COMPLETE:

            wave_complete_timer -= dt

            if wave_complete_timer <= 0:
                
                generate_upgrade_choices()

                enemy_projectiles.clear()
                bullets.clear()

                game_state = (
                    GAME_STATE_UPGRADE
                )

        # ====================================================
        # ENEMY TIMERS
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            for enemy in enemies:

                enemy.update_communication_timer(
                    dt
                )

        # ====================================================
        # ENEMY AI
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            for enemy in enemies:

                enemy.update_vision(
                    player_pos,
                    walls,
                    enemies
                )

                enemy.update_ai(
                    player_pos,
                    navigation_grids,
                    walls,
                    dt
                )

                keep_inside_play_area(
                    enemy.rect,
                    PLAY_AREA
                )

        # ====================================================
        # PLAYER BULLET UPDATE
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            for bullet in bullets:

                bullet.update(
                    dt,
                    walls
                )

        # ====================================================
        # ENEMY PROJECTILE UPDATE
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            for projectile in enemy_projectiles:

                projectile.update(
                    dt,
                    walls,
                    player
                )

        # ====================================================
        # PLAYER BULLET -> ENEMY
        # ====================================================

        if game_state == GAME_STATE_ACTIVE:

            for bullet in bullets:

                if not bullet.alive:
                    continue

                for enemy in enemies:

                    if enemy.health <= 0:
                        continue

                    enemy_distance = (
                        bullet.position.distance_to(
                            pg.Vector2(
                                enemy.rect.center
                            )
                        )
                    )

                    collision_distance = (
                        bullet.radius
                        + enemy.rect.width / 2
                    )

                    if (
                        enemy_distance
                        <= collision_distance
                    ):

                        # ------------------------------------
                        # NEW AI PERCEPTION SYSTEM
                        # ------------------------------------

                        enemy.register_attack(
                            bullet,
                            enemies
                        )

                        # ------------------------------------
                        # Damage
                        # ------------------------------------

                        enemy.health -= (
                            bullet.damage
                        )

                        bullet.alive = False

                        break

        # ====================================================
        # REMOVE DEAD ENEMIES
        # ====================================================

        alive_enemies = []

        for enemy in enemies:
            if enemy.health > 0:
                alive_enemies.append(enemy)
            else:
                drop_item(enemy)

        enemies[:] = alive_enemies

        # ====================================================
        # REMOVE DEAD PLAYER BULLETS
        # ====================================================

        bullets[:] = [
            bullet
            for bullet in bullets
            if bullet.alive
        ]

        # ====================================================
        # REMOVE DEAD ENEMY PROJECTILES
        # ====================================================

        enemy_projectiles[:] = [
            projectile
            for projectile in enemy_projectiles
            if projectile.alive
        ]

    # ========================================================
    # RENDER
    # ========================================================

    if game_state == GAME_STATE_HOME:

        draw_home_screen(screen)

    elif game_state == GAME_STATE_SHOP:

        draw_weapon_shop(screen)

    else:

        draw_map(screen)
        draw_top_bar(screen)
        draw_player_vision(screen)

        if (
            player_damage_timer > 0
            and
            int(player_damage_timer * 12) % 2 == 0
        ):
            player_color = (255, 255, 255)
        else:
            player_color = (80, 220, 120)

        pg.draw.rect(
            screen,
            player_color,
            player
        )

        mouse_position = pg.Vector2(
            pg.mouse.get_pos()
        )

        player_center = pg.Vector2(
            player.center
        )

        aim_direction = (
            mouse_position
            - player_center
        )

        if aim_direction.length_squared() > 0:

            aim_direction.normalize_ip()

            aim_end = (
                player_center
                + aim_direction * 35
            )

            pg.draw.line(
                screen,
                (255, 255, 255),
                player_center,
                (
                    round(aim_end.x),
                    round(aim_end.y)
                ),
                3
            )

        for bullet in bullets:
            bullet.draw(screen)

        for projectile in enemy_projectiles:
            projectile.draw(screen)

        for item in items:
            item.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        draw_communication_debug(screen)

        if game_state == GAME_STATE_COMPLETE:
            draw_wave_complete(screen)

        if game_state == GAME_STATE_UPGRADE:
            draw_upgrade_screen(screen)

        if game_state == GAME_STATE_GAME_OVER:
            draw_game_over(screen)

    pg.display.flip()


# ============================================================
# EXIT
# ============================================================

pg.quit()