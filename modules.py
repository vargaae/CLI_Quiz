from os import system
from time import sleep
from QuestionTypes import *
import json

def welcome_message(nr_of_questions: int) -> str:
    system("cls")
    print("\033[36mK V Í Z J Á T É K" + "\n" + "=================\033[0m")
    print(f"(A kvíz {nr_of_questions} kérdést tartalmaz, egyenként maximálisan {points_for_perfect} pont kapható.)\n")
    player_name = input("\033[33mAdd meg a játékos neved: ")
    print(f"Üdv {player_name}! Jó játékot!\033[0m")
    sleep(2.5)
    system("cls")
    return player_name


def read_highscore() -> list[str, int]:
    try:
        with open("highscore.txt", encoding="utf-8") as file:
            data = json.load(file)
        return data["highscoreholder"], data["highscore"]
    except Exception as e:
        print("Még nincs elmentve legmagasabb pontszám!")
        return "", 0


def write_highscore(name: str, highscore :int) -> None:
    try:
        with open("highscore.txt", "w", encoding="utf-8") as file:
            print("Elért pontjaid mentése...")
            json.dump({"highscoreholder": name, "highscore": highscore }, file)
    except Exception as e:
        print("Nem tudtam elmenteni az adatokat :(")


def import_questions(points_for_perfect: int) -> list[list, int, int]:
    try:
        with open("questions_and_answers.json", encoding="utf-8") as file:
            questions_answers = []
            questions = json.load(file)
            for row in questions:
                match row["qtype"]:
                    case "ABCD":
                        question = ABCDQuestion(row)
                    case "BOOL":
                        question = BoolQuestion(row)
                    case "DATE":
                        question = DateQuestion(row)
                    case "INTEGER":
                        question = IntegerQuestion(row)
                    case "FLOAT":
                        question = FloatQuestion(row)
                    case "SET":
                        question = SetQuestion(row)
                    case "TEXT":
                        question = TextQuestion(row)
                    case _:
                        raise UnknownError()
                questions_answers.append(question)

            class UnknownError(Exception):
                print("Adatfeldolgozási hiba!")
                system("exit")

            nr_of_questions = len(questions_answers)
            max_points = points_for_perfect * nr_of_questions
            return questions_answers, nr_of_questions, max_points
    except Exception as e:
        print("\033[33mHiba történt a kérdésfájl olvasásakor:\033[0m", e)
        exit()


def cycle_through_questions(questions_answers: list) -> list[int, int]:
    question_count = 1
    points = 0
    nr_of_right_answers = 0
    for question in questions_answers:
        print(f"\033[36m{question_count}. kérdés:\033[0m")
        is_right, text_answer, actual_points = question.check_answer(question.ask_question())
        points += actual_points
        print(text_answer)
        if is_right:
            nr_of_right_answers += 1
        question_count += 1
    return points, nr_of_right_answers


def get_results(nr_of_questions: int, points: int, max_points: int, nr_of_right_answers: int, player_name: str) -> None:
    highscoreholder, highscore = read_highscore()
    print(f"\033[033mA helyes válaszok száma: {nr_of_right_answers}/{nr_of_questions}")
    print(f"Összpontszám: {points}/{max_points}pont")
    print(f"Teljesítmény: {points / max_points * 100:.1f}%\033[0m")
    if points > highscore:
        if highscore != 0:
            print(f"\033[1;33;41mGratulálok! Megdöntötted {highscoreholder} legmagasabb pontszámát!\033[0m")
        write_highscore(player_name, points)
    else:
        print(f"\033[033mA rekordot {highscoreholder} tartja {highscore} ponttal!\033[0m")