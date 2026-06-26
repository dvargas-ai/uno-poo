"""Logica central del juego UNO: turnos, reglas y efectos de las cartas."""

from uno.modelos.baraja import Baraja
from uno.modelos.carta import Carta
from uno.modelos.jugador import Jugador
from uno.persistencia.almacenamiento import borrar_partida, guardar_partida


class JuegoUNO:
    """Controla una partida entre el jugador humano y la maquina."""

    def __init__(self):
        self.baraja = Baraja()
        self.jugador1 = Jugador("Jugador 1")
        self.jugador2 = Jugador("Maquina")
        self.carta_en_mesa: Carta | None = None
        self.color_actual: str = ""
        self.saltar_j1 = False
        self.saltar_j2 = False
        self.cartas_jugadas: list[Carta] = []

        self._repartir_cartas()
        self._inicializar_mesa()

    def _repartir_cartas(self):
        """Reparte 7 cartas a cada jugador."""
        for _ in range(7):
            self.jugador1.agregar_carta(self.baraja.robar())
            self.jugador2.agregar_carta(self.baraja.robar())

    def _inicializar_mesa(self):
        """Coloca la primera carta en la mesa (debe ser numerica)."""
        while True:
            carta = self.baraja.robar()
            if carta and carta.es_numero():
                self.carta_en_mesa = carta
                self.color_actual = carta.color
                self.cartas_jugadas.append(carta)
                break

    def _tiene_jugada(self, jugador: Jugador) -> bool:
        """True si el jugador tiene al menos una carta valida para jugar."""
        for carta in jugador.mano:
            if self._es_jugada_valida(carta):
                return True
        return False

    def jugar(self):
        """Bucle principal de la partida hasta que alguien se quede sin cartas."""
        terminado = False

        while not terminado:
            self._mostrar_estado()

            # Turno del jugador humano
            if self.saltar_j1:
                print("Jugador 1 pierde turno.")
                self.saltar_j1 = False
            else:
                terminado = self._turno_humano(self.jugador1)
                guardar_partida(self)
                if terminado:
                    break

            if self.jugador1.tamano_mano() == 0 or self.jugador2.tamano_mano() == 0:
                break

            print("\n--- TURNO MAQUINA ---\n")

            # Turno de la maquina
            if self.saltar_j2:
                print("La maquina pierde turno.")
                self.saltar_j2 = False
            else:
                terminado = self._turno_maquina(self.jugador2)
                guardar_partida(self)
                if terminado:
                    break

            print("\n-----------------------------\n")

        self._fin_juego()

    def _mostrar_estado(self):
        """Imprime el estado actual de la mesa y las manos."""
        print(f"\nCarta en mesa: {self.carta_en_mesa} | Color actual: {self.color_actual}")
        print("Cartas jugadas:", " ".join(str(c) for c in self.cartas_jugadas))

        print()
        self.jugador1.mostrar_mano()
        print()
        print("Mano de la maquina:")
        for c in self.jugador2.mano:
            print(c, end="  ")
        print()

        print(f"\nCartas en mazo: {self.baraja.tamano()}\n")

    def _es_jugada_valida(self, carta: Carta) -> bool:
        """Aplica las reglas de UNO para validar si una carta puede jugarse."""
        cima_es_comodin = self.carta_en_mesa.es_comodin()

        if cima_es_comodin and carta.es_comodin():
            return False

        if carta.es_numero():
            return carta.color == self.color_actual or carta.valor == self.carta_en_mesa.valor
        else:
            if carta.color != "N":
                return carta.color == self.color_actual and not cima_es_comodin
            else:
                return not cima_es_comodin

    def _turno_humano(self, jugador: Jugador) -> bool:
        """Gestiona el turno del humano. Devuelve True si gano."""
        if not self._tiene_jugada(jugador):
            print("No tienes carta valida. Robas y pierdes turno.")
            jugador.agregar_carta(self.baraja.robar())
            return False

        while True:
            try:
                i = int(input("Indice de carta a jugar: "))
                carta = jugador.mano[i]
                if not self._es_jugada_valida(carta):
                    print("Carta invalida.")
                    continue
                break
            except (ValueError, IndexError):
                print("Entrada invalida.")

        jugada = jugador.jugar_carta(i)
        print(f"Juegas {jugada}")
        self._procesar_jugada(jugada, jugador)

        if jugador.tamano_mano() == 1:
            print("UNO!!!")

        return jugador.tamano_mano() == 0

    def _turno_maquina(self, jugador: Jugador) -> bool:
        """Gestiona el turno de la maquina. Devuelve True si gano."""
        for i, c in enumerate(jugador.mano):
            if self._es_jugada_valida(c):
                jugada = jugador.jugar_carta(i)
                print(f"Maquina juega {jugada}")
                self._procesar_jugada(jugada, jugador)
                break
        else:
            print("Maquina roba carta.")
            jugador.agregar_carta(self.baraja.robar())

        if jugador.tamano_mano() == 1:
            print("UNO!!! (Maquina)")

        return jugador.tamano_mano() == 0

    def _procesar_jugada(self, carta: Carta, jugador: Jugador):
        """Coloca la carta en la mesa, ajusta el color y aplica su efecto."""
        self.carta_en_mesa = carta
        self.cartas_jugadas.append(carta)

        if carta.color == "N":
            if jugador == self.jugador1:
                self.color_actual = self._pedir_color()
            else:
                self.color_actual = self._color_maquina()
                print("Maquina cambia color a:", self.color_actual)
        else:
            self.color_actual = carta.color

        self._aplicar_efecto(carta, jugador)

    def _aplicar_efecto(self, carta: Carta, jugador: Jugador):
        """Aplica el efecto de saltar/robar segun el valor de la carta."""
        otro = self.jugador2 if jugador == self.jugador1 else self.jugador1
        v = carta.valor

        if v in ["^", "&"]:
            if jugador == self.jugador1:
                self.saltar_j2 = True
            else:
                self.saltar_j1 = True

        elif v == "+2":
            print("El otro jugador roba 2.")
            for _ in range(2):
                otro.agregar_carta(self.baraja.robar())
            if jugador == self.jugador1:
                self.saltar_j2 = True
            else:
                self.saltar_j1 = True

        elif v == "+4":
            print("El otro jugador roba 4.")
            for _ in range(4):
                otro.agregar_carta(self.baraja.robar())
            if jugador == self.jugador1:
                self.saltar_j2 = True
            else:
                self.saltar_j1 = True

    def _pedir_color(self) -> str:
        """Pide al humano elegir un color tras jugar un comodin."""
        while True:
            c = input("Elige color (R,A,V,Z): ").upper()
            if c in ["R", "A", "V", "Z"]:
                return c

    def _color_maquina(self) -> str:
        """La maquina elige el color del que mas cartas tiene."""
        conteo = {"R": 0, "A": 0, "V": 0, "Z": 0}
        for c in self.jugador2.mano:
            if c.color in conteo:
                conteo[c.color] += 1
        return max(conteo, key=conteo.get)

    def _fin_juego(self):
        """Anuncia al ganador y borra la partida guardada."""
        print("\n=== FIN DEL JUEGO ===")
        if self.jugador1.tamano_mano() == 0:
            print("GANASTE")
        else:
            print("GANA LA MAQUINA")

        borrar_partida()
