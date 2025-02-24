import json

#  Adatok beolvasása JSON fájlból
def load_questions(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
        # with open("./quizes/" + question_type.name + ".json", "r", encoding="utf-8") as file:
            try:
                raw_data = json.load(file)
            except json.JSONDecodeError as e:
                print("\tHIBA! Érvénytelen JSON formátum!")
                # print(c.error("\tHIBA! Érvénytelen JSON formátum!"))
                exit()
        return raw_data
    except FileNotFoundError:
        print("\tHIBA! A kérdésfájl nem található!")
        # print(c.error("\tHIBA! A kérdésfájl nem található!"))
        exit()

# def load_questions(filename):
#     try:
#         with open(filename, "r", encoding="utf-8") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         print("Error: Questions file not found!")
#         return []
#     except json.JSONDecodeError:
#         print("Error: Invalid JSON format!")
#         return []
