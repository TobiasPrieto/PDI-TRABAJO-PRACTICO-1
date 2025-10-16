import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv



# EJERCICIO 2 -------------------------------------------------------------------------------------------------




def separar_renglones(img):
    '''
    Esta función toma como argumento una imagen de tipo 'uint8' identifica los renglones y devuelve una lista de diccionarios 
    que contienen para cada renglón encontrado el numero de renglón y un crop del mismo.
    '''

    # Binarizo la imagen
    img_bool = img < 100

    # Analizo filas
    img_row_zeros_idxs = np.argwhere(img_bool.sum(axis=1) > 500)

    # Duplicar todos los indices de las filas excepto el primero y el ultimo (cada renglon empieza donde termina el anterior)
    idx = np.arange(len(img_row_zeros_idxs))
    repeats = np.where((idx == 0) | (idx == len(img_row_zeros_idxs)-1), 1, 2)
    nuevo = np.repeat(img_row_zeros_idxs, repeats)

    # De esta manera, cada fila de r_idxs contiene el inicio y final de cada renglón
    r_idxs = np.reshape(nuevo, (-1, 2))
                                    
    # Recortar y guardar los renglones                           
    renglones = []
    for ir, idxs in enumerate(r_idxs):
        renglones.append({"Nro renglon": ir+1, "img": img[idxs[0]+2:idxs[1]-2, :]})

    return renglones

def separar_columnas(img):
    '''
    Esta función toma como argumento una imagen de tipo 'uint8' y devuelve una lista de diccionarios 
    que contienen para cada columna encontrada el numero y un crop de la misma.
    '''
    # Binarizo la imagen
    img_bool = img < 100
    # Analizo columnas
    img_col_zeros_idxs = np.argwhere(img_bool.sum(axis=0) > 35)

    # Duplicar todos los indices de las columnas excepto la primera y la ultima 
    idx = np.arange(len(img_col_zeros_idxs))
    repeats = np.where((idx == 0) | (idx == len(img_col_zeros_idxs)-1), 1, 2)
    nuevo = np.repeat(img_col_zeros_idxs, repeats)

    # Cada columna contiene el inicio y fin de cada una
    c_idxs = np.reshape(nuevo, (-1, 2))

    # Si detecta que hay 3 bloques de contenido, fusiona los ultimos dos
    if len(c_idxs) == 3:
        c_idxs = np.vstack((c_idxs[0], [c_idxs[1, 0], c_idxs[2, 1]]))

    # Recortar y guardar las columnas
    columnas = []
    for ic, idxs in enumerate(c_idxs):
        columnas.append({"Nro columna": ic+1, "img": img[: , idxs[0]+2:idxs[1]-2]})

    return columnas

def separar_campos(ruta: str):
    '''
    Esta función toma como argumento la ruta de ubicacion de una imagen 'uint8', lee la imagen en escala de grises, identifica las filas y columnas 
    y devuelve una lista de diccionarios que contienen para cada campo encontrado el numero, el nombre del campo y un crop del mismo.
    '''

    # Carga la imagen
    img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

    # Llama a la primer funcion
    renglones = separar_renglones(img)

    # Para cada renglon ejecuta separar_columnas
    campos = []
    for renglon in renglones:
        campos.append(separar_columnas(renglon["img"]))

    nombres_campos = ['Formulario', 'Nombre y Apellido', 'Contenido Nombre y Apellido', 'Edad', 'Contenido Edad', 'Mail', 'Contenido Mail', 'Legajo', 'Contenido Legajo', 'Espacio en blanco', 'Si_No', 'Pregunta 1', 'Contenido Pregunta 1', 'Pregunta 2', 'Contenido Pregunta 2','Pregunta 3', 'Contenido Pregunta 3', 'Comentarios', 'Contenido Comentarios']

    # Crea una lista de diccionarios donde guarda cada recorte 
    figuras_finales = []
    nro_figura = 1
    nro_nombre = 0
    for renglon in campos:
        for columna in renglon:
            figuras_finales.append({"Nro figura" : nro_figura, "Nombre figura" : nombres_campos[nro_nombre], "img" : columna['img']})
            nro_figura += 1
            nro_nombre +=1

    return figuras_finales

