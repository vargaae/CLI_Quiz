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
    track_progress = []
    for question in questions:
        answer, right_answer = ask_questions(question, question_type)
        if check_answer(answer, right_answer):
            points += 1
            track_progress.append(True)
        else:
            track_progress.append(False)
        time.sleep(1)
        show_welcome_screen()
    end_time = time.time() 
    total_time = round(end_time - start_time) # Timer vége + kalkuláció
    show_results(track_progress, total_time, points, num_of_questions)


if __name__ == "__main__":
    main()
