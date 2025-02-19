import settings
import time
from modules import *


def main() -> None:
    points = 0
    num_of_questions = get_num_of_questions(len(cars))
    num_of_choices = get_num_of_choices(settings.MIN_CHOICE, settings.MAX_CHOICE)
    questions = generate_questions(num_of_questions, num_of_choices)

    start_time = time.time() # Timer indítása
    for question in questions:
        answer, right_answer = ask_questions(question)
        points += check_answer(answer, right_answer)
    end_time = time.time() 
    total_time = round(end_time - start_time) # Timer vége + kalkuláció
    minutes, seconds = divmod(total_time, 60) # Időeredmény kiírása mm:ss formátumban
    
    print(f"-------------------------\nGratulálok!") # TODO Észrevétel: csak akkor kéne gratulálni ha az eredmény kifejezetten jó
    print(f"\033[33mJátékidőd:\033[0m {minutes:02}:{seconds:02}")
    print(f"\033[33mEredményed:\033[0m {100 * points / num_of_questions:.1f}%\n")


if __name__ == "__main__":
    main()
