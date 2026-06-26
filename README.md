# 🎴 Juego UNO en Python (POO)

Implementación por consola del clásico juego **UNO**, desarrollada como proyecto
del **2do Parcial de Programación Orientada a Objetos**. El código fue migrado
desde Java a Python y se le añadió la funcionalidad de **guardar y continuar
partida** mediante serialización.

## 👥 Integrantes

- Aaron Lopez
- Damián Vargas
- Francisco Quezada

**Materia:** Programación Orientada a Objetos

## 🚀 Ejecución

Requiere **Python 3.10 o superior** (no usa dependencias externas, solo la
librería estándar).

```bash
python run.py
```

## 🎮 Cómo jugar

- Juegas contra la **máquina**. Cada jugador empieza con **7 cartas**.
- En tu turno se muestra tu mano numerada; escribe el **índice** de la carta
  que quieres jugar.
- Una carta es válida si **coincide en color o en número/símbolo** con la carta
  de la mesa.
- Si no tienes jugada válida, robas una carta y pierdes el turno.
- Gana quien se quede **sin cartas**.

### Cartas

| Símbolo | Significado            |
|---------|------------------------|
| `0`-`9` | Carta numérica         |
| `^`     | Saltar turno           |
| `&`     | Reversa                |
| `%`     | Cambio de color        |
| `+2`    | El rival roba 2        |
| `+4`    | El rival roba 4        |

Colores: **R** (rojo), **A** (amarillo), **V** (verde), **Z** (azul), **N** (negro/comodín).

## 💾 Guardar partida

La partida se guarda **automáticamente** después de cada turno en un archivo
`partida.dat` usando el módulo `pickle`. Al iniciar el juego, si existe una
partida guardada, se ofrece continuarla. Al terminar la partida, el archivo se
elimina automáticamente.

## 📁 Estructura del proyecto

```
.
├── run.py                  # Punto de entrada (python run.py)
├── README.md
├── .gitignore
├── docs/
│   └── ESTRUCTURA.md       # Explicación del diseño orientado a objetos
└── src/
    └── uno/
        ├── main.py         # Menú inicial: nueva partida o continuar
        ├── modelos/        # Entidades del dominio
        │   ├── carta.py
        │   ├── baraja.py
        │   └── jugador.py
        ├── juego/          # Lógica y reglas del juego
        │   └── juego_uno.py
        └── persistencia/   # Guardado y carga de la partida
            └── almacenamiento.py
```

## 🧩 Conceptos de POO aplicados

- **Encapsulamiento:** cada clase administra su propio estado (la mano del
  `Jugador`, las cartas de la `Baraja`).
- **Abstracción:** la `Carta`, la `Baraja` y el `Jugador` modelan entidades
  reales del juego con métodos claros.
- **Composición:** `JuegoUNO` está compuesto por una `Baraja` y dos `Jugador`.
- **Separación de responsabilidades:** modelos, lógica del juego y persistencia
  están en paquetes distintos.

## 📊 Diagrama de clases (UML)

```mermaid
classDiagram
    class Carta {
        +str color
        +str valor
        +es_numero() bool
        +es_comodin() bool
        +__str__() str
    }

    class Baraja {
        -list~Carta~ cartas
        +robar() Carta
        +esta_vacia() bool
        +tamano() int
        +mostrar()
    }

    class Jugador {
        +str nombre
        -list~Carta~ mano
        +agregar_carta(carta)
        +jugar_carta(indice) Carta
        +tamano_mano() int
        +mostrar_mano()
    }

    class JuegoUNO {
        -Baraja baraja
        -Jugador jugador1
        -Jugador jugador2
        -Carta carta_en_mesa
        -str color_actual
        +jugar()
        -_repartir_cartas()
        -_es_jugada_valida(carta) bool
        -_turno_humano(jugador) bool
        -_turno_maquina(jugador) bool
        -_aplicar_efecto(carta, jugador)
    }

    JuegoUNO "1" *-- "1" Baraja : compone
    JuegoUNO "1" *-- "2" Jugador : compone
    Baraja "1" o-- "*" Carta : contiene
    Jugador "1" o-- "*" Carta : mano
```

> GitHub renderiza este diagrama automáticamente al ver el README.

## 🔄 De Java a Python

Este proyecto se migró desde una implementación original en **Java**. Estas son
las principales diferencias que aplicamos durante la conversión:

| Concepto                | Java                                    | Python (este proyecto)                  |
|-------------------------|-----------------------------------------|-----------------------------------------|
| Definición de clase     | `public class Carta { ... }`            | `class Carta:`                          |
| Atributos + getters/setters | Campos privados + métodos `getX()`  | Atributos directos / `@dataclass`       |
| Constructor             | `public Carta(String color) { ... }`    | `def __init__(self, color):`            |
| Tipado                  | Estático y obligatorio (`String color`) | Dinámico, con *type hints* opcionales   |
| Listas                  | `ArrayList<Carta>`                      | `list[Carta]`                           |
| Referencia a instancia  | `this`                                  | `self` (explícito en cada método)       |
| Serialización (guardar) | `Serializable` + `ObjectOutputStream`   | módulo `pickle`                         |
| Punto de entrada        | `public static void main(String[])`     | `if __name__ == "__main__":`            |
| Impresión               | `System.out.println(...)`               | `print(...)`                            |

**La funcionalidad añadida** respecto al original fue **guardar y continuar
partida** (`src/uno/persistencia/almacenamiento.py`), que en Java se haría con
`Serializable` y en Python se resolvió con `pickle`.
