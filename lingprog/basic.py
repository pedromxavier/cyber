from sound import som

## Frquência de referência para o lá central (A4)
A = 440.0

def f(n: int) -> float:
    """ n (distância da nota para o lá central A4)
    """
    if n is None:
        return None
    else:
        return A * pow(2.0, n / 12.0)

NOTAS = {
    'A' : 0,
    'B' : 2,
    'C' : 3,
    'D' : 5,
    'E' : 7,
    'F' : 8,
    'G' : 10,
}

ACIDENTES = {
    'b' : -1,
    '#' : 1,
}

def n(nota: str) -> int:
    """
    """
    if len(nota) == 1 and nota == "$":
        return None
    if len(nota) == 2:
        letra = nota[0]
        oitava = int(nota[1])
        n = NOTAS[letra] + 12 * (oitava - 4)
    elif len(nota) == 3:
        letra = nota[0]
        acidente = nota[1]
        oitava = int(nota[2])
        n = NOTAS[letra] + 12 * (oitava - 4) + ACIDENTES[acidente]
    else:
        raise ValueError

    return n

partitura = [
    "B4", "B4", "C4", "D4", "D4", "C4", "B4", "A4", "G3", "G3", "A4", "B4", "B4", "A4", "A4", "$",
    "B4", "B4", "C4", "D4", "D4", "C4", "B4", "A4", "G3", "G3", "A4", "B4", "A4", "G3", "G3"
]

def reproduzir(partitura: list, tempo: int):
    """ partitura
        tempo (bpm)
    """

    duração = 60 / tempo

    for nota in partitura:
        frequência = f(n(nota))
        som(frequência, duração)