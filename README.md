# Snake vs Snake - Juego Humano-Máquina

Implementación del juego estratégico "Snake vs Snake" usando técnicas de Inteligencia Artificial.

## Descripción del Juego

Snake vs Snake es una variante estratégica del clásico juego Snake donde dos jugadores compiten en un tablero 7x7. Cada jugador coloca fichas para formar serpientes que crecen desde la cabeza. El objetivo es bloquear al oponente impidiendo que pueda hacer más movimientos.

### Reglas
- Tablero de 7x7 casilleros con wraparound (bordes conectados)
- Las fichas solo se pueden colocar adyacentes (horizontal/vertical) a la cabeza de la serpiente
- No se puede chocar con serpientes propias o del oponente
- Gana quien logre que el oponente no tenga movimientos válidos

### Niveles de Dificultad
- **Principiante**: Selección aleatoria de movimientos
- **Normal**: Primero el mejor (función evaluadora)
- **Experto**: Algoritmo Minimax con anticipación de jugadas

## Configuración del Entorno

### Opción 1: Windows
```cmd
setup.bat
run.bat
```

### Opción 2: Linux/Mac
```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

### Opción 3: Manual (cualquier OS):**
```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -m venv .venv
.venv\Scripts\activate

# Instalar y ejecutar (todos los OS)
pip install -r requirements.txt
python main.py
```

## Arquitectura del Proyecto

### Estructura de Módulos

```
snake_vs_snake/
├── core/           # Motor del juego y lógica principal
│   ├── __init__.py   
│   ├── interfaces.py   # Definiciones compartidas
│   ├── estado.py       # Gestión de estados
│   └── juego.py        # Lógica principal
├── ai/             # Algoritmos de Inteligencia Artificial
│   ├── __init__.py 
│   ├── evaluador.py    # Función evaluadora f(e) = Ma(e) - Mr(e)
│   └── estrategias.py  # Estrategias (aleatorio, greedy, minimax)
├── gui/            # Interfaz gráfica con pygame
│   ├── __init__.py 
│   └── interfaz.py     # Pantallas y controles
├── tests/          # Para validar que cada módulo hace lo que debe.
│   ├── __init__.py 
│   ├── test_core.py    # pruebas del motor del juego
│   ├── test_ai.py      # pruebas de las estrategias y evaluador
│   └── test_gui.py     # pruebas de la interfaz pygame
├── main.py          # Punto de entrada
└── requirements.txt # requerimientos para python

```

### Algoritmos Implementados

**Función Evaluadora:**
```
f(e) = Ma(e) - Mr(e)
```
Donde Ma(e) es la cantidad de movimientos disponibles para Azul y Mr(e) para Rojo.

**Estrategias de IA:**
- **No Determinística**: Selección aleatoria
- **Primero el Mejor**: Maximiza función evaluadora
- **Minimax**: Anticipa respuestas del oponente (profundidad 3)

## Desarrollo y Contribución

### División de Tareas

**Módulo Core** (`core/`):
- Representación de estados
- Sistema de producción (reglas)
- Validación de movimientos
- Detección de condiciones de victoria

**Módulo IA** (`ai/`):
- Función evaluadora
- Implementación de estrategias
- Algoritmo minimax

**Módulo GUI** (`gui/` + `main.py`):
- Interfaz gráfica con pygame
- Pantallas de configuración
- Integración de componentes

### Workflow Git

```bash
# Branches de desarrollo
git checkout persona1-motor    # Para módulo core
git checkout persona2-ia       # Para módulo ai
git checkout persona3-gui      # Para módulo gui

# Integración
git checkout master
git merge persona1-motor
git merge persona2-ia  
git merge persona3-gui
```

### Testing

```bash
pytest tests/
pytest tests/ --cov=core --cov=ai --cov=gui
```

## Tecnologías Utilizadas

- **Python 3.11**: Lenguaje principal
- **Pygame**: Interfaz gráfica y manejo de eventos
- **NumPy**: Operaciones matemáticas (opcional)
- **Docker**: Containerización y portabilidad
- **Pytest**: Testing automatizado

## Interfaces Clave

### Motor de Juego
```python
class MotorJuego:
    def obtener_movimientos_validos(jugador: str) -> List[Posicion]
    def realizar_movimiento(posicion: Posicion) -> MovimientoResult
    def verificar_fin_juego() -> Tuple[bool, Optional[str]]
```

### Estrategias de IA
```python
class EstrategiaIA:
    def seleccionar_movimiento(motor_juego) -> Optional[Posicion]
```

### Gestión de Estados
```python
class EstadoJuego:
    tablero: List[List[str]]
    turno: str
    cabeza_azul: Optional[Posicion]
    cabeza_roja: Optional[Posicion]
```
