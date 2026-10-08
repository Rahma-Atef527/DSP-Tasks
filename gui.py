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

from Task2.task2 import (
    sub_signal,
    square_signal,
    normalize_signal,
    accumulate_signal,
    quantize_signal,
    read_signal as read_quantization_signal
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

ORANGE_COLOR = "#FB923C"
ORANGE_HOVER = "#F97316"

TEAL_COLOR = "#2DD4BF"
TEAL_HOVER = "#14B8A6"

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

    return read_signal(
        SIGNAL_FILES[signal_name]
    )


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def button_hover(
    button,
    normal_color,
    hover_color
):

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


def create_button(
    parent,
    text,
    command,
    color,
    hover_color,
    width=20
):

    button = tk.Button(
        parent,
        text=text,
        font=("Arial", 10, "bold"),
        bg=color,
        fg="#FFFFFF",
        activebackground=hover_color,
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        width=width,
        height=2,
        cursor="hand2",
        command=command
    )

    button_hover(
        button,
        color,
        hover_color
    )

    return button


# =========================================================
# SCROLLABLE PAGE
# =========================================================

def create_scrollable_page(parent):

    container = tk.Frame(
        parent,
        bg=BG_COLOR
    )

    canvas = tk.Canvas(
        container,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview
    )

    content = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    window_id = canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Update scroll region
    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    content.bind(
        "<Configure>",
        update_scroll_region
    )

    # Make content width equal to canvas width
    def resize_content(event):

        canvas.itemconfig(
            window_id,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        resize_content
    )

    # Mouse wheel
    def on_enter(event):

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(
                int(-e.delta / 120),
                "units"
            )
        )

    def on_leave(event):

        canvas.unbind_all(
            "<MouseWheel>"
        )

    canvas.bind(
        "<Enter>",
        on_enter
    )

    canvas.bind(
        "<Leave>",
        on_leave
    )

    return container, content


# =========================================================
# TASK 1 FUNCTIONS
# =========================================================

def display_signal():

    selected_signal = task1_signal_combo.get()
    display_type = task1_display_combo.get()

    signal = get_signal(
        selected_signal
    )

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


def display_two_signals():

    selected_signals = []

    if signal1_display_var.get() == 1:

        selected_signals.append(
            "Signal 1"
        )

    if signal2_display_var.get() == 1:

        selected_signals.append(
            "Signal 2"
        )

    if signal3_display_var.get() == 1:

        selected_signals.append(
            "Signal 3"
        )

    if len(selected_signals) != 2:

        messagebox.showwarning(
            "Select Two Signals",
            "Please select exactly two signals."
        )

        return

    signal_a = get_signal(
        selected_signals[0]
    )

    signal_b = get_signal(
        selected_signals[1]
    )

    indices1 = signal_a[2]
    samples1 = signal_a[3]

    indices2 = signal_b[2]
    samples2 = signal_b[3]

    if task1_display_combo.get() == "Continuous":

        plot_two_signals(
            indices1,
            samples1,
            indices2,
            samples2,
            selected_signals[0]
            + " and "
            + selected_signals[1]
        )

    else:

        plot_two_discrete_signals(
            indices1,
            samples1,
            indices2,
            samples2,
            selected_signals[0]
            + " and "
            + selected_signals[1]
        )


def add_selected_signals():

    signals = []
    indices = None

    if signal1_var.get() == 1:

        signal = get_signal(
            "Signal 1"
        )

        indices = signal[2]

        signals.append(
            signal[3]
        )

    if signal2_var.get() == 1:

        signal = get_signal(
            "Signal 2"
        )

        indices = signal[2]

        signals.append(
            signal[3]
        )

    if signal3_var.get() == 1:

        signal = get_signal(
            "Signal 3"
        )

        indices = signal[2]

        signals.append(
            signal[3]
        )

    if len(signals) < 2:

        messagebox.showwarning(
            "Add Signals",
            "Please select at least two signals."
        )

        return

    try:

        result = add_signal(
            signals
        )

    except ValueError as error:

        messagebox.showerror(
            "Addition Error",
            str(error)
        )

        return

    if task1_display_combo.get() == "Continuous":

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


def multiply_selected_signal():

    selected_signal = task1_signal_combo.get()

    if constant_entry.get().strip() == "":

        messagebox.showwarning(
            "Missing Constant",
            "Please enter a constant."
        )

        return

    try:

        constant = float(
            constant_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Constant",
            "Please enter a valid number."
        )

        return

    signal = get_signal(
        selected_signal
    )

    indices = signal[2]
    samples = signal[3]

    result = mul_signal(
        samples,
        constant
    )

    if task1_display_combo.get() == "Continuous":

        plot_continuous(
            indices,
            result,
            selected_signal
            + " x "
            + str(constant)
        )

    else:

        plot_discrete(
            indices,
            result,
            selected_signal
            + " x "
            + str(constant)
        )


