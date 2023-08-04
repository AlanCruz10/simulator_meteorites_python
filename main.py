import time
import tkinter
from tkinter import ttk
import random
import numpy as np
import Meteorite
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
import math

window = tkinter.Tk()
window.geometry("500x500")
window.title("Meteoritos")
window.configure(bg='#%02x%02x%02x' % (101, 47, 185))

list_meteorites_main = []
list_meteorites = []
list_meteorites_exploited = []
list_amount_meteorites = []
list_meteorites_inactive = []
list_trajectories_x = []
list_trajectories_z = []
list_min = []
list_max = []

label_meteorites_limit = None
amount_meteorites_limit = None
add_meteorites_limit_button = None

# Variables relacionadas con el tiempo
label_type_time = None
entry_time = None
add_time = None

# Variables relacionadas con meteoritos
label_meteorites = None
amount_meteorites = None
add_meteorites = None

# Variables relacionadas con tiempo de muestreo
label_sampling_time = None
amount_sampling_time = None
add_sampling_time = None

# Variables relacionadas con la altura
label_height = None
amount_height = None
add_height = None

# Variables relacionadas con la probabilidad de explosión
label_probability_explosion = None
probability_explosion = None
add_probability_button = None

see_tables = None
simulate_fall = None
clear_button = None

def show_tables():
    canvas_tables = tkinter.Canvas(window, background='#%02x%02x%02x' % (100, 20, 70))
    canvas_tables.pack(fill="both", expand=True)

    scrollbar_vertical = tkinter.Scrollbar(canvas_tables, orient="vertical", command=canvas_tables.yview)
    scrollbar_vertical.pack(side="right", fill="y")

    canvas_tables.configure(yscrollcommand=scrollbar_vertical.set)

    frame_inner = tkinter.Frame(canvas_tables, background='#%02x%02x%02x' % (100, 20, 70))
    canvas_tables.create_window((0, 0), window=frame_inner, anchor="nw")

    df_meteorites_all = pd.DataFrame(list_meteorites)
    df_meteorites_all_drop_u = df_meteorites_all.drop(
        columns=["id", "x", "z", "x_speed", "z_speed", "status"])
    df_meteorites_all_drop = df_meteorites_all.drop(
        columns=['trajectory_x', 'trajectory_z', 'trajectory_x_speed', 'trajectory_z_speed'])

    table_title_label = tkinter.Label(frame_inner, text="Tabla de Meteoritos", font=("Arial", 14, "bold"),
                                      bg='#%02x%02x%02x' % (20, 120, 185), fg="white")
    table_title_label.pack(pady=5)

    table_meteorites = ttk.Treeview(frame_inner, columns=("x", "z", "x_speed", "z_speed", "status"))
    table_meteorites.heading("#0", text="id")
    table_meteorites.heading("x", text="x")
    table_meteorites.heading("z", text="z")
    table_meteorites.heading("x_speed", text="x°")
    table_meteorites.heading("z_speed", text="z°")
    table_meteorites.heading("status", text="status")

    table_meteorites.column("#0", width=50, anchor="center")
    table_meteorites.column("x", width=101, anchor="center")
    table_meteorites.column("z", width=101, anchor="center")
    table_meteorites.column("x_speed", width=101, anchor="center")
    table_meteorites.column("z_speed", width=101, anchor="center")
    table_meteorites.column("status", width=80, anchor="center")

    table_meteorites.pack(pady=1)

    for index, row in df_meteorites_all_drop.iterrows():
        table_meteorites.insert("", "end", text=row["id"] + 1, values=(
            row["x"], row["z"], row["x_speed"], row["z_speed"], row["status"]))

    for index, row in df_meteorites_all_drop_u.iterrows():
        table_title_label = tkinter.Label(frame_inner, text=f'Meteorito: {index + 1}', font=("Arial", 14, "bold"),
                                          bg='#%02x%02x%02x' % (20, 120, 120), fg="white")
        table_title_label.pack(pady=5)
        table_trajectory = ttk.Treeview(frame_inner,
                                        columns=("trajectory_x", "trajectory_z", "trajectory_x_speed", "trajectory_z_speed"))
        table_trajectory.heading("#0", text="id")
        table_trajectory.heading("trajectory_x", text="x")
        table_trajectory.heading("trajectory_z", text="z")
        table_trajectory.heading("trajectory_x_speed", text="x°")
        table_trajectory.heading("trajectory_z_speed", text="z°")

        table_trajectory.column("#0", width=50, anchor="center")
        table_trajectory.column("trajectory_x", width=121, anchor="center")
        table_trajectory.column("trajectory_z", width=121, anchor="center")
        table_trajectory.column("trajectory_x_speed", width=121, anchor="center")
        table_trajectory.column("trajectory_z_speed", width=121, anchor="center")

        table_trajectory.pack(pady=1)
        # trajectory_xo = list(row["trajectory_x"][1:])
        # trajectory_zo = list(row["trajectory_z"][1:])
        # trajectory_xo.append(0.0) trajectory_zo.append(0.0) for t_index, (x, z, xo, zo) in enumerate(zip(row[
        # "trajectory_x"], row["trajectory_z"], row["trajectory_x_noise"], row["trajectory_z_noise"])):
        for t_index, (x, z, xo, zo) in enumerate(zip(row["trajectory_x"], row["trajectory_z"], row["trajectory_x_speed"], row["trajectory_z_speed"])):
            # table_trajectory.insert("", "end", text=t_index + 1, values=(x, z, xo, zo))
            table_trajectory.insert("", "end", text=t_index + 1, values=(x, z, xo, zo))
        table_trajectory.pack(pady=1)

    frame_inner.update_idletasks()
    bbox = canvas_tables.bbox(tkinter.ALL)
    canvas_tables.configure(scrollregion=bbox)

    canvas_tables.place(anchor="nw", width=560, height=738, x=804, y=1, bordermode="inside")


