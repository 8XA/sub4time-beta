#!/bin/env python

import os, curses, sys, string
from modulos.subs import subs
from modulos.descarga import descarga
from modulos.update import update


rabs = "/data/data/com.termux/files/home/"
rabs = ""
rvids = "storage/shared/time4popcorn/downloads"


#FUNCIÓN SALIR
def salir():
    #FINALIZAR SCRIPT
    i = input("\nPresiona enter para salir.")
    sys.exit()


#DETERMINANDO EL NÚMERO DE CARACTERES POR LÍNEA
def numcols():
    screen = curses.initscr() 
    num_cols = screen.getmaxyx()[1]
    curses.endwin()
    os.system("stty sane && clear")
    return num_cols
num_cols = numcols()


#ACTUALIZAR
if update(num_cols) == 1:
    print("Debes reiniciar Termux.")
    salir()


#VIDEOS CON SU RUTA
extensiones = ["mp4", "mkv", "avi"]
videos = []
for ext in extensiones:
    videos += os.popen("find '" + rvids + "' -iname *." + ext).read().split("\n")
videos = [video for video in videos if video != ""]


#NOMBRES DE LOS VIDEOS
nombres = [ruta[len(ruta) - [ruta[x] for x in range(len(ruta)-1,-1,-1)].index("/"):] for ruta in videos]


