# importacines imporantes
import tkinter
import Meteorite
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
import matplotlib.lines as mlines
import mplcursors
import numpy as np
import math

# variables globales
window = tkinter.Tk()
list_meteorite = []
list_meteorite_before = []
list_trajectories_x = []
list_trajectories_z = []
list_before_trajectories_x = []
list_before_trajectories_z = []
min_x = []
min_z = []
max_x = []
max_z = []
see_tables = None
canvas_legend = None

# caractericas de la ventana que se ejecuta
window.geometry("500x500")
window.title("Meteoritos")
window.configure(bg='#%02x%02x%02x' % (101, 47, 185))


def show_tables(time):
    if time == "first":
        canvas_tables = tkinter.Canvas(window, background='#%02x%02x%02x' % (100, 20, 70))
        canvas_tables.pack(fill="both", expand=True)

        scrollbar_vertical = tkinter.Scrollbar(canvas_tables, orient="vertical", command=canvas_tables.yview)
        scrollbar_vertical.pack(side="right", fill="y")

        canvas_tables.configure(yscrollcommand=scrollbar_vertical.set)

        frame_inner = tkinter.Frame(canvas_tables, background='#%02x%02x%02x' % (100, 20, 70))
        canvas_tables.create_window((0, 0), window=frame_inner, anchor="nw")

        df_meteorites_all = pd.DataFrame(list_meteorite)
        df_meteorites_all_drop_u = df_meteorites_all.drop(
            columns=["coordinate_x", "coordinate_z", "probability_explosion", "parts_explodes", "time_minute"])
        # df_meteorites_all_drop = df_meteorites_all.drop(columns=['trajectory_x', 'trajectory_z', 'time_minute',
        # 'trajectory_x_noise', 'trajectory_z_noise'])
        df_meteorites_all_drop = df_meteorites_all.drop(columns=['trajectory_x', 'trajectory_z', 'time_minute'])

        table_title_label = tkinter.Label(frame_inner, text="Tabla de Meteoritos", font=("Arial", 14, "bold"),
                                          bg='#%02x%02x%02x' % (20, 120, 185), fg="white")
        table_title_label.pack(pady=5)

        table_meteorites = ttk.Treeview(frame_inner,
                                        columns=(
                                            "coordinate_x", "coordinate_z", "probability_explosion", "parts_explodes"))
        table_meteorites.heading("#0", text="id")
        table_meteorites.heading("coordinate_x", text="x")
        table_meteorites.heading("coordinate_z", text="z")
        table_meteorites.heading("probability_explosion", text="prob. explo.")
        table_meteorites.heading("parts_explodes", text="part. explo.")

        table_meteorites.column("#0", width=50, anchor="center")
        table_meteorites.column("coordinate_x", width=192, anchor="center")
        table_meteorites.column("coordinate_z", width=192, anchor="center")
        table_meteorites.column("probability_explosion", width=50, anchor="center")
        table_meteorites.column("parts_explodes", width=50, anchor="center")

        table_meteorites.pack(pady=1)

        for index, row in df_meteorites_all_drop.iterrows():
            table_meteorites.insert("", "end", text=row["id"] + 1, values=(
                row["coordinate_x"], row["coordinate_z"], row["probability_explosion"], row["parts_explodes"]))

        for index, row in df_meteorites_all_drop_u.iterrows():
            table_title_label = tkinter.Label(frame_inner, text=f'Meteorito: {index + 1}', font=("Arial", 14, "bold"),
                                              bg='#%02x%02x%02x' % (20, 120, 120), fg="white")
            table_title_label.pack(pady=5)
            table_trajectory = ttk.Treeview(frame_inner,
                                            columns=("trajectory_x", "trajectory_z", "trajectory_xo", "trajectory_zo"))
            table_trajectory.heading("#0", text="id")
            table_trajectory.heading("trajectory_x", text="x")
            table_trajectory.heading("trajectory_z", text="z")
            table_trajectory.heading("trajectory_xo", text="x°")
            table_trajectory.heading("trajectory_zo", text="z°")
            # table_trajectory.heading("trajectory_x_noise", text="trajectory_x_noise")
            # table_trajectory.heading("trajectory_z_noise", text="trajectory_z_noise")

            table_trajectory.column("#0", width=50, anchor="center")
            table_trajectory.column("trajectory_x", width=121, anchor="center")
            table_trajectory.column("trajectory_z", width=121, anchor="center")
            table_trajectory.column("trajectory_xo", width=121, anchor="center")
            table_trajectory.column("trajectory_zo", width=121, anchor="center")
            # table_trajectory.column("trajectory_x_noise", width=121, anchor="center")
            # table_trajectory.column("trajectory_z_noise", width=121, anchor="center")

            table_trajectory.pack(pady=1)
            trajectory_xo = list(row["trajectory_x"][1:])
            trajectory_zo = list(row["trajectory_z"][1:])
            # trajectory_xo.append(0.0) trajectory_zo.append(0.0) for t_index, (x, z, xo, zo) in enumerate(zip(row[
            # "trajectory_x"], row["trajectory_z"], row["trajectory_x_noise"], row["trajectory_z_noise"])):
            for t_index, (x, z, xo, zo) in enumerate(
                    zip(row["trajectory_x"], row["trajectory_z"], trajectory_xo, trajectory_zo)):
                # table_trajectory.insert("", "end", text=t_index + 1, values=(x, z, xo, zo))
                table_trajectory.insert("", "end", text=t_index + 1, values=(x, z, xo, zo))
            table_trajectory.pack(pady=1)

        frame_inner.update_idletasks()
        bbox = canvas_tables.bbox(tkinter.ALL)
        canvas_tables.configure(scrollregion=bbox)

        canvas_tables.place(anchor="nw", width=560, height=738, x=804, y=1, bordermode="inside")
    else:
        canvas_tables = tkinter.Canvas(window, background='#%02x%02x%02x' % (100, 20, 70))
        canvas_tables.pack(fill="both", expand=True)

        scrollbar_vertical = tkinter.Scrollbar(canvas_tables, orient="vertical", command=canvas_tables.yview)
        scrollbar_vertical.pack(side="right", fill="y")

        canvas_tables.configure(yscrollcommand=scrollbar_vertical.set)

        frame_inner = tkinter.Frame(canvas_tables, background='#%02x%02x%02x' % (100, 20, 70))
        canvas_tables.create_window((0, 0), window=frame_inner, anchor="nw")

        df_meteorites_all = pd.DataFrame(list_meteorite)
        print(list_meteorite)
        df_meteorites_all_drop_u = df_meteorites_all.drop(
            columns=["coordinate_x", "coordinate_z", "probability_explosion", "parts_explodes", "time_minute"])
        # df_meteorites_all_drop = df_meteorites_all.drop(columns=['trajectory_x', 'trajectory_z', 'time_minute',
        # 'trajectory_x_noise', 'trajectory_z_noise'])
        df_meteorites_all_drop = df_meteorites_all.drop(columns=['trajectory_x', 'trajectory_z', 'time_minute'])

        table_title_label = tkinter.Label(frame_inner, text="Tabla de Meteoritos", font=("Arial", 14, "bold"),
                                          bg='#%02x%02x%02x' % (20, 120, 185), fg="white")
        table_title_label.pack(pady=5)

        table_meteorites = ttk.Treeview(frame_inner,
                                        columns=(
                                            "coordinate_x", "coordinate_z", "probability_explosion", "parts_explodes"))
        table_meteorites.heading("#0", text="id")
        table_meteorites.heading("coordinate_x", text="x")
        table_meteorites.heading("coordinate_z", text="z")
        table_meteorites.heading("probability_explosion", text="prob. explo.")
        table_meteorites.heading("parts_explodes", text="part. explo.")

        table_meteorites.column("#0", width=50, anchor="center")
        table_meteorites.column("coordinate_x", width=192, anchor="center")
        table_meteorites.column("coordinate_z", width=192, anchor="center")
        table_meteorites.column("probability_explosion", width=50, anchor="center")
        table_meteorites.column("parts_explodes", width=50, anchor="center")

        table_meteorites.pack(pady=1)

        for index, row in df_meteorites_all_drop.iterrows():
            table_meteorites.insert("", "end", text=row["id"] + 1, values=(
                row["coordinate_x"], row["coordinate_z"], row["probability_explosion"], row["parts_explodes"]))

        for index, row in df_meteorites_all_drop_u.iterrows():
            table_title_label = tkinter.Label(frame_inner, text=f'Meteorito: {index + 1}', font=("Arial", 14, "bold"),
                                              bg='#%02x%02x%02x' % (20, 120, 120), fg="white")
            table_title_label.pack(pady=5)
            table_trajectory = ttk.Treeview(frame_inner,
                                            columns=("trajectory_x", "trajectory_z", "trajectory_xo", "trajectory_zo"))
            table_trajectory.heading("#0", text="id")
            table_trajectory.heading("trajectory_x", text="x")
            table_trajectory.heading("trajectory_z", text="z")
            table_trajectory.heading("trajectory_xo", text="x°")
            table_trajectory.heading("trajectory_zo", text="z°")
            # table_trajectory.heading("trajectory_x_noise", text="trajectory_x_noise")
            # table_trajectory.heading("trajectory_z_noise", text="trajectory_z_noise")

            table_trajectory.column("#0", width=50, anchor="center")
            table_trajectory.column("trajectory_x", width=121, anchor="center")
            table_trajectory.column("trajectory_z", width=121, anchor="center")
            table_trajectory.column("trajectory_xo", width=121, anchor="center")
            table_trajectory.column("trajectory_zo", width=121, anchor="center")
            # table_trajectory.column("trajectory_x_noise", width=121, anchor="center")
            # table_trajectory.column("trajectory_z_noise", width=121, anchor="center")

            table_trajectory.pack(pady=1)
            trajectory_xo = list(row["trajectory_x"][1:])
            trajectory_zo = list(row["trajectory_z"][1:])
            # trajectory_xo.append(0.0) trajectory_zo.append(0.0) for t_index, (x, z, xo, zo) in enumerate(zip(row[
            # "trajectory_x"], row["trajectory_z"], row["trajectory_x_noise"], row["trajectory_z_noise"])):
            for t_index, (x, z, xo, zo) in enumerate(
                    zip(row["trajectory_x"], row["trajectory_z"], trajectory_xo, trajectory_zo)):
                # table_trajectory.insert("", "end", text=t_index + 1, values=(x, z, xo, zo))
                table_trajectory.insert("", "end", text=t_index + 1, values=(x, z, xo, zo))
            table_trajectory.pack(pady=1)

        frame_inner.update_idletasks()
        bbox = canvas_tables.bbox(tkinter.ALL)
        canvas_tables.configure(scrollregion=bbox)

        canvas_tables.place(anchor="nw", width=560, height=738, x=804, y=1, bordermode="inside")


