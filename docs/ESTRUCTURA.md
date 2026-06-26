# Diseño orientado a objetos

Este documento describe las clases del proyecto y cómo se relacionan.

## Clases

### `Carta` (`src/uno/modelos/carta.py`)
Modela una carta con `color` y `valor`. Implementada como `dataclass`.
- `es_numero()` / `es_comodin()`: clasifican la carta.

### `Baraja` (`src/uno/modelos/baraja.py`)
Mazo de cartas. Se crea con todas las cartas y se mezcla automáticamente.
- `robar()`: entrega la carta superior.
- `esta_vacia()`, `tamano()`.

### `Jugador` (`src/uno/modelos/jugador.py`)
Representa a un jugador (humano o máquina) y su mano.
- `agregar_carta()`, `jugar_carta()`, `mostrar_mano()`.

### `JuegoUNO` (`src/uno/juego/juego_uno.py`)
Controla la partida completa: reparto, turnos, validación de jugadas, efectos
de las cartas (saltar, +2, +4, cambio de color) y fin del juego.

### Persistencia (`src/uno/persistencia/almacenamiento.py`)
Funciones para guardar/cargar el estado del juego con `pickle`:
`guardar_partida`, `cargar_partida`, `existe_partida`, `borrar_partida`.

## Relaciones (composición)

```
JuegoUNO
 ├── Baraja            (1)
 │     └── Carta       (*)
 └── Jugador           (2)
       └── Carta       (mano, *)
```

`JuegoUNO` se apoya en el módulo de persistencia para guardar su estado tras
cada turno.

## Flujo de una partida

1. `main.py` revisa si hay partida guardada y ofrece continuarla.
2. `JuegoUNO` reparte cartas y coloca la carta inicial en la mesa.
3. Se alternan los turnos (humano ↔ máquina) hasta que alguien se queda sin
   cartas. Tras cada turno se guarda la partida.
4. Al finalizar se anuncia el ganador y se borra el archivo de guardado.