#IMPRIME PANTALLA
print(num_cols*"=")
titulo = "SUB4TIME Beta v1.2.0"
titulo2 = "Lista"
print(((num_cols-len(titulo))//2)*" " + titulo)
print(num_cols*"=")
print(((num_cols-len(titulo2))//2)*" " + titulo2)


#IMPRIME NOMBRES DE VIDEOS
for x in range(len(nombres)):
    print(num_cols*"-")
    print(str(x) + ": " + nombres[x])


#SELECCIONA NOMBRE DE VIDEO
print(num_cols*"=")
iv = int(input("Número de video: "))


#LISTA DE PALABRAS PARA BÚSQUEDA
buscar = [palabra for palabra in " ".join(nombres[iv].split(".")).split(" ") if (palabra != " " and palabra.lower() not in extensiones)]


#BÚSQUEDA
busqueda_correcta = ""
while busqueda_correcta.lower() != "s":
    os.system("clear")
    print(num_cols*"=")
    titulo = "LISTA DE PALABRAS"
    print(((num_cols-len(titulo))//2)*" " + titulo + "\n" + num_cols*"-")
    for x in range(len(buscar)):
        print(str(x) + ": " + buscar[x])

    #PALABRAS DE BUSQUEDA
    buscar_depurado = []
    print(num_cols*"=")
    print(((num_cols-9)//2)*" " + "OPCIONES:")
    print(num_cols*"-")
    print("""- URL subdivx
- Palabras de la lista: num0,num1,num2
- Lista completa: t
- Ingresa una búsqueda personalizada""")
    print(num_cols*"=")
    ibusq = input(": ")

    urlDirecta = False

    #SI ES UNA URL
    if ibusq[:24].lower() == "https://www.subdivx.com/":
        urlDirecta = True
    elif ibusq.lower() == "t":
        buscar_depurado = buscar
    #SI ES UNA SELECCION DE PALABRAS
    elif "".join([x for x in ibusq if x in "0123456789,"]) == ibusq:
        buscar_depurado = [buscar[int(indice)] for indice in [x for x in ibusq.split(",") if x != ""]]
    #SI ES BÚSQUEDA PERSONALIZADA
    else:
        buscar_depurado = ibusq.split(" ")

    #CORROBORANDO INFORMACIÓN DE BÚSQUEDA
    if urlDirecta == False:
        print("\nTus palabras de búsqueda son:")
        print(buscar_depurado)
    else:
        print("\nSeleccionaste descargar el subtítulo:\n----------\n" + ibusq + "\n----------\nY asignarlo a la película: " + nombres[iv])
    busqueda_correcta = input(num_cols*"=" +"Es esto correcto (s|n)? ")


#SALTA EL ALGORITMO DE BÚSQUEDA SI SE INGRESÓ DIRECTAMENTE EL LINK DE DESCARGA DEL SUBTÍTULO   
if urlDirecta == False:
    #LISTA CON RESULTADO DE BUSQUEDA
    listaSubs = subs(buscar_depurado)


    #DEFINE LOS SUBTITULOS A MOSTRAR
    isub, subxpag, filtro = "", 50, []
    #letras = string.ascii_letters + "ÁÉÍÓÚÑáéíóúñ"
    while "".join([x for x in isub if x in "0123456789"]) != isub or isub == "":
        if filtro == []:
            listaSubsF = [x for x in listaSubs]
        else:
            listaSubsF = [listaSubs[x] for x in range(len(listaSubs)) if (len(filtro) == len([palabra for palabra in filtro if (palabra.lower() in ((listaSubs[x][0]+listaSubs[x][1]).lower()))]))]

        pagina = 1
        num_subs = len(listaSubsF)

        #IMPRIME, NUMERA SUBTÍTULOS Y NAVEGA A TRAVÉS DE ELLOS
        for x in range(len(listaSubsF)):
            print("\n" + num_cols*"=")
            print(str(x) + ": " + listaSubsF[x][0])
            print(num_cols*"-")
            print(listaSubsF[x][1])
        print(num_cols*"=")

        print("\n\n" + num_cols*"=")
        print(((num_cols-9)//2)*" " + "OPCIONES:")
        print(num_cols*"-")
        print("Navegar entre páginas")
        print("Anterior  <- : a")
        print("Siguiente -> : Enter")
        print("Filtrar subs : palabra1,palabra2")
        print("Quitar filtro: f")
        print("Descargar sub: num")
        print("Salir        : q")
        print(num_cols*"=")
        isub = input(": ")
        if isub.lower() == "a":
            pagina -= 1
        elif isub.lower() == "":
            pagina +=1
        elif isub.lower() == "f":
            filtro = []
        elif isub.lower() == "q":
            salir()
        else:
            filtro = [x for x in isub.split(",") if x != ""]


    #SELECCIÓN DE SUBTÍTULO
    link = descarga(listaSubsF[int(isub)][2])
else:
    link = descarga(ibusq)


#DESCARGA SUBTITULO ELEGIDO
os.system("rm -r tmp")
os.system("mkdir tmp")
os.system("wget -P tmp " + link[0] + ".rar")
os.system("wget -P tmp " + link[0] + ".zip")


#DESCOMPRIME SUBTITULO
if os.popen("find tmp -iname *.zip").read() != "":
    os.system("unzip -o " + "tmp/" + link[1] + ".zip -d tmp/")
if os.popen("find tmp -iname *.rar").read() != "":
    os.system("unrar x -y " + "tmp/" + link[1] + ".rar tmp/")


#SUBTITULOS DESCOMPRIMIDOS COMO LISTA DE RUTAS
if os.popen("find tmp -iname *.srt").read() != "":
    ruta_sub = [ruta for ruta in os.popen("find tmp -iname *.srt").read().split("\n") if ruta != ""]
    ext = ".srt"
elif os.popen("find tmp -iname *.ssa").read() != "":
    ruta_sub = [ruta for ruta in os.popen("find tmp -iname *.ssa").read().split("\n") if ruta != ""]
    ext = ".ssa"


#IMPRESIÓN DE OPCIONES DE UN SOLO COMPRIMIDO
os.system("clear")
if len(ruta_sub) > 1:
    for x in range(len(ruta_sub)):
        print(str(x) + ": " + ruta_sub[x][4:])
    nsub = int(input("Ingresa el número de subtítulo: "))
else:
    nsub = 0


#MUEVE EL SUBTITULO ELEGIDO A LA CARPETA DE LA PELICULA
os.system('mv "' + ruta_sub[nsub] + '" "' + videos[iv][:-4] + ext + '"')
os.system("rm -r tmp")

print("listo")
