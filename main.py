from modules import run_game
from colors_cli import highlight

def main() -> None:
    while True:
        run_game()
        while True:
            again = input(highlight("\tSzeretnél újra játszani? I/N "))
            if again.lower() not in "in": continue
            else: break
        if again.lower() == "i":
            continue
        else:
            print(highlight("\tV I S Z L Á T !"))
            break

if __name__ == "__main__":
    main()