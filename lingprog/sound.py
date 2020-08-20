import time

try:
    ## Disponível para windows
    import winsound
    def som(frequência: float, duração: float):
        """ frequência (Hz)
            duração (s)
        """
        if frequência is None:
            time.sleep(duração)
            return
        winsound.Beep(int(frequência), int(duração * 1000))

    raise ImportError

except ImportError:
    try:
        import numpy as np
    except ImportError:
        print('''
        $ pip3 install numpy
        ''')
    try:
        import simpleaudio as sa
    except ImportError:
        print('''
        $ apt-get install -y python3-dev libasound2-dev
        $ pip3 install simpleaudio
        ''')
        exit(1)

    def som(frequência: float, duração: float, volume: float = 1.0):
        """ frequência (Hz)
            duração (s)
        """
        if frequência is None:
            time.sleep(duração)
            return

        canais = 1 # mono
        taxa = 44100  # 44100 amostras por segundo
        bits = 16

        ## Garante que `volume` está entre 0 e 1
        volume = np.clip(volume, 0, 1)

        amplitude = ((1 << (bits - 1)) - 1)

        # Cria um vetor com de tamanho `duração * taxa`, entre 0 e a duração (segundos).
        t = np.linspace(0, duração, int(duração * taxa), False)

        # Gera a onda na frequência estabelecida, valores entre -1 e 1
        onda = np.sin(frequência * t * 2 * np.pi)

        # Amplifica o som valores entre `-amplitude` e `amplitude`
        áudio = onda * amplitude * volume

        # Converte para inteiro de 16 bits
        áudio = áudio.astype(np.int16)

        # Reproduz o som
        play = sa.play_buffer(áudio, canais, bits >> 3, taxa)

        # Espera o fim da reprodução
        play.wait_done()