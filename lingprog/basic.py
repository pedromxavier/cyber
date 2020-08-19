from winsound import Beep

A = 440.0

def f(n: int) -> float:
    return A * pow(2.0, n / 12.0)