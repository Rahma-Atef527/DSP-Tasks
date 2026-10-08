#gui code
import tkinter as tk
from tkinter import ttk, messagebox

from Task1.task1 import (
    read_signal,
    add_signal,
    mul_signal,
    plot_continuous,
    plot_discrete,
    plot_two_signals,
    plot_two_discrete_signals
)


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"

TEXT_COLOR = "#F8FAFC"
SECONDARY_TEXT = "#94A3B8"

ACCENT_COLOR = "#38BDF8"
ACCENT_HOVER = "#0EA5E9"

SUCCESS_COLOR = "#22C55E"
SUCCESS_HOVER = "#16A34A"

PURPLE_COLOR = "#A78BFA"
PURPLE_HOVER = "#8B5CF6"

ENTRY_BG = "#0F172A"
BORDER_COLOR = "#334155"


# =========================================================
# SIGNAL FILES
# =========================================================

SIGNAL_FILES = {
    "Signal 1": "Task1/Signal1.txt",
    "Signal 2": "Task1/Signal2.txt",
    "Signal 3": "Task1/Signal3.txt"
}

def get_signal(signal_name):
    return read_signal(SIGNAL_FILES[signal_name])


# =========================================================
# DISPLAY ONE SIGNAL
# =========================================================

def display_signal():

    selected_signal = signal_combo.get()
    display_type = display_combo.get()

    signal = get_signal(selected_signal)

    indices = signal[2]
    samples = signal[3]

    if display_type == "Continuous":

        plot_continuous(
            indices,
            samples,
            selected_signal + " - Continuous"
        )

    else:

        plot_discrete(
            indices,
            samples,
            selected_signal + " - Discrete"
        )


# =========================================================
# DISPLAY TWO SIGNALS
# =========================================================

def display_two_signals():

    selected_signals = []

    if signal1_display_var.get() == 1:
        selected_signals.append("Signal 1")

    if signal2_display_var.get() == 1:
        selected_signals.append("Signal 2")

    if signal3_display_var.get() == 1:
        selected_signals.append("Signal 3")

    if len(selected_signals) != 2:

        messagebox.showwarning(
            "Select Two Signals",
            "Please select exactly two signals."
        )

        return

    signal_a = get_signal(selected_signals[0])
    signal_b = get_signal(selected_signals[1])

    indices1 = signal_a[2]
    samples1 = signal_a[3]

    indices2 = signal_b[2]
    samples2 = signal_b[3]

    if display_combo.get() == "Continuous":

        plot_two_signals(
            indices1,
            samples1,
            indices2,
            samples2,
            selected_signals[0] + " and " + selected_signals[1]
        )

    else:

        plot_two_discrete_signals(
            indices1,
            samples1,
            indices2,
            samples2,
            selected_signals[0] + " and " + selected_signals[1]
        )


# =========================================================
# ADD SIGNALS
# =========================================================

def add_selected_signals():

    signals = []
    indices = None

    if signal1_var.get() == 1:

        signal = get_signal("Signal 1")

        indices = signal[2]
        signals.append(signal[3])

    if signal2_var.get() == 1:

        signal = get_signal("Signal 2")

        indices = signal[2]
        signals.append(signal[3])

    if signal3_var.get() == 1:

        signal = get_signal("Signal 3")

        indices = signal[2]
        signals.append(signal[3])

    if len(signals) < 2:

        messagebox.showwarning(
            "Add Signals",
            "Please select at least two signals."
        )

        return

    try:

        result = add_signal(signals)

    except ValueError as error:

        messagebox.showerror(
            "Addition Error",
            str(error)
        )

        return

    if display_combo.get() == "Continuous":

        plot_continuous(
            indices,
            result,
            "Addition Result"
        )

    else:

        plot_discrete(
            indices,
            result,
            "Addition Result"
        )


# =========================================================
# MULTIPLY SIGNAL
# =========================================================

