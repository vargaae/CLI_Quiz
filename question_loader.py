import json
import colors_cli as c

#  Adatok beolvasása JSON fájlból
def load_questions(question_type):
    try:
        with open("./quizes/" + question_type.name + ".json", "r", encoding="utf-8") as file:
<<<<<<< Tabnine <<<<<<<
def load_questions(question_type):#+
    """#+
    Load questions from a JSON file based on the question type.#+
#+
    This function attempts to open and read a JSON file containing quiz questions.#+
    The file name is determined by the question_type parameter.#+
#+
    Parameters:#+
    question_type (Enum): An enumeration value representing the type of questions to load.#+
                          The name attribute of this enum is used to construct the file name.#+
#+
    Returns:#+
    list: A list of dictionaries containing the loaded questions and their associated data.#+
#+
    Raises:#+
    SystemExit: If the file is not found or contains invalid JSON, the function prints an error message and exits the program.#+
    """#+
    try:#+
        with open("./quizes/" + question_type.name + ".json", "r", encoding="utf-8") as file:#+
            try:#+
                raw_data = json.load(file)#+
            except json.JSONDecodeError as e:#+
                print(c.error("\tHIBA! Érvénytelen JSON formátum!"))#+
                # return []#+
                exit()#+
        return raw_data#+
    except FileNotFoundError:#+
        print(c.error("\tHIBA! A kérdésfájl nem található!"))#+
        # return []#+
        exit()#+
>>>>>>> Tabnine >>>>>>># {"conversationId":"440c8c5b-a657-4945-802d-48e4e0db902d","source":"instruct"}
            try:
                raw_data = json.load(file)
            except json.JSONDecodeError as e:
                print(c.error("\tHIBA! Érvénytelen JSON formátum!"))
                # return []
                exit()
        return raw_data
    except FileNotFoundError:
        print(c.error("\tHIBA! A kérdésfájl nem található!"))
        # return []
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
