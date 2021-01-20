#!/bin/env python

import os, curses 
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


#Imprime pantalla
print(num_cols*"=")
titulo = "SUB4TIME Alpha v1.1.1"
print(((num_cols-len(titulo))//2)*" " + titulo)
print(num_cols*"=")


#Imprime nombres de videos
for x in range(len(nombres)):
    print(str(x) + ": " + nombres[x])
    print(num_cols*"-")

#Selecciona nombre de video
print(num_cols*"=")
iv = int(input("Número de video: "))


#Lista de palabras para búsqueda
buscar = [palabra for palabra in " ".join(nombres[iv].split(".")).split(" ") if (palabra != " " and palabra.lower() not in extensiones)]


#Búsqueda
busqueda_correcta = ""
while busqueda_correcta.lower() != "s":
    os.system("clear")
    print(num_cols*"=")
    titulo = "LISTA DE PALABRAS"
    print(((num_cols-len(titulo))//2)*" " + titulo + "\n" + num_cols*"-")
    for x in range(len(buscar)):
        print(str(x) + ": " + buscar[x])

    #Palabras de busqueda
    buscar_depurado = []
    print(num_cols*"=")
    print("Opciones:\n" + num_cols*"-")
    print("""- URL subdivx
- Palabras de la lista: num0,num1,num2
- Lista completa: t
- Ingresa una búsqueda personalizada""")
    print(num_cols*"=")
    ibusq = input(": ")

    #Si es una URL
    if ibusq[:24].lower() == "https://www.subdivx.com/":
        i = input("URL B)")
        pass
    elif ibusq.lower() == "t":
        buscar_depurado = buscar
    #Si es una seleccion de palabras
    elif "".join([x for x in ibusq if x in "0123456789,"]) == ibusq:
        buscar_depurado = [buscar[int(indice)] for indice in [x for x in ibusq.split(",") if x != ""]]
    #Si es búsqueda personalizada
    else:
        buscar_depurado = ibusq.split(" ")

    #Corroborando información de búsqueda
    print("\nTus palabras de búsqueda son:")
    print(buscar_depurado)
    busqueda_correcta = input(num_cols*"=" +"Es esto correcto (s|n)? ")


#Lista con resultado de busqueda
listaSubs = subs(buscar_depurado)

#Selecciona subtítulo
#os.system("clear")
for x in range(len(listaSubs)):
    print("\n" + num_cols*"=")
    print(str(x) + ": " + listaSubs[x][0])
    print(num_cols*"-")
    print(listaSubs[x][1])
print(num_cols*"=")
isub = int(input("Elige uno: "))


#Descarga subtitulo elegido
link = descarga(listaSubs[isub][2])
os.system("rm -r tmp")
os.system("mkdir tmp")
os.system("wget -P tmp " + link[0] + ".rar")
os.system("wget -P tmp " + link[0] + ".zip")

#Descomprime subtitulo
if os.popen("find tmp -iname *.zip").read() != "":
    os.system("unzip -o " + "tmp/" + link[1] + ".zip -d tmp/")
if os.popen("find tmp -iname *.rar").read() != "":
    os.system("unrar x -y " + "tmp/" + link[1] + ".rar tmp/")

#Subtitulos descomprimidos como lista de rutas
if os.popen("find tmp -iname *.srt").read() != "":
    ruta_sub = [ruta for ruta in os.popen("find tmp -iname *.srt").read().split("\n") if ruta != ""]
    ext = ".srt"
elif os.popen("find tmp -iname *.ssa").read() != "":
    ruta_sub = [ruta for ruta in os.popen("find tmp -iname *.ssa").read().split("\n") if ruta != ""]
    ext = ".ssa"

#Impresión de opciones de un solo comprimido
os.system("clear")
if len(ruta_sub) > 1:
    for x in range(len(ruta_sub)):
        print(str(x) + ": " + ruta_sub[x][4:])
    nsub = int(input("Ingresa el número de subtítulo: "))
else:
    nsub = 0

#Mueve el subtitulo elegido a la carpeta de la pelicula
os.system('mv "' + ruta_sub[nsub] + '" "' + videos[iv][:-4] + ext + '"')
os.system("rm -r tmp")

print("listo")