# boton para ver las tablas de las coordenadas de los meteoritos
def options_show_tables(time):
    global see_tables
    see_tables = tkinter.Button(canvas_options, text="Ver tablas", background="blue", foreground="white",
                                command=lambda: show_tables(time))
    see_tables.pack(padx=2, pady=15, ipady=2, ipadx=8)


def create_legend(figure_legend, list_meteorites):
    figure_legends = figure_legend.figure
    ax_legend = figure_legends.add_subplot(111)
    x_start = 20
    y_start = 20
    spacing = 25
    default_colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']  # Colores por defecto
    legend_lines = []

    for i, meteorite in enumerate(list_meteorites):
        color = default_colors[i % len(default_colors)]
        line = mlines.Line2D([], [], color=color, label=f'Meteorito {meteorite["id"] + 1}')
        ax_legend.axes.add_line(line)
        ax_legend.axes.text(x_start + spacing, y_start + i * spacing, f'Meteorito {meteorite["id"] + 1}',
                            color=color, verticalalignment='center')
        legend_lines.append(line)

    ax_legend.legend(loc="center")
    ax_legend.axis('off')
    ax_legend.set_frame_on(False)
    # return figure_legend
    return figure_legend


def restore_zoom(toolbar):
    toolbar.home()


def get_hex_color(color):
    try:
        return "#{:02x}{:02x}{:02x}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
    except ValueError:
        return '#000000'  # Usar color negro (#000000) como color por defecto


