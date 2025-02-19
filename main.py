from random import sample, shuffle
import time
import json
import settings

# TODO: Program modulokra bontása:
from modules import ask_questions

# JSON beolvasása fájlból
with open("cars.json", "r", encoding="utf-8") as file:
    cars = json.load(file)


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


def get_num_of_choices(min: int, max: int) -> int:
    while True:
        try:
            num_of_choices = int(
                input(f"Hány választási lehetőséget szeretnél [{min}-{max}]? ")
            )
            if (min <= num_of_choices <= max) and (num_of_choices % 2 == 0):
                return num_of_choices
            else:
                print(
                    f"A választási lehetőségek száma {min} és {max} közötti páros szám lehet!"
                )
                continue
        except ValueError:
            print("Egész számot adj meg!")


def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        print(f"\033[32m\u2588\u2588\033[0m\n") # Zöld kocka kiíratása ha helyes a válasz
        return 1
    else:
        print(f"\033[31m\u2588\u2588\033[0m\n") # Piros kocka kiíratása ha helytelen a válasz
        return 0


def main() -> None:
    points = 0
    num_of_questions = get_num_of_questions(len(cars))
    num_of_choices = get_num_of_choices(settings.MIN_CHOICE, settings.MAX_CHOICE)
    questions = generate_questions(num_of_questions, num_of_choices)
    # timer indítása
    start_time = time.time()

    for question in questions:
        answer, right_answer = ask_questions(question)
        points += check_answer(answer, right_answer)
    # timer vége + kalkuláció
    end_time = time.time()
    total_time = round(end_time - start_time)
    # időeredmény kiírása mm:ss formátumban
    minutes, seconds = divmod(total_time, 60)
    
    print(f"-------------------------\nGratulálok!") # TODO Észrevétel: csak akkor kéne gratulálni ha az eredmény kifejezetten jó
    print(f"\033[33mJátékidőd:\033[0m {minutes:02}:{seconds:02}")
    print(f"\033[33mEredményed:\033[0m {100 * points / num_of_questions:.1f}%\n")


if __name__ == "__main__":
    main()
