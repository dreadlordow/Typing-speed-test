from tkinter import *
import time


list_of_texts = [
    ['The moon shines very bright tonight.'],
    ['What it means to write and run a Python script depends on whether you look at these '
     'tasks as a programmer, or as a Python interpreter. Both views offer important perspectives on Python programming.'],
    ['In its simplest form, a Python program is just a text file containing Python statements.'
     'For example, the following file, named script0.py, is one of the simplest Python scriptsI could dream up, '
     'but it passes for a fully functional Python program'],
    ['There was a long, dreary pause, which only Thud filled up by a vigorous onslaught on the mutton. '
     'He had almost satisfied his appetite, and was beginning, in nautical phrase, '
     'to get his talking-tackle on board, when the circle was joined by Pinfold.'],
    ['As may be imagined, the dinner which was soon afterwards partaken of by the '
     'family was anything but a cheerful meal. '
     'For the first time Io sat opposite to her husband gloomy and silent, '
     'scarcely touching the food before her'],
    ['chop confess sea conscious irritating hesitant juggle good tickle magical '
     'jam friend fluttering invent bump food '
     'stingy sniff whip rub zippy minute wish'
     ' cynical recognise understood yard hug '
     'substance acidic nosy charge consist industry '
     'follow wicked grandmother queue continue class '
     'jeans same flat quick petite purpose powder coat apologise gorgeous'],
    ]


# Main window
window = Tk()
window.title('Typing speed test')
window.configure(background='black')
window.geometry('800x600')

# Title Widget
lbl = Label(window, text='Typing speed test', font=('Arial', 30))
lbl.config(bg='black')
lbl.config(fg='#FFFF00')
lbl.place(x=400, y=50, anchor='center')


index = 0
# Levels widget
level_var = StringVar()
level_lbl = Label(window, textvar=level_var, font=('Arial', 16), bg='black', fg='#FFFFFF')
level_var.set(f'Level {index+1}')
level_lbl.place(x=350, y=100)

# The text you need to type in
text_var = StringVar()
text_var.set(list_of_texts[index][0])
example_text = Label(window, textvariable=text_var, wraplength=750, font=('Arial', 18), borderwidth=1, relief='solid', bg='black')
example_text.config(fg='#800080')
example_text.place(x=400, y=280, anchor='center')


# The textbox where you type
user_input = StringVar()
placeholder_text = '<When you finished typing your words click ENTER>'
txt = Entry(window, textvariable=user_input, justify='center')
txt.pack()
txt.insert(0, placeholder_text)
txt.configure(state=DISABLED)
txt.config(highlightthickness=2,highlightbackground='red',highlightcolor='red')
txt.place(width=700,height=50, x=400, y=450,anchor='center')


# Clear textfield when clicked
def on_click(event):
    txt.configure(state=NORMAL)
    txt.delete(0, END)
    txt.unbind('<Button-1>', on_click_id)


on_click_id = txt.bind('<Button-1>', on_click)


# Check how many of the words were correct
def check_correct_words():
    correct_words = 0
    list_of_words = list_of_texts[index][0].split()
    for i, word in enumerate(user_input.get().split()):
        try:
            if word == list_of_words[i]:
                correct_words += 1
        except IndexError:
            pass
    return correct_words


# Check how many characters you've entered
def check_char_entries():
    characters = 0
    for word in user_input.get().split():
        for _ in word:
            characters += 1
    return characters


start = 0
i = 0


# Start timer when you enter the first character
def start_time(*args):
    global i
    global start
    key = f'key{i}'
    if key == 'key0':
        start = time.time()
    i += 1


txt.bind('<KeyPress>', start_time)

wpm, accuracy, correct_words, end = 0, 0, 0, 0
wpm_list = []
info_text = StringVar()
correct_words_lbl = Label(window, textvar=info_text, font=('Arial', 18), bg='sky blue', anchor='center')


# Display your stats when you hit Enter-key
def callback(event):
    global index
    global wpm
    global accuracy
    global correct_words
    global end
    list_of_words = list_of_texts[index][0].split()
    length = len(list_of_words)
    correct_words = check_correct_words()
    accuracy = (correct_words / length) * 100
    end = time.time()
    chars = check_char_entries()
    wpm = (chars/5) / ((end - start) / 60)
    wpm_list.append(wpm)
    info_text.set(f'WPM: {wpm:.2f} Accuracy: {accuracy:.2f}%, Correct words: {correct_words}, Time: {end - start:.2f}')
    correct_words_lbl.place(x=80, y=425)
    txt.place_forget()


txt.bind('<Return>', callback)


# Refresh the screen with the next level, or show endscreen when game is over
def next_level():
    global start
    global i
    global index
    start = 0
    i = 0
    index += 1
    if index == len(list_of_texts):
        level_lbl.place_forget()
        correct_words_lbl.place_forget()
        txt.place_forget()
        example_text.place_forget()
        reset_btn.place_forget()
        average = sum(wpm_list) / len(wpm_list)
        end_game_lbl = Label(window, text=f'Congratulations! You finished all levels. Average WPM: {average:.2f}',
                             font=('Arial', 18), bg='black', fg='#FFFFFF')
        end_game_lbl.place(x=75, y=300)
    else:
        time.sleep(0.2)
        txt.delete(0, 'end')
        text_var.set(list_of_texts[index][0])
        correct_words_lbl.place_forget()
        level_var.set(f'Level {index + 1}')
        txt.place(width=700, height=50, x=400, y=450, anchor='center')


# Next level button
reset_btn = Button(window, text='Next level', width=10, height=3, bg='red', command=next_level)
reset_btn.place(x=350, y=500)


window.mainloop()

