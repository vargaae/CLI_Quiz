import random
import time
import json

class QuizGame:
    def __init__(self, filename="questions.json"):
        self.filename = filename
        self.questions = self.load_questions()
        self.score = 0
        self.lifelines = {"50-50": 1, "hint": 1}
        self.start_time = None

    def load_questions(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: Questions file not found!")
            return []
        except json.JSONDecodeError:
            print("Error: Invalid JSON format!")
            return []

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

    def play(self):
        if not self.questions:
            print("No questions available. Exiting game.")
            return

        print("Welcome to the Python Quiz!")
        self.start_time = time.time()
        random.shuffle(self.questions)

        for i, question in enumerate(self.questions[:10], start=1):
            print(f"\nQuestion {i}: {question['question']}")
            options, correct_index = self.shuffle_answers(question)
            
            for idx, option in enumerate(options, start=1):
                print(f"{chr(96 + idx)}) {option}")

            options, correct_index = self.use_lifeline(question)
            
            answer = input("Your answer (a/b/c/d): ").lower()
            if 0 <= ord(answer) - 97 < len(options) and options[ord(answer) - 97] == question["answer"]:
                print("Correct!")
                self.score += 10 if i % 5 != 0 else 20  # Risk factor: every 5th question is worth double
            else:
                print(f"Wrong! Correct answer was: {question['answer']}")

        self.show_results()

    def show_results(self):
        total_time = round(time.time() - self.start_time, 2)
        print(f"\nGame Over! Your final score: {self.score}")
        print(f"Time taken: {total_time} seconds")
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
    game = QuizGame()
    game.play()