# =========================================================
# TASK 2 FUNCTIONS
# =========================================================

def subtract_selected_signals():

    selected_signal1 = subtraction_signal1_combo.get()
    selected_signal2 = subtraction_signal2_combo.get()

    if selected_signal1 == selected_signal2:

        messagebox.showwarning(
            "Subtraction",
            "Please select two different signals."
        )

        return

    signal1 = get_signal(
        selected_signal1
    )

    signal2 = get_signal(
        selected_signal2
    )

    indices1 = signal1[2]
    samples1 = signal1[3]

    indices2 = signal2[2]
    samples2 = signal2[3]

    if len(indices1) != len(indices2):

        messagebox.showerror(
            "Subtraction Error",
            "Signals must have the same number of samples."
        )

        return

    try:

        result = sub_signal(
            samples1,
            samples2
        )

    except ValueError as error:

        messagebox.showerror(
            "Subtraction Error",
            str(error)
        )

        return

    if task2_display_combo.get() == "Continuous":

        plot_continuous(
            indices1,
            result,
            selected_signal1
            + " - "
            + selected_signal2
        )

    else:

        plot_discrete(
            indices1,
            result,
            selected_signal1
            + " - "
            + selected_signal2
        )


def square_selected_signal():

    selected_signal = square_signal_combo.get()

    signal = get_signal(
        selected_signal
    )

    indices = signal[2]
    samples = signal[3]

    result = square_signal(
        samples
    )

    if task2_display_combo.get() == "Continuous":

        plot_continuous(
            indices,
            result,
            selected_signal + " - Squared"
        )

    else:

        plot_discrete(
            indices,
            result,
            selected_signal + " - Squared"
        )


def normalize_selected_signal():

    selected_signal = normalize_signal_combo.get()

    choice = normalization_choice.get()

    if choice == 0:

        messagebox.showwarning(
            "Normalization",
            "Please select a normalization range."
        )

        return

    signal = get_signal(
        selected_signal
    )

    indices = signal[2]
    samples = signal[3]

    try:

        result = normalize_signal(
            samples,
            choice
        )

    except ValueError as error:

        messagebox.showerror(
            "Normalization Error",
            str(error)
        )

        return

    if choice == 1:

        title = (
            selected_signal
            + " - Normalized (-1 to 1)"
        )

    else:

        title = (
            selected_signal
            + " - Normalized (0 to 1)"
        )

    if task2_display_combo.get() == "Continuous":

        plot_continuous(
            indices,
            result,
            title
        )

    else:

        plot_discrete(
            indices,
            result,
            title
        )


def accumulate_selected_signal():

    selected_signal = accumulate_signal_combo.get()

    signal = get_signal(
        selected_signal
    )

    indices = signal[2]
    samples = signal[3]

    result = accumulate_signal(
        samples
    )

    if task2_display_combo.get() == "Continuous":

        plot_continuous(
            indices,
            result,
            selected_signal
            + " - Accumulation"
        )

    else:

        plot_discrete(
            indices,
            result,
            selected_signal
            + " - Accumulation"
        )


# =========================================================
# TASK 2 - QUANTIZATION
# =========================================================

def quantize_selected_signal():

    selected_file = quantization_file_combo.get()

    if selected_file == "":

        messagebox.showwarning(
            "Quantization",
            "Please select an input file."
        )

        return

    if selected_file == "Quan1_input":

        bits = 3
        levels = None

    else:

        bits = None
        levels = 4

    file_path = (
        "Task2/"
        + selected_file
    )

    try:

        samples = read_quantization_signal(
            file_path
        )

        (
            interval_indices,
            encoded_values,
            quantized_values,
            sampled_error
        ) = quantize_signal(
            samples,
            bits=bits,
            levels=levels
        )

    except Exception as error:

        messagebox.showerror(
            "Quantization Error",
            str(error)
        )

        return

    # Clear old table
    for item in quantization_tree.get_children():

        quantization_tree.delete(
            item
        )

    # Add new results
    for i in range(len(samples)):

        quantization_tree.insert(
            "",
            "end",
            values=(
                i,
                f"{samples[i]:.3f}",
                interval_indices[i],
                encoded_values[i],
                f"{quantized_values[i]:.3f}",
                f"{sampled_error[i]:.3f}"
            )
        )

    if selected_file == "Quan1_input":

        quantization_info.config(
            text="Quan1_input  •  3 Bits  •  8 Levels"
        )

    else:

        quantization_info.config(
            text="Quan2_input  •  4 Levels  •  2 Bits"
        )


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title(
    "DSP Signal Processing"
)

