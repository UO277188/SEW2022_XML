import xml.etree.ElementTree as ET
import sys


def main():
    print("------------------------------------------------------------------------------")
    print("| Generador de archivos HTML5, KML y SVG para el ejercicio 2 de XML de SEW   |")
    print("| Método de uso: generadorSEW.py [nombre del fichero XML] [html | kml | svg] |")
    print("| Autor: Diego Villa García (UO277188)                                       |")
    print("------------------------------------------------------------------------------")
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
    archivoHtml = open("redSocialHTML.html", "w", encoding="utf8")
    generaCabeceraHTML(archivoHtml)
    generaCuerpoHTML(archivoHtml, arbol)
    generaCierreHTML(archivoHtml)
    print("Generado correctamente en el fichero redSocialHTML.html")


def generaCabeceraHTML(archivo):
    archivo.write("<!DOCTYPE HTML>")
    archivo.write("<html lang=\"es\">")
    archivo.write("<head>")
    archivo.write("<meta charset=\"UTF-8\"/>")
    archivo.write("<meta name=\"author\" content=\"Diego Villa García - UO277188\"/>")
    archivo.write( "<meta name=\"description\" content=\"HTML convertido a partir de XML usando Python\">")
    archivo.write("<meta name=\"keywords\" content=\"HTML, XML\">")
    archivo.write("<meta name =\"viewport\" content =\"width=device-width, initial scale=1.0\" />")
    archivo.write("<title>SEW XML A HTML UO277188</title>")
    archivo.write( "<link rel=\"stylesheet\" type=\"text/css\" href=\"estilo.css\" />")
    archivo.write("</head>")
    archivo.write("<body>")
    archivo.write("<main>")


def generaCuerpoHTML(archivo, arbol):
    archivo.write("<h1>Miembros de la red social</h1>")
    raiz = arbol.getroot()
    
    # raiz (primera persona)
    archivo.write("<h2>"+raiz.attrib.get('nombre')+" "+raiz.attrib.get('apellidos')+"</h2>")
    archivo.write("<ul>")
    # datos de la persona
    for dato in raiz.findall("datos/*"):
        # datos individuales
        if(len(dato.text.strip("\n").strip("\t"))!=0):
            archivo.write("<li>"+dato.tag+": "+dato.text+"</li>")
        # lugares
        else:
            archivo.write("<li>"+dato.tag)
            archivo.write("<ul>")
            for contenido in dato.findall("*"):
                # fecha
                if(len(contenido.text.strip("\n").strip("\t"))!=0):
                    archivo.write("<li>"+contenido.tag+": "+contenido.text+"</li>")
                # lugares
                else:
                    archivo.write("<li>"+contenido.tag+": "+contenido.attrib.get("nombre")+"</li>")
                    coordenadas = contenido.find("coordenadas")
                    archivo.write("<li>")
                    archivo.write("Latitud: "+coordenadas.attrib.get("latitud"))
                    archivo.write(", Longitud: "+coordenadas.attrib.get("longitud"))
                    archivo.write(", Altitud: "+coordenadas.attrib.get("altitud"))
                    archivo.write("</li>")
            archivo.write("</ul>")
            archivo.write("</li>")
    archivo.write("</ul>")

    generaHTMLAmigosDe(raiz, archivo)

    

def generaHTMLAmigosDe(persona, archivo):
    for persona in persona.findall("persona"):
        archivo.write("<h2>"+persona.attrib.get('nombre')+" "+persona.attrib.get('apellidos')+"</h2>")
        archivo.write("<ul>")
        # datos de la persona
        for dato in persona.findall("datos/*"):
            # datos individuales
            if(len(dato.text.strip("\n").strip("\t"))!=0):
                archivo.write("<li>"+dato.tag+": "+dato.text+"</li>")
            # lugares
            else:
                archivo.write("<li>"+dato.tag)
                archivo.write("<ul>")
                for contenido in dato.findall("*"):
                    # fecha
                    if(len(contenido.text.strip("\n").strip("\t"))!=0):
                        archivo.write("<li>"+contenido.tag+": "+contenido.text+"</li>")
                    # lugares
                    else:
                        archivo.write("<li>"+contenido.tag+": "+contenido.attrib.get("nombre")+"</li>")
                        coordenadas = contenido.find("coordenadas")
                        archivo.write("<li>")
                        archivo.write("Latitud: "+coordenadas.attrib.get("latitud"))
                        archivo.write(", Longitud: "+coordenadas.attrib.get("longitud"))
                        archivo.write(", Altitud: "+coordenadas.attrib.get("altitud"))
                        archivo.write("</li>")
                archivo.write("</ul>")
                archivo.write("</li>")
        archivo.write("</ul>")
        generaHTMLAmigosDe(persona, archivo)

def generaCierreHTML(archivo):
    archivo.write("</main>")
    archivo.write("</body>")
    archivo.write("</html>")
    archivo.close()


if __name__ == "__main__":
    main()
