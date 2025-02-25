from os import system, name as OSname
from .ascii import ascii_art
import features.colors_cli as c

#  Splash screen
def show_splash_screen():
    system("cls" if OSname == "nt" else "clear")
    print(c.col(ascii_art, c.C.PURPLE))