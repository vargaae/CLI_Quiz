import settings
import time
from modules import *


def main() -> None:
    points = 0
    show_welcome_screen()
    question_type = get_question_type()
    questions_data = load_questions(question_type)
    num_of_questions = get_num_of_questions(len(questions_data))
    num_of_choices = get_num_of_choices(settings.MIN_CHOICE, settings.MAX_CHOICE)
    questions = generate_questions(num_of_questions, num_of_choices, questions_data)

    start_time = time.time() # Timer indítása
    for question in questions:
        answer, right_answer = ask_questions(question, question_type)
        points += check_answer(answer, right_answer)
    end_time = time.time() 
    total_time = round(end_time - start_time) # Timer vége + kalkuláció
    minutes, seconds = divmod(total_time, 60) # Időeredmény kiírása mm:ss formátumban
    
    print(c.col(f"-------------------------\nGratulálok!", c.C.YELLOW)) # TODO Észrevétel: csak akkor kéne gratulálni ha az eredmény kifejezetten jó
    print(c.col(f"Játékidőd: {minutes:02}:{seconds:02}", c.C.YELLOW))
    print(c.col(f"Eredményed: {100 * points / num_of_questions:.1f}%\n", c.C.YELLOW))


if __name__ == "__main__":
    main()
