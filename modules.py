import settings
import json
from random import choice, shuffle, sample


#  Adatok beolvasása JSON fájlból
with open("cars.json", "r", encoding="utf-8") as file:
    cars = json.load(file)

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
def generate_questions(qty: int = 1, num_of_choices: int = 4) -> tuple[str, str, str]:
    questions = []
    for car_brand in sample(list(cars.keys()), qty):
        right_answer = cars[car_brand]
        wrong_answers = list(cars.values())
        wrong_answers.remove(right_answer)
        answers_picked = sample(wrong_answers, num_of_choices - 1)
        answers_picked.append(right_answer)
        shuffle(answers_picked)
        questions.append((car_brand, right_answer, answers_picked))
    return questions


#  A kérdések feltétele, a felhasználói válasz és a jó válasz visszaadásával
def ask_questions(question: list) -> int:
    help_count = settings.HELP_COUNT
    car_brand, right_answer, choices_picked = question
    answers_picked_dict = { chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked)) }
    already_used_help = False
    while True:
        print(f"Melyik a jellemző modellje a(z) \033[36m{car_brand}\033[0m autómárkának?")
        for letter, car_model in answers_picked_dict.items():
            print("    " + letter + ". " + car_model)
        if help_count: print(f'\033[35mFelező segítség ({help_count}db) használata: "/2"\033[0m')
        your_answer = input("Tipped --> ").upper()
        if your_answer == "/2":
            if help_count == 0:
                print("\033[33mNincs több felezési lehetőséged!\033[0m")
                continue
            if already_used_help:
                print("\033[33mMár használtál egy felezést ennél a kérdésnél!\033[0m")
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