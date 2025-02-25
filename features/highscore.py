import json
import time
import features.colors_cli as c
from .splash_screen import show_splash_screen

#  Highscore-ok betöltése
def load_highscores() -> list:
    try:
        with open("highscores.json", encoding="utf-8") as file:
            try:
                highscores = json.load(file)
                return highscores["highscores"]
            except json.JSONDecodeError:
                return {}
    except FileNotFoundError:
        return {}


#  Elért eredmény ellenőrzése, hogy befér-e a highscore táblába
def check_for_new_highscore(highscores, quiz_type, percentage, gametime):
    new_highscore_index = -1
    if quiz_type.name not in highscores:
        highscores = add_highscore(highscores, quiz_type, -1, percentage, gametime)
    elif len(highscores[quiz_type.name]) > 0:
        for i in range(len(highscores[quiz_type.name])):
            if percentage > highscores[quiz_type.name][i]["percentage"]:
                new_highscore_index = i
                break
            if percentage == highscores[quiz_type.name][i]["percentage"] and gametime <= highscores[quiz_type.name][i]["gametime"]:
                new_highscore_index = i
                break
            elif len(highscores[quiz_type.name]) < 5:
                new_highscore_index = len(highscores[quiz_type.name])
        if new_highscore_index >= 0:
            highscores = add_highscore(highscores, quiz_type, new_highscore_index, percentage, gametime)
        else:
            print(c.info("\tNem sikerült bekerülnöd a TOP 5-be!"))
            time.sleep(5)
    return highscores


#  Eredmény beszúrása a highscore táblába és mentés fle-ba
def add_highscore(highscores, quiz_type, new_highscore_index, percentage, gametime):
    print(c.highlight(f"\tGratulálok, az eredményed benne van a(z) {quiz_type.value} kategória TOP 5-ben!"))
    name = input(c.highlight("\tAdd meg a neved: "))
    new_entry = {"name": name, "percentage": percentage, "gametime": gametime}
    if new_highscore_index == -1:
        highscores[quiz_type.name] = []
        highscores[quiz_type.name].append(new_entry)
    else:
        highscores[quiz_type.name].insert(new_highscore_index, new_entry)
    update_highscores_file(highscores)
    return highscores


#  Highscore táblázat kiíratása
def show_highscores(highscores, quiz_type):
    show_splash_screen()
    print(c.info(f"{f'{quiz_type.value} TOP 5 helyezett':^102}\n"))
    print(c.info(f'{f"{'Név:':<15}{'Százalék:':^15}{'Idő:':>8}":^100}'))
    print(c.info(f'{("-" * 38):^100}'))
    for i in range(len(highscores[quiz_type.name])):
        minutes, seconds = divmod(highscores[quiz_type.name][i]["gametime"], 60)
        name_str = f'{f"{i+1}. {highscores[quiz_type.name][i]['name']}"}'
        percentage_str = f'{highscores[quiz_type.name][i]["percentage"]}%'
        time_str = f"{minutes:02}:{seconds:02}"
        print(c.highlight(f'{f"{name_str:<20}{percentage_str:>4}{time_str:>14}": ^100}'))
    print("\n")


#  Highscore file frissítése
def update_highscores_file(highscores):
    with open("highscores.json", "w", encoding="utf-8") as file:
        highscores = {"highscores": highscores}
        json.dump(highscores, file)