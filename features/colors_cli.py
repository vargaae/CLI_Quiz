from enum import Enum

class C(Enum):
    F = "\033[38;5;" #foreground color modifier
    B = "\033[48;5;" #background color modifier
    END = "\033[00m" #closing tag of the modifier
    BLACK = "232m"
    BLUE = "20m"
    CYAN = "45m"
    GREEN = "34m"
    GREY = "243m"
    LIGHTBLUE ="75m"
    ORANGE = "214m"
    PINK = "207m"
    PURPLE = "93m"
    RED = "160m"
    WHITE = "231m"
    YELLOW = "226m"

def col(input: str, color: C, bgcolor: C = None) -> str:
    return str(C.F.value)+str(color.value)+(str(C.B.value)+str(bgcolor.value) if bgcolor else "")+input+str(C.END.value)

def ok(input: str) -> str:
    return str(C.F.value)+str(C.GREEN.value)+input+str(C.END.value)

def info(input: str) -> str:
    return str(C.F.value)+str(C.LIGHTBLUE.value)+input+str(C.END.value)

def highlight(input: str) -> str:
    return str(C.F.value)+str(C.YELLOW.value)+input+str(C.END.value)

def warning(input: str) -> str:
    return str(C.F.value)+str(C.ORANGE.value)+input+str(C.END.value)

def error(input: str) -> str:
    return str(C.F.value)+str(C.RED.value)+input+str(C.END.value)