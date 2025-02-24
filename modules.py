from random import choice, shuffle, sample
from functools import reduce
from ascii import ascii_art
from os import system
import categories as cat
import colors_cli as c
import settings
import time
import json

#  Fő futási ciklus
def run_game():
    points = 0
    win_streak = 0
    act_streak = 0
    help_count = settings.HELP_COUNT
    show_splash_screen()
    question_type = get_question_type()
    questions_data = load_questions(question_type)
    num_of_choices = get_difficulty(question_type)
    questions = generate_questions(num_of_choices, questions_data)

    start_time = time.time() # Timer indítása
    track_progress = []
    for i in range(settings.QUESTION_COUNT):
        answer, right_answer, help_count = ask_questions(questions[i], question_type, help_count, i, act_streak)
        if check_answer(answer, right_answer):
            track_progress.append(True)
            points += 1
            act_streak += 1
            if act_streak and act_streak % 5 == 0:
                help_count += 1
            if act_streak > win_streak:
                win_streak = act_streak
        else:
            track_progress.append(False)
            act_streak = 0
        time.sleep(1.2)
    end_time = time.time() 
    total_time = round(end_time - start_time) # Timer vége + kalkuláció
    percentage, gametime = show_results(track_progress, total_time, points)
    highscores = check_for_new_highscore(load_highscores(), percentage, gametime)
    show_highscores(highscores)


#  Splash screen
def show_splash_screen():
    system("cls")
    print(c.col(ascii_art, c.C.PURPLE))


#  Kérdéstípus választási lehetőség
def get_question_type() -> str:
    print(c.highlight("\tVálassz az alábbi témakörök közül:\n"))
    print(f"\t\tA: {cat.Cat.capitals.value}")
    print(f"\t\tB: {cat.Cat.cars.value}")
    print(f"\t\tC: {cat.Cat.songs_hu.value}")
    print(f"\t\tD: {cat.Cat.songs_int.value}")
    while True:
        user_input = input("\t--> ")
        if user_input.lower() not in "abcd" or user_input == "":
            print(c.warning('\t"A", "B", "C" vagy "D" választási lehetőséged van!'))
            continue
        break
    match user_input.lower():
        case "a":
            question_type = cat.Cat.capitals
        case "b":
            question_type = cat.Cat.cars
        case "c":
            question_type = cat.Cat.songs_hu
        case "d":
            question_type = cat.Cat.songs_int
    return question_type


#  Adatok beolvasása JSON fájlból
def load_questions(question_type):
    try:
        with open("./quizes/" + question_type.name + ".json", encoding="utf-8") as file:
            try:
                raw_data = json.load(file)
            except json.JSONDecodeError as e:
                print(c.error("\tHIBA! Érvénytelen JSON formátum!"))
                exit()
        return raw_data
    except FileNotFoundError:
        print(c.error("\tHIBA! A kérdésfájl nem található!"))
        exit()


#  A választási lehetőségek számának bekérése
def get_difficulty(question_type) -> int:
    show_splash_screen()
    print(c.highlight(f"\tA választott kategória: {question_type.value}\n\n"))
    print(c.info("\tVálassz nehézségi szintet:\n"))
    print(c.ok("\t\t1. Könnyű"), c.warning("\t2. Közepes"), c.error("\t3. Nehéz"), "\n")
    while True:
        num_of_choices = input("\t--> ")
        if num_of_choices not in ["1","2","3"]:
            print(c.warning("\tVálassz egy számot: 1-2-3"))
            continue
        else:
            match num_of_choices:
                case "1": num_of_choices = 4
                case "2": num_of_choices = 6
                case "3": num_of_choices = 8
            break
    input(c.info("\n\tÜss egy [Enter]-t és kezdünk"))
    return num_of_choices


#  A bekért mennyiségű kvízkérdés generálása bekért mennyiségű válaszlehetőséggel
def generate_questions(num_of_choices: int, questions_data: dict) -> tuple[str, str, list[str]]:
    questions = []
    for question_subject in sample(list(questions_data.keys()), settings.QUESTION_COUNT):
        right_answer = questions_data[question_subject]
        wrong_answers = list(questions_data.values())
        wrong_answers.remove(right_answer)
        answers_picked = sample(wrong_answers, num_of_choices - 1)
        answers_picked.append(right_answer)
        shuffle(answers_picked)
        questions.append((question_subject, right_answer, answers_picked))
    return questions


