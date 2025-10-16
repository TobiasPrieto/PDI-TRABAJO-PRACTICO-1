import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv


# EJERCICIO 1 -------------------------------------------------------------------------------------------------

def ecualizacion_local(img, M, N):
    
    # Guardamos el tamaño del espacio que tendra la expansion de la imagen
    # en nuestro caso se expandira la mitad del tamaño de la ventana
    pad_y = M // 2
    pad_x = N // 2 

    # Se expande la imagen
    img_expandida = cv2.copyMakeBorder(img, pad_y, pad_y, pad_x, pad_x, borderType=cv2.BORDER_REPLICATE) 

    # Imagen vacia donde se escribiran los resultados
    salida = np.zeros_like(img)  


    # Recorremos filas y columnas
    for i in range(img.shape[0]):       
        for j in range(img.shape[1]):   

            # Se crea la ventana 
            ventana = img_expandida[i:i+M, j:j+N]

            # Calcula el histograma
            hist = cv2.calcHist([ventana], [0], None, [256], [0, 256]).flatten()
        
            # Se calcula suma de distribucion acumulada
            cdf = hist.cumsum()  
            cdf = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
            cdf = cdf.astype('uint8')

            # Se mapea el valor del pixel central de laventana
            valor_original = img_expandida[i+pad_y, j+pad_x]  
            valor_transformado = cdf[valor_original]          

            # Guarda el valor del pixel en la imagen de salida
            salida[i, j] = valor_transformado

    # Devuelve la nueva imagen
    return salida


# Se prueba con 3 tamaños de ventanas distintos para comparar
img = cv2.imread("Imagen_con_detalles_escondidos.tif", cv2.IMREAD_GRAYSCALE)
img_eqh1 = ecualizacion_local(img, 5, 5)
img_eqh2 = ecualizacion_local(img, 15, 15)
img_eqh3 = ecualizacion_local(img, 35, 35)

# Graficamos
ax1 = plt.subplot(232)
plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.title("Imagen Original")

plt.subplot(234, sharex = ax1, sharey = ax1)
plt.imshow(img_eqh1, cmap='gray', vmin=0, vmax=255)
plt.title("Imagen Procesada 1 (Kernel 5x5)")

plt.subplot(235, sharex = ax1, sharey = ax1)
plt.imshow(img_eqh2, cmap='gray', vmin=0, vmax=255)
plt.title("Imagen Procesada 2 (Kernel 15x15)")

plt.subplot(236, sharex = ax1, sharey = ax1)
plt.imshow(img_eqh3, cmap='gray', vmin=0, vmax=255)
plt.title("Imagen Procesada 3 (Kernel 35x35)")
plt.suptitle("Ecualizacion de histograma local")
plt.show()


