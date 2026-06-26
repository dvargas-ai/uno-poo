"""Punto de entrada del juego UNO.

Ofrece continuar una partida guardada o iniciar una nueva.
"""

from uno.juego.juego_uno import JuegoUNO
from uno.persistencia.almacenamiento import cargar_partida, existe_partida


def main():
    if existe_partida():
        op = input("Hay partida guardada. Continuar? (S/N): ").strip().upper()
        if op == "S":
            juego = cargar_partida()
            if juego is not None:
                juego.jugar()
                return
            print("No se pudo cargar la partida. Se iniciara una nueva.")

    juego = JuegoUNO()
    juego.jugar()


if __name__ == "__main__":
    main()
