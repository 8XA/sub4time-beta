#!/bin/env python

import os, curses, sys, readline
from modulos.subs import subs
from modulos.descarga import descarga
from modulos.update import update
from modulos.navegador import navegar
from termcolor import colored


ruta_conf = "/data/data/com.termux/files/usr/share/sub4time/ruta_videos"
#ruta_conf = "./ruta_videos"
if not os.path.isfile(ruta_conf):
    rvids = os.popen("pwd").read()[:-1]
else:
    with open(ruta_conf,"r") as file:
        rvids = file.readlines()[0]
if rvids[-1:] == "\n":
    rvids = rvids[:-1]

rabs = "/data/data/com.termux/files/home/"
#rabs = ""


#FUNCIÓN SALIR
def salir():
    #FINALIZAR SCRIPT
    print("\nPrograma finalizado.")
    sys.exit()


#DETERMINANDO EL NÚMERO DE CARACTERES POR LÍNEA
def numcols():
    screen = curses.initscr() 
    num_cols = screen.getmaxyx()[1]
    curses.endwin()
    os.system("stty sane && clear")
    return num_cols
num_cols = numcols()


def imprimevideos(rvids, num_cols):
    global extensiones, videos, nombres

    #VIDEOS CON SU RUTA
    extensiones = ["mp4", "mkv", "avi"]
    videos = []
    os.system("clear")
    print("Buscando videos en la ruta especificada y sus subdirectorios inmediatos...")
    for ext in extensiones:
        videos += os.popen("find '" + rvids + "' -iname *." + ext).read().split("\n")
    videos = [video for video in videos if video != ""]
    #NOMBRES DE LOS VIDEOS
    nombres = sorted([ruta[len(ruta) - [ruta[x] for x in range(len(ruta)-1,-1,-1)].index("/"):] for ruta in videos], key=str.casefold)

    #IMPRIME PANTALLA
    os.system("clear")
    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    titulo = "SUB4TIME Beta v1.6.5"
    titulo2 = "Lista"
    print(((num_cols-len(titulo))//2)*" " + titulo)
    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    print(((num_cols-len(titulo2))//2)*" " + titulo2)

    #IMPRIME NOMBRES DE VIDEOS
    for x in range(len(nombres)):
        print(num_cols*"-")
        indice = colored(str(x), 'green', attrs=['bold', 'dark'])
        print(indice + ": " + nombres[x])

    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    return 0


#OPCIONES DE LA PANTALLA PRINCIPAL
readline.clear_history()
iv = "."
while type(iv) != type(0):
    imprimevideos(rvids, num_cols)

    iv = input("Número de video ('s': salir | 'act: actualizar' | '.': Cambiar carpeta): ")
    if iv == ".":
        rvids = navegar(num_cols, rvids, ruta_conf)

    #ACTUALIZAR
    elif iv == "act":
        if update(num_cols) == 1:
            i = input("Debes reiniciar Termux.")
            salir()

    elif "".join([x for x in iv if x in "0123456789"]) == iv and len(iv) > 0:
        if int(iv) < len(nombres):
            iv = int(iv)
    
    elif iv.lower() == "s":
        salir()


#LISTA DE PALABRAS PARA BÚSQUEDA
buscar = [palabra for palabra in " ".join(nombres[iv].split(".")).split(" ") if (palabra != " " and palabra.lower() not in extensiones)]


#BÚSQUEDA
busqueda_correcta = ""
readline.clear_history()
while busqueda_correcta.lower() != "s":
    os.system("clear")
    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    titulo = "LISTA DE PALABRAS"
    print(((num_cols-len(titulo))//2)*" " + titulo)
    print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
    for x in range(len(buscar)):
        indice = colored(str(x), 'green', attrs=['bold', 'dark'])
        print(indice + ": " + buscar[x])

    #PALABRAS DE BUSQUEDA
    buscar_depurado = []
    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    print(((num_cols-9)//2)*" " + "OPCIONES:")
    print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
    print("""- URL subdivx
- Palabras de la lista: num0,num1,num2
- Lista completa: t
- Ingresa una búsqueda personalizada""")
    print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
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
    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    busqueda_correcta = input("Es esto correcto (s|n)? ")
os.system("clear")


#SALTA EL ALGORITMO DE BÚSQUEDA SI SE INGRESÓ DIRECTAMENTE EL LINK DE DESCARGA DEL SUBTÍTULO   
if urlDirecta == False:
    #LISTA CON RESULTADO DE BUSQUEDA
    listaSubsBruta, listaSubs = subs(buscar_depurado), []
    for x in listaSubsBruta:
        if x not in listaSubs:
            listaSubs.append(x)


    #DEFINE LOS SUBTITULOS A MOSTRAR
    isub, subxpag, filtro, pagina = "", 50, [], 0
    readline.clear_history()
    while "".join([x for x in isub if x in "0123456789"]) != isub or isub == "":
        if filtro == []:
            listaSubsF = [listaSubs[x][:2]+[x] for x in range(len(listaSubs))]
        else:
            listaSubsF = [listaSubs[x][:2]+[x] for x in range(len(listaSubs)) if (len(filtro) == len([palabra for palabra in filtro if (palabra.lower() in ((listaSubs[x][0]+listaSubs[x][1]).lower()))]))]

        #NÚMERO DE PÁGINAS
        paginas = len(listaSubsF)//subxpag
        if len(listaSubsF)/subxpag != len(listaSubsF)//subxpag:
            paginas += 1

        #IMPRIME, NUMERA SUBTÍTULOS Y NAVEGA A TRAVÉS DE ELLOS
        os.system("clear")
        for x in range((pagina+1)*subxpag-1, pagina*subxpag-1, -1):
            if len(listaSubsF) > x:
                print("\n")
                print(colored(num_cols*"=", 'yellow', attrs=['bold', 'dark']))
                print(str(x) + ": " + colored("ID " + str(listaSubsF[x][2]), 'green', attrs=['bold', 'dark']) + " -> " + listaSubsF[x][0])
                print(num_cols*"-")
                print(listaSubsF[x][1])
        print('\n')
        print(colored(num_cols*"=", 'yellow', attrs=['bold', 'dark']))

        #IMPRIME OPCIONES
        print("\n")
        print(colored(num_cols*"=", 'red', attrs=['bold', 'dark']))
        print(((num_cols-len(nombres[iv]))//2)*" " + nombres[iv])
        print(colored(num_cols*"=", 'red', attrs=['bold', 'dark']))
        print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
        print(((num_cols-9)//2)*" " + "OPCIONES:")
        print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
        print("Pag anterior  <- : a")
        print("Pag siguiente -> : Enter")
        print("Filtrar subs     : palabra1,palabra2")
        print("Quitar filtro    : f")
        print("Descargar sub    : num")
        print("Salir            : q")
        print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
        print("Pagina:",pagina+1, "de",paginas, "-", len(listaSubsF), "subs")
        isub = input(": ")

        #NAVEGANDO
        if isub.lower() == "a":
            pagina -= 1
            if pagina == -1:
                pagina = paginas-1
        elif isub == "":
            pagina +=1
            if pagina == paginas:
                pagina = 0

        elif isub.lower() == "f":
            filtro, pagina = [], 0
        elif isub.lower() == "q":
            salir()
        else:
            filtro, pagina = [x for x in isub.split(",") if x != ""], 0


    #SELECCIÓN DE SUBTÍTULO
    link = descarga(listaSubs[int(isub)][2])
else:
    link = descarga(ibusq)


#DESCARGA SUBTITULO ELEGIDO
os.system("clear")
print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
print("Descargando subtítulo...")
print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
os.system("rm -r tmp")
os.system("mkdir tmp")
os.system("wget -P tmp " + link[0] + ".rar")
os.system("wget -P tmp " + link[0] + ".zip")


#DESCOMPRIME SUBTITULO
print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
print("Descomprimiendo...")
print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
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
if len(ruta_sub) > 1:
    os.system("clear")
    print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
    for x in range(len(ruta_sub)):
        indice = colored(str(x), 'green', attrs=['bold', 'dark'])
        print(indice + ": " + ruta_sub[x][4:])
    print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
    nsub = int(input("Ingresa el número de subtítulo: "))
else:
    nsub = 0


#MUEVE EL SUBTITULO ELEGIDO A LA CARPETA DE LA PELICULA
print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
print("Asignando subtítulo...")
os.system('mv "' + ruta_sub[nsub] + '" "' + videos[iv][:-4] + ext + '"')
os.system("rm -r tmp")

print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
i = input("Listo. Presione Enter para salir.")
