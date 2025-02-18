def ask_question(question) -> int:
    car_brand, right_answer, choices_picked = question
    answers_picked_dict = {
        chr(ord("A") + i): choices_picked[i] for i in range(len(choices_picked))
    }
    print(f"Melyik a jellemző modellje a(z) \033[36m{car_brand}\033[0m autómárkának?")
    for letter, car_model in answers_picked_dict.items():
        print("    " + letter + ". " + car_model)
    while True:
        your_answer = input("Tipped --> ").upper()  # TODO felezés lehetőségének kiírása
        if your_answer in answers_picked_dict.keys():
            your_answer = answers_picked_dict[your_answer]
            # TODO input ellenőrzése a "/2" felezőkulcsszó használatára
            break
        else:
            print(f"\033[33mNem lehetséges válaszlehetőség!\033[0m")
    return your_answer, right_answer