def analizar_campo(img):

    # Binariza la imagen y la invierte
    img_bool = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]

    # Detecta componentes
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_bool, connectivity=8)

    min_area = 5  # Area minima a tener en cuenta
    componentes_validos = []

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        
        # Filtrar líneas verticales (ancho <= 3 píxeles y altura > ancho)
        es_linea_vertical = w <= 1 and h > w
        
        if area >= min_area and not es_linea_vertical:
            componentes_validos.append({
                'label': i,
                'x': stats[i, cv2.CC_STAT_LEFT],
                'y': stats[i, cv2.CC_STAT_TOP],
                'w': w,
                'h': h,
                'area': area,
                'centroid_x': centroids[i][0]
            })

    componentes_validos.sort(key=lambda c: c['centroid_x'])
    
    # Contar caracteres
    num_caracteres = len(componentes_validos)
    
    # Detectar palabras basándose en espacios horizontales
    num_palabras = 0
    tiene_espacios = False


    if num_caracteres > 0:
        num_palabras = 1  # Al menos hay una palabra si hay caracteres
        
        # Calcular el ancho promedio de los caracteres
        anchos = [c['w'] for c in componentes_validos]
        ancho_promedio = np.mean(anchos) if anchos else 0
        
        # Umbral para detectar espacios entre palabras
        umbral_espacio = ancho_promedio * 0.5
        
        for i in range(len(componentes_validos) - 1):
            actual = componentes_validos[i]
            siguiente = componentes_validos[i + 1]
            
            # Calcular distancia entre componentes
            distancia = siguiente['x'] - (actual['x'] + actual['w'])
            
            if distancia > umbral_espacio:
                num_palabras += 1
                tiene_espacios = True
    
    return {'caracteres': num_caracteres,'palabras': num_palabras,'tiene_espacios': tiene_espacios}

