#!/bin/env python

import os
from termcolor import colored

def navegar(num_cols, rvids, guardar):
    ruta = rvids.split("/")

    accion = "."
    while accion != "":
        os.system("clear")
        titulo = "SELECCIÓN DE CARPETA"
        print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
        print(((num_cols-len(titulo))//2)*" " + titulo)
        print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
        print("/".join(ruta) + "\n")

        carpetas = sorted([x.path.split("/")[-1:][0] for x in os.scandir("/".join(ruta)) if x.is_dir()])
        
        for x in range(len(carpetas)):
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])
            print(indice + ":",carpetas[x])
        print(colored(num_cols*"-", 'blue', attrs=['bold', 'dark']))
        indice = colored("..", 'green', attrs=['bold', 'dark'])
        print(indice + ": Directorio anterior")
        indice = colored("Enter", 'green', attrs=['bold', 'dark'])
        print(indice + ": Aceptar")

        print(colored(num_cols*"=", 'blue', attrs=['bold', 'dark']))
        accion = input(": ")
        
        if accion == "":
            with open(guardar,"w") as file:
                file.write("/".join(ruta))
            return "/".join(ruta)
        elif "".join([x for x in accion if x in "0123456789"]) == accion:
            if len(carpetas) > int(accion) >= 0:
                ruta.append(carpetas[int(accion)])
        elif accion == "..":
            if len(ruta) > 8:
                ruta.pop()
        else:
            pass

