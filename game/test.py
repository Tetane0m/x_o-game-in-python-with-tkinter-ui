import time
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import *
from tkinter import ttk

import random
import string
import json


## ----------------------------------------------- ##
## ----------------------------------------------- ##
## --------****************************----------- ##
## --------**  FUNCTION OF THE GAME  **----------- ##
## --------****************************----------- ##
## ----------------------------------------------- ##
## ----------------------------------------------- ##


# Function to handle button clicks //////
def button_click(row, col):
    global player
    if buttons[row][col]["text"] == " ":
        buttons[row][col]["text"] = player

        if check_winner():
            highlight_winner()
            messagebox.showinfo("X_O game", "Player {} wins!".format(player))
            update_counter(player)
            clear_board()

        elif is_board_full():
            highlight_tie()
            messagebox.showinfo("X_O game", "It's a tie!")
            clear_board()
            return

        # Computer's turn
        if AUTO_PLAY == "True":
            if not check_winner() and not is_board_full():
                computer_turn()

        if AUTO_PLAY == "False":
            if player == CHARECKTER.split(",")[0]:
                player = CHARECKTER.split(",")[1]
            else:
                player = CHARECKTER.split(",")[0]


# Function for the computer's turn //////
def computer_turn():
    available_buttons = []
    pl = CHARECKTER.split(",")
    pl.remove(PLAYER_CHAR)

    for i in range(3):
        for j in range(3):
            if " " == buttons[i][j]["text"]:
                available_buttons.append((i, j))

    row, col = random.choice(available_buttons)
    buttons[row][col]["text"] = pl

    if check_winner():
        highlight_winner()
        messagebox.showinfo("X_O game", "Player {} wins!".format(pl[0]))
        update_counter(pl[0])
        clear_board()
        rand = random.choice(CHARECKTER.split(","))
        if rand != player:
            computer_turn()
            return

    elif is_board_full():
        highlight_tie()
        messagebox.showinfo("X_O game", "It's a tie!")
        clear_board()
        return


# Function to check if a player has won //////
def check_winner():
    for i in range(3):
        if (
                buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != " "
                or buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != " "
        ):
            return True

    if (
            buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != " "
            or buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != " "
    ):
        return True

    return False


# Function to highlight the winning blocks in blue /////
def highlight_winner():
    # Check rows
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != " ":
            buttons[i][0].config(bg="blue")
            buttons[i][1].config(bg="blue")
            buttons[i][2].config(bg="blue")

    # Check columns
    for i in range(3):
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != " ":
            buttons[0][i].config(bg="blue")
            buttons[1][i].config(bg="blue")
            buttons[2][i].config(bg="blue")

    # Check diagonals
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != " ":
        buttons[0][0].config(bg="blue")
        buttons[1][1].config(bg="blue")
        buttons[2][2].config(bg="blue")

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != " ":
        buttons[0][2].config(bg="blue")
        buttons[1][1].config(bg="blue")
        buttons[2][0].config(bg="blue")


# Function to highlight the blocks in red for a tie /////
def highlight_tie():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(bg="red")


# Function to check if the board is full /////
def is_board_full():
    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == " ":
                return False
    return True


# Function to clear the game board /////
def clear_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", bg=BACKGROUND)
    game_counter.set(f"Player {CHARECKTER.split(',')[0]} : {player_x_count.get()}\n"
                     f"Player {CHARECKTER.split(',')[1]} : {player_o_count.get()}")
    if AUTO_PLAY == True:
        rand = random.choice(["X", "O"])
        if rand != player:
            computer_turn()


# Function to clear the counter /////
def clear_counter():
    if player_x_count.get() > 0 or player_o_count.get() > 0:
        for i in range(3):
            for j in range(3):
                buttons[i][j].config(text=" ", state=NORMAL, bg=BACKGROUND)

        player_x_count.set(0)
        player_o_count.set(0)
        game_counter.set(f"Player {CHARECKTER.split(',')[0]} : {player_x_count.get()}\n"
                         f"Player {CHARECKTER.split(',')[1]} : {player_o_count.get()}")

        messagebox.showinfo("Reset", "The counter has been reset successfully!! ")

        if AUTO_PLAY == "True":
            rand = random.choice(["X", "O"])
            if rand != player:
                computer_turn()


# Function to update the game counter /////
def update_counter(player):
    if player == CHARECKTER.split(',')[0]:
        player_x_count.set(player_x_count.get() + 1)
    elif player == CHARECKTER.split(',')[1]:
        player_o_count.set(player_o_count.get() + 1)


# Function to re rite the file ////
def re_write_file(item, value):
    with open("C:\\Users\\asus\\Desktop\\game\\color.json", "r") as file_r:
        data = json.loads(file_r.read())
        file_r.close()

    if item == 1:
        data["chareckter"] = f"{value[0]},{value[1]}"
        data["your_char"] = value[0]

    elif item == 2:
        valu = "True" if AUTO_PLAY == "False" else "False"
        data["auto_play"] = valu

    elif item == 3:
        data["your_char"] = value

    elif item == 4:
        data["font_styel"] = value

    elif item == 5:
        data["color_data"] = value
        data["them"] = "Dark" if data["them"] == "Light" else "Light"

    elif item == 6:
        data["count"] = 0

    else:
        data["user_and_password"] = value

    with open("C:\\Users\\asus\\Desktop\\game\\color.json", "w") as file_w:
        file_w.write(json.dumps(data, indent=2))
        file_w.close()
    read_file()