def multiply_selected_signal():

    selected_signal = signal_combo.get()

    if constant_entry.get().strip() == "":

        messagebox.showwarning(
            "Missing Constant",
            "Please enter a constant."
        )

        return

    try:

        constant = float(constant_entry.get())

    except ValueError:

        messagebox.showerror(
            "Invalid Constant",
            "Please enter a valid number."
        )

        return

    signal = get_signal(selected_signal)

    indices = signal[2]
    samples = signal[3]

    result = mul_signal(
        samples,
        constant
    )

    if display_combo.get() == "Continuous":

        plot_continuous(
            indices,
            result,
            selected_signal + " x " + str(constant)
        )

    else:

        plot_discrete(
            indices,
            result,
            selected_signal + " x " + str(constant)
        )


# =========================================================
# BUTTON HOVER
# =========================================================

def button_hover(button, normal_color, hover_color):

    button.bind(
        "<Enter>",
        lambda event: button.config(
            bg=hover_color
        )
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(
            bg=normal_color
        )
    )


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title("DSP Signal Processing")
window.geometry("850x850")

window.configure(
    bg=BG_COLOR
)

window.resizable(
    False,
    False
)


# =========================================================
# STYLE
# =========================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground=ENTRY_BG,
    background=ENTRY_BG,
    foreground=TEXT_COLOR,
    bordercolor=BORDER_COLOR,
    arrowcolor=ACCENT_COLOR,
    padding=8
)

style.map(
    "TCombobox",
    fieldbackground=[
        ("readonly", ENTRY_BG)
    ],
    foreground=[
        ("readonly", TEXT_COLOR)
    ]
)


# =========================================================
# HEADER
# =========================================================

header_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

header_frame.pack(
    pady=(25, 10)
)


