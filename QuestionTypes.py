import datetime
import re
import ABCD_question
from unidecode import unidecode

points_for_perfect = 5

class Question():
    def __init__(self, tmp):
        self.qtype = tmp["qtype"]
        self.question = tmp["question"]
        self.answer = tmp["answer"]
        self.regex = rf"{tmp['regex']}"

    def ask_question(self) -> list[str, str]:
        while True:
            try:
                your_answer = input(self.question)
                return your_answer
            except Exception as e:
                print(e)
                continue

    def check_answer(self, your_answer):
        if bool(re.search(self.regex, simplify_string(your_answer))):
            return True, "\033[32mHelyes a válasz!\033[0m\n", points_for_perfect
        else:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna!\033[0m\n", 0


class ABCDQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)

    def ask_question(self) -> str:
        your_answer, answer = ABCD_question.ask_question(ABCD_question.generate_questions())
        self.answer = answer
        return your_answer
    
    def check_answer(self, your_answer: str):
        return ABCD_question.check_answer(your_answer, self.answer)


class BoolQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)
    
    def ask_question(self) -> str:
        while True:
            try:
                your_answer = input(f"Igaz vagy hamis: {self.question}")
                if your_answer.strip().lower() not in ["igaz","igen","i","hamis","nem","h","n"]:
                    raise ValueError(f"\033[33m[I]gaz-[h]amis, [i]gen-[n]em válaszok elfogadhatóak!\033[0m")
                return your_answer
            except Exception as e:
                print(e)
                continue

    def check_answer(self, your_answer: str) -> list[bool, str, int]:
        if bool(re.search(self.regex, simplify_string(your_answer))):
            return True, "\033[32mHelyes a válasz!\033[0m\n", points_for_perfect
        else:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna!\033[0m\n", 0


class DateQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)

    def ask_question(self) -> str:
        while True:
            try:
                your_answer = input(f"{self.question} (Formátum: ÉÉÉÉ-HH-NN) ")
                if not bool(re.search(self.regex, simplify_string(your_answer))):
                    raise ValueError(f"\033[33mHelytelen dátumformátum! ÉÉÉÉ-HH-NN\033[0m")
                return your_answer
            except Exception as e:
                print(e)
                continue

    def check_answer(self, your_answer: str) -> list[bool, str, int]:
        try:
            deviation_day = (datetime.date.fromisoformat(your_answer) - datetime.date.fromisoformat(self.answer)).days
        except ValueError as e:
            print("Hiba:", e)
        if deviation_day == 0:
            return True, "\033[32mHelyes a válasz!\033[0m\n", points_for_perfect
        else:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna! Eltérés: {deviation_day} nap.\033[0m\n", 0


class IntegerQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)
        self.answer = int(tmp["answer"])

    def ask_question(self) -> str:
        while True:
            try:
                your_answer = input(self.question)
                if not your_answer.isdigit():
                    raise ValueError("\033[33mCsak számot írj be!\033[0m")
                return your_answer
            except Exception as e:
                print(e)
                continue

    def check_answer(self, your_answer: str) -> list[bool, str, int]:
        your_answer_asnum = int(your_answer)
        if  your_answer_asnum == self.answer:
            return True, "\033[32mHelyes a válasz!\033[0m\n", points_for_perfect
        else:
            text_answer = ""
            deviation_percent = 100 * your_answer_asnum / self.answer - 100
            text_answer =f"\033[31mNEM! A helyes válasz {self.answer} lett volna! Az eltérésed: {round(deviation_percent,1)}%\033[0m\n"
            match deviation_percent:
                case deviation_percent if abs(deviation_percent) < 5:
                    text_answer += f"így is kaptál {points_for_perfect-1} pontot!\n"
                    return False, text_answer, points_for_perfect-1
                case deviation_percent if abs(deviation_percent) < 10:
                    text_answer += f"így is kaptál {points_for_perfect-2} pontot!\n"
                    return False, text_answer, points_for_perfect-2
                case _:
                    pass
            return False, text_answer, 0


class FloatQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)
        self.answer = float(tmp["answer"])

    def ask_question(self) -> str:
        while True:
            try:
                your_answer = input(self.question)
                if not your_answer.replace(".", "", 1).isdigit():
                    raise ValueError("\033[33mCsak szabványos lebegőpontos számot írj be! Pl.: 2.46\033[0m")
                return your_answer
            except Exception as e:
                print(e)
                continue

    def check_answer(self, your_answer: str) -> list[bool, str, int]:
        your_answer_asnum = float(your_answer)
        tolerance = your_answer_asnum / self.answer
        if 0.99 < tolerance < 1.01:
            return True, f"\033[32mHelyes a válasz!\033[0m Az eltérésed nincs 1%-nyi\nMegkaptad a maximális {points_for_perfect} pontot!\n", points_for_perfect
        elif 0.95 < tolerance < 1.05:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna! Az eltérésed: max.5%\nígy is kaptál {points_for_perfect-1} pontot!\033[0m\n", points_for_perfect-1
        elif 0.90 < tolerance < 1.10:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna! Az eltérésed: max.10%\nígy is kaptál {points_for_perfect-2} pontot!\033[0m\n", points_for_perfect-2
        else:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna!\033[0m\n", 0


class SetQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)
        self.answer = self.answer.split()
        self.regex = self.regex.split("|")
        #létrehozok egy {regex:kiírandó_szöveg} megfeleltető szótárat
        self.correspondes = {reg:ans for reg, ans in zip(self.regex, self.answer)}
        self.answer = set(self.answer)

    def ask_question(self) -> set:
        try:
            your_answer = input(self.question)
            if "," in your_answer:
                return set(your_answer.split(","))
            else:
                return set(your_answer.split())
        except Exception as e:
            print("Hiba:", e)

    def check_answer(self, your_answer: set) -> list[bool, str, int]:
        simplified_user_values = {simplify_string(word) for word in your_answer}
        #A felhasználótól érkező inputot megfeleltetem a formázott kiírandó szöveggel és halmazba mentem
        good_guesses = {correct for your_answer in simplified_user_values for pattern, correct in self.correspondes.items() if re.fullmatch(pattern, your_answer)}
        total_good_answers = len(self.answer)
        total_good_guesses = len(good_guesses)
        missing: str = ", ".join(w for w in (self.answer - good_guesses))
        if total_good_answers == 0:
            return False, f"\033[31mSajnos nem találtál el egyet sem. A helyes válaszok: {missing}!\033[0m\n", 0
        elif total_good_answers == total_good_guesses:
            return True, "\033[32mHelyes a válasz! Mind eltaláltad!\033[0m\n", points_for_perfect
        elif total_good_answers - total_good_guesses < 2:
            return False, f"\033[32mSzinte mind megvan, de ez kimaradt: {missing}\033[0m\nKaptál {points_for_perfect-1} pontot", points_for_perfect-1
        elif total_good_answers - total_good_guesses < 4:
            return False, f"\033[31mNem rossz, de ezek kimaradtak: {missing}\033[0m\nKaptál {points_for_perfect-2} pontot", points_for_perfect-2
        else:
            return False, f"\033[31mEz azért kevés lesz! Kimaradtak: {missing}\033[0m\n", 0


class TextQuestion(Question):
    def __init__(self, tmp):
        super().__init__(tmp)

    def check_answer(self, your_answer: str) -> list[bool, str, int]:
        if bool(re.search(self.regex, simplify_string(your_answer))):
            return True, "\033[32mHelyes a válasz!\033[0m\n", points_for_perfect
        else:
            return False, f"\033[31mNEM! A helyes válasz {self.answer} lett volna!\033[0m\n", 0


def simplify_string(text: str) -> str:
    return unidecode(text.strip().lower())