import numpy as np
import simpleaudio as sa
import re

from basic import NOTAS, ACIDENTES, A

TONS = {
    'C' : {},
    'G' : {'F' : '#'},
    'D' : {'C' : '#', 'F' : '#'}
    ## temos muitos outros!
}

def f(nota: str, tom: str='C') -> int:
    """
    """
    if len(nota) == 1 and nota == "~": ## pausa
        return None
    if len(nota) == 2: ## nota natural, sem acidentes
        letra = nota[0]
        oitava = int(nota[1])
        if letra in TONS[tom]:
            n = NOTAS[letra] + 12 * (oitava - 4) + ACIDENTES[TONS[tom][letra]]
        else:
            n = NOTAS[letra] + 12 * (oitava - 4) 
    elif len(nota) == 3: ## nota com acidente
        letra = nota[0]
        acidente = nota[1]
        oitava = int(nota[2])
        n = NOTAS[letra] + 12 * (oitava - 4) + ACIDENTES[acidente]
    else:
        raise ValueError

    return A * pow(2.0, n / 12.0)

def formatar_erro(tipo:str, partitura: str, i: int):
    """
    """
    ## sepração do código fonte por linhas
    linhas = partitura.split('\n')

    total = 0

    n = len(linhas)
    k = 0
    while k < n:
        linha = linhas[k]
        ## linha encontrada
        if i < (total + len(linha) + 1):  ## quebra de linha inclusa
            break
        else:
            total += len(linha) + 1 ## quebra de linha inclusa
            k += 1
            continue
    else:
        ## erro na ultima linha
        k -= 1

    return f"""{tipo}:
    {k:2d} {linhas[k-1] if k > 0 else ''}
--> {k+1:2d} {linhas[k]}
{((i - total) - 1 + 3 + 4) * ' '}^
"""

def compilar(partitura: str, **opções) -> list:
    """ compilar(partitura: str) -> np.ndarray.
    """
    símbolos = análise_léxica(partitura)
    print('Análise Léxica [OK]')
    instruções = análise_sintática(símbolos, partitura)
    print('Análise Sintática [OK]')
    instruções = análise_semântica(instruções, partitura)
    print('Análise Semântica [OK]')
    return instruções

def análise_léxica(partitura: str) -> list:
    """
    """

    ## Estados
    estados = {
        # 0 -> aguardando nota, pausa, repetição, espaço, comentário ou final (estado base)
        0 : {
            'ABCDEFG' : 1, ## nota
            '~' : 3, ## pausa
            ':' : 7, ## fim de repetição
            '|' : 6, ## início de repetição
            ' \n\t' : 0, ## espaço (descarte)
            '/': 8, ##comentário
            '$': 13 ## Clave (definição de tonalidade)
        },
        # 1 -> aguardando acidente ou oitava (recebeu nota)
        1 : {
            'b#%' : 2, ## acidente
            '0123456789' : 3, ## oitava
        },
        # 2 -> aguardando oitava (recebeu nota e acidente)
        2 : {
            '0123456789' : 3, ## oitava
        },

        # 3 -> aguardando início do indicador de duração, ponto de aumento ou espaço (`[`, recebeu oitava)
        3 : {
            '[' : 4,
            '.' : 11,
            ' \n\t' : 0,
        },
        # 4 -> aguardando conteúdo do indicador de duração (recebeu `[`)
        4 : {
            '0123456789' : 5,
        },
        # 5 -> aguardando conteúdo do indicador de duração ou fim (`]`, recebeu `0-9`)
        5 : {
            '0123456789' : 5,
            ']' : 12,
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

        # 11 -> aguardando espaço
        11 : {
            ' \n\t' : 0 
        },

        # 12 -> Aguardando ponto de aumento ou espaço
        12 : {
            '.' : 11,
            ' \n\t' : 0,
        },

        # 13 -> Aguardando tonalidade
        13 : {
            'ABCDEFG' : 11,
        }
    }

    estados_finais = {0, 3, 11, 12}

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
        3 : 'NOTA',
        4 : 'NOTA[]',
        6 : 'LOOP',
        7 : 'LOOP',
        13: 'TOM'
    }

    tipo = None

    while i < n:
        c = partitura[i] ## caracter atual

        for regra in estados[e]:
            if (regra is None) or (c in regra):
                f = estados[e][regra]
                ## print(f'{e} -> {f} [{c!r}]')

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

    mensagem_de_erro = formatar_erro('Símbolo Inválido', partitura, i)

    print(mensagem_de_erro)
    exit(1)

def análise_sintática(símbolos: list, partitura: str) -> list:
    """
    """
    ## Nível e pilha de recursão dos loops
    nível = 0
    pilha = []

    instruções = []

    n = len(símbolos)

    j = 0
    while j < n:
        tipo = símbolos[j][0]
        símbolo = símbolos[j][1]
        i = símbolos[j][2]

        ## print(f'[{tipo}] ({símbolo}) @ {j}')

        ## definição de tom
        if tipo == 'TOM':
            tom = símbolos[j][1]
            instruções.append(('TOM', tom))

        ## repetição
        if tipo == 'LOOP':
            ## início
            if símbolo == '|:':
                nível += 1
                pilha.append(j)
                j += 1
                continue
            ## fim
            if símbolo == ":|":
                if nível > len(pilha): ## terminando de repetir
                    nível -= 1
                    j += 1
                    continue
                elif nível == len(pilha): ## repetindo
                    if nível > 0:
                        j = pilha.pop() + 1
                        continue
                    else:
                        mensagem_de_erro = formatar_erro('Repetição Inconsistente', partitura, i)
                        break
        
        elif tipo == "NOTA":
            if símbolo[-1] == '.':
                nota = símbolo[:-1]
                ponto = True
            else:
                nota = símbolo
                ponto = False
            ## padrão
            figura = 4

            instruções.append(('NOTA', nota, figura, ponto, i))

            j += 1
            continue

        elif tipo == "NOTA[]":
            regex = re.match(r'(.*)\[([0-9]+)\](\.?)', símbolo)

            nota = regex.group(1)
            figura = int(regex.group(2))
            ponto = bool(regex.group(3))

            instruções.append(('NOTA', nota, figura, ponto, i))
            j += 1
            continue

    else:
        if nível != 0:
            mensagem_de_erro = formatar_erro('Repetição incompleta', partitura, i)
            pass
        else:
            return instruções
    
    print(mensagem_de_erro)
    exit(1)

