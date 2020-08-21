import numpy as np
import simpleaudio
import re

def lançar_erro(tipo:str, partitura: str, i: int):
    linhas = partitura.split('\n')

    total = 0

    for linha in linhas:
        ## linha encontrada
        if i < total + len(linha):
            break
        else:
            total = total + len(linha) + 1 ## quebra de linha inclusa
            continue
    
    print(linha)
    print(' ' * (i - total - 1) + '^')

def compilar(partitura: str, **opções) -> np.ndarray:
    """ compilar(P: str) -> np.ndarray.
    """
    símbolos = análise_léxica(partitura)

    instruções = análise_sintática(símbolos)

    return instruções

def análise_léxica(partitura: str) -> list:
    """
    """

    ## Estados
    estados = {
        # 0 -> aguardando nota, pausa, repetição, espaço, comentário ou final (estado base)
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
            ']' : 11,
        },

        # 6 -> aguardando início da repetição (`|:`)
        6 : {
            ':' : 11,
        },
        # 7 -> aguardando fim de repetição (`:|`)
        7 : {
            '|' : 11,
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
        },

        # 11 -> aguardando espaço ou quebra de linha
        11 : {
            ' \n' : 0 
        }
    }

    estados_finais = {0, 3, 11}

    ignorar = {0, 10}

    e = 0 ## estado atual

    ## Tamanho da partitura
    n = len(partitura)

    ## índice atual
    i = 0 

    ## símbolo atual
    s = '' 
    símbolos = []

    ## tipo do próximo símbolo
    tipos = {
        1 : 'NOTA',
        4 : 'NOTA[]',
        6 : 'LOOP',
        7 : 'LOOP',
    }

    tipo = None

    while i < n:
        c = partitura[i] ## caracter atual

        for regra in estados[e]:
            if (regra is None) or (c in regra):
                f = estados[e][regra]
                print(f'{e} -> {f} [{c!r}]')

                ## atualiza o tipo
                if f in tipos:
                    tipo = tipos[f]

                ## fim de um símbolo
                if f == 0:
                    if e not in ignorar:
                        símbolos.append((tipo, s, i))
                    tipo = None
                    s = ''
                else:
                    ## Adiciona caracter ao símbolo
                    s = s + c
                e = f 
                break
            else:
                continue
        else:
            break
        i += 1
    else:
        if e not in estados_finais:
            pass
        else:
            if e not in ignorar:
                símbolos.append((tipo, s, i))
            return símbolos

    erro = f'''
{partitura}
{(i-1) * ' '}^
'''
    raise SyntaxError(erro)

def análise_sintática(símbolos: list) -> list:
    """
    """
    ## Nível e pilha de recursão dos loops
    nível = 0
    pilha = []

    instruções = []

    n = len(instruções)

    j = 0
    while j < n:
        tipo = símbolos[j][0]
        símbolo = símbolos[j][1]
        i = símbolos[j][2]

        ## repetição
        if tipo == 'REPE':
            ## início
            if símbolo == '|:':
                nível += 1
                pilha.append(j)
                j += 1
                continue
            ## fim
            if símbolo == ":|":
                if len(pilha) == nível:
                    if nível == 0:
                        break
                    else:
                        j = pilha.pop() + 1
                        continue
                else:
                    nível -= 1
                    j += 1
                    continue
        
        elif tipo == "NOTA":
            nota = símbolo
            duração = 1
            instruções.append((nota, duração))

            j += 1
            continue

        elif tipo == "NOTA[]":
            regex = re.match(r'(.*)(\[[0-9]+\])', símbolo)

            nota = regex.group(1)
            duração = regex.group(2)

            instruções.append((nota, duração))
            j += 1
            continue

    else:
        if nível > 0:
            raise SyntaxError()
        else:
            return instruções

def gravar(M: np.ndarray, **opções):
    ...

def síntese(instruções: list, **opções):
    if 'timbre' in opções:
        timbre = list(opções['timbre'])
    else:
        timbre = [1.0]

    return timbre