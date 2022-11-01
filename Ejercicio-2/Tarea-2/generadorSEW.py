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
    """
    Carga el fichero xml de nombre indicado
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


def procesar(arbol):
    """
    Procesa el árbol y genera el tipo de archivo que se indicó en línea de comandos
    """
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






# ---------------------------------------------
# GENERACIÓN DE HTML 
# ---------------------------------------------


def generaHTML(arbol):
    """
    Genera el html a partir del árbol indicado
    """
    archivoHtml = open("redSocialHTML.html", "w", encoding="utf8")
    generaCabeceraHTML(archivoHtml)
    generaCuerpoHTML(archivoHtml, arbol)
    generaCierreHTML(archivoHtml)
    print("Generado correctamente en el fichero redSocialHTML.html")


def generaCabeceraHTML(archivo):
    """
    Genera la cabecera del html, siempre es igual
    """
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
    """
    Genera el cuerpo del html, la parte variable
    """
    archivo.write("<h1>Miembros de la red social</h1>")
    raiz = arbol.getroot()
    
    # raiz (primera persona)
    archivo.write("<h2>"+raiz.attrib.get('nombre')+" "+raiz.attrib.get('apellidos')+"</h2>")
    archivo.write("<ul>")
    # datos de la persona
    for dato in raiz.findall("datos/*"):
        if(dato.tag=="foto"):
            archivo.write("<li><img src=\"multimedia/"+dato.text+"\""+" alt=\"imagen\"/></li>")
        elif(dato.tag=="video"):
            archivo.write("<li><video controls><source src=\"multimedia/"+dato.text+"\""+" type=\"video/mp4\"/></video></li>")
        else:
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
    """
    Genera el html de los amigos de la persona indicada en el archivo indicado
    """
    for persona in persona.findall("persona"):
        archivo.write("<h2>"+persona.attrib.get('nombre')+" "+persona.attrib.get('apellidos')+"</h2>")
        archivo.write("<ul>")
        # datos de la persona
        for dato in persona.findall("datos/*"):
            if(dato.tag=="foto"):
                archivo.write("<li><img src=\"multimedia/"+dato.text+"\""+" alt=\"imagen\"/></li>")
            elif(dato.tag=="video"):
                archivo.write("<li><video controls><source src=\"multimedia/"+dato.text+"\""+" type=\"video/mp4\"/></video></li>")
            else:
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
    """
    Genera el cierre del html, siempre es igual
    """
    archivo.write("</main>")
    archivo.write("</body>")
    archivo.write("</html>")
    archivo.close()





# ---------------------------------------------
# GENERACIÓN DE KML 
# ---------------------------------------------


def generaKML(arbol):
    """
    Genera el kml a partir del árbol indicado
    """
    archivoKml = open("redSocialKML.kml", "w", encoding="utf8")
    generaCabeceraKML(archivoKml)
    generaCuerpoKML(archivoKml, arbol)
    generaCierreKML(archivoKml)
    print("Generado correctamente en el fichero redSocialKML.kml")

def generaCabeceraKML(archivo):
    """
    Genera la cabecera del KML
    """
    archivo.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    archivo.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">")

def generaCuerpoKML(archivo, arbol):
    """
    Genera el cuerpo del KML en el archivo a partir del arbol
    """
    raiz = arbol.getroot()
    archivo.write("<Document>")
    archivo.write("<name>Ejercicio-1 Tarea-2</name>")

    # raiz (primera persona)
    # datos de la persona
    for dato in raiz.findall("datos/*"):
        # lugares
        if(len(dato.text.strip("\n").strip("\t"))==0):
            for contenido in dato.findall("*"):
                # lugares
                if(len(contenido.text.strip("\n").strip("\t"))==0):
                    archivo.write("<Placemark>")
                    archivo.write("<name>"+raiz.attrib.get('nombre')+" "+raiz.attrib.get('apellidos')+" ("+dato.tag+")"+"</name>")
                    coordenadas = contenido.find("coordenadas")
                    archivo.write("<Point>")
                    archivo.write("<coordinates>")
                    archivo.write(coordenadas.attrib.get("latitud")+",")
                    archivo.write(coordenadas.attrib.get("longitud")+",")
                    archivo.write(coordenadas.attrib.get("altitud"))
                    archivo.write("</coordinates>")
                    archivo.write("</Point>")
                    archivo.write("</Placemark>")

    generaKMLAmigosDe(raiz, archivo)
    archivo.write("</Document>")

def generaKMLAmigosDe(persona, archivo):
    """
    Genera el cuerpo del KML en el archivo de los amigos de la persona
    """
    for persona in persona.findall("persona"):
        # datos de la persona
        for dato in persona.findall("datos/*"):
            # lugares
            if(len(dato.text.strip("\n").strip("\t"))==0):
                for contenido in dato.findall("*"):
                    # lugares
                    if(len(contenido.text.strip("\n").strip("\t"))==0):
                        archivo.write("<Placemark>")
                        archivo.write("<name>"+persona.attrib.get('nombre')+" "+persona.attrib.get('apellidos')+" ("+dato.tag+")"+"</name>")
                        coordenadas = contenido.find("coordenadas")
                        archivo.write("<Point>")
                        archivo.write("<coordinates>")
                        archivo.write(coordenadas.attrib.get("latitud")+",")
                        archivo.write(coordenadas.attrib.get("longitud")+",")
                        archivo.write(coordenadas.attrib.get("altitud"))
                        archivo.write("</coordinates>")
                        archivo.write("</Point>")
                        archivo.write("</Placemark>")
        generaKMLAmigosDe(persona, archivo)

def generaCierreKML(archivo):
    """
    Genera el cierre del KML
    """
    archivo.write("</kml>")


# --------------------
# GENERACIÓN DE SVG 
# --------------------


if __name__ == "__main__":
    main()
