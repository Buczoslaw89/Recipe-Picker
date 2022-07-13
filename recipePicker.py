from tkinter import *
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet

bg_color = "#3d6466"

pyglet.font.add_file("fonts/Shanti-Regular.ttf")
pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")


def clear_screen(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()

    idx = random.randint(0, len(all_tables)-1)

    # fetch ingredients
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    ingredients = cursor.fetchall()

    connection.close()
    return table_name, ingredients


def pre_process(table_name, ingredients):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    ingr = []

    for i in ingredients:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingr.append(qty + " " + unit + " of " + name)

    return title, ingr


def load_frame1():
    clear_screen(frame2)
    frame1.tkraise()
    frame1.propagate(False)
    # frame1 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    # text
    Label(frame1,
          text="Ready for your random recipe?",
          bg=bg_color,
          fg="white",
          font=("Shanti", 14)
          ).pack()

    # Button
    Button(
        frame1,
        text="Shuffle",
        font=("Ubuntu", 20),
        bg="#28393a",
        activebackground="#28393a",
        fg="white",
        activeforeground="white",
        cursor="hand2",
        command=lambda: load_frame2()
        ).pack(pady=20)


def load_frame2():
    clear_screen(frame1)
    frame2.tkraise()
    table_name, ingredients = fetch_db()
    title, ingr = pre_process(table_name, ingredients)

    # frame2 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    # text
    Label(frame2,
          text=title,
          bg=bg_color,
          fg="white",
          font=("Ubuntu", 20)
          ).pack(pady=25)

    for i in ingr:
        Label(frame2,
              text=i,
              bg="#28393a",
              fg="white",
              font=("Shanti", 12)
              ).pack(fill="both")

    # Button
    Button(
        frame2,
        text="Back",
        font=("Ubuntu", 18),
        bg="#28393a",
        activebackground="#28393a",
        fg="white",
        activeforeground="white",
        cursor="hand2",
        command=lambda: load_frame1()
        ).pack(pady=20)


# initialize app
root = Tk()
root.title("Recipe picker")

# created a frame
frame1 = Frame(root, width=500, height=600, bg=bg_color)
frame2 = Frame(root, bg=bg_color)
for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")


load_frame1()


# run app
root.mainloop()