def análise_semântica(instruções: list, partitura: str):
    novas_instruções = []

    n = len(instruções)
    j = 0
    while j < n:
        if instruções[j][0] == 'NOTA':
            nota = instruções[j][1]
            figura = instruções[j][2]
            ponto = instruções[j][3]
            i = instruções[j][4]

            if figura == 0: ## dividir por zero!
                break
            else:
                novas_instruções.append(('NOTA', nota, figura, ponto))
                j += 1

        elif instruções[j][0] == 'TOM':
            tom = instruções[j][1]
            novas_instruções.append(('TOM', tom))
            j += 1
    else:
        return novas_instruções

    mensagem_de_erro = formatar_erro('Duração Inválida:', partitura, i)

    print(mensagem_de_erro)
    exit(1)

def síntese(instruções: list, **opções) -> np.ndarray:
    if 'timbre' in opções:
        timbre = np.array(opções['timbre'], dtype=float)
    else:
        timbre = np.array([1.0], dtype=float)

    if 'tempo' in opções:
        tempo = int(opções['tempo'])
    else:
        tempo = 120

    ## amostras por segundo
    if 'taxa' in opções:
        taxa = int(opções['taxa'])
    else:
        taxa = 44_100

    if 'tom' in opções:
        tom = opções['tom']
    else:
        tom = 'C'

    if 'compasso' in opções:
        compasso = tuple(opções['compasso'])
    else:
        compasso = (4, 4)

    if 'bits' in opções:
        bits = int(opções['bits'])
    else:
        bits = 16

    if 'volume' in opções:
        volume = np.clip(opções['volume'], 0.0, 1.0)
    else:
        volume = 1.0

    amplitude = ((2 ** (bits - 1)) - 1)

    ## valores de timbre precisam estar entre 0.0 e 1.0
    timbre = np.power(10.0, timbre)

    ## normalizando o timbre, para que soma(timbre) = 1
    if np.sum(timbre) == 0.0:
        print('Timbre inválido')
        exit(1)
    else:
        timbre = timbre / np.sum(timbre)

    l = len(timbre)

    ## pares (frequência, duração)
    sons = []
    
    ## duração total da música (segundos)
    duração_total = 0.0

    n = len(instruções)
    i = 0
    while i < n:
        if instruções[i][0] == 'TOM':
            tom = instruções[i][1]

        nota = instruções[i][1]
        figura = instruções[i][2]
        ponto = instruções[i][3] ## True ou False

        duração = (compasso[1] / figura) * (60.0 /tempo) ## 4 / 4

        ## Aplica o ponto de aumento
        if ponto: duração += (duração / 2.0)

        frequência = f(nota, tom=tom)

        sons.append((frequência, duração))

        duração_total += duração

        i += 1

    ## linha do tempo
    m = int(duração_total * taxa)

    t = np.linspace(0, duração_total, m, False)

    onda = np.zeros(m, dtype=float)

    n = len(sons)
    i = 0
    j = 0
    while i < n:
        som = sons[i]

        frequência = som[0]
        duração = som[1]

        d = int(duração * taxa)

        if frequência is None:
            j += d
            i += 1
            continue

        k = 0
        while k < l:
            # intensidade do harmônico
            harmônico = timbre[k] ## [1.0, 1.0]

            # Gera a onda na frequência estabelecida (valores entre -1 e 1)
            # sen(f * t * 2 * pi)
            onda[j:j+d] += harmônico * np.sin((k + 1) * frequência * t[j:j+d] * 2 * np.pi)

            k += 1

        onda[j:j+d] *= bow(min(d, len(onda) - j), 15.0)

        j += d
        i += 1
    else:
        # Amplifica o som (valores entre `-amplitude` e `amplitude`)
        áudio = onda * amplitude * volume

        ## Converte para inteiro de 16 bits
        áudio = áudio.astype(np.int16)

        return áudio

def bow(d: int, a = 10.0):
    x = np.linspace(-1, 1, d)
    return (1.0 / (1.0 + np.exp(-a * (x - 0.5)))) - (1.0 / (1.0 + np.exp(-a * (x + 0.5))))

def reproduzir(áudio: np.ndarray, **opções):
    if 'bits' in opções:
        bits = int(opções['bits'])
    else:
        bits = 16

    if 'taxa' in opções:
        taxa = int(opções['taxa'])
    else:
        taxa = 44_100 ## amostras por segundo

    if 'canais' in opções:
        canais = int(opções['canais'])
    else:
        canais = 1

    # Reproduz o som
    play = sa.play_buffer(áudio, canais, bits // 8, taxa)

    # Espera o fim da reprodução
    play.wait_done()

def união(*áudios: list, **opções) -> np.ndarray:
    """
    """
    assert áudios
    print(áudios)
    n = len(áudios)
    m = max([len(áudio) for áudio in áudios])

    áudio_final = np.zeros(m, dtype=float)

    for áudio in áudios:
        áudio_final[:len(áudio)] += (1.0 / n) * áudio

    return áudio_final.astype(np.int16)
