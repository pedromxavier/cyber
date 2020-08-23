from basic import f, n, reproduzir

partitura = [ ## beethoven
    "B4", "B4", "C4", "D4", "D4", "C4", "B4", "A4", "G3", "G3", "A4", "B4", "B4", "A4", "A4", "~",
    "B4", "B4", "C4", "D4", "D4", "C4", "B4", "A4", "G3", "G3", "A4", "B4", "A4", "G3", "G3"
]


##exit(0)

from advanced import compilar, síntese, reproduzir, união

import sys

violino_A = [1.00, 0.59, 0.26, 0.38, 0.78, 0.40, 0.42, 0.10]
violino_D = [1.00, 0.36, 0.30, 0.26, 0.28, 0.08, 0.28, 0.31]

if len(sys.argv) > 1:
    áudios = []
    for nome_do_arquivo in sys.argv[1:]:
        with open(nome_do_arquivo, 'r') as arquivo:
            print(f"Lendo `{nome_do_arquivo}`")
            partitura = arquivo.read()
            instruções = compilar(partitura)
            áudio = síntese(instruções, timbre=violino_D, tom='G', tempo=140)
            print("Síntese [OK]")
        áudios.append(áudio)
    reproduzir(união(*áudios))
    exit(0)
else:
    print("Erro: Nenhum arquivo especificado")
    exit(1)