# Function to read the file ////
def read_file():
    global BACKGROUND, CHARECKTER, AUTO_PLAY, PLAYER_CHAR, COLOR_DATA, THEM, COUNT
    global FONT_STYEL, USER_NAME, PASSWORD, PRI_COL, INPUT_ENTRY_COLOR, TITLE_COLOR

    with open("C:\\Users\\asus\\Desktop\\game\\color.json", "r") as file:
        date = json.loads(file.read())

        THEM = date["them"]
        CHARECKTER = date["chareckter"]
        AUTO_PLAY = date["auto_play"]
        PLAYER_CHAR = date["your_char"]
        FONT_STYEL = date["font_styel"]
        USER_NAME = date["user_and_password"][0]
        PASSWORD = date["user_and_password"][1]
        COLOR_DATA = date["color_data"]
        BACKGROUND = COLOR_DATA[0]
        PRI_COL = COLOR_DATA[1]
        INPUT_ENTRY_COLOR = COLOR_DATA[2]
        TITLE_COLOR = COLOR_DATA[3]
        COUNT = date['count']
        file.close()


read_file()


## ----------------------------------------------- ##
## ----------------------------------------------- ##
## --------****************************----------- ##
## --------** INTERFACE OF THE  GAME **----------- ##
## --------****************************----------- ##
## ----------------------------------------------- ##
## ----------------------------------------------- ##


