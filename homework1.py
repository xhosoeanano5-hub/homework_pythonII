class Character:
    count = 0
    def __init__(self, name, hp=100, level=1):
        self.name = name
        self._hp = hp
        self.level = level
        Character.count += 1
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)
    def take_damage(self, amount):
        self.hp = self._hp - amount
    @property
    def is_alive(self):
        return self._hp > 0
    def attack(self, target):
        target.take_damage(5)
    @classmethod
    def from_string(cls, text):
        name, hp = text.split(";")
        return cls(name, hp=int(hp))
    @staticmethod
    def is_valid_name(name):
        return 2 <= len(name) <= 20
    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        return self.name == other.name and self.level == other.level
    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self._hp})"
def log_action(func):
    def wrapper(self, *args, **kwargs):
        print(f"{self.name} → {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper
class Warrior(Character):
    def __init__(self, name, hp=100, level=1, strength=10):
        super().__init__(name, hp=hp, level=level)
        self.strength = strength
    @log_action
    def attack(self, target):
        target.take_damage(self.strength)
class Mage(Character):
    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp=hp, level=level)
        self.mana = mana
    @log_action
    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(20)
        else:
            super().attack(target)
    def __str__(self):
        return f"{super().__str__()} MP {self.mana}"
class HealerMixin:
    @log_action
    def heal(self, target, amount):
        target.hp += amount
class Priest(HealerMixin, Mage):
    pass
class Inventory:
    def __init__(self):
        self.items = []
    def add(self, **item):
        self.items.append(item)
    def find(self, **filters):
        result = []
        for item in self.items:
            if all(item.get(k) == v for k, v in filters.items()):
                result.append(item)
        return result
    def __len__(self):
        return len(self.items)
def battle(a, b):
    while a.is_alive and b.is_alive:
        a.attack(b)
        print(a)
        print(b)
        if not b.is_alive:
            break
        b.attack(a)
        print(a)
        print(b)
    return a if a.is_alive else b