def options_show_tables():
    global see_tables
    see_tables = tkinter.Button(canvas_options, text="Ver tablas", background="blue", foreground="white",
                                command=lambda: show_tables())
    see_tables.pack(padx=2, pady=15, ipady=2, ipadx=8)


def restore_zoom(toolbar):
    toolbar.home()


def graph_meteorites(height):
    fig, ax = plt.subplots()
    canvas_graphic = FigureCanvasTkAgg(fig, master=window)

    for t in range(len(list_meteorites)):
        ax.plot(list_meteorites[t]["trajectory_x"], list_meteorites[t]["trajectory_z"], label=f'Meteorito : {t + 1}')
        # ax.plot(trajectory_x_noise, trajectory_z_noise, linestyle="dashed")

    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_color('gray')

    if len(list_meteorites) == 0:
        ax.set_xlim(-10, 10)
        ax.set_ylim(0, height + 1)
    else:
        for i, m in enumerate(list_meteorites):
            list_min.append(min(m["trajectory_x"]))
            list_max.append(max(m["trajectory_x"]))

        if min(list_min) <= 0:
            min_min = min(list_min) - 1
            ax.set_xlim(min_min, max(list_max) + 1)
        else:
            ax.set_xlim(0, max(list_max) + 1)

    ax.set_ylim(0, height + 1)
    ax.set_xlabel('Coordenada x', fontsize=12)
    ax.set_ylabel('Coordenada z', fontsize=12)
    ax.set_title('Gráfico de Meteoritos', fontsize=14)
    ax.grid(True, linewidth=0.5, color='gray', alpha=0.7)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    canvas_graphic.draw()
    mplcursors.cursor(hover=True)
    canvas_graphic.get_tk_widget().place(anchor="c", width=600, height=412, x=502, y=207, bordermode="inside")
    toolbar = NavigationToolbar2Tk(canvas_graphic, window)
    toolbar.zoom(10)
    toolbar.configure(background='#%02x%02x%02x' % (75, 30, 30))
    toolbar.place(height=30, width=600, x=202, y=412)
    restore_button = tkinter.Button(master=window, text="Restaurar zoom",
                                    background='#%02x%02x%02x' % (100, 30, 170),
                                    foreground="white",
                                    command=lambda: restore_zoom(toolbar))
    restore_button.place(height=30, x=460, y=412)


