import random
import colorama
from colorama import Fore, Back, Style


class Thing:
    """
    Класс содержит в себе следующие параметры - название, процент защиты, атаку и жизнь;
    Это могут быть предметы одежды, магические кольца, всё что угодно)
    """

    def __init__(self, name, defend, attack, life):
        self.name = name
        self.defend = defend
        self.attack = attack
        self.life = life


class Person:
    """
    Класс, содержащий в себе следующие параметры:
    Имя, кол-во hp/жизней, базовую атаку, базовый процент защиты.
    Параметры передаются через конструктор
    """
    def __init__(self, name, hp, base_attack, base_defend):
        self.name = name
        self.hp = hp
        self.base_attack = base_attack
        self.base_defend = base_defend
        self.things = []
        self.type = 'Персонаж'

    def __str__(self):
        return (str(self.type) + "-" + str(self.name) + " HP " + str(self.hp)
                + " Атака " + str(self.base_attack) + " Защита " + str(round(self.base_defend, 1))
                + " Экипировка " + str("+".join(self.things[i].name for i in range(len(self.things)))))

    def set_things(self, things):
        """
        метод, принимающий на вход список вещей
        """
        self.things.append(things)

    def damage(self, hit):
        self.hp -= hit


class Paladin(Person):
    """
    Класс наследуется от персонажа, при этом количество присвоенных
    жизней и процент защиты умножается на 2 в конструкторе;
    """
    def __init__(self, name, hp, base_attack, base_defend):
        super().__init__(name, hp, base_attack, base_defend)
        self.hp = self.hp * 2
        self.base_defend = self.base_defend * 2
        self.type = 'Паладин'


class Warrior(Person):
    """
    Класс наследуется от персонажа, при этом атака умножается на 2 в конструкторе.
    """
    def __init__(self, name, hp, base_attack, base_defend):
        super().__init__(name, hp, base_attack, base_defend)
        self.base_attack = self.base_attack * 2
        self.type = 'Воин'


colorama.init()
ring = Thing('Кольцо', 0, 50, 30)
helmet = Thing('Шлем', 0.1, 0, 50)
sword = Thing('Меч', 0, 100, 0)
shield = Thing('Щит', 0.1, 0, 70)
things = [ring, helmet, sword, shield]

amount = int(input(Back.LIGHTCYAN_EX + Fore.BLACK + 'Выберите сколько персонажей отправим на арену (от 2 до 10)'))
if amount < 2 or amount > 10:
    print(Back.RED + Fore.LIGHTGREEN_EX + 'Вы ввели недопустимое число')
    exit()

names = ['Буратино', 'Чиполино', 'Крокодил Гена', 'Чебурашка',
         'Шапокляк', 'Винни пух', 'Пятачок', 'Тигра', 'Кролик', 'Иа-Иа',
         'Супермэн', 'Человек паук', 'Халк', 'Капитан Америка', 'Бэтмэн',
         'Дэдпул', 'Росомаха', 'Тор', 'Железный человек', 'Блэйд']
# перемешаем имена, чтобы они выдавались в случайно порядке:
random.shuffle(names)

# Создаем случайное количество паладинов и войнов:
amount_paladin = random.randint(1, amount-1)
amount_warrior = amount - amount_paladin
paladins = [Paladin(names[i], 200, 50, 0.1) for i in range(amount_paladin)]
warriors = [Warrior(names[i+amount_paladin], 200, 50, 0.1) for i in range(amount_warrior)]
persons = paladins
persons.extend(warriors)

# Дадим каждому персонажу от 1 до 4 вещи
for person in persons:
    for i in range(random.randint(1, 4)):
        person.set_things(things[random.randint(0, len(things) - 1)])
        person.hp += person.things[i].life
        person.base_attack += person.things[i].attack
        person.base_defend += person.things[i].defend

print(Back.CYAN + Fore.BLACK + '______________________________')
print('Персонажи вышли на арену:')
for person in persons:
    print(Back.YELLOW + person.__str__())
print(Back.CYAN + Fore.BLACK + '______________________________')

while amount > 1:
    print(Back.BLACK + '')
    print(Back.CYAN + Fore.BLACK + '______________________________')

    # Выберем атакующего и защищающегося
    attack_person = random.randint(0, amount-1)
    while True:
        defend_person = random.randint(0, amount-1)
        if attack_person != defend_person:
            break
    damage = persons[attack_person].base_attack -\
             persons[attack_person].base_attack * persons[defend_person].base_defend
    print(Back.LIGHTGREEN_EX + Fore.RED + persons[attack_person].name, 'нанес удар по',
          persons[defend_person].name, 'и снял', damage, 'HP')
    persons[defend_person].damage(damage)
    if persons[defend_person].hp <= 0:
        amount -= 1
        print(persons[defend_person].type, persons[defend_person].name, 'убит')
        del persons[defend_person]
    print(Back.CYAN + '')
    print(Back.YELLOW + Fore.BLACK + 'Оставшиеся на арене Персонажи:')
    for person in persons:
        print(person.__str__())
    print(Back.CYAN + '______________________________')
    input(Back.LIGHTGREEN_EX + Fore.RED + 'Нажмите enter')

print(Back.BLACK + '')
for person in persons:
    print(Back.GREEN + Fore.BLACK + 'Победитель', person.__str__())
