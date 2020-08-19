"""
            /* Ode à Alegria */
B4 B4 C4 D4 D4 C4 B4 A4 G3 G3 A4 B4 B4 A4 A4
B4 B4 C4 D4 D4 C4 B4 A4 G3 G3 A4 B4 A4 G3 G3
"""
import numpy as np
import wave

def compilar(partitura: str, **opções) -> np.ndarray:
    """ compilar(P: str, **opções) -> np.ndarray.
    """

    if 'timbre' in opções:
        timbre = list(opções['timbre'])
    else:
        timbre = [1.0]

    símbolos = análise_léxica(partitura)

    notas = análise_sintática(símbolos)

    return notas

def análise_léxica(partitura: str) -> list:
    """
    """

    ## Estados
    estados = {
        # -1 -> aguardando qualquer símbolo (descarte)
        -1 : {
            None : 0
        },

        # 0 -> aguardando nota, pausa, repetição, espaço ou comentário (estado base)
        0 : {
            'ABCDEFG' : 1, ## nota
            '$' : 3, ## pausa
            ':' : 7, ## fim de repetição
            '|' : 6, ## início de repetição
            ' \n' : 0, ## espaço (descarte)
            '/': 8, ##comentário
        },
        # 1 -> aguardando acidente ou oitava (recebeu nota)
        1 : {
            'b#' : 2,
            '0123456789' : 3, 
        },
        # 2 -> aguardando oitava (recebeu nota e acidente)
        2 : {
            '0123456789' : 3, 
        },

        # 3 -> aguardando início do indicador de duração ou espaço (`[`, recebeu oitava)
        3 : {
            '[' : 4,
            ' \n' : 0,
        },
        # 4 -> aguardando conteúdo do indicador de duração (recebeu `[`)
        4 : {
            '0123456789' : 5,
        },
        # 5 -> aguardando conteúdo do indicador de duração ou fim (`]`, recebeu `0-9`)
        5 : {
            '0123456789' : 5,
            ']' : 0,
        },

        # 6 -> aguardando início da repetição (`|:`)
        6 : {
            ':' : 0,
        },
        # 7 -> aguardando fim de repetição (`:|`)
        7 : {
            '|' : 0,
        },

        # 8 -> aguardando início do comentário (`/*`)
        8 : {
            '*' : 9,
        },
        # 9 -> aguardando conteúdo do comentário
        9 : {
            '*' : 10,
            None : 9,
        },
        # 10 -> aguardando fim do comentário (`*/`, recebeu `*`)
        10 : {
            '/' : 0
        }
    
    }

    e = 0 ## estado atual

    ## Tamanho da partitura
    n = len(partitura)

    i = 0 ## índice atual

    s = '' ## símbolo atual

    símbolos = []

    while i < n:

        c = partitura[i] ## caracter atual

        for regra in estados[e]:
            if c in regra or regra is None:
                f = estados[e][regra]

                if f >= 0:
                    símbolos.append(s + c)
                
                e = f 
                break
            else:
                continue
        else:
            break

        i += 1

    else:
        return símbolos

    raise SyntaxError(f'Erro de sintaxe no token {i}')

def análise_sintática(símbolos: list) -> list:
    """
    """

    return []


def gravar(M: np.ndarray, **opções):
    ...


if __name__ == '__main__':
    notas = compilar(__doc__)
    print(notas)