window.geometry(
    "950x850"
)

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

style.theme_use(
    "clam"
)

style.configure(
    "TNotebook",
    background=BG_COLOR,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background=CARD_COLOR,
    foreground=SECONDARY_TEXT,
    padding=(35, 12),
    font=("Arial", 11, "bold")
)

style.map(
    "TNotebook.Tab",
    background=[
        ("selected", ACCENT_COLOR)
    ],
    foreground=[
        ("selected", "#0F172A")
    ]
)

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
# TREEVIEW STYLE
# =========================================================

style.configure(
    "Treeview",
    background=ENTRY_BG,
    foreground=TEXT_COLOR,
    fieldbackground=ENTRY_BG,
    rowheight=28,
    borderwidth=0,
    font=("Arial", 9)
)

style.configure(
    "Treeview.Heading",
    background=CARD_COLOR,
    foreground=ACCENT_COLOR,
    font=("Arial", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[
        ("selected", ACCENT_COLOR)
    ],
    foreground=[
        ("selected", "#0F172A")
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
    pady=(15, 5)
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
# NOTEBOOK
# =========================================================

notebook = ttk.Notebook(
    window
)

notebook.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=10
)


# =========================================================
# TASK 1 PAGE
# =========================================================

task1_container = tk.Frame(
    notebook,
    bg=BG_COLOR
)

notebook.add(
    task1_container,
    text="  TASK 1  "
)

task1_page, task1_content = create_scrollable_page(
    task1_container
)

task1_page.pack(
    fill="both",
    expand=True
)


# =========================================================
# TASK 2 PAGE
# =========================================================

task2_container = tk.Frame(
    notebook,
    bg=BG_COLOR
)

notebook.add(
    task2_container,
    text="  TASK 2  "
)

task2_page, task2_content = create_scrollable_page(
    task2_container
)

task2_page.pack(
    fill="both",
    expand=True
)


# =========================================================
# TASK 1 - DISPLAY CARD
# =========================================================

display_frame = tk.LabelFrame(
    task1_content,
    text="  SIGNAL DISPLAY  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=20
)

display_frame.pack(
    fill="x",
    padx=20,
    pady=10
)


tk.Label(
    display_frame,
    text="Signal",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)


task1_signal_combo = ttk.Combobox(
    display_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=20
)

task1_signal_combo.grid(
    row=0,
    column=1,
    padx=15,
    pady=8
)

task1_signal_combo.set(
    "Signal 1"
)


tk.Label(
    display_frame,
    text="Display Type",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)


task1_display_combo = ttk.Combobox(
    display_frame,
    values=[
        "Continuous",
        "Discrete"
    ],
    state="readonly",
    width=20
)

task1_display_combo.grid(
    row=1,
    column=1,
    padx=15,
    pady=8
)

task1_display_combo.set(
    "Continuous"
)


display_button = create_button(
    display_frame,
    "Display Signal",
    display_signal,
    ACCENT_COLOR,
    ACCENT_HOVER,
    20
)

display_button.grid(
    row=0,
    column=2,
    rowspan=2,
    padx=30
)


# =========================================================
# TASK 1 - TWO SIGNALS
# =========================================================

two_signals_frame = tk.LabelFrame(
    task1_content,
    text="  DISPLAY TWO SIGNALS  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

two_signals_frame.pack(
    fill="x",
    padx=20,
    pady=10
)


signal1_display_var = tk.IntVar()
signal2_display_var = tk.IntVar()
signal3_display_var = tk.IntVar()


for index, text_value, variable in [
    (0, "Signal 1", signal1_display_var),
    (1, "Signal 2", signal2_display_var),
    (2, "Signal 3", signal3_display_var)
]:

    tk.Checkbutton(
        two_signals_frame,
        text=text_value,
        variable=variable,
        font=("Arial", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        selectcolor=ENTRY_BG,
        activebackground=CARD_COLOR,
        activeforeground=TEXT_COLOR
    ).grid(
        row=0,
        column=index,
        padx=35,
        pady=5
    )


two_signals_button = create_button(
    two_signals_frame,
    "Display Two Signals",
    display_two_signals,
    ACCENT_COLOR,
    ACCENT_HOVER,
    25
)

two_signals_button.grid(
    row=1,
    column=0,
    columnspan=3,
    pady=10
)


# =========================================================
# TASK 1 - ADD
# =========================================================

add_frame = tk.LabelFrame(
    task1_content,
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
    padx=20,
    pady=10
)


signal1_var = tk.IntVar()
signal2_var = tk.IntVar()
signal3_var = tk.IntVar()


tk.Label(
    add_frame,
    text="Select Signals",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=0,
    padx=10
)


for index, text_value, variable in [
    (1, "Signal 1", signal1_var),
    (2, "Signal 2", signal2_var),
    (3, "Signal 3", signal3_var)
]:

    tk.Checkbutton(
        add_frame,
        text=text_value,
        variable=variable,
        font=("Arial", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        selectcolor=ENTRY_BG,
        activebackground=CARD_COLOR,
        activeforeground=TEXT_COLOR
    ).grid(
        row=0,
        column=index,
        padx=15
    )


add_button = create_button(
    add_frame,
    "Add Selected Signals",
    add_selected_signals,
    SUCCESS_COLOR,
    SUCCESS_HOVER,
    25
)

add_button.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=12
)


# =========================================================
# TASK 1 - MULTIPLY
# =========================================================

multiply_frame = tk.LabelFrame(
    task1_content,
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
    padx=20,
    pady=10
)


tk.Label(
    multiply_frame,
    text="Constant",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=0,
    padx=10
)


constant_entry = tk.Entry(
    multiply_frame,
    width=20,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat"
)

constant_entry.grid(
    row=0,
    column=1,
    padx=15,
    pady=8,
    ipady=7
)


multiply_button = create_button(
    multiply_frame,
    "Multiply Signal",
    multiply_selected_signal,
    PURPLE_COLOR,
    PURPLE_HOVER,
    22
)

multiply_button.grid(
    row=0,
    column=2,
    padx=25
)


# =========================================================
# TASK 2 - DISPLAY TYPE
# =========================================================

task2_display_frame = tk.LabelFrame(
    task2_content,
    text="  RESULT DISPLAY  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

task2_display_frame.pack(
    fill="x",
    padx=20,
    pady=10
)


tk.Label(
    task2_display_frame,
    text="Display Type",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=15
)


task2_display_combo = ttk.Combobox(
    task2_display_frame,
    values=[
        "Continuous",
        "Discrete"
    ],
    state="readonly",
    width=20
)

task2_display_combo.pack(
    side="left",
    padx=15
)

task2_display_combo.set(
    "Continuous"
)


# =========================================================
# TASK 2 - SUBTRACTION
# =========================================================

subtraction_frame = tk.LabelFrame(
    task2_content,
    text="  SUBTRACTION  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

subtraction_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


subtraction_signal1_combo = ttk.Combobox(
    subtraction_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=15
)

subtraction_signal1_combo.pack(
    side="left",
    padx=10
)

subtraction_signal1_combo.set(
    "Signal 1"
)


tk.Label(
    subtraction_frame,
    text="−",
    font=("Arial", 18, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE_COLOR
).pack(
    side="left",
    padx=5
)


subtraction_signal2_combo = ttk.Combobox(
    subtraction_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=15
)

subtraction_signal2_combo.pack(
    side="left",
    padx=10
)

subtraction_signal2_combo.set(
    "Signal 2"
)


subtract_button = create_button(
    subtraction_frame,
    "Subtract",
    subtract_selected_signals,
    ORANGE_COLOR,
    ORANGE_HOVER,
    15
)

subtract_button.pack(
    side="left",
    padx=20
)


# =========================================================
# TASK 2 - SQUARING
# =========================================================

square_frame = tk.LabelFrame(
    task2_content,
    text="  SQUARING  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

square_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


square_signal_combo = ttk.Combobox(
    square_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=20
)

square_signal_combo.pack(
    side="left",
    padx=15
)

square_signal_combo.set(
    "Signal 1"
)


square_button = create_button(
    square_frame,
    "Square Signal",
    square_selected_signal,
    ORANGE_COLOR,
    ORANGE_HOVER,
    18
)

square_button.pack(
    side="left",
    padx=20
)


# =========================================================
# TASK 2 - NORMALIZATION
# =========================================================

normalization_frame = tk.LabelFrame(
    task2_content,
    text="  NORMALIZATION  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

normalization_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


normalize_signal_combo = ttk.Combobox(
    normalization_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=15
)

normalize_signal_combo.pack(
    side="left",
    padx=10
)

normalize_signal_combo.set(
    "Signal 1"
)


normalization_choice = tk.IntVar(
    value=0
)


tk.Radiobutton(
    normalization_frame,
    text="-1 to 1",
    variable=normalization_choice,
    value=1,
    font=("Arial", 9),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
).pack(
    side="left",
    padx=8
)


tk.Radiobutton(
    normalization_frame,
    text="0 to 1",
    variable=normalization_choice,
    value=2,
    font=("Arial", 9),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR
).pack(
    side="left",
    padx=8
)


normalize_button = create_button(
    normalization_frame,
    "Normalize",
    normalize_selected_signal,
    ORANGE_COLOR,
    ORANGE_HOVER,
    15
)

normalize_button.pack(
    side="left",
    padx=20
)


# =========================================================
# TASK 2 - ACCUMULATION
# =========================================================

accumulation_frame = tk.LabelFrame(
    task2_content,
    text="  ACCUMULATION  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE_COLOR,
    bd=1,
    relief="solid",
    padx=25,
    pady=15
)

accumulation_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


accumulate_signal_combo = ttk.Combobox(
    accumulation_frame,
    values=[
        "Signal 1",
        "Signal 2",
        "Signal 3"
    ],
    state="readonly",
    width=20
)

accumulate_signal_combo.pack(
    side="left",
    padx=15
)

accumulate_signal_combo.set(
    "Signal 1"
)


accumulate_button = create_button(
    accumulation_frame,
    "Accumulate Signal",
    accumulate_selected_signal,
    ORANGE_COLOR,
    ORANGE_HOVER,
    20
)

accumulate_button.pack(
    side="left",
    padx=20
)


# =========================================================
# TASK 2 - QUANTIZATION
# =========================================================

quantization_frame = tk.LabelFrame(
    task2_content,
    text="  QUANTIZATION  ",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=TEAL_COLOR,
    bd=1,
    relief="solid",
    padx=20,
    pady=15
)

quantization_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


# =========================================================
# QUANTIZATION CONTROLS
# =========================================================

quantization_controls = tk.Frame(
    quantization_frame,
    bg=CARD_COLOR
)

quantization_controls.pack(
    fill="x"
)


tk.Label(
    quantization_controls,
    text="Input File",
    font=("Arial", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=(5, 10)
)


quantization_file_combo = ttk.Combobox(
    quantization_controls,
    values=[
        "Quan1_input",
        "Quan2_input"
    ],
    state="readonly",
    width=18
)

quantization_file_combo.pack(
    side="left",
    padx=5
)

quantization_file_combo.set(
    "Quan1_input"
)


quantization_info = tk.Label(
    quantization_controls,
    text="Quan1_input  •  3 Bits  •  8 Levels",
    font=("Arial", 10, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

quantization_info.pack(
    side="left",
    padx=20
)


quantize_button = create_button(
    quantization_controls,
    "QUANTIZE SIGNAL",
    quantize_selected_signal,
    TEAL_COLOR,
    TEAL_HOVER,
    20
)

quantize_button.pack(
    side="right",
    padx=5
)


# =========================================================
# QUANTIZATION TABLE
# =========================================================

table_frame = tk.Frame(
    quantization_frame,
    bg=CARD_COLOR
)

table_frame.pack(
    fill="x",
    pady=(15, 0)
)


quantization_columns = (
    "sample",
    "original",
    "interval",
    "encoded",
    "quantized",
    "error"
)


quantization_tree = ttk.Treeview(
    table_frame,
    columns=quantization_columns,
    show="headings",
    height=9
)


quantization_tree.heading(
    "sample",
    text="Sample"
)

quantization_tree.heading(
    "original",
    text="Original"
)

quantization_tree.heading(
    "interval",
    text="Interval"
)

quantization_tree.heading(
    "encoded",
    text="Encoded"
)

quantization_tree.heading(
    "quantized",
    text="Quantized"
)

quantization_tree.heading(
    "error",
    text="Error"
)


quantization_tree.column(
    "sample",
    width=70,
    anchor="center"
)

quantization_tree.column(
    "original",
    width=100,
    anchor="center"
)

quantization_tree.column(
    "interval",
    width=80,
    anchor="center"
)

quantization_tree.column(
    "encoded",
    width=100,
    anchor="center"
)

quantization_tree.column(
    "quantized",
    width=100,
    anchor="center"
)

quantization_tree.column(
    "error",
    width=100,
    anchor="center"
)


quantization_tree.pack(
    side="left",
    fill="x",
    expand=True
)


quantization_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=quantization_tree.yview
)

quantization_scrollbar.pack(
    side="right",
    fill="y"
)


quantization_tree.configure(
    yscrollcommand=quantization_scrollbar.set
)


# =========================================================
# TASK 2 BOTTOM SPACE
# =========================================================

tk.Frame(
    task2_content,
    bg=BG_COLOR,
    height=30
).pack()


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
    pady=5
)


# =========================================================
# RUN
# =========================================================

window.mainloop()