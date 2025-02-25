from functools import reduce
from .splash_screen import show_splash_screen
import features.categories as cat
import features.colors_cli as c
import settings
import time
from .highscore import show_highscores, load_highscores, check_for_new_highscore
from .question_loader import load_questions
from .question_generator import generate_questions
from .quiz_handler import ask_questions


#  Fő futási ciklus
def run_game():
    points = 0
    win_streak = 0
    help_count = settings.HELP_COUNT
    quiz_type = get_quiz_type()
    quiz_data = load_questions(quiz_type)
    num_of_choices = get_difficulty(quiz_type)
    if (quiz_type == cat.Cat.python_learning):
        questions = generate_questions(num_of_choices, quiz_data, quiz_type)
    else: questions = generate_questions(num_of_choices, quiz_data, quiz_type)

    start_time = time.time()
    track_progress = []
    for i in range(settings.QUESTION_COUNT):
        answer, right_answer, help_count = ask_questions(questions[i], quiz_type, help_count, i, win_streak, quiz_data, i)
        if check_answer(answer, right_answer):
            track_progress.append(True)
            points += 1
            win_streak += 1
            if win_streak and win_streak % 5 == 0:
                help_count += 1
        else:
            track_progress.append(False)
            win_streak = 0
        time.sleep(1.2)
    end_time = time.time() 
    total_time = round(end_time - start_time)
    percentage, gametime = show_results(track_progress, total_time, points)
    highscores = check_for_new_highscore(load_highscores(), quiz_type, percentage, gametime)
    show_highscores(highscores, quiz_type)


#  Kérdéstípus választási lehetőség
def get_quiz_type() -> str:
    while True:
        show_splash_screen()
        print(c.highlight("\tVálassz az alábbi témakörök közül:\n"))
        print(f"\t\tA: {cat.Cat.capitals.value}")
        print(f"\t\tB: {cat.Cat.cars.value}")
        print(f"\t\tC: {cat.Cat.songs_hu.value}")
        print(f"\t\tD: {cat.Cat.songs_int.value}")
        print(f"\t\tE: {cat.Cat.python_learning.value}")
        user_input = input("\t--> ")
        if user_input.lower() not in "abcde" or user_input == "":
            print(c.warning("\tA-B-C-D-E választási lehetőséged van!"))
            time.sleep(1.2)
            continue
        break
    match user_input.lower():
        case "a":
            quiz_type = cat.Cat.capitals
        case "b":
            quiz_type = cat.Cat.cars
        case "c":
            quiz_type = cat.Cat.songs_hu
        case "d":
            quiz_type = cat.Cat.songs_int
        case "e":
            quiz_type = cat.Cat.python_learning
    return quiz_type


#  A választási lehetőségek számának bekérése
def get_difficulty(quiz_type) -> int:
    while True:
        show_splash_screen()
        print(c.highlight(f"\tA választott kategória: {quiz_type.value}\n\n"))
        print(c.info("\tVálassz nehézségi szintet:\n"))
        print(c.ok("\t\t1. Könnyű"), c.warning("\t2. Közepes"), c.error("\t3. Nehéz"), "\n")
        num_of_choices = input("\t--> ")
        if num_of_choices not in ["1","2","3"]:
            print(c.warning("\tVálassz egy számot: 1-2-3"))
            time.sleep(1.2)
            continue
        else:
            match num_of_choices:
                case "1": num_of_choices = 4
                case "2": num_of_choices = 6
                case "3": num_of_choices = 8
            break
    input(c.info("\n\tÜss egy [Enter]-t és kezdünk!"))
    return num_of_choices


#  A válaszok kiértékelése, vizuális visszajelzés, pontszám visszaadása
def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        print("\x1b[1A\x1b[2K", end="")
        print(c.col(f"\t\t\u2588\u2588", c.C.GREEN)) # Zöld kocka kiíratása, ha helyes a válasz
        return True
    else:
        print("\x1b[1A\x1b[2K", end="")
        print(c.col(f"\t\t\u2588\u2588", c.C.RED)) # Piros kocka kiíratása, ha helytelen a válasz
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