def graph_meteorites(time):
    if time == "first":
        fig, ax = plt.subplots()
        canvas_graphic = FigureCanvasTkAgg(fig, master=window)

        for t in range(len(list_trajectories_x)):
            ax.plot(list_trajectories_x[t], list_trajectories_z[t], label=f'Meteorito : {t + 1}')
            # ax.plot(trajectory_x_noise, trajectory_z_noise, linestyle="dashed")

        min_min_z = min(min_z)
        min_min_x = min(min_x)
        max_max_z = max(max_z)
        max_max_x = max(max_x)

        if min_min_z <= 0:
            ax.spines['left'].set_position('zero')
            ax.spines['left'].set_color('gray')
            limit_negative = (0 - (min_min_z - 1)) * 1
            ax.set_ylim(-limit_negative, max_max_z + 1)
        else:
            ax.spines['left'].set_position('zero')
            ax.spines['left'].set_color('gray')
            ax.set_xlim(0, max_max_z + 1)

        if min_min_x <= 0:
            ax.spines['bottom'].set_position('zero')
            ax.spines['bottom'].set_color('gray')
            limit_negative = (0 - (min_min_x - 1)) * 1
            ax.set_xlim(-limit_negative, max_max_x + 1)
        else:
            ax.spines['bottom'].set_position('zero')
            ax.spines['bottom'].set_color('gray')
            ax.set_xlim(0, max_max_x + 1)

        ax.set_xlabel('Coordenada x', fontsize=12)
        ax.set_ylabel('Coordenada z', fontsize=12)
        ax.set_title('Gráfico de Meteoritos', fontsize=14)
        ax.grid(True, linewidth=0.5, color='gray', alpha=0.7)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        canvas_graphic.draw()
        mplcursors.cursor(hover=True)
        canvas_graphic.get_tk_widget().place(anchor="c", width=600, height=412, x=502, y=207, bordermode="inside")

        # # Crea un scrollbar para la leyenda y agrega las líneas de la leyenda al frame
        # canvas_legend = tkinter.Canvas(window)
        # canvas_legend.pack(fill="both", expand=True)
        #
        # scrollbar_vertical = tkinter.Scrollbar(canvas_legend, orient="vertical", command=canvas_legend.yview)
        # scrollbar_vertical.pack(side="right", fill="y")
        #
        # canvas_legend.configure(yscrollcommand=scrollbar_vertical.set)
        #
        # frame_inner = tkinter.Frame(canvas_legend)
        #
        # legend_list = []
        # fig2, ax2 = plt.subplots()
        # for i, m in enumerate(list_meteorite):
        #     legend = f'Meteorito: {i + 1}'
        #     legend_list.append(legend)
        #     ax2.plot(list_trajectories_x[i], list_trajectories_z[i], )
        #
        # ax2.legend(legend_list, title="meteoritos", loc="upper left")
        # figure_legend = FigureCanvasTkAgg(fig2, master=canvas_legend)
        # for line in ax2.lines:
        #     line.set_visible(False)
        # ax2.axis('off')
        # ax2.set_frame_on(False)
        # figure_legend.draw()
        # figure_legend.get_tk_widget().place(anchor="nw", width=190, height=302)
        # canvas_legend.create_window((0, 0), window=frame_inner, anchor="nw")
        # frame_inner.update_idletasks()
        # bbox = canvas_legend.bbox(tkinter.ALL)
        # canvas_legend.configure(scrollregion=bbox)
        #
        # canvas_legend.place(anchor="nw", width=207, height=302, x=400, y=442)

        toolbar = NavigationToolbar2Tk(canvas_graphic, window)
        toolbar.zoom(10)
        toolbar.configure(background='#%02x%02x%02x' % (75, 30, 30))
        toolbar.place(height=30, width=600, x=202, y=412)
        restore_button = tkinter.Button(master=window, text="Restaurar zoom",
                                        background='#%02x%02x%02x' % (100, 30, 170),
                                        foreground="white",
                                        command=lambda: restore_zoom(toolbar))
        restore_button.place(height=30, x=460, y=412)
    else:
        fig, ax = plt.subplots()
        canvas_graphic = FigureCanvasTkAgg(fig, master=window)

        for t in range(len(list_before_trajectories_x)):
            ax.plot(list_before_trajectories_x[t], list_before_trajectories_z[t], label=f'Meteorito : {t + 1}')
            # ax.plot(trajectory_x_noise, trajectory_z_noise, linestyle="dashed")

        min_min_z = min(min_z)
        min_min_x = min(min_x)
        max_max_z = max(max_z)
        max_max_x = max(max_x)

        if min_min_z <= 0:
            ax.spines['left'].set_position('zero')
            ax.spines['left'].set_color('gray')
            limit_negative = (0 - (min_min_z - 1)) * 1
            ax.set_ylim(-limit_negative, max_max_z + 1)
        else:
            ax.spines['left'].set_position('zero')
            ax.spines['left'].set_color('gray')
            ax.set_xlim(0, max_max_z + 1)

        if min_min_x <= 0:
            ax.spines['bottom'].set_position('zero')
            ax.spines['bottom'].set_color('gray')
            limit_negative = (0 - (min_min_x - 1)) * 1
            ax.set_xlim(-limit_negative, max_max_x + 1)
        else:
            ax.spines['bottom'].set_position('zero')
            ax.spines['bottom'].set_color('gray')
            ax.set_xlim(0, max_max_x + 1)

        ax.set_xlabel('Coordenada x', fontsize=12)
        ax.set_ylabel('Coordenada z', fontsize=12)
        ax.set_title('Gráfico de Meteoritos', fontsize=14)
        ax.grid(True, linewidth=0.5, color='gray', alpha=0.7)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        canvas_graphic.draw()
        mplcursors.cursor(hover=True)
        canvas_graphic.get_tk_widget().place(anchor="c", width=600, height=412, x=502, y=207, bordermode="inside")

        # # Crea un scrollbar para la leyenda y agrega las líneas de la leyenda al frame
        # canvas_legend = tkinter.Canvas(window)
        # canvas_legend.pack(fill="both", expand=True)
        #
        # scrollbar_vertical = tkinter.Scrollbar(canvas_legend, orient="vertical", command=canvas_legend.yview)
        # scrollbar_vertical.pack(side="right", fill="y")
        #
        # canvas_legend.configure(yscrollcommand=scrollbar_vertical.set)
        #
        # frame_inner = tkinter.Frame(canvas_legend)
        #
        # legend_list = []
        # fig2, ax2 = plt.subplots()
        # for i, m in enumerate(list_meteorite):
        #     legend = f'Meteorito: {i + 1}'
        #     legend_list.append(legend)
        #     ax2.plot(list_trajectories_x[i], list_trajectories_z[i], )
        #
        # ax2.legend(legend_list, title="meteoritos", loc="upper left")
        # figure_legend = FigureCanvasTkAgg(fig2, master=canvas_legend)
        # for line in ax2.lines:
        #     line.set_visible(False)
        # ax2.axis('off')
        # ax2.set_frame_on(False)
        # figure_legend.draw()
        # figure_legend.get_tk_widget().place(anchor="nw", width=190, height=302)
        # canvas_legend.create_window((0, 0), window=frame_inner, anchor="nw")
        # frame_inner.update_idletasks()
        # bbox = canvas_legend.bbox(tkinter.ALL)
        # canvas_legend.configure(scrollregion=bbox)
        #
        # canvas_legend.place(anchor="nw", width=207, height=302, x=400, y=442)

        toolbar = NavigationToolbar2Tk(canvas_graphic, window)
        toolbar.zoom(10)
        toolbar.configure(background='#%02x%02x%02x' % (75, 30, 30))
        toolbar.place(height=30, width=600, x=202, y=412)
        restore_button = tkinter.Button(master=window, text="Restaurar zoom",
                                        background='#%02x%02x%02x' % (100, 30, 170),
                                        foreground="white",
                                        command=lambda: restore_zoom(toolbar))
        restore_button.place(height=30, x=460, y=412)