# settings bage part!!!
def setting_bage(*args):
    global settings_bage_frame, \
        theme_frame, \
        theme_frame, \
        settings_label, \
        mood_frame, \
        mood_button, \
        chareckter_frame, \
        charckter_entry, \
        charekter_plyer_button

    home_bage_button.config(state=NORMAL, bg=BACKGROUND)
    game_bage_button.config(state=NORMAL, bg=BACKGROUND)
    setting_bage_button.config(state=DISABLED, bg=PRI_COL)

    window.bind("<Left>", game_bage)
    window.bind("<Right>", "")
    window.bind("<Escape>", "")
    window.bind("<Return>", "")
    setting_bage_button.bind("<Enter>", "")
    setting_bage_button.bind("<Leave>", "")
    game_bage_button.bind("<Enter>", lambda x: game_bage_button.config(bg=INPUT_ENTRY_COLOR))
    game_bage_button.bind("<Leave>", lambda x: game_bage_button.config(bg=BACKGROUND))
    home_bage_button.bind("<Enter>", lambda x: home_bage_button.config(bg=INPUT_ENTRY_COLOR))
    home_bage_button.bind("<Leave>", lambda x: home_bage_button.config(bg=BACKGROUND))

    # change password bage part!!!
    def change_password():
        settings_bage_frame.destroy()
        navbar_button_frame.destroy()
        window.bind("<Left>", "")

        # made the fuction of eye img  /////
        def show_password():
            if password_entry['show'] == "*":
                password_entry.config(show="")
                eye_img.config(image=show_pass_img)
                confirm_entry.config(show="")
                return
            else:
                password_entry.config(show="*")
                eye_img.config(image=hide_pass_img)
                confirm_entry.config(show="*")

        # made the fuction for random information /////
        def random_choice():
            number = string.ascii_letters + string.digits + string.punctuation
            random_password = "".join(random.choice(number) for i in range(8))
            str(random_password)
            e = [password_entry, confirm_entry]
            for entry in e:
                entry.delete(0, END)
                entry.insert(0, random_password)

        # made the fuction of back button /////
        def back_button_f(*args):
            security_frame.destroy()
            nav_bar()
            setting_bage()

        # made the fuction of save button /////
        def save_button_f(*args):
            if len(user_name_entry.get()) > 0 and len(password_entry.get()) > 0 and len(confirm_entry.get()) > 0:
                if (password_entry.get() == confirm_entry.get()):
                    if len(password_entry.get()) <= 8 and len(confirm_entry.get()) <= 8:
                        if len(password_entry.get().split(" ")) == 1:
                            if user_name_entry.get() == USER_NAME and password_entry.get() == PASSWORD:
                                return messagebox.showerror('invalid inputs',
                                                            'this information are alredy used !!')
                            else:
                                re_write_file(7, [user_name_entry.get(), password_entry.get()])
                                for item in [user_name_entry, password_entry, confirm_entry]:
                                    item.delete(0, END)
                                return messagebox.showinfo('data saved succussfily ',
                                                           'your data has ben changed succussfily !!')
                        return messagebox.showerror('invalid inputs',
                                                    'dont make the password many secttion like \"hai der\"\n'
                                                    'inter it in one word \nand dont start and end with space !!')
                    return messagebox.showerror('invalid inputs', 'inter password less than 8 digts !!')
                return messagebox.showerror('invalid inputs', 'invalid input in confirm password , \n'
                                                              'inter the same value you have inter in fild before it !!')
            return messagebox.showerror('invalid inputs', 'pleace sure to inter all the information before save !!')

        security_frame = Frame(window,
                               bg=BACKGROUND,
                               height=640,
                               width=520)

        security_label = Label(security_frame,
                               text='Security ',
                               font=("Fixedsys", 50),
                               fg=TITLE_COLOR,
                               bg=BACKGROUND,
                               compound='right',
                               image=security_img,
                               cursor=['hand2'])

        inputs_frame = Frame(security_frame,
                             bg=BACKGROUND,
                             width=520)

        first_frame = Frame(inputs_frame,
                            bg=BACKGROUND)

        user_label = Label(first_frame,
                           text="new user name :",
                           font=("consolas", 20),
                           justify="left",
                           fg=PRI_COL,
                           bg=BACKGROUND)

        input_entry_img_frame = Frame(first_frame,
                                      bg=BACKGROUND)

        user_name_entry = Entry(input_entry_img_frame,
                                font=("consloas", 18),
                                width=22,
                                highlightbackground=PRI_COL,
                                highlightthickness=4,
                                highlightcolor=INPUT_ENTRY_COLOR,
                                bg=BACKGROUND,
                                fg=PRI_COL,
                                justify='left')

        random_img = Button(input_entry_img_frame,
                            bg=BACKGROUND,
                            borderwidth=0,
                            image=rand_img,
                            width=100,
                            compound='left',
                            cursor=['hand2'],
                            command=random_choice,
                            activebackground=BACKGROUND)

        second_frame = Frame(inputs_frame,
                             bg=BACKGROUND)

        password_label = Label(second_frame,
                               text="new password :",
                               font=("consolas", 20),
                               justify="left",
                               fg=PRI_COL,
                               bg=BACKGROUND)

        input_entry_img_password_frame = Frame(second_frame,
                                               bg=BACKGROUND)

        password_entry = Entry(input_entry_img_password_frame,
                               width=22,
                               highlightbackground=PRI_COL,
                               highlightthickness=4,
                               highlightcolor=INPUT_ENTRY_COLOR,
                               bg=BACKGROUND,
                               fg=PRI_COL,
                               justify='left',
                               font=("consloas", 18),
                               show="*")

        eye_img = Button(input_entry_img_password_frame,
                         bg=BACKGROUND,
                         borderwidth=0,
                         image=hide_pass_img,
                         width=100,
                         compound='left',
                         cursor=['hand2'],
                         command=show_password,
                         activebackground=BACKGROUND)

        third_frame = Frame(inputs_frame,
                            bg=BACKGROUND,
                            width=520)

        confirm_label = Label(third_frame,
                              text="confirm password :",
                              font=("consolas", 20),
                              justify="left",
                              fg=PRI_COL,
                              bg=BACKGROUND)

        confirm_entry = Entry(third_frame,
                              width=22,
                              highlightbackground=PRI_COL,
                              highlightthickness=4,
                              highlightcolor=INPUT_ENTRY_COLOR,
                              bg=BACKGROUND,
                              fg=PRI_COL,
                              justify='left',
                              font=("consloas", 18),
                              show="*")

        buttons_frame = Frame(inputs_frame,
                              bg=BACKGROUND,
                              width=500)

        back_btn_frame = Frame(buttons_frame,
                               bg=PRI_COL,
                               highlightbackground=PRI_COL,
                               highlightthickness=2)

        back_button = Button(back_btn_frame,
                             text="Back",
                             fg=PRI_COL,
                             font=("system", 23),
                             bg=BACKGROUND,
                             command=back_button_f,
                             compound="right",
                             image=back_img,
                             padx=20,
                             justify='left',
                             cursor=['hand2'],
                             borderwidth=0,
                             activebackground=PRI_COL,
                             activeforeground=BACKGROUND)

        back_button.bind("<Enter>", lambda x: back_button.config(bg=INPUT_ENTRY_COLOR))
        back_button.bind("<Leave>", lambda x: back_button.config(bg=BACKGROUND))

        save_btn_frame = Frame(buttons_frame,
                               bg=PRI_COL,
                               highlightbackground=PRI_COL,
                               highlightthickness=2)

        save_button = Button(save_btn_frame,
                             text="Save",
                             fg=PRI_COL,
                             font=("system", 23),
                             bg=BACKGROUND,
                             command=save_button_f,
                             compound="right",
                             image=saved_img,
                             padx=20,
                             justify='left',
                             cursor=['hand2'],
                             borderwidth=0,
                             activebackground=PRI_COL,
                             activeforeground=BACKGROUND)

        save_button.bind("<Enter>", lambda x: save_button.config(bg=INPUT_ENTRY_COLOR))
        save_button.bind("<Leave>", lambda x: save_button.config(bg=BACKGROUND))

        security_frame.pack(pady=[20, 0])
        security_label.pack(pady=[0, 70])
        inputs_frame.pack()
        first_frame.pack(pady=[0, 15])
        user_label.pack(anchor=W)
        input_entry_img_frame.pack(padx=[30, 0])
        user_name_entry.pack(side='left')
        random_img.pack(side='right')

        second_frame.pack(pady=15)
        password_label.pack(anchor=W)
        input_entry_img_password_frame.pack(padx=[30, 0])
        password_entry.pack(side='left')
        eye_img.pack(side='right')
        third_frame.pack(pady=[15, 0], anchor=W)
        confirm_label.pack(anchor=W)
        confirm_entry.pack(padx=[30, 0])
        buttons_frame.pack(pady=[50, 0])
        back_btn_frame.pack(side='left', padx=[0, 40], pady=50)
        back_button.pack()
        save_btn_frame.pack(side='right', padx=[40, 0], pady=50)
        save_button.pack()

        window.bind("<Return>", save_button_f)
        window.bind("<Escape>", back_button_f)

    # Function to change the color ////
    def change_background_color():
        if THEM == "Dark":
            re_write_file(5, [
                "white",
                "black",
                "#30302f",
                "#1ecbe1"
            ])
        elif THEM == "Light":
            re_write_file(5, [
                "black",
                "white",
                "#30302f",
                "blue"
            ])

        settings_bage_frame.destroy()
        navbar_button_frame.destroy()
        nav_bar()
        setting_bage()
        window.config(bg=BACKGROUND)

    # Function to change game mood play (1 x 1) or with coumputer /////
    def change_player():
        re_write_file(2, f"{AUTO_PLAY}")
        mood_button.config(text=AUTO_PLAY)

    # Function to change chareckter of the player /////
    def chang_char_player():
        if PLAYER_CHAR == CHARECKTER.split(",")[0]:
            re_write_file(3, CHARECKTER.split(",")[1])
            charekter_plyer_button.config(text=PLAYER_CHAR)
        else:
            re_write_file(3, CHARECKTER.split(",")[0])

        charekter_plyer_button.config(text=PLAYER_CHAR)

    # Function to change styel of text of the game /////
    def chang_font_styel():

        if FONT_STYEL == "normal":
            re_write_file(4, "italic")
        elif FONT_STYEL == "italic":
            re_write_file(4, "underline")
        else:
            re_write_file(4, "normal")

        font_styel_button.config(text=FONT_STYEL)

        button_item = [mood_button,
                       charekter_plyer_button,
                       font_styel_button,
                       theme_button]
        for i in button_item:
            i.config(font=("consolas", 20, FONT_STYEL))

        item_label = [theme_label,
                      chareckter_label,
                      mood_label,
                      plyer_chareckter,
                      fontstyel_label]
        for i in item_label:
            i.config(font=("consolas", 28, FONT_STYEL))

    # Function to change chareckter of the game /////
    def check_charckter(*args):
        n2_split = charckter_entry.get().split(",")
        if len(charckter_entry.get()) < 5 \
                and len(n2_split) == 2 \
                and len(n2_split[0]) > 0 \
                and len(n2_split[1]) > 0 \
                and n2_split[0] != n2_split[1] \
                and len(n2_split[0]) < 3 \
                and len(n2_split[1]) < 3 \
                and " " not in n2_split[0] \
                and " " not in n2_split[1]:
            if n2_split[0] != CHARECKTER.split(",")[0] \
                    and n2_split[1] != CHARECKTER.split(",")[1]:
                re_write_file(1, charckter_entry.get().split(","))
                charckter_entry.delete(0, END)
                charckter_entry.insert(0, CHARECKTER)
                charekter_plyer_button.config(text=PLAYER_CHAR)
                player_x_count.set(0)
                player_o_count.set(0)
                return messagebox.showinfo("info",
                                           "your charckter have been changed suucussfily !")
            return messagebox.showerror("invalid input",
                                        "this charckter is alredy in use !!! ")

        charckter_entry.delete(0, END)
        return messagebox.showerror("invalid input",
                                    "inter only tow charckter less than 4 charckter for every one .")

    try:
        game_bage_frame.destroy()
    except:
        pass
    try:
        hame_bage_frame.destroy()
    except:
        pass

    settings_bage_frame = Frame(window,
                                width=370,
                                height=520,
                                bg=BACKGROUND)
    settings_bage_frame.pack()

    settings_label = Label(settings_bage_frame,
                           fg=TITLE_COLOR,
                           text="Settings  ",
                           bg=BACKGROUND,
                           font=("Fixedsys", 50),
                           compound='right',
                           image=setting_img,
                           cursor=['hand2'])
    settings_label.pack(pady=10)

    setting_item = Frame(settings_bage_frame,
                         bg=BACKGROUND,
                         pady=10,
                         padx=10)
    setting_item.pack(pady=[30, 0])

    theme_frame = Frame(setting_item,
                        bg=BACKGROUND)

    theme_label = Label(theme_frame,
                        text='Theme      :',
                        width=14,
                        fg=PRI_COL,
                        font=("consolas", 28, FONT_STYEL),
                        bg=BACKGROUND,
                        anchor=W)

    theme_btn_frame = Frame(theme_frame,
                            bg=BACKGROUND,
                            highlightbackground=PRI_COL,
                            highlightthickness=3,
                            highlightcolor=PRI_COL)

    theme_button = Button(theme_btn_frame,
                          text=THEM,
                          font=("consolas", 20, FONT_STYEL),
                          command=change_background_color,
                          bg=BACKGROUND,
                          fg=PRI_COL,
                          width=11,
                          cursor=['hand2'],
                          borderwidth=0,
                          activebackground=PRI_COL,
                          activeforeground=BACKGROUND)
    theme_button.bind("<Enter>", lambda x: theme_button.config(bg=INPUT_ENTRY_COLOR))
    theme_button.bind("<Leave>", lambda x: theme_button.config(bg=BACKGROUND))

    theme_frame.pack(pady=6)
    theme_label.grid(row=0, column=0)
    theme_btn_frame.grid(row=0, column=1)
    theme_button.pack()

    chareckter_frame = Frame(setting_item,
                             bg=BACKGROUND)

    chareckter_label = Label(chareckter_frame,
                             text='Charckter  :',
                             width=14,
                             fg=PRI_COL,
                             font=("consolas", 28, FONT_STYEL),
                             bg=BACKGROUND,
                             anchor=W)

    chareckter_btn_frame = Frame(chareckter_frame,
                                 bg=BACKGROUND,
                                 highlightbackground=PRI_COL,
                                 highlightthickness=3,
                                 highlightcolor=INPUT_ENTRY_COLOR)

    charckter_entry = Entry(chareckter_btn_frame,
                            font=("consolas", 26),
                            width=6,
                            bg=BACKGROUND,
                            fg=PRI_COL,
                            cursor=['hand2'])
    charckter_entry.insert(0, CHARECKTER)
    charckter_entry.bind("<Return>", check_charckter)

    save_button = Button(chareckter_btn_frame,
                         text="Save",
                         command=check_charckter,
                         bg=BACKGROUND,
                         fg=PRI_COL,
                         font=("consolas", 15, FONT_STYEL),
                         border=0,
                         cursor=['hand2'],
                         borderwidth=0,
                         activebackground=PRI_COL,
                         activeforeground=BACKGROUND)
    save_button.bind("<Enter>", lambda x: save_button.config(bg=INPUT_ENTRY_COLOR))
    save_button.bind("<Leave>", lambda x: save_button.config(bg=BACKGROUND))

    chareckter_frame.pack(pady=6)
    chareckter_label.grid(row=0, column=0)
    chareckter_btn_frame.grid(row=0, column=1)
    save_button.pack(side='right', fill=Y)
    charckter_entry.pack(side='right')

    mood_frame = Frame(setting_item,
                       bg=BACKGROUND)

    mood_label = Label(mood_frame,
                       text='Auto play  :',
                       width=14,
                       fg=PRI_COL,
                       font=("consolas", 28, FONT_STYEL),
                       bg=BACKGROUND,
                       anchor=W)

    mood_btn_frame = Frame(mood_frame,
                           bg=BACKGROUND,
                           highlightbackground=PRI_COL,
                           highlightthickness=3)

    mood_button = Button(mood_btn_frame,
                         text=AUTO_PLAY,
                         command=change_player,
                         font=("consolas", 20, FONT_STYEL),
                         bg=BACKGROUND,
                         fg=PRI_COL,
                         width=11,
                         relief=["raised"],
                         cursor=['hand2'],
                         borderwidth=0,
                         activebackground=PRI_COL,
                         activeforeground=BACKGROUND)
    mood_button.bind("<Enter>", lambda x: mood_button.config(bg=INPUT_ENTRY_COLOR))
    mood_button.bind("<Leave>", lambda x: mood_button.config(bg=BACKGROUND))

    mood_frame.pack(pady=6)
    mood_label.grid(row=0, column=0)
    mood_btn_frame.grid(row=0, column=1)
    mood_button.pack()

    charekter_frame = Frame(setting_item,
                            bg=BACKGROUND)

    plyer_chareckter = Label(charekter_frame,
                             text='Play as    :',
                             width=14,
                             fg=PRI_COL,
                             font=("consolas", 28, FONT_STYEL),
                             bg=BACKGROUND,
                             anchor=W)

    charekter_btn_frame = Frame(charekter_frame,
                                bg=BACKGROUND,
                                highlightbackground=PRI_COL,
                                highlightthickness=3)

    charekter_plyer_button = Button(charekter_btn_frame,
                                    text=PLAYER_CHAR,
                                    font=("consolas", 20, FONT_STYEL),
                                    command=chang_char_player,
                                    bg=BACKGROUND,
                                    fg=PRI_COL,
                                    width=11,
                                    cursor=['hand2'],
                                    borderwidth=0,
                                    activebackground=PRI_COL,
                                    activeforeground=BACKGROUND)
    charekter_plyer_button.bind("<Enter>", lambda x: charekter_plyer_button.config(bg=INPUT_ENTRY_COLOR))
    charekter_plyer_button.bind("<Leave>", lambda x: charekter_plyer_button.config(bg=BACKGROUND))

    charekter_frame.pack(pady=6)
    plyer_chareckter.grid(row=0, column=0)
    charekter_btn_frame.grid(row=0, column=1)
    charekter_plyer_button.pack()

    font_styel_frame = Frame(setting_item,
                             bg=BACKGROUND)

    fontstyel_label = Label(font_styel_frame,
                            text='Font styel :',
                            width=14,
                            fg=PRI_COL,
                            font=("consolas", 28, FONT_STYEL),
                            bg=BACKGROUND,
                            anchor=W,
                            borderwidth=0)

    font_styel_btn_frame = Frame(font_styel_frame,
                                 bg='red',
                                 highlightbackground=PRI_COL,
                                 highlightthickness=3)

    font_styel_button = Button(font_styel_btn_frame,
                               text=FONT_STYEL,
                               font=("consolas", 20, FONT_STYEL),
                               command=chang_font_styel,
                               bg=BACKGROUND,
                               fg=PRI_COL,
                               width=11,
                               cursor=['hand2'],
                               borderwidth=0,
                               activebackground=PRI_COL,
                               activeforeground=BACKGROUND)
    font_styel_button.bind("<Enter>", lambda x: font_styel_button.config(bg=INPUT_ENTRY_COLOR))
    font_styel_button.bind("<Leave>", lambda x: font_styel_button.config(bg=BACKGROUND))

    font_styel_frame.pack(pady=6)
    fontstyel_label.grid(row=0, column=0)
    font_styel_btn_frame.grid(row=0, column=1)
    font_styel_button.pack()

    # logout and change password button /////

    bottom_buttons_frame = Frame(setting_item,
                                 bg=BACKGROUND)

    log_out_frame = Frame(bottom_buttons_frame,
                          bg=BACKGROUND,
                          highlightbackground=PRI_COL,
                          highlightthickness=3)

    log_out_btn = Button(log_out_frame,
                         text="Log out  ",
                         font=("system", 14),
                         command=Login_bage,
                         bg=BACKGROUND,
                         fg='red',
                         justify='center',
                         compound='right',
                         image=log_out_img,
                         cursor=['hand2'],
                         width=200,
                         pady=8,
                         borderwidth=0,
                         activebackground=PRI_COL,
                         activeforeground='red')

    log_out_btn.bind("<Enter>", lambda x: log_out_btn.config(bg=INPUT_ENTRY_COLOR))
    log_out_btn.bind("<Leave>", lambda x: log_out_btn.config(bg=BACKGROUND))

    change_password_frame = Frame(bottom_buttons_frame,
                                  bg=BACKGROUND,
                                  highlightbackground=PRI_COL,
                                  highlightthickness=3,
                                  borderwidth=0)

    change_password_btn = Button(change_password_frame,
                                 text="change password ",
                                 font=("system", 14),
                                 command=change_password,
                                 bg=BACKGROUND,
                                 fg=TITLE_COLOR,
                                 justify='center',
                                 compound='right',
                                 image=change_password_img,
                                 cursor=['hand2'],
                                 width=200,
                                 pady=8,
                                 borderwidth=0,
                                 activebackground=PRI_COL,
                                 activeforeground=TITLE_COLOR)
    change_password_btn.bind("<Enter>", lambda x: change_password_btn.config(bg=INPUT_ENTRY_COLOR))
    change_password_btn.bind("<Leave>", lambda x: change_password_btn.config(bg=BACKGROUND))

    bottom_buttons_frame.pack(pady=[40, 0])
    log_out_frame.pack(side='left', padx=[0, 20])
    log_out_btn.pack()
    change_password_frame.pack(side='right', padx=[20, 0])
    change_password_btn.pack()


