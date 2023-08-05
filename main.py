from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

#-------------Create new flashcards Setup------------------#
#First time it runs it will crash so need to catch exception
try:
    data = pandas.read_csv("words_to_learn.csv")
#orient to grab entries not index number
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

#-------------Flilp flashcards Setup------------------#
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# -------------Save Progress------------------#
    #remove cards we know from the list we need to learn and french_words list is reduced
def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    #create new data fram created for to_learn list cuz  french_words resets to all words after run
    data = pandas.DataFrame(to_learn)
    #do not add index number
    data.to_csv("words_to_learn.csv", index=False)
    next_card()

#-------------FRONT UI Setup------------------#

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
#flip card after 3 seconds
window.after(3000, func=flip_card)
flip_timer = window.after(3000, func=flip_card)

#---------------Flashcard canvas__________#
canvas = Canvas(width=800, height=526)
#must be in canvas. Won't work inside function
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

#-------------Buttons X and Y------------------#
#image to buttons
wrong_image = PhotoImage(file="wrong.png")
right_image = PhotoImage(file="right.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, relief=FLAT, command=next_card)
wrong_button.grid(row=1, column=0, sticky="EW")
wrong_button.config(padx=50, pady=50)
right_button = Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, relief=FLAT, command=is_known)
right_button.grid(row=1, column=1)
right_button.config(padx=50, pady=50)

next_card()




window.mainloop()