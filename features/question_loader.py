import json
import features.colors_cli as c

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