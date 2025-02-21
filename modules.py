from random import choice, shuffle, sample
from functools import reduce
from ascii import ascii_art
from os import system
import categories as cat
import colors_cli as c
import settings
import time
import json
from classic_quiz import QuizGame


#  Fő futási ciklus
def run_game():
    points = 0
    help_count = settings.HELP_COUNT
    show_welcome_screen()
    question_type = get_question_type()
    questions_data = load_questions(question_type)
    num_of_questions = get_num_of_questions(len(questions_data), question_type)
    num_of_choices = get_difficulty()
    questions = generate_questions(question_type, num_of_questions, num_of_choices, questions_data)

    start_time = time.time() # Timer indítása
    track_progress = []
    for i in range(len(questions)):
        answer, right_answer, help_count = ask_questions(questions[i], question_type, help_count, i)
        if check_answer(answer, right_answer):
            points += 1
            track_progress.append(True)
        else:
            track_progress.append(False)
        time.sleep(1.2)
        show_welcome_screen()
    end_time = time.time() 
    total_time = round(end_time - start_time) # Timer vége + kalkuláció
    show_results(track_progress, total_time, points, num_of_questions)


#  Splash screen
def show_welcome_screen():
    system("cls")
    print(c.col(ascii_art, c.C.PURPLE))


#  Kérdéstípus választási lehetőség
def get_question_type() -> str:
    print(c.highlight("\tVálassz az alábbi témakörök közül:\n"))
    print(f"\t\tA: {cat.Cat.capitals.value}")
    print(f"\t\tB: {cat.Cat.cars.value}")
    print(f"\t\tC: {cat.Cat.songs_hu.value}")
    print(f"\t\tD: {cat.Cat.songs_int.value}")
    print(f"\t\tE: {cat.Cat.pyquestions.value}")
    while True:
        user_input = input("\t--> ")
        if user_input.lower() not in "abcde":
            print(c.warning('\t"A", "B", "C", "D" vagy "E" választási lehetőséged van!'))
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
        case "e":
            question_type = cat.Cat.pyquestions
    return question_type


#  Adatok beolvasása JSON fájlból
def load_questions(question_type):
    try:
        with open("./quizes/" + question_type.name + ".json", "r", encoding="utf-8") as file:
            try:
                raw_data = json.load(file)
            except json.JSONDecodeError as e:
                print(c.error("\tHIBA! Érvénytelen JSON formátum!"))
                exit()
        return raw_data
    except FileNotFoundError:
        print(c.error("\tHIBA! A kérdésfájl nem található!"))
        exit()


#  A kérdések számának bekérése
def get_num_of_questions(max: int, question_type: cat.Cat) -> int:
    show_welcome_screen()
    print(c.highlight(f"\tA választott kategória: {question_type.value}\n"))
    while True:
        try:
            num_of_questions = int(input("\tHány kérdést szeretnél? "))
            if num_of_questions < 2:
                print(c.warning(f"\tEz túl kevés lesz, nem?"))
                continue
            if num_of_questions > max:
                print(c.warning(f"\tMaximum {max} kérdést választhatsz!"))
                continue
            else:
                return num_of_questions
        except ValueError:
            print(c.error("\tEgész számot adj meg!"))


#  A választási lehetőségek számának bekérése
def get_difficulty() -> int:
    print(c.info("\tVálassz nehézségi szintet:"))
    print(c.ok("\t\t1. Könnyű"),c.warning("\t2. Közepes"),c.error("\t3. Nehéz"))
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
    input(c.info("\tÜss egy [Enter]-t és kezdünk"))
    system("cls")
    show_welcome_screen()
    return num_of_choices


