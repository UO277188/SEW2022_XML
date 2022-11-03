import xml.etree.ElementTree as ET
import sys

def main():
    print("-------------------------------------------------------------------")
    print("| Programa que analiza un fichero GXL - Ejercicio 3 de XML de SEW |")
    print("| Método de uso: analizaGXL.py [nombre del fichero GXL]           |")
    print("| Autor: Diego Villa García (UO277188)                            |")
    print("-------------------------------------------------------------------")
    try:
        arbol = cargarGXL(sys.argv[1])
        analizar(arbol)
    except IndexError:
        print("ERROR - Falta el nombre del archivo a procesar")

def cargarGXL(nombre):
    """
    Carga el fichero gxl de nombre indicado
    """
    try:
        arbol = ET.parse(nombre)
        return arbol
    except IOError:
        print("ERROR - No se ha podido leer el fichero", nombre)
        exit()
    except ET.ParseError:
        print("ERROR - No se ha podido procesar el fichero", nombre)
        exit()

def analizar(arbol):
    """
    Analiza el árbol indicado del fichero gxl e imprime por pantalla el número de nodos y aristas
    """
    numNodos = 0
    numAristas = 0

    for hijo in arbol.getroot().findall(".//"):
        if(hijo.tag == "node"):
            numNodos += 1
        elif(hijo.tag == "edge"):
            numAristas += 1

    print("Total de nodos: " + str(numNodos))
    print("Total de aristas: " + str(numAristas))


if __name__ == "__main__":
    main()
