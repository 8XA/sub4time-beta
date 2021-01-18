#!/bin/env python

import os, time

def update(num_cols):
    rabs = '/data/data/com.termux/files/usr/share/downpipe/sub4time/'
    os.system("clear")
    print("Verificando actualizaciones de script...\n")
    remoto = os.popen('cd '+ rabs + ' && git fetch origin master && git checkout remotes/origin/master').read()
    local = os.popen('cd ' + rabs + ' && git checkout master').read()
    if "commit" in local:
        print("Actualizando script...\n")
        os.system('rm -rf update')
        clonar = os.system('git clone --branch master --single-branch https://github.com/8XA/sub4time.git update')
        if clonar == 0:
            os.system('rm -rf ' + rabs[:-1])
            os.system('mv update ' + rabs[:-1] + ' && clear')
            print(((num_cols-22)//2)*" " + "ACTUALIZACIÓN COMPLETA")
            print(num_cols*"=")
            with open(rabs + "/novedades","r") as nov:
                novedades = nov.readlines()
            for line in novedades:
                print(line[:-1])
            print("\n" + num_cols*"=")
            return 1

    else:
        os.system("clear")
        print("Script ya actualizado. Nada para hacer...")
        time.sleep(1)
        os.system("clear")
        return 0
