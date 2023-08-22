import tkinter
import math
import pygame

# vals and consts
red = '#BD1616'
fire_orange = '#FF8E00'
tomato_red = "#D7402B"
almost_black = "#1C080A"
pomo_timer = 25
pomo_pause = 5
pomo_break = 20
cycle = 0
starts_timer = "NONE"
streaks = "NONE"


def reset_timer():
    pomodoro.after_cancel(starts_timer)
    global cycle
    cycle = 0
    message = "Boost your productivity!"
    canvas.itemconfig(disp_heading,
                      text=message)
    canvas.itemconfig(timer_text, text="00:00")
    global streaks
    canvas.itemconfig(streaks, text="")


def start_timer():
    pomodoro.after_cancel(starts_timer)
    global cycle
    cycle += 1
    productive_time = pomo_timer * 60
    pomo_pause_minutes = pomo_pause * 60
    pomo_break_minutes = pomo_break * 60

    if cycle % 8 == 0:  # long break after 4th pomodoro
        pygame.mixer.music.load("src/break.wav")
        pygame.mixer.music.play(loops=0)
        break_message = "Awesome! You've earned a longer break!"
        canvas.itemconfig(disp_heading, text=break_message)
        count_down_clock(pomo_break_minutes)
    elif cycle % 2 == 0:  # short pause after every pomodoro
        pygame.mixer.music.load("src/pause.wav")
        pygame.mixer.music.play(loops=0)
        pause_message = "Nice! Now take a short pause.\n" \
                        "Stretch, walk around, drink some water."
        canvas.itemconfig(disp_heading, text=pause_message)
        count_down_clock(pomo_pause_minutes)
    else:  # productivity time
        pygame.mixer.music.load("src/focus.wav")
        pygame.mixer.music.play(loops=0)
        productive_message = "Try to focus at your task"
        canvas.itemconfig(disp_heading, text=productive_message)
        count_down_clock(productive_time)


def count_down_clock(count):
    mins_count = math.floor(count / 60)
    secs_count = count % 60
    # add zeroes in front of seconds when there are less than 10 of them
    if secs_count < 10:
        secs_count = f"0{secs_count}"

    # timer text
    canvas.itemconfig(timer_text, text=f"{mins_count}:{secs_count}")
    if count > 0:
        global starts_timer
        starts_timer = pomodoro.after(1000, count_down_clock, count - 1)
    else:
        start_timer()
        streak = ""
        streak_counter = math.floor(cycle / 2)
        for i in range(streak_counter):
            streak += "🍅"
        canvas.itemconfig(streak_text, text="Your current streak count: ")
        canvas.itemconfig(streaks, text=streak)


# Main script
pomodoro = tkinter.Tk()
pomodoro.title("Productivity Booster")
pomodoro.config(padx=25, pady=25, bg=red)
pomodoro.resizable(False, False)

# initializing the pygame mixer for sound output
pygame.mixer.init()

canvas = tkinter.Canvas(width=500, height=560,
                        bg=red,
                        highlightthickness=False)

# background image
tomato_image = tkinter.PhotoImage(file="src/tomato1.png")
canvas.create_image(250, 280, image=tomato_image)

# heading
disp_heading = canvas.create_text(245, 30, justify="center",
                                  text="Improve your productivity",
                                  fill=almost_black,
                                  font=('calibri', 20, 'bold'))
# text for timer
timer_text = canvas.create_text(245, 290, text="00:00", fill='white',
                                justify="center",
                                font=('calibri', 95, 'bold'))

# buttons to start and end timer
start_btn = tkinter.Button(canvas, text="START", width=8, height=1, bd="3",
                           font=("calibri", 15, "bold"), justify="center",
                           background=tomato_red,
                           command=start_timer)
start_btn.place(x=120, y=375)

reset_btn = tkinter.Button(canvas, text="RESET", width=8, height=1, bd='3',
                           font=("calibri", 15, "bold"), justify="center",
                           background=tomato_red,
                           command=reset_timer)
reset_btn.place(x=280, y=375)

# streak text
streak_text = canvas.create_text(160, 540, text="Your current streak count: ",
                                 fill=almost_black,
                                 font=("calibri", 20, "bold"))
streaks = canvas.create_text(270, 540, text="",
                             fill=fire_orange,
                             font=("calibri", 25, "bold"))

canvas.pack()
pomodoro.mainloop()
