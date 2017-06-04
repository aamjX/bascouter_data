#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""En el presente archivo se encuentra todo el código necesario para construir los datasets, con los cuales, vamos a popular la
base de datos de nuestra aplicación. Hay que tener en cuenta que extraemos la información de la web www.transfermarket.es, por
lo que es posible que un cambio mínimo en el código de ésta provoque que este ejecutable no funcione corractamente. A día
16/05/2017 a las 1:28 am funciona correctamente."""

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

"""Declaramos los 5 DataFrame a partir de los cuales vamos a ir almacenando la información y finalmente exportarlos a .csv """

data_Competicion = pd.DataFrame(columns=['nombre','logo','categoria'])
data_Equipo = pd.DataFrame(columns=['competicion','nombre_Equipo', 'escudo', 'plantilla', 'edad_media', 'extranjeros', 'valor'])
data_Jugadores = pd.DataFrame(columns=['Avatar','Nombre','Nombre_Completo','Dorsal','Nacionalidad','bandera_pais', 'valor', 'Equipo', 'Altura', 'Pie','Edad', 'Fecha_nacimiento','Contrato_hasta','Posicion','Fichado','Agente', 'Lugar_nacimiento', 'Proveedror'])
data_Estadisticas = pd.DataFrame(columns=['Jugador','Temporada', 'Competicion', 'Club', 'Plantilla', 'Alineaciones', 'Puntos por partido', 'Goles', 'PasesGol',
                                           'GolesPropiaMeta', 'CambiosFuera', 'CambiosDentro', 'Amarillas', 'DobleAmarillas', 'Rojas',
                                           'PenaltisAnotados', 'MinutosPorGol', 'MinutosJugados', 'GolesEnContra', 'PartidoSinGolEnContra'])
data_Fichajes = pd.DataFrame(columns=['Jugador', 'Temporada','Dato','Ultimo_club','Nuevo_club','Valor','Coste'])

""" Declaramos una lista con todas las urls sobre las que queremos extraer información, la url debe de ser de una competición nacional,
por ejemplo la liga Santader y/o la Premier League"""

urls = ['http://www.transfermarkt.es/serie-b/startseite/wettbewerb/IT2']

""" Entrada: cadena de texto (str)
    Salida: cadena de texto sin etiquetas HTML (str) """

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

""" Entrada: cadena de texto (str)
    Salida: cadena de texto sin tildes (str) """

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

""" Entrada: lista de urls de las cuales se va a extraer informacióm
    Salida: 5 datasets en formato .csv con la información extraida
    IMPORTANTE: En caso de añadir datos ----> Actualizar los identificadores de cada dataFrame para que los ids sigan el orden establecido.