def validate_meteorites_explosion(trajectory_z, probability_explosion_meteorites, parts_explodes):
    # prob = random.random()
    # yes_or_not_explode = random.randint(0, 1)
    # if trajectory_z[-1] <= 0.0 or 0.0 < trajectory_z[-1] < 0.1:
    #     return 0, "exploto"
    # elif prob == 1 or probability_explosion >= 100 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes)
    #     return value, identifier
    # elif prob + ((probability_explosion / 100) / 2) <= probability_explosion / 100 <= 1 and trajectory_z[
    #     -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes)
    #     return value, identifier
    # else:
    #     return 0, "no exploto"

    low_probability = random.random()
    top_probability = random.uniform(1, 2)
    yes_or_not_explode = random.randint(0, 100)
    if trajectory_z[-1] <= 0.0 or 0.0 < trajectory_z[-1] < 0.1:
        return 0, "exploto"
    else:
        if probability_explosion_meteorites >= 100 >= yes_or_not_explode >= 95 and low_probability == 1 and parts_explodes >= 2:
            value, identifier = number_of_meteorites_generated(parts_explodes, 100, probability_explosion_meteorites)
            return value, identifier
        elif 0 <= probability_explosion_meteorites <= 20 and 95 <= yes_or_not_explode <= 100 and low_probability / 2 >= probability_explosion_meteorites / 100 and parts_explodes >=2:
            value, identifier = number_of_meteorites_generated(parts_explodes, 0, 20)
            return value, identifier
        elif 80 <= probability_explosion_meteorites < 100 and 95 <= yes_or_not_explode <= 100 and top_probability / 2 >= probability_explosion_meteorites / 100 and parts_explodes >=2:
            value, identifier = number_of_meteorites_generated(parts_explodes, 80, 100)
            return value, identifier
        elif 20 < probability_explosion_meteorites < 50 and 95 <= yes_or_not_explode <= 100 and low_probability / 2 >= probability_explosion_meteorites / 100 and parts_explodes >=2:
            value, identifier = number_of_meteorites_generated(parts_explodes, 20, 50)
            return value, identifier
        elif 50 <= probability_explosion_meteorites < 80 and 95 <= yes_or_not_explode <= 100 and top_probability / 2 >= probability_explosion_meteorites / 100 and parts_explodes >=2:
            value, identifier = number_of_meteorites_generated(parts_explodes, 20, 80)
            return value, identifier
        else:
            return 0, "no exploto"

    # elif prob == 1 or probability_explosion >= 100 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes, probability_explosion, 100)
    #     return value, identifier
    # elif 0.8 <= probability_explosion / 100 < 1.0 or 0.8 <= probability_explosion / 100 < 1 and mid_p / 2 >= probability_explosion / 100 <= 1 and \
    #         trajectory_z[
    #             -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes, 100, 80)
    #     return value, identifier
    # elif 0 <= probability_explosion / 100 < 0.2 or 0.0 <= probability_explosion / 100 <= 0.2 and prob / 2 >= probability_explosion / 100 <= 0.2 and \
    #         trajectory_z[
    #             -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes, 20, 0)
    #     return value, identifier
    # elif 0.2 < probability_explosion / 100 < 0.8 and random_p / 2 >= probability_explosion / 100 <= 0.8 and \
    #         trajectory_z[
    #             -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes, 20, 80)
    #     return value, identifier

    # elif probability_explosion / 100 > 0.5 and mid_p / 2 >= probability_explosion / 100 and trajectory_z[
    #     -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes)
    #     return value, identifier
    # elif prob / 2 >= probability_explosion / 100 and trajectory_z[
    #     -1] > 0.0 and yes_or_not_explode == 1 and parts_explodes >= 2:
    #     value, identifier = number_of_meteorites_generated(parts_explodes)
    #     return value, identifier
    # else:
    #     return 0, "no exploto"


