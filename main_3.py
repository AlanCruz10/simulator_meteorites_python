# import math
# import random
# import sys
# import tkinter as tk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
#
# def calculate_trajectory():
#     return random.randint(0, 360)
#
#
# def calculate_coordinate_x(altitude, tan_x):
#     coordinate_x = altitude / tan_x
#     return coordinate_x
#
#
# def calculate_coordinate_y(coordinate_x, tan_y):
#     coordinate_y = tan_y * coordinate_x
#     return coordinate_y
#
#
# def quadrant_validation(angle):
#     if 0 <= angle <= 90:
#         return angle
#     elif 90 < angle <= 180:
#         return 180 - angle
#     elif 180 < angle <= 270:
#         return 90 - (270 - angle)
#     elif 270 < angle <= 360:
#         return 360 - angle
#     else:
#         print("Error")
#
#
# def calculate_x(plane, altitude):
#     tan_x = math.tan(math.radians(plane[1]))
#
#     coordinate_x = calculate_coordinate_x(altitude, tan_x)
#
#     # print(coordinate_x, tan_x)
#
#     if plane[2] == "-" and coordinate_x > 0:
#         return coordinate_x * -1
#     elif plane[2] == "-" and coordinate_x < 0:
#         return coordinate_x
#     elif plane[2] == "+" and coordinate_x > 0:
#         return coordinate_x
#     elif plane[2] == "+" and coordinate_x < 0:
#         return coordinate_x * -1
#
#
# def calculate_y(plane, coordinate_x):
#     tan_y = math.tan(math.radians(plane[0]))
#
#     coordinate_y = round(calculate_coordinate_y(coordinate_x, tan_y))
#
#     # print(coordinate_y, tan_y)
#     print(plane[3])
#     print(coordinate_y)
#     if plane[3] == "-" and coordinate_y > 0:
#         y_ = coordinate_y * -1
#         if coordinate_y < 0.1:
#             return 0
#         else:
#             return y_
#     elif plane[3] == "-" and coordinate_y < 0:
#         y = coordinate_y
#         if coordinate_y > -0.1:
#             return 0
#         else:
#             return y
#     elif plane[3] == "+" and coordinate_y > 0:
#         y1 = coordinate_y
#         if coordinate_y < 0.1:
#             return 0
#         else:
#             return y1
#     elif plane[3] == "+" and coordinate_y < 0:
#         coordinate_y_ = coordinate_y * -1
#         if coordinate_y > -0.1:
#             return 0
#         else:
#             return coordinate_y_
#
#
# def validate_coordinate(alpha_angle, beta_angle):
#     plane_xy = None
#     if 0 <= alpha_angle <= 90 and 0 <= beta_angle <= 90:
#         plane_xy = alpha_angle, beta_angle, "+", "+"
#     elif 0 <= alpha_angle <= 90 < beta_angle <= 180:
#         plane_xy = alpha_angle, 180 - beta_angle, "+", "+"
#     elif 180 >= alpha_angle > 90 >= beta_angle >= 0:
#         plane_xy = 180 - alpha_angle, beta_angle, "-", "+"
#     elif 90 < alpha_angle <= 180 and 90 < beta_angle <= 180:
#         plane_xy = 180 - alpha_angle, 180 - beta_angle, "-", "+"
#     elif 180 < alpha_angle <= 270 and 0 <= beta_angle <= 90:
#         plane_xy = 270 - alpha_angle, beta_angle, "-", "-"
#     elif 270 >= alpha_angle > 180 >= beta_angle > 90:
#         plane_xy = 270 - alpha_angle, 180 - beta_angle, "-", "-"
#     elif 270 < alpha_angle <= 360 and 0 <= beta_angle <= 90:
#         plane_xy = 360 - alpha_angle, beta_angle, "+", "-"
#     elif 270 < alpha_angle <= 360 and 90 < beta_angle <= 180:
#         plane_xy = 360 - alpha_angle, 180 - beta_angle, "+", "-"
#     else:
#         print("Error")
#         sys.exit(0)
#     return plane_xy
#
#
# def main():
#     def draw_point(canvas, x, y):
#         # Ajustar las coordenadas al sistema del canvas (origen en la esquina superior izquierda)
#         x = x + canvas_width // 2
#         y = canvas_height // 2 - y
#
#         # Dibujar un punto en el canvas
#         canvas.create_oval(x, y, x + 5, y + 5, fill="red")
#
#     def draw_cartesian_plane(canvas):
#         # Dibujar los ejes x e y
#         canvas.create_line(0, canvas_height // 2, canvas_width, canvas_height // 2, fill="black")
#         canvas.create_line(canvas_width // 2, 0, canvas_width // 2, canvas_height, fill="black")
#
#         # Dibujar las marcas del eje x y etiquetas
#         for x in range(-canvas_width // 2, canvas_width // 2, 20):
#             x_pixel = canvas_width // 2 + x
#             canvas.create_line(x_pixel, canvas_height // 2 - 5, x_pixel, canvas_height // 2 + 5, fill="black")
#             canvas.create_text(x_pixel, canvas_height // 2 + 15, text=str(x), anchor="center")
#
#         # Dibujar las marcas del eje y y etiquetas
#         for y in range(-canvas_height // 2, canvas_height // 2, 20):
#             y_pixel = canvas_height // 2 - y
#             canvas.create_line(canvas_width // 2 - 5, y_pixel, canvas_width // 2 + 5, y_pixel, fill="black")
#             canvas.create_text(canvas_width // 2 + 15, y_pixel, text=str(y), anchor="center")
#
#     def draw_point_from_input():
#         try:
#             altura = float(altura_input.get())
#             masa = float(masa_input.get())
#             angulo_xy = float(angulo_xy_input.get())
#             angulo_xz = float(angulo_xz_input.get())
#             velocidad = float(velocidad_input.get())
#
#             if altura < 0:
#                 print("Error")
#                 sys.exit(0)
#
#             plane_xy = validate_coordinate(angulo_xy, angulo_xz)
#
#             print(plane_xy)
#
#             coordinate_x = calculate_x(plane_xy, altura)
#
#             coordinate_y = calculate_y(plane_xy, coordinate_x)
#
#             trajectory = calculate_trajectory()
#
#             print(masa, velocidad, coordinate_x, coordinate_y, altura, angulo_xy, angulo_xz, trajectory)
#
#             # Calcular las coordenadas x e y del punto en el plano cartesiano
#             # (Reemplazar por las operaciones para sacar los calculos)
#
#             draw_point(canvas, coordinate_x, coordinate_y)
#         except ValueError:
#             # Si los valores ingresados no son válidos, ignoramos el dibujo del punto.
#             pass
#
#     # Configuración de la ventana
#     window = tk.Tk()
#     window.title("Dibujar Punto en Plano Cartesiano")
#     canvas_width = 400
#     canvas_height = 400
#     tk.Label(text="plano xy")
#     canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, background="blue")
#     canvas.pack(side=tk.LEFT)
#
#     # Widgets para ingresar las coordenadas y parámetros
#     tk.Label(window, text="Altura:").pack()
#     altura_input = tk.Entry(window)
#     altura_input.pack()
#
#     tk.Label(window, text="Masa:").pack()
#     masa_input = tk.Entry(window)
#     masa_input.pack()
#
#     tk.Label(window, text="Ángulo (xy):").pack()
#     angulo_xy_input = tk.Entry(window)
#     angulo_xy_input.pack()
#
#     tk.Label(window, text="Ángulo (xz):").pack()
#     angulo_xz_input = tk.Entry(window)
#     angulo_xz_input.pack()
#
#     tk.Label(window, text="Velocidad:").pack()
#     velocidad_input = tk.Entry(window)
#     velocidad_input.pack()
#
#     # Botón para dibujar el punto
#     draw_button = tk.Button(window, text="Aceptar", command=draw_point_from_input)
#     draw_button.pack()
#
#     # Dibujar el plano cartesiano
#     draw_cartesian_plane(canvas)
#     window.mainloop()
#
#     # mass = float(input("Ingresa la masa del meteorito (kg): "))
#     # speed = float(input("Ingresa la velocidad inicial del meteorito (m/s): "))
#     # alpha_angle = float(input("Ingresa el ángulo inicial en el eje x y y (grados): "))
#     # beta_angle = float(input("Ingresa el ángulo inicial en el eje x y z (grados): "))
#     # altitude = float(input("Ingresa la altura desde donde cae el meteorito o z (m): "))
#
#
# if __name__ == "__main__":
#     main()

