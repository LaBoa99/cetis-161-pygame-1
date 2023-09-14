import random
# Lista de palabras
words = ["gael", "rodriguez", "vega", "fresas", "manzanas"]
# Seleccionar una palabra al azar
palabraJuego = random.choice(words)
# Inicializar las variables
palabraJugador = ["_"] * len(palabraJuego)
oportunidades = 6
# Bucle principal del juego
while oportunidades > 0:
    # Mostrar el estado actual de la palabra
    print("Palabra a adivinar:", " ".join(palabraJugador), "vidas restantes: ", oportunidades)
    # Obtener la letra del jugador
    letraJugador = input("Ingresa una letra: ").lower()
    # Verificar si la letra está en la palabra objetivo
    if letraJugador in palabraJuego:
        for indice, letra in enumerate(palabraJuego):
            if letra == letraJugador:
                palabraJugador[indice] = letra
    else:
        oportunidades = oportunidades - 1
    # Verificar si el jugador ha adivinado la palabra
    if "".join(palabraJugador) == palabraJuego:
        print("¡Ganaste! La palabra era:", palabraJuego)
        break
# Si el jugador se queda sin intentos, mostrar un mensaje de derrota
if oportunidades <= 0:
    print("Perdiste. La palabra era:", palabraJuego)

print("¡Gracias por jugar!")