from random import choice
import features.categories as cat
import features.colors_cli as c
import settings
import time
from .modules import show_splash_screen


def ask_questions(question: list, quiz_type: cat.Cat, help_count: int, act_question, win_streak: int, quiz_data, i) -> list[str]:
    act_question += 1
    question_topic, right_answer, choices_picked = question
    answers_picked_dict = { chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked)) }
    already_used_help = False
    already_used_hint = False
    while True:
        show_splash_screen()
        print(f"\t{act_question}/{settings.QUESTION_COUNT}. ", end="")
        match quiz_type.name:
            case "python_learning":
                print(f"{c.highlight(question_topic)}?")
            case "capitals":
                print(f"Mi {c.highlight(question_topic)} fővárosa?")
            case "cars":
                print(f"Melyik a jellemző modellje a(z) {c.highlight(question_topic)} autómárkának?")
            case "songs_hu" | "songs_int":
                print(f"Melyik a(z) {c.highlight(question_topic)} egyik ismert dala?")
        if already_used_help: print(c.info("\tFeleztél! Az alábbi lehetőségek maradtak:"))
        if already_used_hint: print(c.info(f"\tPuska: {quiz_data[i]['hint']}"))
        for letter, item in answers_picked_dict.items():
            print(f"\t\t{letter}. {item}") # Válaszlehetőségek kiírása
        if help_count and not already_used_help and quiz_type.name == "python_learning":
            match help_count:
                case 2|3|4|5: print(c.info(f"{'Felező: "/", Súgás: "*": ' + c.ok(str(help_count) + 'db'):>90}"))
                case 1: print(c.info(f"{'Felező: "/", Súgás: "*": ' + c.warning(str(help_count) + 'db'):>91}"))
                case _: print(c.info(f"{'Felező: "/", Súgás: "*": ' + c.error(str(help_count) + 'db'):>91}"))
        elif help_count and not already_used_help:
            match help_count:
                case 2|3|4|5: print(c.info(f"{'Felező "/": ' + c.ok(str(help_count) + 'db'):>90}"))
                case 1: print(c.info(f"{'Felező "/": ' + c.warning(str(help_count) + 'db'):>91}"))
                case _: print(c.info(f"{'Felező "/": ' + c.error(str(help_count) + 'db'):>91}"))
            
        match win_streak % 5:
            case 3: print(f"{f'{c.info("Win streak: ") + c.warning(str(win_streak) + "x")}':>105}")
            case 4: print(f"{f'{c.info("Win streak: ") + c.error(str(win_streak) + "x")}':>105}")
            case _: print(f"{f'{c.info("Win streak: ") + c.ok(str(win_streak) + "x")}':>104}")
        your_answer = input("\tTipped --> ").upper()
        if your_answer == "/"  or your_answer == "*" and quiz_type.name == "python_learning":
            if help_count == 0:
                print(c.warning("\tNincs több segítséged!\n"))
                time.sleep(1.2)
                continue
            if already_used_help:
                print(c.warning("\tMár használtál egy segítséget ennél a kérdésnél!!\n"))
                time.sleep(1.2)
                continue
            help_count -= 1
            num_of_choices = len(answers_picked_dict)
            if your_answer == "*":
                already_used_hint = True
                continue
            else:
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