def ultima_letra_es_A (img):

    # Binarizo e invierto la imagen
    img_bool = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]

    # Llamamos a la funcino findContours para detectar huecos en la letra del formulario
    contours, hierarchy = cv2.findContours(img_bool, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    x, y, w, h = cv2.boundingRect(contours[-1])

    # Segmenta la letra
    letra = img_bool[y:y+h, x:x+w]

    # Contar huecos internos
    cont_int, hier = cv2.findContours(letra, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    num_huecos = sum(1 for h in hier[0] if h[3] != -1)

    # Si la letra tiene un solo hueco indica que es A sino es B
    if num_huecos == 1:
        return True
    else:
        return False

def informe_formulario(ruta: str):

    # Guarda en la variable la lista de diccionarios de la funcion
    campos = separar_campos(ruta)

    # Guardamos en una lista los nombres que luego usaremos en validacion
    nombres_campos_a_validar = ['Formulario', 'Contenido Nombre y Apellido', 'Contenido Edad', 'Contenido Mail', 'Contenido Legajo',
                                'Contenido Pregunta 1', 'Contenido Pregunta 2', 'Contenido Pregunta 3', 'Contenido Comentarios']

    # Si el nombre de la figura es uno de los campos validar los guarda en campos_relevantes
    campos_relevantes = []
    for campo in campos:
        if campo['Nombre figura'] in nombres_campos_a_validar:
            campos_relevantes.append(campo)

    # Realiza la validacion sobre todos los relevantes 
    for campo in campos_relevantes:
        img = campo['img']
        metricas_imagen = analizar_campo(img)
        campo['cantidad_caracteres'] = metricas_imagen['caracteres']
        campo['cantidad_palabras'] = metricas_imagen['palabras']
        campo['tiene_espacios'] = metricas_imagen['tiene_espacios']

        if  campo['Nombre figura'] == 'Formulario':
            if ultima_letra_es_A(img):
                campo['Tipo_form'] = 'A'
            else:
                campo['Tipo_form'] = 'B'

        elif campo['Nombre figura'] == 'Contenido Nombre y Apellido':
            if (campo['cantidad_caracteres'] > 25) | (campo['cantidad_palabras'] < 2):
                campo['status'] = 'MAL'
            else: 
                campo['status'] = 'OK'

        elif campo['Nombre figura'] == 'Contenido Edad':
            if (campo['cantidad_caracteres'] < 2) | (campo['cantidad_caracteres'] > 3 ) | (campo['tiene_espacios']):
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'

        elif campo['Nombre figura'] == 'Contenido Mail':
            if (campo['tiene_espacios']) | (campo['cantidad_caracteres'] > 25):
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'
        
        elif campo['Nombre figura'] == 'Contenido Legajo':
            if (campo['cantidad_caracteres'] != 8 ) |  (campo['tiene_espacios']):
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'


        elif campo['Nombre figura'] == 'Contenido Pregunta 1':
            if campo['cantidad_caracteres'] != 1:
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'

        elif campo['Nombre figura'] == 'Contenido Pregunta 2':
            if campo['cantidad_caracteres'] != 1:
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'

        elif campo['Nombre figura'] == 'Contenido Pregunta 3':
            if campo['cantidad_caracteres'] != 1:
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'

        elif campo['Nombre figura'] == 'Contenido Comentarios':
            if (campo['cantidad_caracteres']  < 1 ) |  (campo['cantidad_caracteres'] > 25):
                campo['status'] = 'MAL'
            else:
                campo['status'] = 'OK'


        nombre = campo['Nombre figura'].replace("Contenido ", "")
        if 'status' in campo:
            print(f"{nombre}: {campo['status']}")
        elif 'Tipo_form' in campo:
            print(f"{nombre}: {campo['Tipo_form']}")


    if all(i.get("status") == "OK" for i in campos_relevantes if "status" in i):
        estado_formulario = 'OK'
    else:
        estado_formulario = 'MAL'

    img_nombre = campos_relevantes[1]['img']
    status_nombre = campos_relevantes[1]['status']
    status_edad = campos_relevantes[2]['status']
    status_mail = campos_relevantes[3]['status']
    status_legajo = campos_relevantes[4]['status']
    status_preg_1 = campos_relevantes[5]['status']
    status_preg_2 = campos_relevantes[6]['status']
    status_preg_3 = campos_relevantes[7]['status']
    status_comentario = campos_relevantes[8]['status']
    formulario_id =  ruta.split('_')[1].split('.')[0]

    # Devuelve un diccionario con los resultados
    return {"ID Formulario" : formulario_id, "Nombre Formulario" : ruta, "img_nombre": img_nombre, "Estado formulario" : estado_formulario,
            "Nombre y Apellido" : status_nombre, "Edad": status_edad, "Mail": status_mail, "Legajo": status_legajo, "Pregunta 1": status_preg_1, "Pregunta 2": status_preg_2,
            "Pregunta 3": status_preg_3, "Comentarios": status_comentario}

def mostrar_formularios(formularios):
    # Separar los formularios por estado
    ok_forms = [f for f in formularios if f['Estado formulario'] == 'OK']
    mal_forms = [f for f in formularios if f['Estado formulario'] == 'MAL']

    # Cantidad de filas (el grupo más grande)
    n_filas = max(len(ok_forms), len(mal_forms))
    n_cols = 2

    fig, axes = plt.subplots(n_filas, n_cols, figsize=(10, 3 * n_filas))
    fig.suptitle("Validación de Formularios", fontsize=16, y=0.98)

    # Asegurar que axes sea 2D
    if n_filas == 1:
        axes = axes.reshape(1, -1)

    for i in range(n_filas):
        # Columna 0 → OK
        ax_ok = axes[i, 0]
        if i < len(ok_forms):
            f_ok = ok_forms[i]
            ax_ok.imshow(f_ok['img_nombre'], cmap='gray', vmin= 0, vmax=255)
            ax_ok.set_title(f_ok['Nombre Formulario'], fontsize=10)
        ax_ok.axis('off')

        # Columna 1 → MAL
        ax_mal = axes[i, 1]
        if i < len(mal_forms):
            f_mal = mal_forms[i]
            ax_mal.imshow(f_mal['img_nombre'], cmap='gray', vmin= 0, vmax=255)
            ax_mal.set_title(f_mal['Nombre Formulario'], fontsize=10)
        ax_mal.axis('off')

    # Títulos de las columnas (una sola vez arriba)
    fig.text(0.25, 0.97, "OK", ha='center', va='bottom', fontsize=12, fontweight='bold')
    fig.text(0.75, 0.97, "MAL", ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show(block=False)

def comprobar_formularios(formularios: list):
    # Para cada formulario guarda su resultado en la nueva lista y los muestra en pantalla
    resultados = []
    for formulario in formularios:
        print(f'Resultados para el formulario: {formulario} \n')
        resultados.append(informe_formulario(formulario))
        print('\n')

    mostrar_formularios(resultados)

    # Genera un archivo csv con el resultado de las validaciones
    columnas = ['ID', 'Nombre y Apellido', 'Edad', 'Mail', 'Legajo', "Pregunta 1", "Pregunta 2", "Pregunta 3", "Comentarios"]

    with open('resultados_formularios.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        for r in resultados:
            writer.writerow({
                'ID': r['ID Formulario'],
                'Nombre y Apellido': r['Nombre y Apellido'],
                'Edad': r['Edad'],
                'Mail': r['Mail'],
                'Legajo': r['Legajo'],
                'Pregunta 1': r['Pregunta 1'],
                'Pregunta 2': r['Pregunta 2'],
                'Pregunta 3': r['Pregunta 3'],
                'Comentarios': r['Comentarios']
            })



# Poner en la lista la ruta a los formularios a analizar
ruta_formularios = ['formulario_01.png','formulario_02.png', 'formulario_03.png', 'formulario_04.png', 'formulario_05.png']
comprobar_formularios(ruta_formularios)

