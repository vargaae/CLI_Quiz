import settings
import json
from ascii import ascii_art
import colors_cli as c
from os import system
from functools import reduce
from random import choice, shuffle, sample


def show_welcome_screen():
    system("cls")
    print(c.col(ascii_art, c.C.PURPLE))


#  Kérdéstípus választási lehetőség
def get_question_type() -> str:
    print(c.highlight("Válassz az alábbi témakörök közül:\n"))
    print("\tA: Fővárosok")
    print("\tB: Autómárkák")
    print("\tC: Dalok")
    while True:
        user_input = input("--> ")
        if user_input.lower() not in "abc":
            print(c.warning('"A", "B" vagy "C" választási lehetőséged van!'))
            continue
        break
    match user_input.lower():
        case "a":
            question_type = "capitals"
        case "b":
            question_type = "cars"
        case "c":
            question_type = "songs"
    return question_type


#  Adatok beolvasása JSON fájlból
def load_questions(question_type):
    try:
        with open("./quizes/" + question_type + ".json", "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        return raw_data
    except FileNotFoundError:
        print(c.error("HIBA! A kérdésfájl nem található!"))
        exit()


#  A kérdések számának bekérése
def get_num_of_questions(max: int) -> int:
    while True:
        try:
            num_of_questions = int(input("Hány kérdést szeretnél? "))
            if num_of_questions < 1:
                print(c.warning(f"Ez túl kevés lesz, nem?"))
                continue
            if num_of_questions > max:
                print(c.warning(f"Maximum {max} kérdést választhatsz!"))
                continue
            else:
                return num_of_questions
        except ValueError:
            print(c.warning("Egész számot adj meg!"))


#  A választási lehetőségek számának bekérése
def get_num_of_choices(min: int, max: int) -> int:
    while True:
        try:
            num_of_choices = int(input(f"Hány választási lehetőséget szeretnél [{min}-{max}]? "))
            if (min <= num_of_choices <= max) and (num_of_choices % 2 == 0):
                input(c.info("Üss [Enter]-t a kezdéshez"))
                system("cls")
                show_welcome_screen()
                return num_of_choices
            else:
                print(c.warning(f"A választási lehetőségek száma {min} és {max} közötti páros szám lehet!"))
                continue
        except ValueError:
            print(c.warning("Egész számot adj meg!"))


#  A bekért mennyiségű kvízkérdés generálása bekért mennyiségű válaszlehetőséggel
def generate_questions(qty: int, num_of_choices: int, questions_data: dict) -> tuple[str, str, list[str]]:
    questions = []
    for question_subject in sample(list(questions_data.keys()), qty):
        right_answer = questions_data[question_subject]
        wrong_answers = list(questions_data.values())
        wrong_answers.remove(right_answer)
        answers_picked = sample(wrong_answers, num_of_choices - 1)
        answers_picked.append(right_answer)
        shuffle(answers_picked)
        questions.append((question_subject, right_answer, answers_picked))
    return questions


#  A kérdések feltétele, a felhasználói válasz és a jó válasz visszaadásával
def ask_questions(question: list, question_type: str) -> int:
    help_count = settings.HELP_COUNT
    question_topic, right_answer, choices_picked = question
    answers_picked_dict = { chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked)) }
    already_used_help = False
    while True:
        match question_type:
            case "capitals":
                print(f"Mi {c.highlight(question_topic)} fővárosa?")
            case "cars":
                print(f"Melyik a jellemző modellje a(z) {c.highlight(question_topic)} autómárkának?")
            case "songs":
                print(f"Melyik a(z) {c.highlight(question_topic)} zenei formáció egyik ismert dala?")
        for letter, item in answers_picked_dict.items():
            print(f"\t{letter}. {item}")
        if help_count: print(c.info(f'Felező segítség ({help_count}db) használata: "/2"'))
        your_answer = input("Tipped --> ").upper()
        if your_answer == "/2":
            if help_count == 0:
                print(c.warning("Nincs több felezési lehetőséged!\n"))
                continue
            if already_used_help:
                print(c.warning("Már használtál egy felezést ennél a kérdésnél!\n"))
                continue
            help_count -= 1
            num_of_choices = len(answers_picked_dict)
            while len(answers_picked_dict) != num_of_choices / 2:
                answer_to_dismiss = choice(list(answers_picked_dict.keys()))
                if answers_picked_dict[answer_to_dismiss] == right_answer:
                    continue
                answers_picked_dict.pop(answer_to_dismiss)
            already_used_help = True
            print(c.info("Feleztél! Az alábbi lehetőségek maradtak:"))
            continue
        elif your_answer in answers_picked_dict.keys():
            your_answer = answers_picked_dict[your_answer]
            already_used_help = False
            break
        else:
            print(c.warning("Nem lehetséges válaszlehetőség!"))
    return your_answer, right_answer


#  A válaszok kiértékelése, vizuális visszajelzés, pontszám visszaadása
def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        print(c.col(f"\u2588\u2588\n", c.C.GREEN)) # Zöld kocka kiíratása ha helyes a válasz
        return True
    else:
        print(c.col(f"\u2588\u2588\n", c.C.RED)) # Piros kocka kiíratása ha helytelen a válasz
        return False
    
def show_results(progress: list, total_time, points, num_of_questions) -> None:
    progress_bar = reduce(lambda x, y: x + y, [c.col(f"\u2588\u2588", c.C.GREEN) if item else c.col(f"\u2588\u2588", c.C.RED) for item in progress])
    percentage = f"{100 * points / num_of_questions:.1f}%"
    print(f"{c.col("Eredményed:", c.C.YELLOW)} {progress_bar} {c.col(percentage, c.C.YELLOW)}\n")
    minutes, seconds = divmod(total_time, 60) # Időeredmény kiírása mm:ss formátumban
    print(c.col(f"-------------------------\nGratulálok!", c.C.YELLOW)) # TODO Észrevétel: csak akkor kéne gratulálni ha az eredmény kifejezetten jó
    print(c.col(f"Játékidőd: {minutes:02}:{seconds:02}", c.C.YELLOW))