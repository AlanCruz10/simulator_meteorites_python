# # import numpy as np
# # import matplotlib.pyplot as plt
# # import tkinter as tk
# # from tkinter import simpledialog
# #
# # def caida_meteorito(x, z, lambda_param):
# #     t = np.random.poisson(lambda_param)
# #     for i in range(t):
# #         x.append(x[-1] + np.random.uniform(-1, 1))  # Cambio aleatorio en la posición x
# #         z.append(z[-1] - 1)  # Decremento en la posición z
# #
# # def calcular_y_graficar():
# #     x_inicial = float(entry_x.get())
# #     z_inicial = float(entry_z.get())
# #     lambda_param = float(entry_lambda.get())
# #
# #     x = [x_inicial]
# #     z = [z_inicial]
# #
# #     caida_meteorito(x, z, lambda_param)
# #
# #     plt.plot(x, z)
# #     plt.xlabel('Posición x')
# #     plt.ylabel('Posición z')
# #     plt.title('Trayectoria de caída del meteorito')
# #     plt.grid(True)
# #     plt.show()
# #
# # # Crear la interfaz gráfica
# # root = tk.Tk()
# # root.title('Cálculo de Trayectoria de Caída del Meteorito')
# #
# # # Entradas para las coordenadas iniciales y lambda
# # label_x = tk.Label(root, text='Posición inicial x:')
# # entry_x = tk.Entry(root)
# # label_z = tk.Label(root, text='Posición inicial z:')
# # entry_z = tk.Entry(root)
# # label_lambda = tk.Label(root, text='Lambda para la distribución de Poisson:')
# # entry_lambda = tk.Entry(root)
# #
# # # Botón para calcular y graficar
# # calculate_button = tk.Button(root, text='Calcular y Graficar', command=calcular_y_graficar)
# #
# # # Colocar elementos en la ventana
# # label_x.pack()
# # entry_x.pack()
# # label_z.pack()
# # entry_z.pack()
# # label_lambda.pack()
# # entry_lambda.pack()
# # calculate_button.pack()
# #
# # # Iniciar el bucle de la interfaz gráfica
# # root.mainloop()
# #
# #
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import tkinter as tk
# from tkinter import simpledialog
#
#
# def caida_meteorito(x, z):
#     t = np.random.poisson(60)
#     print(f'El valor del tiempo es {t}')
#     for i in range(t):
#         x_change = np.random.normal(loc=0, scale=1)
#         x.append(x[-1] + x_change)
#
#         z.append(z[-1] - 1)  # Decremento en la posición z
#         if z[-1] <= 0:
#             return len(z) - 1, x[-1]  # Retorna el tiempo y la posición en x cuando z <= 0
#     return -1, "No llego a tocar el suelo"  # Valor predeterminado cuando el meteorito no llega a z=0
#
#
# def calcular_y_graficar(entry_x, entry_z):
#     x_inicial = float(entry_x.get())
#     z_inicial = float(entry_z.get())
#
#     x = [x_inicial]
#     z = [z_inicial]
#
#     tiempo_llegada, posicion_x_llegada = caida_meteorito(x, z)
#
#     data = {
#         'X': x[:-1],
#         'X*': x[1:],
#         'Z': z[:-1],
#         'Z*': z[1:]
#     }
#
#     df = pd.DataFrame(data)
#
#     print("Tabla de valores:")
#     print(df)
#
#     print(f"\nEl meteorito llegó a z=0 en el tiempo: {tiempo_llegada} y posición en x: {posicion_x_llegada}")
#
#     plt.plot(x, z)
#     plt.xlabel('Posición x')
#     plt.ylabel('Posición z')
#     plt.title('Trayectoria de caída del meteorito')
#     plt.grid(True)
#     plt.show()
#
#
# # Crear la interfaz gráfica
# root = tk.Tk()
# root.title('Cálculo de Trayectoria de Caída del Meteorito')
#
# # Entradas para las coordenadas iniciales y lambda
# label_x = tk.Label(root, text='Posición inicial x:')
# entry_x = tk.Entry(root)
# label_z = tk.Label(root, text='Posición inicial z:')
# entry_z = tk.Entry(root)
#
# # Botón para calcular y graficar
# calculate_button = tk.Button(root, text='Calcular y Graficar', command=lambda: calcular_y_graficar(entry_x, entry_z))
#
# # Colocar elementos en la ventana
# label_x.pack()
# entry_x.pack()
# label_z.pack()
# entry_z.pack()
# calculate_button.pack()
#
# # Iniciar el bucle de la interfaz gráfica
# root.mainloop()
import matplotlib.pyplot as plt