def number_of_meteorites_generated(parts_explodes, probability_explosion_lower, probability_explosion_meteorites):
    explosion = random.randint(probability_explosion_lower, probability_explosion_meteorites)
    if explosion >= 100:
        random_number = random.randint(2, parts_explodes)
        return random_number, "meteoritos"
    elif 0 <= explosion <= 20:
        if 0 <= explosion <= 10:
            return 0, "no exploto"
        else:
            choice = random.randint(0, 2)
            if choice == 0:
                return 0, "no exploto"
            elif choice == 2:
                random_number = random.randint(2, parts_explodes)
                return random_number, "meteoritos"
            else:
                return 0, "exploto"
    elif 80 <= explosion < 100:
        choice = random.randint(0, 2)
        if choice == 0 and explosion <= 85:
            return 0, "no exploto"
        elif choice == 2:
            random_number = random.randint(2, parts_explodes)
            return random_number, "meteoritos"
        else:
            return 0, "exploto"
    elif 20 < explosion < 80:
        if 50 <= explosion < 80:
            choice = random.randint(0, 2)
            if choice == 0 and explosion <= 60:
                return 0, "no exploto"
            elif choice == 2:
                random_number = random.randint(2, parts_explodes)
                return random_number, "meteoritos"
            else:
                return 0, "exploto"
        else:
            choice = random.randint(0, 2)
            if choice == 0 and explosion <= 30:
                return 0, "no exploto"
            elif choice == 2:
                random_number = random.randint(2, parts_explodes)
                return random_number, "meteoritos"
            else:
                return 0, "exploto"
    else:
        return 0, "no exploto"

    # if 80 <= explosion <= 100:
    #     choice = random.randint(0, 1)
    #     if choice == 0:
    #         return 0, "no exploto"
    #     else:
    #         random_number = random.randint(2, parts_explodes)
    #         return random_number, "meteoritos"
    #         # random_number = np.random.poisson(parts_explodes)
    #         # if random_number == 1:
    #         #     return random_number + 1, "meteoritos"
    #         # return random_number, "meteoritos"
    # elif 0 <= explosion <= 20:
    #     return 0, "no exploto"
    # elif 20 < explosion < 80:
    #     explosion = random.randint(20, 80)
    #     if 50 <= explosion <= 80:
    #         explosion_random = random.randint(0, 1)
    #         if explosion_random == 1:
    #             return 0, "exploto"
    #         else:
    #             return 0, "no exploto"
    #     else:
    #         return 0, "no exploto"
    # else:
    #     random_number = random.randint(2, parts_explodes)
    #     return random_number, "meteoritos"


# def validate_meteorites_explosion(trajectory_z):
#     explosion = random.randint(80, 100)
#     if trajectory_z[-1] <= 0.0 or 0.0 < trajectory_z[-1] < 0.1:
#         return 0, "exploto"
#     elif 80 <= explosion <= 100:
#         meteorites = numbers_meteorites()
#         if meteorites == 0:
#             return 0, "no exploto"
#         else:
#             return meteorites, "meteorites"
#     elif 0 <= explosion <= 20:
#         return 0, "no exploto"
#     else:
#         # arrival = random.uniform(20, 80)
#         # arrival = np.random.uniform(20, 80)
#         arrival = random.randint(20, 80)
#         if 50 <= arrival <= 80:
#             choice = random.randint(0, 1)
#             if choice == 0:
#                 return 0, "no exploto"
#             else:
#                 meteorites = numbers_meteorites()
#                 if meteorites == 0:
#                     return 0, "no exploto"
#                 else:
#                     return meteorites, "meteorites"
#         else:
#             return 0, "no exploto"