title = tk.Label(
    header_frame,
    text="DSP SIGNAL PROCESSING",
    font=("Arial", 26, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title.pack()


subtitle = tk.Label(
    header_frame,
    text="Digital Signal Processing Tool",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

subtitle.pack(
    pady=(5, 0)
)


# =========================================================
# DISPLAY CARD
# =========================================================

display_frame = tk.LabelFrame(
    window,
    text="  SIGNAL DISPLAY  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

display_frame.pack(
    fill="x",
    padx=45,
    pady=8
)


signal_label = tk.Label(
    display_frame,
    text="Signal",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

signal_label.grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=6
)


signal_combo = ttk.Combobox(
    display_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=22
)

signal_combo.grid(
    row=0,
    column=1,
    padx=15,
    pady=6
)

signal_combo.set("Signal 1")


display_label = tk.Label(
    display_frame,
    text="Display Type",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

display_label.grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=6
)


display_combo = ttk.Combobox(
    display_frame,
    values=[
        "Continuous",
        "Discrete"
    ],
    state="readonly",
    width=22
)

display_combo.grid(
    row=1,
    column=1,
    padx=15,
    pady=6
)

display_combo.set("Continuous")


display_button = tk.Button(
    display_frame,
    text="Display Signal",
    font=("Arial", 11, "bold"),
    bg=ACCENT_COLOR,
    fg="#0F172A",
    activebackground=ACCENT_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    bd=0,
    width=22,
    height=2,
    cursor="hand2",
    command=display_signal
)

display_button.grid(
    row=0,
    column=2,
    rowspan=2,
    padx=30
)

button_hover(
    display_button,
    ACCENT_COLOR,
    ACCENT_HOVER
)


# =========================================================
# TWO SIGNALS CARD
# =========================================================

two_signals_frame = tk.LabelFrame(
    window,
    text="  DISPLAY TWO SIGNALS  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=12
)

two_signals_frame.pack(
    fill="x",
    padx=45,
    pady=8
)


signal1_display_var = tk.IntVar()
signal2_display_var = tk.IntVar()
signal3_display_var = tk.IntVar()


check_display1 = tk.Checkbutton(
    two_signals_frame,
    text="Signal 1",
    variable=signal1_display_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
)

check_display1.grid(
    row=0,
    column=0,
    padx=20,
    pady=5
)


check_display2 = tk.Checkbutton(
    two_signals_frame,
    text="Signal 2",
    variable=signal2_display_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
)

check_display2.grid(
    row=0,
    column=1,
    padx=20,
    pady=5
)


check_display3 = tk.Checkbutton(
    two_signals_frame,
    text="Signal 3",
    variable=signal3_display_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
)

check_display3.grid(
    row=0,
    column=2,
    padx=20,
    pady=5
)


two_signals_button = tk.Button(
    two_signals_frame,
    text="Display Two Signals",
    font=("Arial", 11, "bold"),
    bg=ACCENT_COLOR,
    fg="#0F172A",
    activebackground=ACCENT_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    bd=0,
    width=25,
    height=2,
    cursor="hand2",
    command=display_two_signals
)

two_signals_button.grid(
    row=1,
    column=0,
    columnspan=3,
    pady=(8, 2)
)

button_hover(
    two_signals_button,
    ACCENT_COLOR,
    ACCENT_HOVER
)


# =========================================================
# ADD SIGNALS CARD
# =========================================================

add_frame = tk.LabelFrame(
    window,
    text="  ADD SIGNALS  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=SUCCESS_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

add_frame.pack(
    fill="x",
    padx=45,
    pady=8
)


add_label = tk.Label(
    add_frame,
    text="Select Signals",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

add_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=6
)


signal1_var = tk.IntVar()
signal2_var = tk.IntVar()
signal3_var = tk.IntVar()


check1 = tk.Checkbutton(
    add_frame,
    text="Signal 1",
    variable=signal1_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
)

check1.grid(
    row=0,
    column=1,
    padx=15
)


check2 = tk.Checkbutton(
    add_frame,
    text="Signal 2",
    variable=signal2_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
)

check2.grid(
    row=0,
    column=2,
    padx=15
)


check3 = tk.Checkbutton(
    add_frame,
    text="Signal 3",
    variable=signal3_var,
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
)

check3.grid(
    row=0,
    column=3,
    padx=15
)


add_button = tk.Button(
    add_frame,
    text="Add Selected Signals",
    font=("Arial", 11, "bold"),
    bg=SUCCESS_COLOR,
    fg="#FFFFFF",
    activebackground=SUCCESS_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    bd=0,
    width=25,
    height=2,
    cursor="hand2",
    command=add_selected_signals
)

add_button.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=(12, 2)
)

button_hover(
    add_button,
    SUCCESS_COLOR,
    SUCCESS_HOVER
)


# =========================================================
# MULTIPLY CARD
# =========================================================

multiply_frame = tk.LabelFrame(
    window,
    text="  MULTIPLY BY CONSTANT  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=PURPLE_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

multiply_frame.pack(
    fill="x",
    padx=45,
    pady=8
)


constant_label = tk.Label(
    multiply_frame,
    text="Constant",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

constant_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=6
)


constant_entry = tk.Entry(
    multiply_frame,
    width=24,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0
)

constant_entry.grid(
    row=0,
    column=1,
    padx=15,
    pady=6,
    ipady=8
)


multiply_button = tk.Button(
    multiply_frame,
    text="Multiply Signal",
    font=("Arial", 11, "bold"),
    bg=PURPLE_COLOR,
    fg="#FFFFFF",
    activebackground=PURPLE_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    bd=0,
    width=25,
    height=2,
    cursor="hand2",
    command=multiply_selected_signal
)

multiply_button.grid(
    row=0,
    column=2,
    padx=25
)

button_hover(
    multiply_button,
    PURPLE_COLOR,
    PURPLE_HOVER
)


# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    window,
    text="Digital Signal Processing • Signal Analysis & Operations",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

footer.pack(
    pady=12
)


# =========================================================
# RUN APPLICATION
# =========================================================

window.mainloop()