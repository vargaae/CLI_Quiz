import settings
import json
from random import choice, shuffle, sample


#  Kérdéstípus választási lehetőség
def get_question_type() -> str:
    print("Milyen témájú kvízt szeretnél?\nLehetőségek:")
    print("A.: Fővárosok")
    print("B.: Autómárkák")
    print("C.: Dalok")
    while True:
        user_input = input("Válassz: ")
        if user_input.lower() not in "abc":
            print('"A", "B" vagy "C" választási lehetőséged van!')
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
        with open(question_type + ".json", "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        return raw_data
    except FileNotFoundError:
        print("\033[31mHIBA! A kérdésfájl nem található!\033[0m")
        exit()


#  A kérdések számának bekérése
def get_num_of_questions(max: int) -> int:
    while True:
        try:
            num_of_questions = int(input("Hány kérdést szeretnél? "))
            if num_of_questions > max:
                print(f"Maximum {max} kérdést választhatsz!")
                continue
            else:
                return num_of_questions
        except ValueError:
            print("Egész számot adj meg!")


#  A választási lehetőségek számának bekérése
def get_num_of_choices(min: int, max: int) -> int:
    while True:
        try:
            num_of_choices = int(input(f"Hány választási lehetőséget szeretnél [{min}-{max}]? "))
            if (min <= num_of_choices <= max) and (num_of_choices % 2 == 0):
                return num_of_choices
            else:
                print(f"A választási lehetőségek száma {min} és {max} közötti páros szám lehet!")
                continue
        except ValueError:
            print("Egész számot adj meg!")


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
                print(f"Mi a fővárosa \033[36m{question_topic}\033[0m-nak/-nek?")
            case "cars":
                print(f"Melyik a jellemző modellje a(z) \033[36m{question_topic}\033[0m autómárkának?")
            case "songs":
                print(f"Melyik a(z) \033[36m{question_topic}\033[0m zenei formáció egyik ismert dala?")
        for letter, item in answers_picked_dict.items():
            print("    " + letter + ". " + item)
        if help_count: print(f'\033[35mFelező segítség ({help_count}db) használata: "/2"\033[0m')
        your_answer = input("Tipped --> ").upper()
        if your_answer == "/2":
            if help_count == 0:
                print("\033[33mNincs több felezési lehetőséged!\033[0m\n")
                continue
            if already_used_help:
                print("\033[33mMár használtál egy felezést ennél a kérdésnél!\033[0m\n")
                continue
            help_count -= 1
            num_of_choices = len(answers_picked_dict)
            while len(answers_picked_dict) != num_of_choices / 2:
                answer_to_dismiss = choice(list(answers_picked_dict.keys()))
                if answers_picked_dict[answer_to_dismiss] == right_answer:
                    continue
                answers_picked_dict.pop(answer_to_dismiss)
            already_used_help = True
            print("\033[33mFeleztél! Az alábbi lehetőségek maradtak:\033[0m")
            continue
        elif your_answer in answers_picked_dict.keys():
            your_answer = answers_picked_dict[your_answer]
            already_used_help = False
            break
        else:
            print("\033[33mNem lehetséges válaszlehetőség!\033[0m")
    return your_answer, right_answer


#  A válaszok kiértékelése, vizuális visszajelzés, pontszám visszaadása
def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        print(f"\033[32m\u2588\u2588\033[0m\n") # Zöld kocka kiíratása ha helyes a válasz
        return 1
    else:
        print(f"\033[31m\u2588\u2588\033[0m\n") # Piros kocka kiíratása ha helytelen a válasz
        return 0