# Datos para las líneas 1 y 2 con diferentes longitudes
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 3, 6, 5]

x2 = [-3, -2, -1, 0, 1, 2]
y2 = [5, 3, 4, 2, 1, 4]

# Crear la figura y los ejes
fig, ax = plt.subplots()

# Graficar las líneas
ax.plot(x1, y1, label='Línea 1', color='blue', linestyle='--', marker='o', markersize=8)
ax.plot(x2, y2, label='Línea 2', color='red', linestyle='-', marker='s', markersize=8)

# Personalizar los ejes, etiquetas y título (opcional)
ax.set_xlabel('Eje x', fontsize=12)
ax.set_ylabel('Eje z', fontsize=12)
ax.set_title('Plano Cartesiano con Múltiples Líneas', fontsize=14)

# Personalizar la cuadrícula (opcional)
ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

# Ajustar los límites del eje x para mostrar la parte negativa
ax.set_xlim(-4, 6)

# Mover el eje y a la posición x=0
ax.spines['left'].set_position('zero')
ax.spines['left'].set_color('gray')

# Eliminar el eje derecho y superior
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Añadir una leyenda (opcional)
# ax.legend(loc='upper left', fontsize=10)

# Ajustar el espaciado entre los elementos del gráfico (opcional)
plt.tight_layout()

# Mostrar el gráfico
plt.show()

#
#
# simulated_fall.destroy()
#
# fig, ax = plt.subplots()
# canvas_graphic = FigureCanvasTkAgg(fig, master=window)
# canvas_graphic.draw()
# # print(list_meteorites)
#
# for meteorite in list_meteorites:
#     id = int(meteorite["id"])
#     xo = int(meteorite["coordinate_x"])
#     zo = int(meteorite["coordinate_z"])
#     probability_explosion = float(meteorite["probability_explosion"])
#     parts_explodes = int(meteorite["parts_explodes"])
#     trajectory_x, trajectory_z, trajectory_z_noise, trajectory_x_noise = fall_meteorite(xo, zo,
#                                                                                         probability_explosion,
#                                                                                         parts_explodes, id)
#     print(trajectory_x, trajectory_z, "trayectorias")
#
#     ax.plot(trajectory_x, trajectory_z, marker="_")
#     ax.plot(trajectory_x_noise, trajectory_z_noise, linestyle="dashed")
#
#     min_traject_x = min(trajectory_x)
#     max_traject_x = max(trajectory_x)
#     max_traject_z = max(trajectory_z)
#     min_traject_z = min(trajectory_z)
#
#     min_z.append(min_traject_z)
#     min_x.append(min_traject_x)
#     max_z.append(max_traject_z)
#     max_x.append(max_traject_x)
#
#     min_min_z = min(min_z)
#     min_min_x = min(min_x)
#     max_max_z = max(max_z)
#     max_max_x = max(max_x)
#
#     meteorite["x_noise"] = trajectory_x_noise
#     meteorite["z_noise"] = trajectory_z_noise
#
# if float(min_min_z) <= 0:
#     ax.spines['left'].set_position('zero')
#     ax.spines['left'].set_color('gray')
#     limit_negative = (0 - (float(min_min_z) - 1)) * 1
#     print(limit_negative, "unu")
#     ax.set_ylim(-limit_negative, float(max_max_z) + 1)
# else:
#     ax.set_xlim(0, float(max_max_z) + 1)
#
# if float(min_min_x) <= 0:
#     ax.spines['bottom'].set_position('zero')
#     ax.spines['bottom'].set_color('gray')
#     limit_negative = (0 - (float(min_min_x) - 1)) * 1
#     ax.set_xlim(-limit_negative, float(max_max_x) + 1)
# else:
#     ax.set_xlim(0, float(max_max_x) + 1)
#
# ax.set_xlabel('Coordenada x', fontsize=12)
# ax.set_ylabel('Coordenada z', fontsize=12)
# ax.set_title('Gráfico de Meteoritos', fontsize=14)
# ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# canvas_graphic.draw()
#
# # Place the canvas in the tkinter window
# canvas_graphic.get_tk_widget().place(anchor="c", width=600, height=412, x=500, y=400, bordermode="inside")


