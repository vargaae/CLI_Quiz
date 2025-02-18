from random import sample, shuffle

cars = {
    "Acura": "NSX",
    "Alfa Romeo": "Giulia",
    "Aston Martin": "DB11",
    "Audi": "A4",
    "AvtoVAZ": "Niva",
    "Bentley": "Continental GT",
    "BMW": "M3",
    "Bufori": "Geneva",
    "Bugatti": "Veyron",
    "Buick": "Regal",
    "BYD": "Seal",
    "Cadillac": "Escalade",
    "Caterham Cars": "Seven",
    "Chevrolet": "Corvette",
    "Chrysler": "300C",
    "Citroën": "DS",
    "Cupra": "Formentor",
    "Dacia": "Duster",
    "Daihatsu": "Copen",
    "Dodge": "Challenger",
    "Dome": "Zero",
    "Faraday Future": "FF 91",
    "Ferrari": "F40",
    "Fiat": "500",
    "Fisker": "Ocean",
    "Ford": "Mustang",
    "General Motors": "EV1",
    "GEO": "Metro",
    "Gumpert": "Apollo",
    "Heuliez": "Pregunta",
    "Holden": "Commodore",
    "Honda": "Civic",
    "Hongqi": "H9",
    "Hyundai": "Tucson",
    "Infiniti": "Q50",
    "Isdera": "Imperator 108i",
    "Isuzu": "D-Max",
    "Izs": "2125 Kombi",
    "Jaguar": "E-Type",
    "Jeep": "Wrangler",
    "Jensen": "Interceptor",
    "Kia": "Sportage",
    "Koenigsegg": "Jesko",
    "Lada": "Samara",
    "Lamborghini": "Aventador",
    "Lancia": "Delta",
    "Land Rover": "Defender",
    "Lexus": "RX",
    "Lightning": "GT",
    "Lincoln": "Navigator",
    "Lingenfelter": "Corvette L28",
    "Lister": "Storm",
    "Lotus": "Elise",
    "Lucid": "Air",
    "Maserati": "Quattroporte",
    "Mazda": "MX-5 Miata",
    "Mega": "Track",
    "Mercedes-Benz": "S-Class",
    "Mercury": "Cougar",
    "Mini": "Cooper",
    "Mitsubishi": "Lancer Evolution",
    "Morgan": "Aero 8",
    "NIO": "ET7",
    "Nissan": "GT-R",
    "Opel": "Astra",
    "Pagani": "Huayra",
    "Peugeot": "308",
    "Pininfarina": "Battista",
    "Polestar": "2",
    "Porsche": "911",
    "Proton": "Saga",
    "Qvale": "Mangusta",
    "Renault": "Clio",
    "Rinspeed": "sQuba",
    "Rivian": "R1T",
    "Rolls-Royce": "Phantom",
    "Saleen": "S7",
    "SEAT": "Leon",
    "Shelby": "Cobra",
    "Smart": "Fortwo",
    "SsangYong": "Rexton",
    "Subaru": "Impreza WRX",
    "Suzuki": "Swift",
    "Škoda": "Octavia",
    "Tata": "Nexon",
    "Tesla": "Model S",
    "Tofas": "Sahin",
    "Toyota": "Supra",
    "TVR": "Griffith",
    "UAZ": "Hunter",
    "Volkswagen": "Golf",
    "Volvo": "XC90",
    "XPeng": "P7",
    "ZAZ": "Tavria",
    "Zenvo": "TSR-S",
    "Xiaomi": "MS11",
}


def generate_questions(qty: int = 1, num_of_choices: int = 4) -> tuple[str, str, str]:
    questions = []
    for car_brand in sample(list(cars.keys()), qty):
        right_answer = cars[car_brand]
        wrong_answers = list(cars.values())
        wrong_answers.remove(right_answer)
        answers_picked = sample(wrong_answers, num_of_choices - 1)
        answers_picked.append(right_answer)
        shuffle(answers_picked)
        questions.append((car_brand, right_answer, answers_picked))
    return questions


def get_num_of_questions(max: int) -> int:
    while True:
        try:
            num_of_questions = int(input("Hány kérdést szeretnél? "))
            if num_of_questions > max:
                print(f"Maximum {max} kérdést választhatsz!")
                continue
            else:
                return num_of_questions
        except ValueError:
            print("Egész számot adj meg!")


def get_num_of_choices(min: int, max: int) -> int:
    while True:
        try:
            num_of_choices = int(
                input(f"Hány választási lehetőséget szeretnél [{min}-{max}]? ")
            )
            if (min <= num_of_choices <= max) and (num_of_choices % 2 == 0):
                return num_of_choices
            else:
                print(
                    f"A választási lehetőségek száma {min} és {max} közötti páros szám lehet!"
                )
                continue
        except ValueError:
            print("Egész számot adj meg!")


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


def check_answer(your_answer, right_answer):
    if your_answer == right_answer:
        return True, f"\033[32mA válasz helyes!\033[0m\n", 5
    else:
        return (
            False,
            f"\033[31mA válasz helytelen, a helyes válasz {right_answer} lett volna.\033[0m\n",
            0,
        )


def main() -> None:
    points = 0
    num_of_questions = get_num_of_questions(len(cars))
    num_of_choices = get_num_of_choices(2, 8)
    questions = generate_questions(num_of_questions, num_of_choices)
    # timer indítása
    for question in questions:
        answer, right_answer = ask_question(question)
        points += check_answer(answer, right_answer)[2]
    # timer vége + kalkuláció
    # időeredmény kiírása mm:ss formátumban
    print(f"Eredményed: {100 * points/5 / num_of_questions:.1f}%" + "\n")


if __name__ == "__main__":
    main()
