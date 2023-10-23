Este es un juego simple desarrollado en Python utilizando la biblioteca Pygame. El juego incluye un jugador que puede moverse en 2D y saltar en un entorno con bloques. El jugador puede colisionar con los bloques y la cámara sigue al jugador horizontalmente.
Requisitos

    Python 3.x
    Pygame (asegúrate de tenerlo instalado)

Cómo Ejecutar el Juego

    Asegúrate de que tienes Python 3.x instalado en tu sistema.
    Instala Pygame si aún no lo tienes instalado con el siguiente comando:

    bash

pip install pygame

Descarga el código fuente del juego y guarda tus texturas de jugador y bloques en el mismo directorio.
Ejecuta el juego con el siguiente comando:

bash

    python main.py

Estructura del Código

El código está dividido en tres clases principales: Player, Block, y Game. A continuación, se explica cada una de estas clases:
Player

La clase Player representa al personaje controlado por el jugador. Aquí están sus principales atributos y métodos:

    __init__(self, x, y, width, height, texture=None, color=None): Constructor que inicializa al jugador con su posición, dimensiones, velocidad, textura (opcional) y color (opcional).

    move(self, keys): Permite que el jugador se mueva a la izquierda o a la derecha según las teclas presionadas (A y D).

    jump(self, keys): Permite que el jugador salte cuando se presiona la tecla Espacio.

    update(self, screen_height): Actualiza la posición del jugador y verifica si ha alcanzado el suelo.

    check_collision(self, platforms): Detecta colisiones entre el jugador y los bloques.

    debug_info(self): Método de depuración (actualmente desactivado) para mostrar información relevante en la consola.

Block

La clase Block representa los bloques del mapa. Sus atributos y métodos son:

    __init__(self, x, y, block_type, texture=None, color=None): Constructor que inicializa un bloque con su posición, tipo de bloque, textura (opcional) y color (opcional).

Game

La clase Game es la clase principal que controla el juego. Aquí están sus principales atributos y métodos:

    __init__(self): Constructor que inicializa el juego y crea la ventana de Pygame.

    initialize_textures(self): Inicializa las texturas de los bloques.

    load_map(self, filename): Carga un mapa desde un archivo de texto, donde cada número representa un tipo de bloque en una cuadrícula.

    run(self): Inicia la ejecución del juego y contiene el bucle principal.

    draw_map(self): Dibuja los bloques del mapa en la pantalla.

    draw_entities(self): Dibuja al jugador en la pantalla.

Personalización

Puedes personalizar el juego agregando tus propias texturas, ajustando las dimensiones de los bloques, cambiando el mapa y mucho más. Asegúrate de explorar y experimentar con el código para crear tu propio juego personalizado.
Créditos

Este juego fue desarrollado utilizando Pygame. Agradecemos a la comunidad de Pygame por proporcionar esta biblioteca de juegos en Python.
Licencia

Este juego se distribuye bajo la Licencia MIT, lo que significa que puedes usar, modificar y distribuir el código como desees. No hay garantías ni responsabilidades.