#  A kérdések feltétele, a felhasználói válasz és a jó válasz visszaadásával
def ask_questions(question: list, question_type: cat.Cat, help_count: int, act_question, act_streak: int) -> list[str]:
    act_question += 1
    question_topic, right_answer, choices_picked = question
    answers_picked_dict = { chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked)) }
    already_used_help = False
    while True:
        show_splash_screen()
        print(f"\t{act_question}/{settings.QUESTION_COUNT}. ", end="")
        match question_type.name:
            case "capitals":
                print(f"Mi {c.highlight(question_topic)} fővárosa?")
            case "cars":
                print(f"Melyik a jellemző modellje a(z) {c.highlight(question_topic)} autómárkának?")
            case "songs_hu" | "songs_int":
                print(f"Melyik a(z) {c.highlight(question_topic)} egyik ismert dala?")
        if already_used_help: print(c.info("\tFeleztél! Az alábbi lehetőségek maradtak:"))
        for letter, item in answers_picked_dict.items():
            print(f"\t\t{letter}. {item}") # Válaszlehetőségek kiírása
        if help_count and not already_used_help: 
            match help_count:
                case 2|3|4|5: print(c.info(f"{'Felező "/": ' + c.ok(str(help_count) + 'db'):>90}"))
                case 1: print(c.info(f"{'Felező "/": ' + c.warning(str(help_count) + 'db'):>90}"))
                case _: print(c.info(f"{'Felező "/": ' + c.error(str(help_count) + 'db'):>90}"))
            
        match act_streak % 5:
            case 3: print_streak = f'{c.info("Win streak: ") + c.warning(str(act_streak) + "x")}'
            case 4: print_streak = f'{c.info("Win streak: ") + c.error(str(act_streak) + "x")}'
            case _: print_streak = f'{c.info("Win streak: ") + c.ok(str(act_streak) + "x")}'
        print(f"{print_streak:>102}")
        your_answer = input("\tTipped --> ").upper()
        if your_answer == "/":
            if help_count == 0:
                print(c.warning("\tNincs több felezési lehetőséged!\n"))
                time.sleep(1.2)
                continue
            if already_used_help:
                print(c.warning("\tMár használtál egy felezést ennél a kérdésnél!\n"))
                time.sleep(1.2)
                continue
            help_count -= 1
            num_of_choices = len(answers_picked_dict)
            while len(answers_picked_dict) != num_of_choices / 2:
                answer_to_dismiss = choice(list(answers_picked_dict.keys()))
                if answers_picked_dict[answer_to_dismiss] == right_answer:
                    continue
                answers_picked_dict.pop(answer_to_dismiss)
            already_used_help = True
            continue
        elif your_answer in answers_picked_dict.keys():
            your_answer = answers_picked_dict[your_answer]
            already_used_help = False
            break
        else:
            print(c.warning("\tNem lehetséges válaszlehetőség!"))
            time.sleep(1.2)
    return your_answer, right_answer, help_count


#  A válaszok kiértékelése, vizuális visszajelzés, pontszám visszaadása
def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        print(c.col(f"\t\u2588\u2588", c.C.GREEN)) # Zöld kocka kiíratása, ha helyes a válasz
        return True
    else:
        print(c.col(f"\t\u2588\u2588", c.C.RED)) # Piros kocka kiíratása, ha helytelen a válasz
        return False


#  Eredmények kijelzése a játék végén
def show_results(progress: list, total_time, points) -> None:
    show_splash_screen()
    progress_bar = reduce(lambda x, y: x + y, [c.col(f"\u2588\u2588", c.C.GREEN) if item else c.col(f"\u2588\u2588", c.C.RED) for item in progress])
    percentage = 100 * points // settings.QUESTION_COUNT
    dashes = c.col("\t"+str('-' * (len(progress_bar)//8 + len(str(percentage))+14)), c.C.YELLOW)
    print(dashes)
    print(f"{c.col("\tEredményed:", c.C.YELLOW)} {progress_bar} {c.col(str(percentage)+"%", c.C.YELLOW)}")
    print(dashes)
    minutes, seconds = divmod(total_time, 60)
    print(c.col(f"\tJátékidőd: {minutes:02}:{seconds:02}", c.C.YELLOW))
    print(dashes  + "\n")
    return percentage, total_time


def load_highscores() -> list:
    try:
        with open("highscores.txt", encoding="utf-8") as file:
            highscores = []
            for row in file:
                data = row.strip().split(";")
                entry = {
                    "name": data[0],
                    "percentage": int(data[1]),
                    "gametime": int(data[2])
                }
                highscores.append(entry)
            return highscores[:5]
    except FileNotFoundError:
        return None


def check_for_new_highscore(highscores, percentage, gametime):
    new_highscore_index = -1
    if highscores == None:
        highscores = add_highscore([], 0, percentage, gametime)
    elif len(highscores) > 0:
        for i in range(len(highscores)):
            if percentage > highscores[i]["percentage"]:
                new_highscore_index = i
                break
            if percentage == highscores[i]["percentage"] and gametime <= highscores[i]["gametime"]:
                new_highscore_index = i
                break
            elif len(highscores) < 5:
                new_highscore_index = len(highscores)
        if new_highscore_index >= 0:
            highscores = add_highscore(highscores, new_highscore_index, percentage, gametime)
    return highscores


def add_highscore(highscores, new_highscore_index, percentage, gametime):
    print(c.highlight("\tGratulálok az eredményed benne van a TOP5-ben!"))
    name = input(c.highlight("\tAdd meg a neved: "))
    new_entry = {"name": name, "percentage": percentage, "gametime": gametime}
    highscores.insert(new_highscore_index, new_entry)
    update_highscores_file(highscores[:5])
    return highscores


def show_highscores(highscores):
    show_splash_screen()
    print(c.info(f"{'TOP 5 helyezett':^102}\n"))
    print(c.info(f'{f"{'Név:':<15}{'Százalék:':^15}{'Idő:':>8}":^100}'))
    print(c.info(f'{("-" * 38):^100}'))
    for i in range(len(highscores)):
        minutes, seconds = divmod(highscores[i]["gametime"], 60)
        name_str = f'{f"{i+1}. {highscores[i]['name']}"}'
        percentage_str = f'{highscores[i]["percentage"]}%'
        time_str = f"{minutes:02}:{seconds:02}"
        print(c.highlight(f'{f"{name_str:<20}{percentage_str:>4}{time_str:>14}": ^100}'))
    print("\n")


def update_highscores_file(highscores):
    with open("highscores.txt", "w", encoding="utf-8") as file:
        for entry in highscores:
            data = ";".join(str(e) for e in entry.values())
            file.write(data + "\n")