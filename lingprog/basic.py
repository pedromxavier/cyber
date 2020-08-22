from sound import som

## Frquência de referência para o lá central (A4)
A = 440.0 #Hz

## bpm (batidas por minuto)
TEMPO = 120 

NOTAS = {
    'A' : 0, # lá
    'B' : 2, # si
    'C' : 3, # dó
    'D' : 5, # ré
    'E' : 7, # mi
    'F' : 8, # fá 
    'G' : 10, # sol
}

ACIDENTES = {
    'b' : -1, # bemol
    '#' : 1, # sustenido
    '%' : 0, # bequadro
}

def f(n: int) -> float:
    """ n (distância da nota para o lá central A4)
    """
    if n is None:
        return None
    else:
        return A * pow(2.0, n / 12.0)

def n(nota: str) -> int:
    """
    """
    if len(nota) == 1 and nota == "~":
        return None

    if len(nota) == 2:
        letra = nota[0]
        oitava = int(nota[1])
        return NOTAS[letra] + 12 * (oitava - 4)

    elif len(nota) == 3:
        letra = nota[0]
        acidente = nota[1]
        oitava = int(nota[2])
        return NOTAS[letra] + 12 * (oitava - 4) + ACIDENTES[acidente]

    else:
        raise ValueError
    
def reproduzir(partitura: list, tempo: int):
    """ partitura
        tempo (bpm)
    """

    duração = (60 / tempo)

    for nota in partitura:
        frequência = f(n(nota))
        som(frequência, duração)