import random
import numpy as np


# aqui no se que hacer con las tablas generadas xd no se si guaradaste en arrays como objetos o que xd
def simulate_explosion(z, prob_explode, parts_explodes):
    # impacto en en la tierra
    if z <= 0:
        print("Exploto por probabilidad (z <= 0)")
        return
    # si no impacto checa la probabilidad de explocion usando distribucion uniforme
    prob = random.random()
    if prob < prob_explode / 100:
        if z > 0:
            yes_or_not_explode = random.randint(0, 1)
            # si exploto pero se dividio tanto que es incontable y no causo daño a la tierra
            if yes_or_not_explode == 0:
                print("Se deshizo, exploto pero se deshizo")
            else:
                # aqui genero un numero aleatorio de la cantidad de meteoritos que se dividio el primero
                choice = random.randint(0, 1)
                if choice == 0:
                    random_number = generate_random_number_uniform(parts_explodes)
                    print("Número de en la cual se dividio el meteorito con distribucion uniforme:", random_number)
                else:
                    random_number = generate_random_number_poisson(parts_explodes)
                    print("Número de en la cual se dividio el meteorito con distribucion poisson:", random_number)
        else:
            print("Exploto por probabilidad")
        return
    # no se que hacer con los demas datos xd


# numero aleatorio con distribucion uniforme de acuerdo a lo que el usuario piensa que se va a dividir
def generate_random_number_uniform(parts_explodes):
    return random.randint(2, parts_explodes)


# numeero aleatorio con disribucion poisson de acuerdo a lo que el usuario considera como media de explocion
def generate_random_number_poisson(parts_explodes):
    return np.random.poisson(parts_explodes)