# home bage part /////
def home_bage(*args):
    global hame_bage_frame
    game_bage_button.config(state=NORMAL, bg=BACKGROUND)
    setting_bage_button.config(state=NORMAL, bg=BACKGROUND)
    home_bage_button.config(state=DISABLED, bg=PRI_COL)

    try:
        game_bage_frame.destroy()
    except:
        pass
    try:
        settings_bage_frame.destroy()
    except:
        pass

    hame_bage_frame = Frame(window,
                            width=1,
                            height=70)
    hame_bage_frame.pack(pady=10)

    home_frame = Frame(hame_bage_frame,
                       width=370,
                       height=520,
                       bg=BACKGROUND)
    home_frame.pack()

    welcome_label = Label(home_frame,
                          font=("Fixedsys", 50),
                          bg=BACKGROUND,
                          fg=TITLE_COLOR,
                          text='Welcome  ',
                          cursor=['hand2'],
                          compound='right',
                          image=hello_img)
    welcome_label.pack(side='top')

    text = "Allow me to introduce myself as Haider Sabah. \n \n" \
           "On the memorable date of 7/1/2023, I embarked on a creative endeavor by" \
           "developing a user-friendly interface using the elegant Python programming language. \n \n " \
           "Upon launching the game, you will be gracefully welcomed with a prompt, inviting you " \
           "to enter your unique username and password, granting you exclusive access to the immersive world that awaits. \n \n" \
           "To ensure a personalized experience, you have the freedom to customize the game to your " \
           "heart's desire. The settings offer a myriad of options, including the ability to alter the " \
           "theme to match your mood and preferences. Moreover, you have the power to choose between engaging in a challenging " \
           "duel against the cunning computer or pitting your skills against your esteemed friends. \n \n" \
           "Immersing yourself in the game will reveal a meticulously designed landscape divided into " \
           "three captivating sections: the captivating game page, the versatile settings page, and the inviting " \
           "home page. Seamlessly navigating between these sections is effortless, presenting you with two intuitive methods.\n" \
           "You can either harness the power of the arrow buttons on your keyboard, gracefully gliding through the pages with " \
           "finesse (left arrow: <--, right arrow: -->). Alternatively, you can indulge in the visual delight of the navigation " \
           "bar located at the bottom of the window, beckoning you to explore each section at your leisure.\n \n" \
           "Delving deeper into the realm of settings, you will be enchanted by " \
           "the wealth of possibilities that lie before you. \n" \
           "Modify the game according to your whims and fancies, transcending mere " \
           "entertainment and transforming it into a personalized masterpiece.\n \n" \
           "In the game page, a delightful surprise awaits you. By simply clicking on the image to the left of the text, you have " \
           "the power to reset the counter at the top, resetting the stage for endless new beginnings. \n \n" \
           "For those seeking an added touch of excitement, activating the automatic play feature in the settings will ignite a " \
           "thrilling twist. With each new game, the system plays the role of a mysterious hand, randomly selecting a player " \
           "to make the all-important first move, injecting an element of unpredictability into your gaming experience. \n \n \n" \
           "With utmost sincerity, I wish you an extraordinary and exhilarating journey filled " \
           "with joyous moments and unforgettable \n \n " \
           "in the fild of the chareckter entry You must enter two characters, and each " \
           "character must be less than three characters, " \
           "and you must separate the two characters with a comma \",\", like X,O   " \
           "and you must not use space between them or at the end or at the beginning of the text .\n \n" \
           "memories. May your time in this enchanting realm be nothing short of sublime. \n \n \n "

    home_data_frame = Frame(home_frame,
                            bg=BACKGROUND)
    home_data_frame.pack(pady=30)

    scroll_bar = Scrollbar(home_data_frame,
                           orient=['vertical'],
                           cursor=['hand2'])
    scroll_bar.pack(side='right', fill=Y)

    home_information = Text(home_data_frame,
                            yscrollcommand=scroll_bar.set,
                            fg=PRI_COL,
                            font=("consolas", 16, FONT_STYEL),
                            bg=BACKGROUND,
                            cursor=['hand2'],
                            width=500,
                            borderwidth=0,
                            wrap=['word'])
    home_information.insert(1.0, text)
    home_information.configure(state='disable', foreground=PRI_COL)
    scroll_bar.config(command=home_information.yview)
    home_information.pack(expand=1, side='left', padx=40)

    window.bind("<Right>", game_bage)
    window.bind("<Left>", "")
    window.bind("<Return>", "")
    home_bage_button.bind("<Enter>", "")
    home_bage_button.bind("<Leave>", "")
    setting_bage_button.bind("<Enter>", lambda x: setting_bage_button.config(bg=INPUT_ENTRY_COLOR))
    setting_bage_button.bind("<Leave>", lambda x: setting_bage_button.config(bg=BACKGROUND))
    game_bage_button.bind("<Enter>", lambda x: game_bage_button.config(bg=INPUT_ENTRY_COLOR))
    game_bage_button.bind("<Leave>", lambda x: game_bage_button.config(bg=BACKGROUND))