"""

def datasetsCreate(listOfURLs):

    for url in listOfURLs:

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response_Equipos = requests.get(url, headers=headers)
        soup_Equipos = BeautifulSoup(response_Equipos.content, 'html.parser')

        infoLiga = soup_Equipos.find('div', attrs={'class':'box'})

        nombreCompeticion = infoLiga.find('div', attrs={'class':'spielername-profil'}).string.strip()
        logoCompeticion = infoLiga.find('div', attrs={'class':'headerfoto'}).img['src']
        categoria = cleanhtml(str(infoLiga.find('table', attrs={'class':'profilheader'}).td)).strip()

        identificador_Competicion = len(data_Competicion) + 10
        data_Competicion.loc[identificador_Competicion] = [nombreCompeticion, logoCompeticion, categoria]

        tabla_Equipos = soup_Equipos.find('table', attrs={'class': 'items'}).tbody

        lista_residual = []
        diccionario_residual = {}

        for equipo in tabla_Equipos.find_all('tr'):

            #Datos del equipo

            nombre = equipo.td.next_sibling.a.string
            plantilla = equipo.td.next_sibling.next_sibling.next_sibling.string
            edad = equipo.td.next_sibling.next_sibling.next_sibling.next_sibling.string
            extranjeros = equipo.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
            valor = equipo.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string

            #Datos de la plantilla del equipo
            response_Plantilla = requests.get("http://www.transfermarkt.es"+equipo.a['href'], headers=headers)
            soup_Plantilla = BeautifulSoup(response_Plantilla.content, 'html.parser')

            escudo = soup_Plantilla.find('div', attrs = {'class':'dataBild'}).img['src']

            identificador = len(data_Equipo) + 198
            data_Equipo.loc[identificador] = [identificador_Competicion,nombre,escudo,plantilla,edad,extranjeros,valor]

            tabla_Plantilla = soup_Plantilla.find('table', attrs={'class': 'items'})
            for i in tabla_Plantilla.find_all('tr'):
                enlace = i.find('a', attrs={'class':'spielprofil_tooltip'})
                if enlace != None and enlace['href'] not in lista_residual:

                    dorsal = i.find('div', attrs={'class':'rn_nummer'}).string
                    nacionalidad = i.find('img', attrs={'class': 'flaggenrahmen'})['title']
                    bandera_pais = i.find('img', attrs={'class':'flaggenrahmen'})['src']
                    valor = i.find('td', attrs={'class':'rechts hauptlink'}).next_element

                    lista_residual.append(enlace['href'])

                    #Datos de cada jugador

                    response_Jugador = requests.get("http://www.transfermarkt.es" + enlace['href'], headers=headers)
                    soup_Jugador = BeautifulSoup(response_Jugador.content, 'html.parser')

                    avatar = soup_Jugador.find('div', attrs={'class':'dataBild'}).img['src'][2:]
                    nombre =  cleanhtml(str(soup_Jugador.h1))

                    #Tabla que contine los principales caracteristicas del jugador

                    for row in soup_Jugador.find('div', attrs={'class': 'row collapse'}).find_all('tr'):
                        key = cleanhtml(str(row.th)).strip()
                        diccionario_residual[elimina_tildes(unicode(key, 'utf-8'))] = cleanhtml(str(row.td)).strip()

                    newDict = {}
                    lista_datos = ['Lugar de nacimiento:','Altura:', 'Pie:','Edad:','Fecha de nacimiento:', 'Contrato hasta::', 'Posicion:', 'Fichado:','Nombre en pais de origen:','Agente:','Proveedor:']

                    for l in lista_datos:
                        if diccionario_residual.has_key(l):
                            newDict[l] = diccionario_residual[l]
                        else:
                            newDict[l] = '-'

                    if diccionario_residual.has_key('Fecha de nacimiento:'):
                        identificador_jugador = len(data_Jugadores) + 5230
                        data_Jugadores.loc[identificador_jugador] = [avatar, nombre,newDict['Nombre en pais de origen:'],dorsal,nacionalidad,bandera_pais,valor, identificador,
                                                                     newDict['Altura:'], newDict['Pie:'],newDict['Edad:'],
                        diccionario_residual['Fecha de nacimiento:'], newDict['Contrato hasta::'], newDict['Posicion:'], newDict['Fichado:'], newDict['Agente:'], newDict['Lugar de nacimiento:'],newDict['Proveedor:']]
                        print len(data_Jugadores)
                        print '----------------------CREANDO DATAFRAME---------------------------------------'
                    else:
                        next

                    #Historial fichajes jugador

                    historialFichajes = soup_Jugador.find('div', attrs={'class':'responsive-table'})

                    for fichaje in historialFichajes.find_all('tr', attrs={'class':'zeile-transfer'}):
                        fichajes = []
                        for f in fichaje.find_all('td'):
                             fichajes.append(cleanhtml(str(f)).strip())
                        identificador_Fichajes = len(data_Fichajes) + 34717
                        data_Fichajes.loc[identificador_Fichajes] = [identificador_jugador,fichajes[0],fichajes[1],fichajes[5],fichajes[9],fichajes[10],fichajes[11]]

                    #Datos de rendimiento de dicho jugador

                    response_Rendimiento = requests.get("http://www.transfermarkt.es"+soup_Jugador.find_all('a', attrs={'name':'SubNavi'})[3]['href'], headers=headers)
                    soup_Rendimiento = BeautifulSoup(response_Rendimiento.content, 'html.parser')

                    enlace_RendimientoDetallado = "http://www.transfermarkt.es"+soup_Rendimiento.find('div', attrs={'class':'kartei-button-bar'}).a.next_sibling['href']

                    response_RendimientoDetallado = requests.get(enlace_RendimientoDetallado, headers=headers)
                    soup_RendimientoDetallado = BeautifulSoup(response_RendimientoDetallado.content, 'html.parser')

                    tabla_Rendimiento = soup_RendimientoDetallado.find('table', attrs={'class':'items'})

                    if tabla_Rendimiento != None:

                        for rendimiento in tabla_Rendimiento.tbody.find_all('tr'):
                            datos = []
                            if diccionario_residual.has_key('Posicion:') and diccionario_residual.has_key('Fecha de nacimiento:'):
                                if diccionario_residual['Posicion:'] == 'Portero':
                                    for d in rendimiento.find_all('td'):
                                        if d.string == None:
                                            datos.append(d.img['alt'])
                                        else:
                                            datos.append(d.string)
                                    identificador_estadistica = len(data_Estadisticas) + 111621
                                    data_Estadisticas.loc[identificador_estadistica] = [identificador_jugador,datos[0],datos[1],datos[3],datos[4],datos[5],datos[6],datos[7],
                                                                                       '-',datos[8],datos[9],datos[10],datos[11],datos[12],datos[13],'-','-',datos[16],datos[14],datos[15]]

                                else:
                                    for d in rendimiento.find_all('td'):
                                        if d.string == None:
                                            datos.append(d.img['alt'])
                                        else:
                                            datos.append(d.string)


                                    identificador_estadistica = len(data_Estadisticas) + 111621
                                    data_Estadisticas.loc[identificador_estadistica] = [identificador_jugador, datos[0],datos[1],datos[3],datos[4],datos[5],datos[6],datos[7],
                                                                                       datos[8],datos[9],datos[10],datos[11],datos[12],datos[13], datos[14],datos[15],datos[16],datos[17],'-','-']
                            else:
                                next

                        diccionario_residual = {}
                    else:
                        next

        print data_Equipo.sort_index()
        data_Jugadores.to_csv('principal/management/commands/Jugadores.csv', encoding='utf-8')
        data_Equipo.to_csv('principal/management/commands/Equipos.csv', encoding='utf-8')
        data_Estadisticas.to_csv('principal/management/commands/Rendimiento_jugadores.csv', encoding='utf-8')
        data_Competicion.to_csv('principal/management/commands/Competiciones.csv', encoding='utf-8')
        data_Fichajes.to_csv('principal/management/commands/Historial_fichajes_jugadores.csv', encoding='utf-8')

def main():
    datasetsCreate(urls)

if __name__ == "__main__":
    main()