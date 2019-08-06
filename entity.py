import tcod
from renderer import RenderOrder

class Entity:
    def __init__(self, x, y, name, faction, char, colour, hp_max, attack, shield, alert_threshold, render_order=RenderOrder.CORPSE, walkable=True, inventory=None, ai=None, item=None, environment=None):
        self.x=x
        self.y=y
        self.name=name
        self.faction=faction
        self.char=char
        self.colour=colour

        self.hp_max=hp_max
        self.hp=hp_max
        self.attack=attack
        self.shield=shield
        self.alert_threshold=alert_threshold
        self.alert=0

        self.render_order=render_order
        # Is pathable and not the ability to walk
        self.walkable=walkable
        # Whether the entity has an inventory, is an item or has an AI (if not then furniture)
        self.inventory=inventory
        if self.inventory:
            self.inventory.owner=self
        self.ai=ai
        if self.ai:
            self.ai.owner=self
        self.item=item
        if self.item:
            self.item.owner=self
        self.environment=environment
        if self.environment:
            self.environment.owner=self

    def take_damage(self, damage_amount, piercing, lethal):
        damage_remaining=damage_amount
        # bools are for announcements
        shielded=False
        death=False
        if not piercing:
            if damage_remaining>self.shield:
                damage_remaining-=self.shield
                self.shield=0
            else:
                self.shield-=damage_remaining
                damage_remaining=0
        if lethal:
            if damage_remaining>self.hp:
                damage_remaining-=self.hp
                self.hp=0
            else:
                self.hp-=damage_remaining
                damage_remaining=0
        else:
            if damage_remaining>self.hp-1:
                damage_remaining-=(self.hp-1)
                self.hp=1
            else:
                self.hp-=damage_remaining
                damage_remaining=0
        damage_taken=damage_amount-damage_remaining
        # EXTEND RESULTS

    def move(self, dx, dy, block_map):
        if not self.walkable:
            block_map[self.y, self.x]=False
        self.x+=dx
        self.y+=dy
        if not self.walkable:
            block_map[self.y, self.x]=(not self.walkable)

    def swap(self, target):
        x=self.x
        y=self.y
        self.x=target.x
        self.y=target.y
        target.x=x
        target.y=y
        return {'swap': target}