# global min_traject_x, max_traject_x, min_traject_z, max_traject_z, trajectory_x, trajectory_z, min_min_z,
    # max_max_z, max_max_x, min_min_x

def fall_meteorite(xo, zo, probability_explosion, parts_explodes, id):
    # xo_copy = xo.copy()
    # zo_copy = zo.copy()
    trajectory_x = [xo]
    trajectory_x_noise = [xo]
    trajectory_z = [zo]
    trajectory_z_noise = [zo]
    # time_one_minute = np.random.poisson(60)
    # print("time", time_one_minute)
    # for i in range(time_one_minute):
        # x_uniform = np.random.uniform(low=trajectory_x[-1], high=trajectory_x[-1]+1)
        # z_uniform = np.random.uniform(low=trajectory_z[-1], high=trajectory_z[-1]+1)
        # x_change = np.random.normal(loc=0, scale=1)
        # z_change = np.random.normal(loc=-1, scale=1)
        # print(trajectory_x[-1])
        # print(trajectory_z[-1])
        # trajectory_x_noise.append(trajectory_x[-1] + (x_change * (i / 60)))
        # trajectory_x.append(trajectory_x[-1] + x_change)
        # value, event = explosion_before_fall(trajectory_z[-1], probability_explosion, parts_explodes)
        # trajectory_z_noise.append(trajectory_z[-1] + (z_change * (i / 60)))
        # trajectory_z.append(trajectory_z[-1] - 1)
        # print(value, event)
        # if trajectory_z[-1] <= 0:
        #     return trajectory_x, trajectory_z, trajectory_z_noise, trajectory_x_noise
    #     if value is int and event == "meteorito":
    #         for e in range(value):
    #             new_meteorite = create_new_meteorite(id + e + 1, trajectory_x[-1], trajectory_z[-1])
    #             print(new_meteorite, "nuevo meteorito")
    #
    #             # fall_meteorite()
    #             # si explosion es un numero hay que graficar estas exlosionce en el punto exacto de donde exploto el anterior
    #             # generar nuevos valores a partir de las ultimas coordenadas de la exposion
    #             # es decir una nuevas x, y porbabilidades que en realidad va a ser 0 para que no vuelvan a explotar y
    #             # y nueva cantidad parts en las que explotara pero sera 0 para que no vuelva a explotar
    #             print(e, "numero de meteorito real")
    #         print(list_meteorite, "lista de meteorite")
    #     elif value == 0 and event == "exploto":
    #         # si exploto deberia de terminar el porceso de trayectoria de este meteorito y graficar solo hasta donde se quedo
    #         # o guardar el arreglo solo hassta loss datos donde se quedo y si hay mas meteoritos que no han explotado
    #         # que continuen su trayecto
    #         print("meteorito exploto")
    #         break
    #     elif value == 0 and event == "no exploto":
    #         # debe continuar el proceso de graficacion del trayecto o el array para poder graficarlo
    #         print("no exploto el meteorito")
    #         continue
    #     print(x_change, z_change, trajectory_x[-1], trajectory_z[-1], "datos iniciales")
    # # print(x_change, z_change, trajectory_x[-1], trajectory_z[-1], "datos iniciales")
    #
    #     trajectory_z_noise.append(trajectory_z[-1] + (z_change * (i / 60)))
    #     trajectory_z.append(trajectory_z[-1] - 1)
    # return trajectory_x, trajectory_z