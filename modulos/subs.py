#!/bin/env python
"""
Recibe una lista de palabras de busqueda y el número de página de busqueda. Retorna una lista de listas de subtitulos, donde cada lista se compone de [titulo, descripcion, enlace]
"""
import os

def subs(palabras):
    subs, subspag, pagina = [], [1], 0
    while subspag != []:
        pagina+=1

        #Búsqueda
        suma = "+".join(palabras)
        linkBusqueda = "https://www.subdivx.com/index.php?buscar=" + suma + "&accion=5&masdesc=&subtitulos=1&realiza_b=1=&pg=" + str(pagina)
        txtBusqueda = os.popen("curl '" + linkBusqueda + "' | iconv -f iso-8859-1 -t utf-8").read()
        
        x, subspag = 0, []
        while '"titulo_menu_izq" href="' in txtBusqueda[x:]:
            ind = txtBusqueda[x:].index('"titulo_menu_izq" href="')
            ind2 = txtBusqueda[x+ind:].index('">')
            ind3 = txtBusqueda[x+ind+ind2:].index('</a>')

            enlace = txtBusqueda[24+x+ind:x+ind+ind2]
            titulo = txtBusqueda[x+ind+ind2+2:x+ind+ind2+ind3]
            
            x += (ind+ind2+ind3)
            ind4 = txtBusqueda[x:].index('<div id="buscador_detalle_sub"')
            ind5 = txtBusqueda[x+ind4:].index('</div>')

            descripcion = txtBusqueda[31+x+ind4:x+ind4+ind5]
            
            descripcion = "".join(descripcion.split("Â"))
            descripcion = " ".join(descripcion.split("\n"))
            descripcion = "ñ".join(descripcion.split("Ã±"))
            descripcion = "á".join(descripcion.split("Ã¡"))
            descripcion = "é".join(descripcion.split("Ã©"))
            descripcion = "í".join(descripcion.split("Ã\xad"))
            descripcion = "ó".join(descripcion.split("Ã³"))
            descripcion = "ú".join(descripcion.split("Ãº"))

            titulo = "".join(titulo.split("Â"))
            titulo = " ".join(titulo.split("\n"))
            titulo = "ñ".join(titulo.split("Ã±"))
            titulo = "á".join(titulo.split("Ã¡"))
            titulo = "é".join(titulo.split("Ã©"))
            titulo = "í".join(titulo.split("Ã\xad"))
            titulo = "ó".join(titulo.split("Ã³"))

            subspag.append([titulo, descripcion, enlace])
            subs += subspag
            x += (ind4+ind5)

    return subs