#  A bekért mennyiségű kvízkérdés generálása bekért mennyiségű válaszlehetőséggel
def generate_questions(question_type, qty: int, num_of_choices: int, questions_data: dict) -> tuple[str, str, list[str]]:
    # TODO: ITT kezdődik a módosítás: Ha Python vizsga kérdéseket választja a User, akkor a classic_quiz\ QuizGame-ból kell hívni a play() metódust, tehát egy külön ágra fut, aminek a felületét az alaphoz kell igazítani
    if (question_type == cat.Cat.pyquestions):
        game = QuizGame()
        game.play()
    else:
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
def ask_questions(question: list, question_type: cat.Cat, help_count: int, act_question) -> list[str]:
    act_question += 1
    question_topic, right_answer, choices_picked = question
    answers_picked_dict = { chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked)) }
    already_used_help = False
    while True:
        match question_type.name:
            case "pyquestions":
                print(f"\t{act_question}. {c.highlight(question_topic)} következnek:")
            case "capitals":
                print(f"\t{act_question}. Mi {c.highlight(question_topic)} fővárosa?")
            case "cars":
                print(f"\t{act_question}. Melyik a jellemző modellje a(z) {c.highlight(question_topic)} autómárkának?")
            case "songs_hu" | "songs_int":
                print(f"\t{act_question}. Melyik a(z) {c.highlight(question_topic)} egyik ismert dala?")
        if already_used_help: print(c.info("\tFeleztél! Az alábbi lehetőségek maradtak:"))
        for letter, item in answers_picked_dict.items():
            print(f"\t\t{letter}. {item}")
        if help_count and not already_used_help: print(c.info(f'\tFelező segítség ({help_count}db) használata: "/"'))
        your_answer = input("\tTipped --> ").upper()
        if your_answer == "/":
            if help_count == 0:
                print(c.warning("\tNincs több felezési lehetőséged!\n"))
                time.sleep(1.2)
                show_welcome_screen()
                continue
            if already_used_help:
                print(c.warning("\tMár használtál egy felezést ennél a kérdésnél!\n"))
                time.sleep(1.2)
                show_welcome_screen()
                continue
            help_count -= 1
            num_of_choices = len(answers_picked_dict)
            while len(answers_picked_dict) != num_of_choices / 2:
                answer_to_dismiss = choice(list(answers_picked_dict.keys()))
                if answers_picked_dict[answer_to_dismiss] == right_answer:
                    continue
                answers_picked_dict.pop(answer_to_dismiss)
            already_used_help = True
            show_welcome_screen()
            continue
        elif your_answer in answers_picked_dict.keys():
            your_answer = answers_picked_dict[your_answer]
            already_used_help = False
            break
        else:
            print(c.warning("\tNem lehetséges válaszlehetőség!"))
            time.sleep(1.2)
            show_welcome_screen()
    return your_answer, right_answer, help_count


#  A válaszok kiértékelése, vizuális visszajelzés, pontszám visszaadása
def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        print(c.col(f"\t\u2588\u2588", c.C.GREEN)) # Zöld kocka kiíratása ha helyes a válasz
        return True
    else:
        print(c.col(f"\t\u2588\u2588", c.C.RED)) # Piros kocka kiíratása ha helytelen a válasz
        return False
    
def show_results(progress: list, total_time, points, num_of_questions) -> None:
    progress_bar = reduce(lambda x, y: x + y, [c.col(f"\u2588\u2588", c.C.GREEN) if item else c.col(f"\u2588\u2588", c.C.RED) for item in progress])
    percentage = f"{100 * points / num_of_questions:.1f}%"
    dashes = c.col("\t"+str('-' * (len(progress_bar)//8 + len(percentage)+13)), c.C.YELLOW)
    print(dashes)
    print(f"{c.col("\tEredményed:", c.C.YELLOW)} {progress_bar} {c.col(percentage, c.C.YELLOW)}")
    print(dashes)
    minutes, seconds = divmod(total_time, 60) # Időeredmény kiírása mm:ss formátumban
    print(c.col(f"\tJátékidőd: {minutes:02}:{seconds:02}", c.C.YELLOW))
    print(dashes  + "\n")