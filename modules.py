import settings
from random import choice

def ask_questions(question: list) -> int:
    help_count = settings.HELP_COUNT
    car_brand, right_answer, choices_picked = question
    answers_picked_dict = {
        chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked))
    }
    while True:
        print(f"Melyik a jellemző modellje a(z) \033[36m{car_brand}\033[0m autómárkának?")
        for letter, car_model in answers_picked_dict.items():
            print("    " + letter + ". " + car_model)
        if help_count: print(f'Felező segítség ({help_count}db): "/2"')
        your_answer = input("Tipped --> ").upper()
        if your_answer == "/2":
            if help_count == 0:
                print("\033[33mNincs több felezési lehetőséged!\033[0m")
                continue
            help_count -= 1
            num_of_choices = len(answers_picked_dict)
            while len(answers_picked_dict) != num_of_choices / 2:
                answer_to_dismiss = choice(list(answers_picked_dict.keys()))
                if answers_picked_dict[answer_to_dismiss] == right_answer:
                    continue
                answers_picked_dict.pop(answer_to_dismiss)
            print("\033[33mFeleztél! Az alábbi lehetőségek maradtak\033[0m")
            continue
        elif your_answer in answers_picked_dict.keys():
            your_answer = answers_picked_dict[your_answer]
            break
        else:
            print("\033[33mNem lehetséges válaszlehetőség!\033[0m")
    return your_answer, right_answer