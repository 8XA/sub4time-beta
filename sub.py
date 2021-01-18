#!/bin/env python

import os
from modulos.subs import subs
from modulos.descarga import descarga
from modulos.update import update


rabs = "/data/data/com.termux/files/home/"
rabs = ""
rvids = "storage/shared/time4popcorn/downloads"


#DETERMINANDO EL NÚMERO DE CARACTERES POR LÍNEA
def numcols():
    screen = curses.initscr() 
    num_cols = screen.getmaxyx()[1]
    curses.endwin()
    os.system("stty sane && clear")
    return num_cols
num_cols = numcols()

#Actualizar
update(num_cols)

#Videos con su ruta
extensiones = ["mp4", "mkv", "avi"]
videos = []
for ext in extensiones:
    videos += os.popen("find '" + rvids + "' -iname *." + ext).read().split("\n")
videos = [video for video in videos if video != ""]


#Nombre de los videos
nombres = [ruta[len(ruta) - [ruta[x] for x in range(len(ruta)-1,-1,-1)].index("/"):] for ruta in videos]


#Imprime nombres de videos
for x in range(len(nombres)):
    print(str(x) + ": " + nombres[x])


#Selecciona nombre de video
iv = int(input("Video: "))


#Lista de palabras para búsqueda
buscar = list(nombres[iv])
while "." in buscar:
    buscar[buscar.index(".")] = " "
buscar = "".join(buscar).split(" ")
buscar = [palabra for palabra in buscar if (palabra != " " and palabra.lower() not in extensiones)]


#Búsqueda
for x in range(len(buscar)):
    print(str(x) + ": " + buscar[x])
buscar_depurado = []
ipalabra = ""
while ipalabra.lower() != "s":
    ipalabra = input("Palabra:")

    if ipalabra.lower() == "t":
        buscar_depurado = buscar
        break
    elif ipalabra.lower() == "s":
        break

    buscar_depurado.append(buscar[int(ipalabra)])
    print(buscar_depurado)

listaSubs = subs(buscar_depurado,1)

#Selecciona subtítulo
#os.system("clear")
for x in range(len(listaSubs)):
    print(x, listaSubs[x][0])
    print(listaSubs[x][1])
    print(num_cols*"-")
isub = int(input("Elige uno: "))


#Descarga subtitulo elegido
link = descarga(listaSubs[isub][2])
os.system("rm -r tmp")
os.system("mkdir tmp && wget -P tmp " + link[0] + ".rar")
os.system("wget -P tmp " + link[0] + ".zip")

os.system("unzip -o " + "tmp/" + link[1] + ".zip -d tmp/")
os.system("unrar x -y " + "tmp/" + link[1] + ".rar tmp/")


ruta_sub = "'" + os.popen("find tmp -iname *.srt").read()[:-1] + "'"
os.system("mv '" + ruta_sub + "' '" + videos[iv][:-4] + ".srt'")
#os.system("rm -r tmp")

print("listo")
