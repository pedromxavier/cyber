from basic import f, n, reproduzir

partitura = [ ## beethoven
    "B4", "B4", "C4", "D4", "D4", "C4", "B4", "A4", "G3", "G3", "A4", "B4", "B4", "A4", "A4", "~",
    "B4", "B4", "C4", "D4", "D4", "C4", "B4", "A4", "G3", "G3", "A4", "B4", "A4", "G3", "G3"
]


##exit(0)

from advanced import compilar, síntese, reproduzir, união

import sys

timbre = [1.0, 0.75, 0.5, 0.25]

if len(sys.argv) > 1:
    for nome_do_arquivo in sys.argv[1:]:
        with open(nome_do_arquivo, 'r') as arquivo:
            partitura = arquivo.read()
            instruções = compilar(partitura)
            print(instruções)
            áudio = síntese(instruções, timbre=timbre, tom='D')
            reproduzir(áudio)
    exit(0)
else:
    print("Erro: Nenhum arquivo especificado")
    exit(1)