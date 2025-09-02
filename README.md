# 🎲 Juego de Dudo en Cacho

**Creado por:** Benjamín Henríquez y Jesús Guevara

Implementación digital del tradicional juego chileno **Dudo** (también conocido como Cacho), desarrollado en Python con arquitectura orientada a objetos y cobertura completa de tests.

## 📋 Descripción del Juego

El **Dudo** es un juego de dados donde los jugadores hacen apuestas sobre la cantidad de dados que muestran una determinada cara (llamadas "pintas") entre todos los jugadores. El objetivo es engañar a los oponentes o detectar cuándo mienten.

### Reglas Básicas
- Cada jugador tiene un cacho (vaso) con 5 dados inicialmente
- Los jugadores hacen apuestas sobre cuántos dados de cierta pinta hay en total
- Se puede **dudar** (desafiar la apuesta) o **calzar** (apostar que es exacta)
- Los **Ases** actúan como comodines (excepto en rondas especiales)
- El jugador que pierde una apuesta pierde un dado
- Gana el último jugador que conserve dados

## 🏗️ Arquitectura del Proyecto

```
src/juego/
├── Dado.py              # Clase básica del dado (1-6)
├── Cacho.py             # Conjunto de 5 dados por jugador
├── Jugador.py           # Representación de cada jugador
├── contador_pintas.py   # Lógica para contar apariciones de pintas
├── validador_apuesta.py # Validación de reglas de apuestas
├── arbitro_ronda.py     # Árbitro que decide ganadores/perdedores
└── gestor_partida.py    # Coordinador general del juego

tests/
├── test_dado.py
├── test_cacho.py
├── test_jugador.py
├── test_contador_pintas.py
├── test_validador_apuesta.py
├── test_arbitro_ronda.py
└── test_gestor_partida.py
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Xaiwu/Tarea-Dudo.git
   cd Tarea-Dudo
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Ejecutar Tests

### Ejecutar todos los tests
```bash
python -m pytest
```

### Ejecutar tests con cobertura
```bash
python -m pytest --cov=src
```

### Ejecutar tests específicos
```bash
# Tests de una clase específica
python -m pytest tests/test_arbitro_ronda.py -v

# Tests de un método específico
python -m pytest tests/test_contador_pintas.py::TestContadorPintas::test_contar_pintas_basico -v

# Tests por palabra clave
python -m pytest -k "calzar" -v
```

### Ver cobertura detallada
```bash
python -m pytest --cov=src --cov-report=html
```
Esto genera un reporte HTML en `htmlcov/index.html`

## 🎯 Componentes Principales

### 🎲 Dado
- Valores del 1 al 6 con denominaciones tradicionales:
  - 1: **As** (comodín)
  - 2: **Tonto**
  - 3: **Tren**
  - 4: **Cuadra**
  - 5: **Quina**
  - 6: **Sexto**

### 🏺 Cacho
- Contiene hasta 5 dados por jugador
- Maneja visibilidad (oculto/revelado)
- Permite ganar/perder dados durante el juego

### 🎯 Contador de Pintas
- Cuenta apariciones de pintas específicas
- Maneja Ases como comodines (modo normal)
- Soporte para modo especial (Ases no son comodines)

### ✅ Validador de Apuestas
- Valida reglas de incremento de apuestas
- Maneja reglas especiales de Ases:
  - **A Ases**: cantidad ÷ 2 (+ 1 si es par, redondear arriba si impar)
  - **De Ases**: cantidad × 2 + 1 (mínimo)
- Valida primera apuesta (no se puede empezar con Ases excepto con 1 dado)

### ⚖️ Árbitro de Ronda
- Decide resultado de **dudas**:
  - Si hay suficientes pintas → pierde quien dudó
  - Si no hay suficientes → pierde quien apostó
- Decide resultado de **calzar**:
  - Si es exacto → gana un dado
  - Si no es exacto → pierde un dado
- Valida condiciones para calzar:
  - Con 1 dado: siempre puede calzar
  - Con mitad+ dados en juego: puede calzar

### 🎮 Gestor de Partida
- Coordina turnos entre jugadores
- Determina iniciador (mayor dado)
- Maneja reglas especiales (ronda de 1 dado)
- Controla fin del juego

## 📊 Cobertura de Tests

El proyecto cuenta con **100% de cobertura** en todas las clases principales:

- ✅ **Dado**: Tests de generación y validación
- ✅ **Cacho**: Tests de manejo de dados y visibilidad  
- ✅ **Contador de Pintas**: Tests de conteo con/sin comodines
- ✅ **Validador de Apuestas**: Tests de todas las reglas complejas
- ✅ **Árbitro de Ronda**: Tests de decisiones y aplicación de consecuencias
- ✅ **Gestor de Partida**: Tests de coordinación y turnos

## 🔧 Uso Programático

### Ejemplo básico de uso:
```python
from src.juego.gestor_partida import GestorPartida
from src.juego.arbitro_ronda import ArbitroRonda

# Crear partida de 3 jugadores
partida = GestorPartida(3)

# Determinar quién inicia
iniciador = partida.determinar_iniciador()

# Crear árbitro para decisiones
arbitro = ArbitroRonda()

# Ejemplo de duda
apuesta = (3, 4)  # "3 cuadras"
todos_los_dados = []  # Recopilar dados de todos los jugadores
resultado = arbitro.determinar_resultado_duda(
    apuesta, todos_los_dados, 
    jugador_apostador, jugador_que_duda
)
```