def calculate_trajectories(meteorite, delta_t, probability_explosion_meteorites, amount_meteorites_limits):
    id = int(meteorite["id"])
    x = float(meteorite["x"])
    z = float(meteorite["z"])
    x_speed = float(meteorite["x_speed"])
    z_speed = float(meteorite["z_speed"])
    trajectory_x = list(meteorite["trajectory_x"])
    trajectory_z = list(meteorite["trajectory_z"])
    trajectory_x_speed = list(meteorite["trajectory_x_speed"])
    trajectory_z_speed = list(meteorite["trajectory_z_speed"])
    if len(trajectory_x) == 1 and trajectory_x[0] == 0.0 and len(trajectory_z) == 1 and trajectory_z[0] == 0.0 and meteorite["status"] == "Active":
        trajectory_x_g = [x]
        trajectory_z_g = [z]
        trajectory_x_speed_g = [x_speed]
        trajectory_z_speed_g = [z_speed]
        meteorite["trajectory_x"] = trajectory_x_g
        meteorite["trajectory_z"] = trajectory_z_g
        meteorite["trajectory_x_speed"] = trajectory_x_speed_g
        meteorite["trajectory_z_speed"] = trajectory_z_speed_g
    else:
        value, identifier = validate_meteorites_explosion(trajectory_z, probability_explosion_meteorites,
                                                          amount_meteorites_limits)
        if value == 0 and identifier == "no exploto" and meteorite["status"] == "Active":
            x_noise = np.random.normal(loc=0, scale=0.1)
            x_speed_noise = x_speed + x_noise
            trajectory_x.append(trajectory_x[-1] + (x_speed_noise * delta_t))
            trajectory_x_speed.append(x_speed_noise)
            z_noise = np.random.normal(loc=0, scale=0.1)
            z_speed_noise = z_speed + z_noise
            if z_speed_noise > 0.0 or z_speed_noise > 0:
                z_speed_noise_n = z_speed_noise * -1
                trajectory_z.append(trajectory_z[-1] + (z_speed_noise_n * delta_t))
                trajectory_z_speed.append(z_speed_noise_n)
            else:
                trajectory_z.append(trajectory_z[-1] + (z_speed_noise * delta_t))
                trajectory_z_speed.append(z_speed_noise)

            meteorite["trajectory_x"] = trajectory_x
            meteorite["trajectory_z"] = trajectory_z
            meteorite["trajectory_x_speed"] = trajectory_x_speed
            meteorite["trajectory_z_speed"] = trajectory_z_speed
            meteorite["status"] = "Active"
        elif value == 0 and identifier == "exploto" and meteorite["status"] == "Active":
            if trajectory_z[-1] <= 0.0 or 0.0 < trajectory_z[-1] < 0.1:
                trajectory_z[-1] = 0.0
                meteorite["trajectory_x"] = trajectory_x
                meteorite["trajectory_z"] = trajectory_z
                meteorite["trajectory_x_speed"] = trajectory_x_speed
                meteorite["trajectory_z_speed"] = trajectory_z_speed
                meteorite["status"] = "Inactive"
            meteorite["trajectory_x"] = trajectory_x
            meteorite["trajectory_z"] = trajectory_z
            meteorite["trajectory_x_speed"] = trajectory_x_speed
            meteorite["trajectory_z_speed"] = trajectory_z_speed
            meteorite["status"] = "Inactive"
        elif value > 1 and identifier == "meteoritos":
            meteorite["trajectory_x"] = trajectory_x
            meteorite["trajectory_z"] = trajectory_z
            meteorite["trajectory_x_speed"] = trajectory_x_speed
            meteorite["trajectory_z_speed"] = trajectory_z_speed
            meteorite["status"] = "Inactive"
            for m in range(value):
                new_meteorite = create_meteorite(len(list_meteorites), trajectory_x[-1], trajectory_z[-1])
                list_meteorites.append(new_meteorite)
    list_trajectories_x.append(trajectory_x)
    list_trajectories_z.append(trajectory_z)
    # for i, meteorite_l in enumerate(list_meteorites):
    #     if meteorite_l["x"] == trajectory_x[-1] and meteorite_l["z"] == trajectory_z[-1]:
    #         break
    #     else:
    #         for m in range(value):
    #             new_meteorite = create_meteorite(len(list_meteorites), trajectory_x[-1], trajectory_z[-1])
    #             list_meteorites.append(new_meteorite)
    #         break


def create_meteorite(id_meteorite, x, z):
    x_speed = calculate_x_speed()
    z_speed = calculate_z_speed()
    new_meteorite = dict(Meteorite.MeteoriteTwo(id=id_meteorite,
                                                x=x,
                                                z=z,
                                                x_speed=x_speed,
                                                z_speed=z_speed,
                                                trajectory_x=[0.0],
                                                trajectory_z=[0.0],
                                                trajectory_x_speed=[0.0],
                                                trajectory_z_speed=[0.0],
                                                status="Active"))
    return new_meteorite


def calculate_z_speed():
    z_speed = np.random.normal(loc=0, scale=0.5)
    return z_speed


def calculate_x_speed():
    x_speed = np.random.normal(loc=0, scale=0.5)
    return x_speed


def calculate_x():
    x = np.random.uniform(low=-50, high=50)
    return x


# # def numbers_meteorites(meteorites):
# def numbers_meteorites():
#     # random_number = np.random.poisson(meteorites)
#     random_number = np.random.poisson(5)
#     if random_number <= 0:
#         return 0
#     return random_number


def valid_arrival_meteorites():
    # arrival = random.uniform(0, 100)
    # arrival = np.random.uniform(0, 100)
    arrival = random.randint(0, 100)
    if 80 <= arrival <= 100:
        choice = random.randint(0, 1)
        if choice == 0:
            return 0
        else:
            return 1
    elif 0 <= arrival <= 20:
        return 0
    elif 20 < arrival < 80:
        # arrival = random.uniform(20, 80)
        # arrival = np.random.uniform(20, 80)
        arrival = random.randint(20, 80)
        if 50 <= arrival < 80:
            choice = random.randint(0, 1)
            if choice == 0:
                return 0
            else:
                return 1
        else:
            return 0
    else:
        print("ArrivalError")


