from django.db import models

from arenafighter.utils import dice
from arenafighter.models.inventory import Inventory, InventoryItem, Armor, Weapon


class Character(models.Model):
    created_by = models.ForeignKey('Profile', null=False, related_name='created_characters')
    level = models.IntegerField(default=1)
    name = models.TextField(default="The Stranger")
    hpmax = models.IntegerField(default=dice.roll(15, 6))
    equipped_armor = models.ForeignKey('Armor', default=None, related_name='equipped_on', blank=True, null=True)
    current_hp = models.IntegerField()
    base_attack = models.IntegerField(default=2)
    base_defense = models.IntegerField(default=3)
    gold = models.IntegerField(default=50)
    xp = models.IntegerField(default=0)
    renown = models.IntegerField(default=0)
    next_levelup = models.IntegerField(default=100)
    num_armor = models.IntegerField(default=0)
    fights_won = models.IntegerField(default=0)
    fights_lost = models.IntegerField(default=0)

    class Meta:
        app_label = 'arenafighter'

    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def attack(self):
        attack_value = self.base_attack
        for weapon in self.equipped_weapon.all():
            attack_value += weapon.attack_value
        attack = dice.roll(attack_value, 6)
        return attack


    def equip(self, item):
        if item.type == 'weapon':
            if len(self.inventory.weapon.filter(equipped=True)) < 2:
                item.equipped = True
                item.save()
            else:
                weapon = self.inventory.weapon.filter(equipped=True)[0]
                self.unequip(weapon)
                item.equipped = True
                item.save()
        elif item.type == 'armor':
            item.equipped = True
        self.save()

    def unequip(self, item):
        item.equipped = False
        item.save()


    def purchase(self, item):
        if item.type == 'potion':
            self.inventory.potion.add(item)
        elif item.type == 'weapon':
            self.inventory.weapon.add(item)
        elif item.type == 'armor':
            self.inventory.armor.add(item)
        self.gold -= item.buy_value
        self.save()

    def sell(self, item):
        if item.type == 'potion':
            self.inventory.potion.remove(item)
        elif item.type == 'weapon':
            self.inventory.weapon.remove(item)
        elif item.type == 'armor':
            self.inventory.armor.remove(item)
        self.unequip(item)
        item.equipped = False
        item.save()
        self.gold += item.sell_value
        self.save()

    @property
    def items(self):
        weapons = self.inventory.weapon.all()
        armor = self.inventory.armor.all()
        potions = self.inventory.potion.all()
        items = []
        items.extend(weapons)
        items.extend(armor)
        items.extend(potions)
        return items

    @property
    def equipped_items(self):
        equipped_items = []
        weapons = self.inventory.weapon.filter(equipped=True)
        armors = self.inventory.armor.filter(equipped=True)
        potions = self.inventory.potion.filter(equipped=True)
        equipped_items.extend(weapons)
        equipped_items.extend(armors)
        equipped_items.extend(potions)
        return equipped_items

    @property
    def defense_value(self):
        defense_value = self.base_defense
        if self.equipped_armor:
            defense_value += self.equipped_armor.defense_value
        return defense_value