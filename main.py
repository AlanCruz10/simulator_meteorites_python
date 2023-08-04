import math
import tkinter
from tkinter import ttk
import random
import numpy as np
import Meteorite
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd

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
label_type_time = None
entry_time = None
add_time = None
label_meteorites = None
amount_meteorites = None
add_meteorites = None
label_sampling_time = None
amount_sampling_time = None
add_sampling_time = None
label_height = None
amount_height = None
add_height = None
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
                                        columns=(
                                            "trajectory_x", "trajectory_z", "trajectory_x_speed", "trajectory_z_speed"))
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
        for t_index, (x, z, xo, zo) in enumerate(
                zip(row["trajectory_x"], row["trajectory_z"], row["trajectory_x_speed"], row["trajectory_z_speed"])):
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
    yes_or_not_explode = random.randint(0, 100)
    if trajectory_z[-1] <= 0:
        return 0, "exploto"
    else:
        if yes_or_not_explode <= probability_explosion_meteorites:
            value, identifier = number_of_meteorites_generated(parts_explodes)
            return value, identifier
        else:
            return 0, "no exploto"


def number_of_meteorites_generated(parts_explodes):
    random_number = random.randint(2, parts_explodes)
    return random_number, "meteoritos"


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
    print(trajectory_z, trajectory_x)
    if len(trajectory_x) == 1 and trajectory_x[0] == 0.0 and len(trajectory_z) == 1 and trajectory_z[0] == 0.0 and \
            meteorite["status"] == "Active":
        trajectory_x_g = [x]
        meteorite["trajectory_x"] = trajectory_x_g
        trajectory_z_g = [z]
        meteorite["trajectory_z"] = trajectory_z_g
        trajectory_x_speed_g = [x_speed]
        meteorite["trajectory_x_speed"] = trajectory_x_speed_g
        trajectory_z_speed_g = [z_speed]
        meteorite["trajectory_z_speed"] = trajectory_z_speed_g

        print(trajectory_x, "del primero")
        print(trajectory_x_g, "del primero")
    else:
        value, identifier = validate_meteorites_explosion(trajectory_z, probability_explosion_meteorites,
                                                          amount_meteorites_limits)
        if value == 0 and identifier == "no exploto" and meteorite["status"] == "Active":
            if trajectory_z[-1] <= 0.0:
                print("entro no unu")
                trajectory_z[-1] = 0.0
                meteorite["trajectory_x"] = trajectory_x
                meteorite["trajectory_z"] = trajectory_z
                meteorite["trajectory_x_speed"] = trajectory_x_speed
                meteorite["trajectory_z_speed"] = trajectory_z_speed
                meteorite["status"] = "Inactive"
            else:
                x_noise = np.random.normal(loc=0, scale=0.1)
                trajectory_x_speed.append(trajectory_x_speed[-1] + x_noise)
                z_noise = abs(np.random.normal(loc=0, scale=0.1))
                trajectory_z_speed.append(trajectory_z_speed[-1] - z_noise)
                trajectory_x.append(trajectory_x[-1] + (trajectory_x_speed[-1] * delta_t))
                trajectory_z.append(trajectory_z[-1] + (trajectory_z_speed[-1] * delta_t))
                print(trajectory_x, trajectory_z, "del segundo")
                meteorite["trajectory_x"] = trajectory_x
                meteorite["trajectory_z"] = trajectory_z
                meteorite["trajectory_x_speed"] = trajectory_x_speed
                meteorite["trajectory_z_speed"] = trajectory_z_speed
                meteorite["status"] = "Active"
        elif value == 0 and identifier == "exploto" and meteorite["status"] == "Active":
            if trajectory_z[-1] <= 0.0:
                trajectory_z[-1] = 0.0
                meteorite["trajectory_x"] = trajectory_x
                meteorite["trajectory_z"] = trajectory_z
                meteorite["trajectory_x_speed"] = trajectory_x_speed
                meteorite["trajectory_z_speed"] = trajectory_z_speed
                meteorite["status"] = "Inactive"
            else:
                meteorite["trajectory_x"] = trajectory_x
                meteorite["trajectory_z"] = trajectory_z
                meteorite["trajectory_x_speed"] = trajectory_x_speed
                meteorite["trajectory_z_speed"] = trajectory_z_speed
                meteorite["status"] = "Inactive"
        elif value > 1 and identifier == "meteoritos" and meteorite["status"] == "Active":
            meteorite["trajectory_x"] = trajectory_x
            meteorite["trajectory_z"] = trajectory_z
            meteorite["trajectory_x_speed"] = trajectory_x_speed
            meteorite["trajectory_z_speed"] = trajectory_z_speed
            meteorite["status"] = "Inactive"
            print(trajectory_z[-1])
            for m in range(value):
                new_meteorite = create_meteorite(len(list_meteorites), trajectory_x[-1], trajectory_z[-1])
                list_meteorites.append(new_meteorite)
        print(trajectory_z)


