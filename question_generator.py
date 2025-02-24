from random import shuffle, sample
import settings
import categories as cat


#  A bekért mennyiségű kvízkérdés generálása bekért mennyiségű válaszlehetőséggel
def generate_questions(num_of_choices: int, quiz_data: dict, quiz_type: cat.Cat, pyquestions) -> tuple[str, str, list[str]]:
    questions = []
    if (quiz_type.name == "python_learning"): 
        for question in quiz_data:
            right_answer = question['answer'] # question_subject->question
            # TODO: num_of_choices-> hány válaszlehetőség legyen:
            answers_picked = sample(question['options'], num_of_choices)
            shuffle(answers_picked) # keverés? TODO: ellenőrizni, hogy jól kever -e
            questions.append((question['question'], right_answer, answers_picked))
    else: 
        for question_subject in sample(list(quiz_data.keys()), settings.QUESTION_COUNT):
            right_answer = quiz_data[question_subject]
            wrong_answers = list(quiz_data.values())
            wrong_answers.remove(right_answer)
            answers_picked = sample(wrong_answers, num_of_choices - 1)
            answers_picked.append(right_answer)
            shuffle(answers_picked)
            questions.append((question_subject, right_answer, answers_picked))
    return questions