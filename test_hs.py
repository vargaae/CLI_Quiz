import json

def load_highscores() -> list:
    try:
        with open("highscores.json", encoding="utf-8") as file:
            try:
                highscores = json.load(file)
                return highscores["highscores"]
            except json.JSONDecodeError:
                print("Nem megfelelő JSON formátum!")
                return None
    except FileNotFoundError:
        print("Nincs meg a highscore file!")
        return None

highscores = load_highscores()

print(highscores["songs_hu"])