def create_meteorite(id_meteorite, x, z):
    x_speed = calculate_x_speed()
    z_speed = calculate_z_speed()
    new_meteorite = dict(Meteorite.Meteorite(id=id_meteorite,
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
    z_speed = np.random.normal(loc=-1000, scale=0.5)
    return z_speed


def calculate_x_speed():
    x_speed = np.random.normal(loc=0, scale=0.5)
    return x_speed


def calculate_x():
    x = np.random.uniform(low=-100, high=100)
    return x


def rule_of_three(numbers_meteorites, time_sampling):
    poisson = (time_sampling * numbers_meteorites) / 1
    return poisson


def number_iterations(time_simulate, time_sampling):
    return math.ceil(time_simulate / time_sampling)


def simulate(time_simulate, numbers_meteorites, time_sampling, amount_meteorites_limits, height,
             probability_explosion_meteorites, simulate_fall):
    simulate_fall.destroy()
    meteorites_lambda = rule_of_three(numbers_meteorites, time_sampling)
    number_iteration = number_iterations(time_simulate, time_sampling)
    for t in range(number_iteration):
        meteorites_poisson = np.random.poisson(meteorites_lambda)
        for i in range(meteorites_poisson):
            x = calculate_x()
            meteorite = create_meteorite(len(list_meteorites), x, height)
            list_meteorites.append(meteorite)
        for j, m in enumerate(list_meteorites):
            calculate_trajectories(m, t, probability_explosion_meteorites, amount_meteorites_limits)
        print(list_meteorites)
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
    clear_button = tkinter.Button(canvas_options, text="Nueva simulacion", background="white", foreground="black",
                                  command=lambda: clean())
    clear_button.place(anchor="w")


def button_simulate(time_simulate, numbers_meteorites, time_sampling, amount_meteorites, height, probability_explosion):
    global simulate_fall
    if probability_explosion < 0:
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
    if height < 1:
        print("HeightError")
    else:
        label_probability_explosion = tkinter.Label(canvas_options, text="Probabilidad explosion % (ej: 20)")
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


def options_numbers_meteorites(time_simulate, time_sampling, numbers_meteorites):
    global label_meteorites_limit, amount_meteorites_limit, add_meteorites_limit_button
    if time_sampling <= 0:
        print("TimeSamplingError")
    else:
        label_meteorites_limit = tkinter.Label(canvas_options, text="Limite de explosion de los meteoritos")
        label_meteorites_limit.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_meteorites_limit = tkinter.Entry(canvas_options)
        amount_meteorites_limit.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_meteorites_limit_button = tkinter.Button(canvas_options, text="Agregar limite",
                                                     command=lambda: options_height_meteorite(time_simulate,
                                                                                              numbers_meteorites,
                                                                                              time_sampling,
                                                                                              int(amount_meteorites_limit.get())))
        add_meteorites_limit_button.pack(padx=2, ipady=2, ipadx=8)


def options_numbers_meteorites_by_day(time_simulate, time_sampling):
    global label_meteorites, amount_meteorites, add_meteorites
    if time_sampling <= 0:
        print("TimeError")
    else:
        label_meteorites = tkinter.Label(canvas_options, text="Media de meteoritos en un dia")
        label_meteorites.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_meteorites = tkinter.Entry(canvas_options)
        amount_meteorites.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_meteorites = tkinter.Button(canvas_options, text="Agregar media de meteoritos",
                                        command=lambda: options_numbers_meteorites(time_simulate,
                                                                                   time_sampling,
                                                                                   int(amount_meteorites.get())))
        add_meteorites.pack(padx=2, ipady=2, ipadx=8)


def options_sampling_time(time_simulate):
    global label_sampling_time, amount_sampling_time, add_sampling_time
    if time_simulate <= 0:
        print("MeteoriteError")
    else:
        label_sampling_time = tkinter.Label(canvas_options, text="Tiempo de muestreo en dias (Δt)")
        label_sampling_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
        amount_sampling_time = tkinter.Entry(canvas_options)
        amount_sampling_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
        add_sampling_time = tkinter.Button(canvas_options, text="Agregar tiempo",
                                           command=lambda: options_numbers_meteorites_by_day(time_simulate,
                                                                                             float(
                                                                                                 amount_sampling_time.get())))
        add_sampling_time.pack(padx=2, ipady=2, ipadx=8)


def options_select_type_time_simulation():
    global label_type_time, entry_time, add_time
    label_type_time = tkinter.Label(canvas_options, text="Tiempo de simulacion en dias")
    label_type_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
    entry_time = tkinter.Entry(canvas_options)
    entry_time.pack(padx=2, pady=8, ipady=2, ipadx=8)
    add_time = tkinter.Button(canvas_options, text="Agregar tiempo de simulacion",
                              command=lambda: options_sampling_time(float(entry_time.get())))
    add_time.pack(padx=2, ipady=2, ipadx=8)


canvas_options = tkinter.Canvas(window, background='#%02x%02x%02x' % (120, 50, 45))
options_select_type_time_simulation()
canvas_options.place(anchor="nw", width=200, height=740, x=1, y=1, bordermode="inside")

window.mainloop()
