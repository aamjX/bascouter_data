# bascouter_data

En el archivo scrap.py se encuentra el código necesario para realizar Web-Scraping sobre https://www.transfermarkt.es/ y extraer la información
necesaria para la aplicación www.bascouter.es. El formato de los csv es el siguiente.

Competiciones.csv
-	Id: Identificador para la competición.
-	Nombre: Nombre de la competición.
-	Logo: Logo de la competición.
-	Categoría: Categoría a la que pertenece la competición.

Equipos.csv
-	Id: Identificador para el equipo.
-	Competición: Identificador de la competición a la que pertenece el equipo.
-	Nombre_equipo: Nombre del equipo.
-	Escudo: Imagen con el escudo del equipo.
-	Plantilla: Número de jugadores que tiene el equipo en plantilla.
-	Edad_media: Edad media de los jugadores que componen el equipo.
-	Extranjeros: Número de jugadores no nacionales que compone la plantilla.
-	Valor: Valor del equipo.

Jugadores.csv
-	Id: Identificador para el jugador.
-	Avatar: Imagen del jugador.
-	Nombre: Nombre o apodo del jugador.
-	Nombre_completo: Nombre completo del jugador.
-	Dorsal: Dorsal del jugador.
-	Nacionalidad: Nacionalidad del jugador.
-	Bandera_país: Imagen de la bandera del país del jugador.
-	Valor: Valor del jugador.
-	Equipo: Identificador del equipo al que pertenece el jugador.
-	Altura: Altura del jugador.
-	Pie: Pierna con la que el jugador tiene un mejor golpeo del balón.
-	Edad: Edad del jugador en años.
-	Fecha_nacimieto: Fecha de nacimiento del jugador.
-	Contrato_hasta: Fecha en la que el contrato actual del jugador cumple.
-	Posición: Posición en la que juega el jugador.
-	Fichado: Fecha en la que el jugador fue fichado.
-	Agente: Agente del jugador.
-	Lugar_nacimiento: Procedencia del jugador.
-	Proveedor: Marca deportica que viste el jugador.

Rendimiento_jugadores.csv
-	Id: Identificador para el rendimiento asociado a un jugador.
-	Jugador: Identificador del jugador al que pertenece el rendimiento.
-	Temporada: Temporada a la que pertenece el rendimiento.
-	Competición: Competición a la que pertenece el rendimiento del jugador.
-	Club: Club al que pertenece el rendimiento del jugador.
-	Plantilla: Veces que ha sido convocado un jugador.
-	Alineaciones: Veces que ha jugado como titular un jugador.
-	Puntos_por_partido: Relación entre puntos conseguidos y partidos jugados.
-	Goles: Goles que ha marcado un jugador.
-	Pases_gol: Pases de gol que ha dado un jugador.
-	Goles_propia_Meta: Goles en propia puerta que ha hecho un jugador.
-	Cambios_Fuera: Veces que un jugador ha sido sutituido.
-	Cambios_Dentro: Veces que un jugador ha entrado al campo para sustituir a un titular.
-	Amarillas: Tarjetas amarillas recibidas.
-	Doble_amarillas: Veces que un jugador ha recibido dos tarjetas amarillas en un mismo partido de fútbol.
-	Rojas: Tarjetas rojas recibidas.
-	Penaltis_anotados: Veces que un jugador ha anotado gol desde penalti.
-	Minutos_por_gol: Relación entre los minutos jugados y los goles anotodos por un jugador.
-	Minutos_jugados: Número de minutos que un jugador ha jugado en total.
-	Goles_en_contra: Goles que un portero ha recibido.
-	Partidos_sin_gol_en_Contra: Número de partidos que un portero no ha recibido ningún gol.
Historial_fichajes_jugadores.csv
-	Id: Identificador del historial asociado a un jugador.
-	Jugador: Identificador del jugador al que pertenece el historial.
-	Temporada: Temporada en la que se realizó el traspaso.
-	Fecha: Fecha en la quese realizó el traspaso.
-	Ultimo_club: Equipo de procedencia.
-	Nuevo_club: Equipo al cual ha sido traspasado.
-	Valor: Valor del jugador en el momento del traspaso.
-	Coste: Coste del traspaso.
