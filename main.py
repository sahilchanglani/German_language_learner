from tkinter import *
import random
import MySQLdb

BACKGROUND_COLOR = "#B1DDC6"
new_card = tuple()

connection = MySQLdb.connect(host="localhost", user="root", password="", database="german_words")
cursor = connection.cursor()



def german_card():
    global new_card, flip_timer
    window.after_cancel(flip_timer)
    str = "SELECT * FROM words"
    cursor.execute(str)
    new_card = random.choice(cursor.fetchall())
    print(new_card)
    canvas.itemconfig(title_text, text="German", fill="black")
    canvas.itemconfig(word_text, text=new_card[1], fill="black")
    canvas.itemconfig(card_background, image=front_image)
    flip_timer = window.after(3000, func=english_card)


def english_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=new_card[2], fill="white")
    canvas.itemconfig(card_background, image=back_image)


def is_known():
    try:
        str = "INSERT INTO known_words VALUES('%s', '%s', '%s')"
        args = (new_card[0], new_card[1], new_card[2])
        cursor.execute(str % args)
        connection.commit()
    except:
        print(f'Row {new_card[0]} not inserted')
    str = "DELETE FROM words WHERE id='%s'"
    args = (new_card[0])
    cursor.execute(str % args)
    connection.commit()
    german_card()


def reverse():
    global flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(title_text, text="German", fill="black")
    canvas.itemconfig(word_text, text=new_card[1], fill="black")
    canvas.itemconfig(card_background, image=front_image)
    flip_timer = window.after(3000, func=english_card)


window = Tk()
window.title("Flashy German")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=english_card)

canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

wrong_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=german_card)
unknown_button.grid(row=1, column=0)

reverse_image = PhotoImage(file="images/back.png")
swap_button = Button(image=reverse_image, highlightthickness=0, command=reverse)
swap_button.grid(row=1, column=1)

right_image = PhotoImage(file="images/right.png")
known_button = Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=2)

german_card()

window.mainloop()