# crea un nuevo meteorito
def create_new_meteorite(m, coordinate_x, coordinate_z, meteorite):
    probability_explosion = random.randint(0, int(meteorite["probability_explosion"]))
    parts_explosion = random.randint(0, int(meteorite["parts_explodes"]))
    new_meteorite = dict(
        Meteorite.Meteorite(id=m, coordinate_x=coordinate_x[-1], coordinate_z=coordinate_z[-1],
                            probability_explosion=float(probability_explosion),
                            parts_explodes=parts_explosion, trajectory_x=[], trajectory_z=[], time_minute=0))
    return new_meteorite


# genera la cantidad de meteoritos que en la que se dividio
def number_of_meteorites_generated(parts_explodes):
    explosion = random.randint(0, 100)
    if 80 <= explosion <= 100:
        choice = random.randint(0, 1)
        if choice == 0:
            random_number = random.randint(2, parts_explodes)
            return random_number, "meteoritos"
        else:
            random_number = np.random.poisson(parts_explodes)
            if random_number == 1:
                return random_number + 1, "meteoritos"
            return random_number, "meteoritos"
    elif 0 <= explosion <= 20:
        return 0, "no exploto"
    else:
        explosion = random.randint(20, 80)
        if 50 <= explosion <= 80:
            explosion_random = random.randint(0, 1)
            if explosion_random == 1:
                return 0, "exploto"
            else:
                return 0, "no exploto"
        else:
            return 0, "no exploto"


