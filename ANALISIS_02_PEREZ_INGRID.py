"""register_id, direction, origin, destination,
year, date, product, transport_mode, company_name, total_value"""

""" Opción 1) Rutas de importación y exportación. 
Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos 
en las 10 rutas más demandadas. Acorde a los flujos de importación y exportación, ¿cuáles son esas 10 rutas?"""
import csv

#pasando los datos de synergy...csv a una lista
lista_datos = []
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.reader(archivo)
    for linea in lector:
        lista_datos.append(linea)
    #archivo.seek(0) #sirve para volver a iterar. si no se pone, no se puede hacer otro for abajo del ya hecho
                
lista_datos.pop(0)  #eliminamos el primer elemento, pues son cadenas de texto que no podemos operar
#Separando synergy.. en importaciones y exportaciones
exportaciones = []
importaciones = []
for linea in lista_datos:
    if linea[1] == "Exports":
        exportaciones.append(linea)
    elif linea[1] == "Imports":
        importaciones.append(linea)

#Funcion para crear archivos csv y escribir en ella una lista especifica
def escritor_csv(nombre_archivo, lista):
    with open(nombre_archivo, "w") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(lista)
        
#ordena lista con respecto a una columna, de mayor a menor
ordenar = lambda lista, columna: lista.sort(reverse = True, key = lambda x:x[columna])

#japon a china != china a japon, en la misma direccion
#definiendo funcion para EXTRAER rutas de importacion y exportacion 
#cuenta cuantas veces se repite una ruta en la misma direccion y suma su valor de ingreso
#se crean dos listas: ordenando de mayor a menor las viajes por ruta 
#y ordenando de mayor a menor los ingresos totales de las rutas
#direcion = importaciones o exportaciones
def extraccion_rutas(direccion, nombre_archivo_cuenta, nombre_archivo_ingreso):
    contador = 0
    ingreso_por_ruta = 0
    rutas_contadas = []
    conteo_rutas = []
    for ruta in direccion:
        ruta_actual = [ruta[2],ruta[3]]
        if ruta_actual not in rutas_contadas:
            for movimiento in direccion:
                if ruta_actual == [movimiento[2],movimiento[3]]:
                    contador += 1
                    ingreso_por_ruta += int(movimiento[9])
            rutas_contadas.append(ruta_actual)
            conteo_rutas.append([ruta[2], ruta[3], contador, ingreso_por_ruta])
            contador = 0  
            ingreso_por_ruta = 0
    ordenar(conteo_rutas,2)     #ordena con respecto al conteo (num. viajes por ruta)
    escritor_csv(nombre_archivo_cuenta, conteo_rutas)
    ordenar(conteo_rutas,3)     #ordena con respecto al ingreso por ruta
    escritor_csv(nombre_archivo_ingreso, conteo_rutas)
    
#llamando la funcion extraccion_rutas
extraccion_rutas(exportaciones, "rutas_exportaciones_conteo.csv", "rutas_exportaciones_ingreso.csv")
extraccion_rutas(importaciones, "rutas_importaciones_conteo.csv", "rutas_importaciones_ingreso.csv")

"""Opción 2) Medio de transporte utilizado. ¿Cuáles son los 3 medios de transporte
más importantes para Synergy logistics considerando el valor de las
importaciones y exportaciones? ¿Cuál es medio de transporte que podrían
reducir?"""

#se crea la lista medios_contados=[transporte, veces usado, ingreso total por transporte]
#el siguiente for cuenta las veces que se usó un transporte y el ingreso total por medio
medios_contados = []
transporte = []
for medio in lista_datos:
    contador = 0
    ingreso_por_medio = 0
    if medio[7] not in medios_contados:
        for movimiento in lista_datos:
            if medio[7] == movimiento[7]:
                contador += 1
                ingreso_por_medio += int(movimiento[9])
        medios_contados.append(medio[7])
        transporte.append([medio[7], contador, ingreso_por_medio])
ordenar(transporte,2)
escritor_csv("transporte.csv", transporte)

"""Opción 3) Valor total de importaciones y exportaciones. Si Synergy Logistics
quisiera enfocarse en los países que le generan el 80% del valor de las
exportaciones e importaciones ¿en qué grupo de países debería enfocar sus
esfuerzos?"""

ingresos_t = [] #[nombre del ingreso, ingreso numerico]
def ingresos_totales(lista, nombre):
    valor = 0
    for linea in lista:
        valor += int(linea[9])
    ingresos_t.append([nombre, valor])
ingresos_totales(lista_datos, "Ingresos totales")       #indice [0][1] en la lista ingresos_t
ingresos_totales(exportaciones, "Ingresos totales de exportaciones")     #indice [1][1] en la lista ingresos_t
ingresos_totales(importaciones, "Ingresos totales de importaciones")     #indice [2][1] en la lista ingresos_t
#
ingresos_t[0].append(100)   #agregamos el porcentaje 100 de los ingresos totales
porcentajes_im_exp = [ingresos_t[0]]    #[[nombre del ingreso1, ingreso numerico1, porcentaje1],...]
porcent = 0
for ingreso in ingresos_t:
    if ingreso[1] == ingresos_t[0][1]:
        continue
    else:
        porcent = (ingreso[1]*100)/ingresos_t[0][1]
        porcentajes_im_exp.append([ingreso[0], ingreso[1], porcent])
escritor_csv("Porcentajes de ingresos totales.csv", porcentajes_im_exp)

#Cuenta las repeticiones de los paises que generan ganancias 
#y suma el ingreso de cada pais al iterar, para obtener el ingreso total por pais
#Con este se obtiene el porcentaje de ingreso por pais con respecto al ingreso total 
#de importaciones y exporaciones        
conteo_paises = [] #[[pais1, direccion, porcentaje1],...]
def ingresos(direccion, origen_o_destino):
    paises_contados = []
    for pais in direccion:
        contador = 0
        ingreso_por_pais = 0
        if pais[origen_o_destino] not in paises_contados:
            for movimiento in direccion:
                if pais[origen_o_destino] == movimiento[origen_o_destino]:
                    contador += 1
                    ingreso_por_pais += int(movimiento[9])
            porcentaje = (ingreso_por_pais*100)/ingresos_t[0][1]
            paises_contados.append(pais[origen_o_destino])
            conteo_paises.append([pais[origen_o_destino], pais[1], porcentaje])
    conteo_paises.sort(reverse = True, key = lambda x:x[2])
#llamando la funcion ingresos    
ingresos(exportaciones, 2)
ingresos(importaciones, 3)

#el siguiente for suma los porcentajes de los elementos superiores hacia los inferiores
#asi podremos ver que paises general el 80% de ingresos y ver los que generan el 20% restante
#no genero solo el 80% con un if porque podria ser de interes ver los demas paises 
#y comparar con las otras consignas
suma_porcentaje = 0
ingresos80 = [] #[[pais1, direccion, ingreso1, suma de porcentajes anteriores hasta ese pais]]
for porcentaje in conteo_paises:
    suma_porcentaje += porcentaje[2]
    ingresos80.append([porcentaje[0], porcentaje[1], porcentaje[2], suma_porcentaje])
escritor_csv("Paises generadores del 80%.csv", ingresos80)
        
    
        