# game bage part /////
def game_bage(*args):
    global counter_label, buttons, f_bord, player
    global game_counter, player_x_count, player_o_count
    global game_bage_frame
    try:
        hame_bage_frame.destroy()
    except:
        pass
    try:
        settings_bage_frame.destroy()
    except:
        pass
    player = PLAYER_CHAR  # Player 1 starts the game
    game_counter.set(f"Player {CHARECKTER.split(',')[0]} : {player_x_count.get()}\n"
                     f"Player {CHARECKTER.split(',')[1]} : {player_o_count.get()}")

    # Create the game counter labels
    game_bage_frame = Frame(window,
                            bg=BACKGROUND)
    game_bage_frame.pack(side='top')

    x_o_label = Label(game_bage_frame,
                      fg=TITLE_COLOR,
                      text="X _ O   Game",
                      bg=BACKGROUND,
                      font=("Fixedsys", 50),
                      cursor=['hand2'])
    x_o_label.pack(pady=10)

    point_frame = Frame(game_bage_frame,
                        bg=BACKGROUND)

    point_frame.pack(anchor=CENTER, pady=[20, 10])
    counter_label = Label(point_frame,
                          textvariable=game_counter,
                          fg=PRI_COL,
                          font=("Helvetica", 16, FONT_STYEL),
                          bg=BACKGROUND,
                          justify="left")
    counter_label.pack(side='left')

    counter_img_btn = Button(point_frame,
                             image=game_img,
                             command=clear_counter,
                             bg=BACKGROUND,
                             borderwidth=0,
                             activebackground=BACKGROUND,
                             cursor=['hand2'])

    counter_img_btn.pack(side='right', padx=[175, 0])

    f_bord = Frame(game_bage_frame, bg=BACKGROUND)
    f_bord.pack()
    # Create the game board buttons
    buttons = [[None, None, None] for _ in range(3)]
    ff = [[None, None, None] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            ff[i][j] = Frame(f_bord,
                             highlightbackground=PRI_COL,
                             highlightthickness=2,
                             borderwidth=0)
            ff[i][j].grid(row=i, column=j, padx=5, pady=5)

            buttons[i][j] = Button(
                ff[i][j],
                text=" ",
                font=("System", 43),
                width=3,
                bg=BACKGROUND,
                fg=PRI_COL,
                command=lambda row=i, col=j: button_click(row, col),
                cursor=['hand2'],
                borderwidth=0)
            buttons[i][j].pack()

    if AUTO_PLAY == "True":
        rand = random.choice(CHARECKTER.split(","))
        if rand != player:
            computer_turn()

    home_bage_button.config(state=NORMAL, bg=BACKGROUND)
    setting_bage_button.config(state=NORMAL, bg=BACKGROUND)
    game_bage_button.config(state=DISABLED, bg=PRI_COL)

    window.bind("<Return>", "")
    window.bind("<Right>", setting_bage)
    window.bind("<Left>", home_bage)
    game_bage_button.bind("<Enter>", "")
    game_bage_button.bind("<Leave>", "")
    home_bage_button.bind("<Enter>", lambda x: home_bage_button.config(bg=INPUT_ENTRY_COLOR))
    home_bage_button.bind("<Leave>", lambda x: home_bage_button.config(bg=BACKGROUND))
    setting_bage_button.bind("<Enter>", lambda x: setting_bage_button.config(bg=INPUT_ENTRY_COLOR))
    setting_bage_button.bind("<Leave>", lambda x: setting_bage_button.config(bg=BACKGROUND))


# made the navbar buttons ////
def nav_bar():
    global home_bage_button, game_bage_button, setting_bage_button
    global first_btn_frame, second_btn_frame, therd_btn_frame, navbar_button_frame

    navbar_button_frame = Frame(window,
                                width=600,
                                height=80,
                                bg=BACKGROUND)
    navbar_button_frame.pack(side='bottom', fill=X)

    first_btn_frame = Frame(navbar_button_frame,
                            bg=BACKGROUND,
                            highlightbackground=PRI_COL,
                            highlightthickness=2)

    home_bage_button = Button(first_btn_frame,
                              width=11,
                              cursor=['hand2'],
                              fg=PRI_COL,
                              foreground=PRI_COL,
                              font=("System", 20),
                              text="Home",
                              bg=BACKGROUND,
                              command=home_bage,
                              borderwidth=0,
                              activebackground=PRI_COL,
                              activeforeground=BACKGROUND)

    first_btn_frame.pack(side='left')
    home_bage_button.pack()

    second_btn_frame = Frame(navbar_button_frame,
                             bg=BACKGROUND,
                             highlightbackground=PRI_COL,
                             highlightthickness=2)

    game_bage_button = Button(second_btn_frame,
                              width=11,
                              cursor=['hand2'],
                              fg=PRI_COL,
                              foreground=PRI_COL,
                              font=("System", 20),
                              text="Game",
                              bg=BACKGROUND,
                              command=game_bage,
                              borderwidth=0,
                              activebackground=PRI_COL,
                              activeforeground=BACKGROUND)

    second_btn_frame.pack(side='left', padx=[5, 0])
    game_bage_button.pack()

    therd_btn_frame = Frame(navbar_button_frame,
                            bg=BACKGROUND,
                            highlightbackground=PRI_COL,
                            highlightthickness=2)

    setting_bage_button = Button(therd_btn_frame,
                                 width=11,
                                 cursor=['hand2'],
                                 fg=PRI_COL,
                                 font=("System", 20),
                                 text="Setting",
                                 bg=BACKGROUND,
                                 command=setting_bage,
                                 borderwidth=0,
                                 activebackground=PRI_COL,
                                 activeforeground=BACKGROUND)
    therd_btn_frame.pack(side='right')
    setting_bage_button.pack()


# log in bage part /////
def Login_bage():
    global password_input, user_input, log_in_frame

    # show and hide the password by click the img ///
    def show_password():
        if password_input['show'] == "*":
            password_input.config(show="")
            password_img.config(image=show_pass_img)
            return
        else:
            password_input.config(show="*")
            password_img.config(image=hide_pass_img)

    # chek information before lunch the game ///
    def chek_before_login(*args):
        if password_input.get() == PASSWORD and user_input.get() == USER_NAME:
            log_in_frame.destroy()
            nav_bar()
            home_bage()
        else:
            if PASSWORD == "2023/8/8" and USER_NAME == "Haider" and COUNT == 1:
                messagebox.showwarning("hi ...", "this message will show jast this time \n"
                                                 "you are use this window for the first time ...\n"
                                                 "the defult user name and password are : \n"
                                                 f"user : {USER_NAME}  ,  password : {PASSWORD}")
                re_write_file(6, 1)
                password_input.delete(0, END)
                user_input.delete(0, END)
                return
            password_input.delete(0, END)
            user_input.delete(0, END)
            return messagebox.showerror("login invalid", "rong password or user name !!")

    try:
        settings_bage_frame.destroy()
    except:
        pass
    try:
        navbar_button_frame.destroy()
    except:
        pass

    log_in_frame = Frame(window,
                         width=456,
                         bg=BACKGROUND)

    detalis_frame = Frame(log_in_frame,
                          height=50,
                          bg=BACKGROUND)

    top_detalis_frame = Frame(log_in_frame,
                              bg=BACKGROUND)

    login_text_label = Label(top_detalis_frame,
                             height=134,
                             text="Log In ",
                             fg=TITLE_COLOR,
                             bg=BACKGROUND,
                             font=("Fixedsys", 70),
                             compound="right",
                             image=welcome_img,
                             cursor=['hand2'])

    first_line = Frame(top_detalis_frame,
                       bg=PRI_COL,
                       width=465,
                       height=5)

    info_text_label = Label(top_detalis_frame,
                            font=("consloas", 12, FONT_STYEL),
                            fg=PRI_COL,
                            justify="left",
                            bg=BACKGROUND,
                            text="plese inter your user name and password \nto log in the parogram ...")

    # log in inputs /////
    input_farme = Frame(top_detalis_frame,
                        bg=BACKGROUND,
                        width=465)
    user_input_frame = Frame(input_farme,
                             width=465,
                             height=97,
                             bg=BACKGROUND)

    user_label = Label(user_input_frame,
                       justify="left",
                       fg=TITLE_COLOR,
                       font=("consolas", 22),
                       text="User Name :",
                       bg=BACKGROUND)

    user_input = Entry(user_input_frame,
                       font=("consloas", 18),
                       width=25,
                       highlightbackground=PRI_COL,
                       highlightthickness=4,
                       highlightcolor=INPUT_ENTRY_COLOR,
                       bg=BACKGROUND,
                       fg=PRI_COL,
                       justify='left')

    password_frame = Frame(input_farme,
                           width=465,
                           height=97,
                           bg=BACKGROUND)

    password_label = Label(password_frame,
                           justify="left",
                           fg=TITLE_COLOR,
                           font=("consolas", 22),
                           text="Password  :",
                           bg=BACKGROUND)

    password_entry_frame = Frame(password_frame,
                                 bg=BACKGROUND)

    password_input = Entry(password_entry_frame,
                           font=("consloas", 18),
                           width=25,
                           highlightbackground=PRI_COL,
                           highlightthickness=4,
                           highlightcolor=INPUT_ENTRY_COLOR,
                           show="*",
                           bg=BACKGROUND,
                           fg=PRI_COL,
                           justify='left')

    password_img = Button(password_entry_frame,
                          image=hide_pass_img,
                          command=show_password,
                          bg=BACKGROUND,
                          width=82,
                          height=35,
                          borderwidth=0,
                          activebackground=BACKGROUND,
                          cursor=['hand2'])

    button_login_close_frame = Frame(log_in_frame,
                                     bg=BACKGROUND,
                                     pady=20,
                                     width=465)

    firstbtn = Frame(button_login_close_frame,
                     bg=PRI_COL,
                     highlightbackground=PRI_COL,
                     highlightthickness=2)

    login_btn = Button(firstbtn,
                       text="Log in",
                       fg=PRI_COL,
                       font=("System", 23),
                       bg=BACKGROUND,
                       command=chek_before_login,
                       compound="left",
                       image=log_in_img,
                       padx=20,
                       cursor=['hand2'],
                       justify='left',
                       width=150,
                       borderwidth=0,
                       activebackground=PRI_COL,
                       activeforeground=BACKGROUND)
    login_btn.bind("<Enter>", lambda x: login_btn.config(bg=INPUT_ENTRY_COLOR))
    login_btn.bind("<Leave>", lambda x: login_btn.config(bg=BACKGROUND))

    secondbtn = Frame(button_login_close_frame,
                      bg=PRI_COL,
                      highlightbackground=PRI_COL,
                      highlightthickness=2)

    Close_btn = Button(secondbtn,
                       fg=PRI_COL,
                       font=("System", 23),
                       text="Close",
                       bg=BACKGROUND,
                       command=window.destroy,
                       compound="left",
                       image=close_img,
                       padx=20,
                       cursor=['hand2'],
                       justify='left',
                       width=150,
                       borderwidth=0,
                       activebackground=PRI_COL,
                       activeforeground=BACKGROUND)
    Close_btn.bind("<Enter>", lambda x: Close_btn.config(bg=INPUT_ENTRY_COLOR))
    Close_btn.bind("<Leave>", lambda x: Close_btn.config(bg=BACKGROUND))

    second_line = Frame(input_farme,
                        bg=PRI_COL,
                        width=465,
                        height=5)

    # pack the main wiget ////
    log_in_frame.pack(anchor=CENTER)
    detalis_frame.pack()

    top_detalis_frame.pack()
    login_text_label.pack()
    first_line.pack(anchor=W)
    info_text_label.pack(anchor=W, pady=20)

    input_farme.pack(anchor=W)
    user_input_frame.pack(anchor=W)
    user_label.pack(anchor=W)
    user_input.pack(padx=[30, 0])

    password_frame.pack(pady=20, anchor=W)
    password_label.pack(anchor=W)
    password_entry_frame.pack(padx=[30, 0])
    password_input.pack(side='left')
    password_img.pack(side='right')
    second_line.pack(pady=20, anchor=W)

    button_login_close_frame.pack(pady=35)
    firstbtn.pack(side="right", padx=[20, 0])
    login_btn.pack()
    secondbtn.pack(side="left", padx=[0, 20])
    Close_btn.pack()
    window.bind("<Return>", chek_before_login)


# Create the main window /////
window = Tk()
window.title("X_O ...Game")
icon = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\games.png")
window.iconphoto(True, icon)
window.config(bg=BACKGROUND)
window.resizable(False, False)
window.geometry("600x700")

# counters points of the game /////
player_x_count = IntVar()
player_o_count = IntVar()
player_x_count.set(0)
player_o_count.set(0)
game_counter = StringVar()

# image files /////
welcome_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\welcome-back.png")
log_in_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\log.png")
close_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\close.png")
setting_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\settings.png")
log_out_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\logout.png")
hello_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\hello.png")
game_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\counter.png")
hide_pass_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\hide_password.png")
show_pass_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\show_password.png")
change_password_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\password.png")
rand_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\random.png")
security_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\security.png")
back_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\back.png")
saved_img = PhotoImage(file="C:\\Users\\asus\\Desktop\\game\\img\\bookmark.png")

# start the main window //////
Login_bage()
window.mainloop()