# valida si el meteorito exploto
def validate_meteorites_explosion(trajectory_z, probability_explosion, parts_explodes):
    prob = random.random()
    yes_or_not_explode = random.randint(0, 1)
    if trajectory_z[-1] <= 0.0 or 0.0 < trajectory_z[-1] < 0.1:
        return 0, "exploto"
    elif prob == 1 or probability_explosion >= 100 and parts_explodes >= 2:
        value, identifier = number_of_meteorites_generated(parts_explodes)
        return value, identifier
    elif prob + ((probability_explosion / 100) / 2) <= probability_explosion / 100 <= 1 and trajectory_z[
        -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
        value, identifier = number_of_meteorites_generated(parts_explodes)
        return value, identifier
    else:
        return 0, "no exploto"


# calcula la trayectoria de cada meterito
def calculate_trajectories(meteorite, time_one_minute):
    id = int(meteorite["id"])
    xo = float(meteorite["coordinate_x"])
    zo = float(meteorite["coordinate_z"])
    probability_explosion = float(meteorite["probability_explosion"])
    parts_explodes = int(meteorite["parts_explodes"])
    trajectory_x = [xo]
    # trajectory_x_noise = [xo]
    trajectory_z = [zo]
    # trajectory_z_noise = [zo]
    for i in range(time_one_minute):
        value, identifier = validate_meteorites_explosion(trajectory_z, probability_explosion, parts_explodes)
        if value == 0 and identifier == "no exploto":
            x_noise = np.random.normal(loc=0, scale=0.1)
            # z_noise = np.random.uniform(low=-1, high=0)
            # z_change = np.random.normal(loc=-0.5, scale=-0.5)
            trajectory_x.append(trajectory_x[-1] + x_noise)
            z_noise = np.random.uniform(low=-trajectory_z[0] / (time_one_minute - i), high=0)
            trajectory_z.append(trajectory_z[-1] + z_noise)
            continue
        elif value == 0 and identifier == "exploto":
            if trajectory_z[-1] <= 0.0 or 0.0 < trajectory_z[-1] < 0.1:
                trajectory_z[-1] = 0.0
                meteorite["trajectory_x"] = trajectory_x
                meteorite["trajectory_z"] = trajectory_z
                meteorite["time_minute"] = i
                break
            meteorite["trajectory_x"] = trajectory_x
            meteorite["trajectory_z"] = trajectory_z
            meteorite["time_minute"] = i
            break
        else:
            meteorite["trajectory_x"] = trajectory_x
            meteorite["trajectory_z"] = trajectory_z
            meteorite["time_minute"] = i
            for m in range(value):
                new_meteorite = create_new_meteorite(len(list_meteorite), trajectory_x, trajectory_z, meteorite)
                list_meteorite.append(new_meteorite)
            break

    list_trajectories_x.append(trajectory_x)
    list_trajectories_z.append(trajectory_z)

    list_before_trajectories_x.append(trajectory_x)
    list_before_trajectories_z.append(trajectory_z)

    min_z.append(min(trajectory_z))
    min_x.append(min(trajectory_x))
    max_z.append(max(trajectory_z))
    max_x.append(max(trajectory_x))


# calcula la trayectoria y la grafica
# calculate_and_graphic(list_meteorites, simulated_fall, amount_meteorite_one):
def calculate_and_graphic(list_meteorites, simulated_fall, time, amount_meteorite):
    global list_meteorite_before
    if time == "first":
        # forma uno de calcular la trayectoria
        time_one_minute = np.random.poisson(60)
        for meteorite in list_meteorites:
            calculate_trajectories(meteorite, time_one_minute)
        graph_meteorites(time)
        simulated_fall.destroy()
        options_show_tables(time)
    else:
        time_one_minute = np.random.poisson(60)
        for i, meteorite in enumerate(list_meteorites[len(list_meteorites) - amount_meteorite:len(list_meteorites)]):
            calculate_trajectories(meteorite, time_one_minute)
        graph_meteorites(time)
        simulated_fall.destroy()
        options_show_tables(time)


# boton de simular para para calcular la trayectoria y graficar los meteoritos
# simulate(amount_meteorite_one)
def simulate(time, amount_meteorite):
    simulated_fall = tkinter.Button(canvas_options, text="Simular", background="red", foreground="white",
                                    command=lambda: calculate_and_graphic(list_meteorite, simulated_fall, time,
                                                                          amount_meteorite))
    # calculate_and_graphic(list_meteorite, simulated_fall, amount_meteorite_one)
    simulated_fall.pack(padx=2, pady=15, ipady=2, ipadx=8)


# agrega la cantodad de partes de en las que se cree que se va a dividir a cada meteorito
def add_parts_explosion(m, parts_explosion, parts_explosion_label, add_parts_button):
    list_meteorite[m]["parts_explodes"] = parts_explosion.get()
    parts_explosion.destroy()
    parts_explosion_label.destroy()
    add_parts_button.destroy()


# opciones para agregar la cantidad de partes en las que se va a dividir el meteorito
def options_parts_explosion(m):
    parts_explosion_label = tkinter.Label(canvas_options, text=f'Partes que se divide el meteorito :{m + 1}')
    parts_explosion_label.pack(padx=2, pady=36, ipady=6, ipadx=8)
    parts_explosion = tkinter.Entry(canvas_options)
    parts_explosion.pack(padx=2, pady=20, ipady=2, ipadx=8)
    add_parts_button = tkinter.Button(canvas_options, text=("Agregar partes"),
                                      command=lambda: add_parts_explosion(m, parts_explosion,
                                                                          parts_explosion_label,
                                                                          add_parts_button))
    add_parts_button.pack(padx=2, pady=36, ipady=6, ipadx=8)


# agrega la probabilidad de explosion a cada meteorito
def add_probability_explosion(m, probability_explosion, probability_explosion_label, add_probability_button):
    list_meteorite[m]["probability_explosion"] = probability_explosion.get()
    probability_explosion.destroy()
    probability_explosion_label.destroy()
    add_probability_button.destroy()


# opciones para agregar la probabilidad de exposicion de los meteoritos
def options_probability_explosion(m):
    probability_explosion_label = tkinter.Label(canvas_options,
                                                text=f'Probabilidad % explossion del meteorito :{m + 1}')
    probability_explosion_label.pack(padx=2, pady=36, ipady=6, ipadx=8)
    probability_explosion = tkinter.Entry(canvas_options)
    probability_explosion.pack(padx=2, pady=20, ipady=2, ipadx=8)
    add_probability_button = tkinter.Button(canvas_options, text=("Agregar probabilidad"),
                                            command=lambda: add_probability_explosion(m, probability_explosion,
                                                                                      probability_explosion_label,
                                                                                      add_probability_button))
    add_probability_button.pack(padx=2, pady=36, ipady=6, ipadx=8)


# agrega las coordenadas a cada meteorito
def add_coordinate(m, coordinate_x, coordinate_z, coordinate_z_label, coordinate_x_label, add_coordinate_button):
    meteorite = dict(Meteorite.Meteorite(id=m,
                                         coordinate_x=coordinate_x.get(),
                                         coordinate_z=coordinate_z.get(),
                                         probability_explosion=0,
                                         parts_explodes=0,
                                         trajectory_x=[0.0],
                                         trajectory_z=[0.0],
                                         time_minute=0))
    list_meteorite.append(meteorite)
    coordinate_z_label.destroy()
    coordinate_x_label.destroy()
    coordinate_z.destroy()
    coordinate_x.destroy()
    add_coordinate_button.destroy()


# opciones para agregar las coordenadas x y z del los meteoritos
def options_coordinates_meteorites(m):
    coordinate_x_label = tkinter.Label(canvas_options, text=f'coordenada x del meteorito: {m + 1}')
    coordinate_x_label.pack(padx=2, pady=15, ipady=2, ipadx=8)
    coordinate_x = tkinter.Entry(canvas_options)
    coordinate_x.pack(padx=2, pady=15, ipady=2, ipadx=8)
    coordinate_z_label = tkinter.Label(canvas_options, text=f'coordenada z del meteorito: {m + 1}')
    coordinate_z_label.pack(padx=2, pady=15, ipady=2, ipadx=8)
    coordinate_z = tkinter.Entry(canvas_options)
    coordinate_z.pack(padx=2, pady=15, ipady=2, ipadx=8)
    add_coordinate_button = tkinter.Button(canvas_options, text=("Agregar coordenadas"),
                                           command=lambda: add_coordinate(m, coordinate_x, coordinate_z,
                                                                          coordinate_z_label,
                                                                          coordinate_x_label,
                                                                          add_coordinate_button))
    add_coordinate_button.pack(padx=2, pady=15, ipady=2, ipadx=8)


def validate_new_meteorite(amount_meteorite):
    if amount_meteorite.get() == "" or amount_meteorite.get() == 0:
        print("no hay meteorito")
    else:
        if len(list_meteorite) == 0:
            for m in range(int(amount_meteorite.get())):
                options_coordinates_meteorites(m)
                options_probability_explosion(m)
                options_parts_explosion(m)
            # simulate(amount_meteorite_one)
            simulate("first", int(amount_meteorite.get()))
        else:
            for m in range(len(list_meteorite), len(list_meteorite) + int(amount_meteorite.get())):
                options_coordinates_meteorites(m)
                options_probability_explosion(m)
                options_parts_explosion(m)
            # simulate(amount_meteorite_one)
            simulate("second", int(amount_meteorite.get()))


# secuencia de ejecucion principal del simulador
# set_coordinates(amount_meteorite, amount_meteorite_one)
def set_coordinates(amount_meteorite):
    if see_tables is not None:
        see_tables.destroy()
        validate_new_meteorite(amount_meteorite)
    else:
        validate_new_meteorite(amount_meteorite)


# cantidad de meteoritos caen en un año
# def options_amount_meteorites_one_year():
#     amount_meteorite_one_label = tkinter.Label(canvas_options, text="Cantidad de meteoritos en un año")
#     amount_meteorite_one_label.pack(padx=2, pady=8, ipady=2, ipadx=8)
#     amount_meteorite_one = tkinter.Entry(canvas_options)
#     amount_meteorite_one.pack(padx=2, pady=8, ipady=2, ipadx=8)
#     add_meteorite_one = tkinter.Button(canvas_options, text="Agregar meteorito(s)",
#                                    command=lambda: set_coordinates(amount_meteorite, amount_meteorite_one))
#     add_meteorite_one.pack(padx=2, ipady=2, ipadx=8)


# opciones de la cantidad de meteoritos
# def options_amount_meteorites():
#     amount_meteorite_label = tkinter.Label(canvas_options, text="Cantidad de meteoritos")
#     amount_meteorite_label.pack(padx=2, pady=8, ipady=2, ipadx=8)
#     amount_meteorite = tkinter.Entry(canvas_options)
#     amount_meteorite.pack(padx=2, pady=8, ipady=2, ipadx=8)
#     add_meteorite = tkinter.Button(canvas_options, text="Agregar meteorito(s)",
#                                    command=lambda: set_coordinates(amount_meteorite))
#     add_meteorite.pack(padx=2, ipady=2, ipadx=8)


def options_height_meteorite():
    amount_meteorite_label = tkinter.Label(canvas_options, text="Altura (z)")
    amount_meteorite_label.pack(padx=2, pady=8, ipady=2, ipadx=8)
    amount_meteorite = tkinter.Entry(canvas_options)
    amount_meteorite.pack(padx=2, pady=8, ipady=2, ipadx=8)
    add_meteorite = tkinter.Button(canvas_options, text="Agregar Altura",
                                   command=lambda: set_coordinates(amount_meteorite))
    add_meteorite.pack(padx=2, ipady=2, ipadx=8)


def options_time_simulation(combobox_time):
    amount_meteorite_label = tkinter.Label(canvas_options, text="Cantidad de tiempo")
    amount_meteorite_label.pack(padx=2, pady=8, ipady=2, ipadx=8)
    amount_meteorite = tkinter.Entry(canvas_options)
    amount_meteorite.pack(padx=2, pady=8, ipady=2, ipadx=8)
    add_meteorite = tkinter.Button(canvas_options, text="Agregar Altura",
                                   command=lambda: set_coordinates(amount_meteorite))
    add_meteorite.pack(padx=2, ipady=2, ipadx=8)


def options_select_type_time_simulation():
    label_time = tkinter.Label(canvas_options, text="Tipo de tiempo de simulacion")
    label_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
    combobox_time = ttk.Combobox(canvas_options, values=["años", "meses", "dias"])
    combobox_time.pack(padx=2, ipady=2, ipadx=8)
    combobox_time.bind("<<ComboboxSelected>>", lambda event: options_time_simulation(combobox_time))


# incio de de la ejecucion de la aplicacion
canvas_options = tkinter.Canvas(window, background='#%02x%02x%02x' % (120, 50, 45))
# options_amount_meteorites_one_year()
# options_height_meteorite()
options_select_type_time_simulation()
canvas_options.place(anchor="nw", width=200, height=412, x=1, y=1, bordermode="inside")

window.mainloop()