def rule_of_three_and_poisson(time_simulate, numbers_meteorites, time_sampling):
    poisson = (time_sampling * numbers_meteorites) / time_simulate
    poisson_calculate = np.random.poisson(poisson)
    # e = math.e
    # factorial = math.factorial(time_sampling)
    # e_pow = pow(e, poisson * -1)
    # poisson_pow = pow(poisson, time_sampling)
    # poisson_calculate = (e_pow * poisson_pow) / factorial
    return poisson_calculate


def simulate(time_simulate, numbers_meteorites, time_sampling, amount_meteorites_limits, height,
             probability_explosion_meteorites, simulate_fall):
    simulate_fall.destroy()
    main_meteorites = 0
    for t in range(time_sampling):
        meteorites_sampling = rule_of_three_and_poisson(time_simulate, numbers_meteorites, time_sampling)
        if meteorites_sampling == 0 and main_meteorites == 0:
            main_meteorites = 0
        else:
            if main_meteorites == 0:
                main_meteorites = meteorites_sampling
            else:
                arrival_meteorites = valid_arrival_meteorites()
                if len(list_meteorites_main) < main_meteorites and arrival_meteorites == 1:
                    if len(list_meteorites_main) == 0:
                        r = random.randint(1, main_meteorites)
                        for i in range(r):
                            x = calculate_x()
                            meteorite = create_meteorite(i, x, height)
                            list_meteorites.append(meteorite)
                            list_meteorites_main.append(meteorite)
                        for i, m in enumerate(list_meteorites):
                            calculate_trajectories(m, t, probability_explosion_meteorites, amount_meteorites_limits)
                        # graph_meteorites(height)
                    else:
                        try:
                            r = random.randint(1, main_meteorites - len(list_meteorites_main))
                            for i in range(r):
                                x = calculate_x()
                                meteorite = create_meteorite(i, x, height)
                                list_meteorites.append(meteorite)
                                list_meteorites_main.append(meteorite)
                            for i, m in enumerate(list_meteorites):
                                calculate_trajectories(m, t, probability_explosion_meteorites, amount_meteorites_limits)
                        except Exception:
                            for i, m in enumerate(list_meteorites):
                                calculate_trajectories(m, t, probability_explosion_meteorites, amount_meteorites_limits)
                        # print(list_meteorites, "1")
                        # graph_meteorites(height)
                    print("creas los meteoritos principales  y evaluara si hay explosiones")
                    continue
                elif arrival_meteorites == 0:
                    if len(list_meteorites) > 0:
                        # print("si hay meteoritos")
                        for m in list_meteorites:
                            calculate_trajectories(m, t, probability_explosion_meteorites, amount_meteorites_limits)
                        # print(list_meteorites, "2")
                        # print("ya los calculo 2")
                    else:
                        print("no llego meteorito")
                    continue
                else:
                    if len(list_meteorites_main) == 0:
                        print("no puedes agregar explosiones")
                    else:
                        # print("si hay meteoritos 2")
                        for m in list_meteorites:
                            calculate_trajectories(m, t, probability_explosion_meteorites, amount_meteorites_limits)
                        # print(list_meteorites, "3")
                        print("si llego meteorito y evaluara si hay explosiones")
                    continue
                    # numbers_meteorites(meteorites)
                    # meteorites = numbers_meteorites()
                    # if meteorites == 0:
                    #     if len(list_meteorites) > 0:
                    #         print("si hay meteoritos")
                    #         for meteorite in list_meteorites:
                    #             calculate_trajectories(meteorite, t, delta_t)
                    #         print("ya los calculo 2")
                    #         continue
                    # else:
                    #     list_amount_meteorites.append(meteorites)
                    #     for m in range(meteorites):
                    #         print("si hay meteoritos")
                    #         x = calculate_x()
                    #         meteorite = create_meteorite(m, x, height)
                    #         list_meteorites.append(meteorite)
                    #     print("ya creo los nuevos meteoritos")
                    #     for meteorite in list_meteorites:
                    #         calculate_trajectories(meteorite, t, delta_t)
                    #     print("ya los calculo")
                    #     continue

    print("final", list_meteorites)
    graph_meteorites(height)
    options_show_tables()
    if clear_button is not None:
        clear_button.destroy()
        button_clear_and_again()
    else:
        button_clear_and_again()


