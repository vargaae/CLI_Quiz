import random
import time

import categories as cat
from question_loader import load_questions
from question_generator import generate_questions

class ClassicQuizGame():
    def __init__(self, quiz_type):
        quiz_type = cat.Cat.python_learning
        self.questions = load_questions(quiz_type)
        self.score = 0
        self.lifelines = {"50-50": 1, "hint": 1}
        self.start_time = None

    def shuffle_answers(self, question):
        options = question["options"][:]
        correct_answer = question["answer"]
        random.shuffle(options)
        return options, options.index(correct_answer)

    def use_lifeline(self, question):
        print("\nLifelines: 1) 50-50  2) Hint")
        choice = input("Choose lifeline (1/2) or press enter to skip: ")
        
        if choice == "1" and self.lifelines["50-50"] > 0:
            self.lifelines["50-50"] -= 1
            correct_answer = question["answer"]
            options = question["options"][:]
            incorrect = [opt for opt in options if opt != correct_answer]
            options = [correct_answer] + random.sample(incorrect, 1)
            random.shuffle(options)
            return options, options.index(correct_answer)
        
        elif choice == "2" and self.lifelines["hint"] > 0:
            self.lifelines["hint"] -= 1
            print("Hint:", question["hint"])
        
        return self.shuffle_answers(question)

    def play(self, num_of_choices):
        num_of_questions:int = 15
        if not self.questions:
            print("No questions available. Exiting game.")
            return

        print("Kezdődjön a Python Kvíz!")

        self.start_time = time.time()
        random.shuffle(self.questions)
        
    # TODO: ITT kezdődik a módosítás: Ha Python vizsga kérdéseket választja a User, akkor a classic_quiz\ ClassicQuizGame-ból kell hívni a play() metódust, tehát egy külön ágra fut, aminek a felületét az alaphoz kell igazítani
        # def generate_questions(question_type, qty: int, num_of_choices: int, questions_data: dict) -> tuple[str, str, list[str]]:
    # if (question_type == cat.Cat.python_learning):
    #     game = ClassicQuizGame()
    #     game.play()
    # else:
    #     questions = []
    #     for question_subject in sample(list(questions_data.keys()), qty):
    #         right_answer = questions_data[question_subject]
    #         wrong_answers = list(questions_data.values())
    #         wrong_answers.remove(right_answer)
    #         answers_picked = sample(wrong_answers, num_of_choices - 1)
    #         answers_picked.append(right_answer)
    #         shuffle(answers_picked)
    #         questions.append((question_subject, right_answer, answers_picked))
    #     return questions

# KÉRDÉS GENERÁLÁS
                                                    # TODO: KÉRDÉSEK SZÁMA
        for i, question in enumerate(self.questions[:num_of_questions], start=1):
        # for i, question in enumerate(self.questions[:10], start=1):
            print(f"\nQuestion {i}: {question['question']}")
            options, correct_index = self.shuffle_answers(question)
            
            for idx, option in enumerate(options, start=1):
                print(f"{chr(96 + idx)}) {option}")
# KÉRDÉS GENERÁLÁS

            options, correct_index = self.use_lifeline(question)
            
            answer = input("Válaszod (a/b/c/d): ").lower()
            if 0 <= ord(answer) - 97 < len(options) and options[ord(answer) - 97] == question["answer"]:
                print("Helyes!")
                self.score += 10 if i % 5 != 0 else 20  # TODO: Risk factor: every 5th question is worth double
            else:
                print(f"Hibás! A helyes válasz: {question['answer']}")

        self.show_results()

    def show_results(self):
        total_time = round(time.time() - self.start_time, 2)
        print(f"\nJáték vége! A végső eredményed: {self.score}")
        print(f"Felhasznált idő: {total_time} másodperc")
        self.save_high_score(total_time)

    def save_high_score(self, total_time):
        try:
            with open("highscores.txt", "r", encoding="utf-8") as file:
                highscores = [eval(line.strip()) for line in file]
        except FileNotFoundError:
            highscores = []
        
        highscores.append({"score": self.score, "time": total_time})
        highscores.sort(key=lambda x: (-x["score"], x["time"]))
        highscores = highscores[:5]
        
        with open("highscores.txt", "w", encoding="utf-8") as file:
            for entry in highscores:
                file.write(str(entry) + "\n")
        
        print("\nHigh Scores:")
        for idx, entry in enumerate(highscores, start=1):
            print(f"{idx}. Score: {entry['score']}, Time: {entry['time']}s")

if __name__ == "__main__":
    game = ClassicQuizGame()
    game.play()
