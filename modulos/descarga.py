#!/bin/env python

"""
Recibe un enlace de descarga. Con él, retorna el enlace directo y el ID de archivo
"""

import os

def descarga(enlace):
    #Descargando html
    txtPagina = os.popen("curl '" + enlace + "' | iconv -f iso-8859-1 -t utf-8").read()
    
    #Scraping
    ind1 = txtPagina.index('"link1" href="bajar.php?id=')
    ind2 = txtPagina[ind1+27:].index('&u=')
    idsub = txtPagina[ind1+27:ind1+27+ind2]
    u = txtPagina[30+ind1+ind2]
    
    #Generando link de descarga
    num = ""
    if u != "1":
        num = u
    link = "https://www.subdivx.com/sub" + num + "/" + idsub

    return [link,idsub]