def clean():
    if see_tables is not None:
        see_tables.destroy()
        label_meteorites_limit.destroy()
        amount_meteorites_limit.destroy()
        add_meteorites_limit_button.destroy()
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
        label_sampling_time.destroy()
        amount_sampling_time.destroy()
        add_sampling_time.destroy()
        label_height.destroy()
        amount_height.destroy()
        add_height.destroy()
        label_probability_explosion.destroy()
        probability_explosion.destroy()
        add_probability_button.destroy()
        clear_button.destroy()
        list_meteorites_main.clear()
        list_meteorites.clear()
        list_meteorites_exploited.clear()
        list_amount_meteorites.clear()
        list_meteorites_inactive.clear()
        list_trajectories_x.clear()
        list_trajectories_z.clear()
        list_min.clear()
        list_max.clear()
    elif simulate_fall is not None:
        label_meteorites_limit.destroy()
        amount_meteorites_limit.destroy()
        add_meteorites_limit_button.destroy()
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
        label_sampling_time.destroy()
        amount_sampling_time.destroy()
        add_sampling_time.destroy()
        label_height.destroy()
        amount_height.destroy()
        add_height.destroy()
        label_probability_explosion.destroy()
        probability_explosion.destroy()
        add_probability_button.destroy()
        clear_button.destroy()
    elif add_probability_button is not None:
        label_meteorites_limit.destroy()
        amount_meteorites_limit.destroy()
        add_meteorites_limit_button.destroy()
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
        label_sampling_time.destroy()
        amount_sampling_time.destroy()
        add_sampling_time.destroy()
        label_height.destroy()
        amount_height.destroy()
        add_height.destroy()
        label_probability_explosion.destroy()
        probability_explosion.destroy()
        add_probability_button.destroy()
        clear_button.destroy()
    elif add_height is not None:
        label_meteorites_limit.destroy()
        amount_meteorites_limit.destroy()
        add_meteorites_limit_button.destroy()
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
        label_sampling_time.destroy()
        amount_sampling_time.destroy()
        add_sampling_time.destroy()
        label_height.destroy()
        amount_height.destroy()
        add_height.destroy()
    elif add_meteorites_limit_button is not None:
        label_meteorites_limit.destroy()
        amount_meteorites_limit.destroy()
        add_meteorites_limit_button.destroy()
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
        label_sampling_time.destroy()
        amount_sampling_time.destroy()
        add_sampling_time.destroy()
    elif add_sampling_time is not None:
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
        label_sampling_time.destroy()
        amount_sampling_time.destroy()
        add_sampling_time.destroy()
    elif add_meteorites is not None:
        label_meteorites.destroy()
        amount_meteorites.destroy()
        add_meteorites.destroy()
    else:
        print("No hay que borrar")


def button_clear_and_again():
    global clear_button
    clear_button = tkinter.Button(canvas_options, text="Otra vez", background="white", foreground="black",
                                   command=lambda: clean())
    clear_button.pack(padx=2, pady=1, ipady=2, ipadx=8)


def button_simulate(time_simulate, numbers_meteorites, time_sampling, amount_meteorites, height, probability_explosion):
    global simulate_fall
    if probability_explosion < 0 or probability_explosion < 0.0:
        print("ProbabilityError")
    else:
        simulate_fall = tkinter.Button(canvas_options, text="Simular", background="red", foreground="white",
                                       command=lambda: simulate(time_simulate, numbers_meteorites, time_sampling,
                                                                amount_meteorites, height, probability_explosion,
                                                                simulate_fall))
        simulate_fall.pack(padx=2, pady=15, ipady=2, ipadx=8)
        if clear_button is not None:
            clear_button.destroy()
            button_clear_and_again()
        else:
            button_clear_and_again()


