# Actividad 3 - Juego de Pacman.
# Autores: Leonardo Delgado Rios-A00827915, Saul Jimenez Torres-A01283849.
# Aplicacion que desarrolla el minijuego de Pacman 
# Fecha de ultima modificacion: 10/29/2020.
# Se importan las librerias que se utilizaran para el correcto desarrollo de
# la aplicación.
from random import choice
from turtle import *
from freegames import floor, vector

# Aqui se definen lo valores default, es decir, el score y las posiciones de
# los fantasmas al igual que la del pacman
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -40)
coursetmp = [vector(10,0),vector(0,10),vector(0,-10),vector(-10,0)]
ghosts = [
    [vector(-180, 160), vector(10, 0)],
    [vector(-180, -180), vector(10, 0)],
    [vector(100, 60), vector(0, 10)],
    [vector(120, -180), vector(0, 10)],
]
# Esta matriz muestra en que posicion del tablero el jugador y los fantasmas
# se podran mover, o bien, el script ddel entorno onde se desarrolla el juego.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

# Funcion square, su objetivo es pintar un cuadrado que sirve como base para
# desarrollar el tablero del juego.
def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()
    
# Funcion offset, regresa el indice donde se podra mover pacman y los fantasmas
# es decir, establece los limites de movimiento dentro del tablero.
def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

# Funcion valid, funcion que determina si el movimiento es valido, es deir, si
# se encuentra dentro de los limites del juego establecido.
def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

# Funcion world, funcion que rellena los recuadros del tablero con su color
# correspondiente, esto depende del valor que se tenga en la matriz, ademas
# de agregar los puntos/comida para pacman.
def world():
    "Draw world using path."
    bgcolor('black')
    path.color('green')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')
                
# Funcion move, menciona los posibles escenarios del Pacman y los fantasmas,
# tambien se tienen cambios de direccion, el movimiento del Pacman y Fantasmas,
# junto con las opciones posibles a las que el fantasma se pueda mover.
def move():
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])
    i = 0

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')
    
    for point, course in ghosts:
        aux = choice(coursetmp)
        if valid(point + course):
            if valid(point + aux) and i%2==0 :
                course.x = aux.x
                course.y = aux.y
                i+=1
            point.move(course)
            i+=1
        else:
            course.x = aux.x
            course.y = aux.y
            
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)

# Funcion que cambia la direccion del Pacman a una direccion valida.
def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y
        
# Aqui se definen las caracterisiticas de la ventana donde se desarrolla
# el programa. Estos son el tamaño de ventana, el contador de puntaje junto
# con el color que tomara. Al presionar la tecla respectiva da una instruccion
# y se cambia la direccion del Pacman.
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()