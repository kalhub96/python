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


class WeaponManager:

    def __init__(self):
        self.owned_weapons = {"pistol"}
        self.equipped_weapon = "pistol"

    def get_current_weapon(self):
        return PLAYER_WEAPONS[
            self.equipped_weapon
        ]

    def buy_weapon(self, weapon_id, coins):

        if weapon_id not in PLAYER_WEAPONS:
            return coins, False

        if weapon_id in self.owned_weapons:
            return coins, False

        weapon = PLAYER_WEAPONS[weapon_id]

        if coins < weapon["cost"]:
            return coins, False

        coins -= weapon["cost"]

        self.owned_weapons.add(
            weapon_id
        )

        return coins, True

    def equip_weapon(self, weapon_id):

        if weapon_id not in self.owned_weapons:
            return False

        self.equipped_weapon = weapon_id

        return True
