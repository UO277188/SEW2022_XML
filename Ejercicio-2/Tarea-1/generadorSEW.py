import xml.etree.ElementTree as ET
import sys

def main():
    print("Generador de archivos HTML5, KML y SVG para el ejercicio 2 de XML de SEW")
    print("Método de uso: generadorSEW.py [nombre del fichero XML] [html | kml | svg]")
    print("Autor: Diego Villa García (UO277188)")
    try:
        arbol = cargarXML(sys.argv[1])
        procesar(arbol)
    except IndexError:
        print("ERROR - Falta el nombre del archivo a procesar")

def cargarXML(nombre):
    try:
        arbol = ET.parse(nombre)
        return arbol
    except IOError:
        print("ERROR - No se ha podido leer el fichero", nombre)
        exit()
    except ET.ParseError:
        print("ERROR - No se ha podido procesar el fichero", nombre)
        exit()

def procesar(arbol):
    try:
        tipo = sys.argv[2]

        if(tipo == "html"):
            generaHTML(arbol)
        elif(tipo == "kml"):
            generaKML(arbol)
        elif(tipo == "svg"):
            generaSVG(arbol)
        else:
            print("ERROR - El tipo de fichero a generar no es válido")
    except IndexError:
        print("ERROR - Falta el tipo de procesado [html | kml | svg]")

def generaHTML(arbol):
    archivoHtml = open("redSocialHTML"+".html", "w", encoding="utf8")
    generaCabeceraHTML(archivoHtml)
    generaCuerpoHTML(archivoHtml, arbol)
    generaCierreHTML(archivoHtml)

def generaCabeceraHTML(archivo):
    archivo.write("<!DOCTYPE HTML>")
    archivo.write("<html lang=\"es\">")
    archivo.write("<head>")
    archivo.write("<meta charset=\"UTF-8\"/>")
    archivo.write("<meta name=\"author\" content=\"Diego Villa García - UO277188\"/>")
    archivo.write("<meta name=\"description\" content=\"HTML convertido a partir de XML usando Python\">")
    archivo.write("<meta name=\"keywords\" content=\"HTML, XML\">")
    archivo.write("<meta name =\"viewport\" content =\"width=device-width, initial scale=1.0\" />")
    archivo.write("<title>SEW XML A HTML UO277188</title>")
    archivo.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"estilo.css\" />")
    archivo.write("</head>")
    archivo.write("<body>")
    archivo.write("<main>")

def generaCuerpoHTML(archivo, arbol):
    archivo.write("<h1>Red Social- Diego Villa García</h1>")
    raiz = arbol.getroot()
    archivo.write("<h2>"+raiz.attrib.get('nombre')+" "+raiz.attrib.get('apellidos')+"</h2>")
    
    for persona in raiz.findall("./persona"):
        archivo.write("<h3>"+persona.attrib.get('nombre')+" "+persona.attrib.get('apellidos')+"</h3>")
        for persona in persona.findall("./persona"):
            archivo.write("<h4>"+persona.attrib.get('nombre')+" "+persona.attrib.get('apellidos')+"</h4>")

def generaCierreHTML(archivo):
    archivo.write("</main>")
    archivo.write("</body>")
    archivo.write("</html>")
    archivo.close()

if __name__ == "__main__":
    main()