def options_probability_explosion(time_simulate, numbers_meteorites, time_sampling, amount_meteorites, height):
    global label_probability_explosion, probability_explosion, add_probability_button
    if height < 1 or height < 1.0:
        print("HeightError")
    else:
        label_probability_explosion = tkinter.Label(canvas_options, text="Probabilidad % explosion")
        label_probability_explosion.pack(padx=2, pady=8, ipady=2, ipadx=8)
        probability_explosion = tkinter.Entry(canvas_options)
        probability_explosion.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_probability_button = tkinter.Button(canvas_options, text=("Agregar probabilidad"),
                                                command=lambda: button_simulate(time_simulate, numbers_meteorites,
                                                                                time_sampling, amount_meteorites,
                                                                                height,
                                                                                float(probability_explosion.get())))
        add_probability_button.pack(padx=2, ipady=2, ipadx=8)
        button_clear_and_again()


def options_height_meteorite(time_simulate, numbers_meteorites, time_sampling, amount_meteorites):
    global label_height, amount_height, add_height
    if amount_meteorites < 0:
        print("AmountMeteoriteError")
    else:
        label_height = tkinter.Label(canvas_options, text="Altura (z) en metros")
        label_height.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_height = tkinter.Entry(canvas_options)
        amount_height.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_height = tkinter.Button(canvas_options, text="Agregar Altura",
                                    command=lambda: options_probability_explosion(time_simulate, numbers_meteorites,
                                                                                  time_sampling, amount_meteorites,
                                                                                  float(amount_height.get())))
        add_height.pack(padx=2, ipady=2, ipadx=8)


def options_numbers_meteorites(time_simulate, numbers_meteorites, time_sampling):
    global label_meteorites_limit, amount_meteorites_limit, add_meteorites_limit_button
    if time_sampling <= 0:
        print("TimeSamplingError")
    else:
        label_meteorites_limit = tkinter.Label(canvas_options, text="Limite de meteoritos de explosion")
        label_meteorites_limit.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_meteorites_limit = tkinter.Entry(canvas_options)
        amount_meteorites_limit.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_meteorites_limit_button = tkinter.Button(canvas_options, text="Agregar meteoritos",
                                                     command=lambda: options_height_meteorite(time_simulate,
                                                                                              numbers_meteorites,
                                                                                              time_sampling,
                                                                                              int(amount_meteorites_limit.get())))
        # options_probability_explosion(time, delta_t, height, amount_meteorites):
        add_meteorites_limit_button.pack(padx=2, ipady=2, ipadx=8)


def options_sampling_time(time_simulate, numbers_meteorites):
    global label_sampling_time, amount_sampling_time, add_sampling_time
    if numbers_meteorites <= 0:
        print("MeteoriteError")
    else:
        label_sampling_time = tkinter.Label(canvas_options, text="Fracmento de tiempo en dias deltat")
        label_sampling_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_sampling_time = tkinter.Entry(canvas_options)
        amount_sampling_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_sampling_time = tkinter.Button(canvas_options, text="Agregar tiempo",
                                           command=lambda: options_numbers_meteorites(time_simulate, numbers_meteorites,
                                                                                      int(amount_sampling_time.get())))
        add_sampling_time.pack(padx=2, ipady=2, ipadx=8)


def options_numbers_meteorites_by_days(time_simulate):
    global label_meteorites, amount_meteorites, add_meteorites
    if time_simulate <= 0:
        print("TimeError")
    else:
        label_meteorites = tkinter.Label(canvas_options, text=f'Media de meteoritos en {time_simulate} dias')
        label_meteorites.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_meteorites = tkinter.Entry(canvas_options)
        amount_meteorites.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_meteorites = tkinter.Button(canvas_options, text="Agregar media de meteoritos",
                                        command=lambda: options_sampling_time(time_simulate,
                                                                              int(amount_meteorites.get())))
        add_meteorites.pack(padx=2, ipady=2, ipadx=8)

def options_select_type_time_simulation():
    global label_type_time, entry_time, add_time
    label_type_time = tkinter.Label(canvas_options, text="Tiempo de simulacion en dias")
    label_type_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
    entry_time = tkinter.Entry(canvas_options)
    entry_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
    add_time = tkinter.Button(canvas_options, text="Agregar tiempo de simulacion",
                              command=lambda: options_numbers_meteorites_by_days(int(entry_time.get())))
    add_time.pack(padx=2, ipady=2, ipadx=8)


canvas_options = tkinter.Canvas(window, background='#%02x%02x%02x' % (120, 50, 45))
options_select_type_time_simulation()
canvas_options.place(anchor="nw", width=200, height=740, x=1, y=1, bordermode="inside")

window.mainloop()
