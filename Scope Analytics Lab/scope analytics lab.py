"""
Variable Scope Lab

Learning focus:
- Local variables live inside functions
- Global variables live at top level
- A function can read globals, but changing it needs the global keyword
- Good practice is to keep most variables local
"""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

APP_TITLE = "Variable Scope Analytics Lab" # global constant
DATA_FILE = Path(__file__).with_name("scope_events.csv")
dashboard_open_count = 0


def increment_open_count():
    """Change a global variable from inside a function"""
    global dashboard_open_count
    dashboard_open_count += 1

def load_data():
    """The dataframe variable is local to this function"""
    dataframe = pd.read_csv(DATA_FILE)
    return dataframe


def add_scope_score(dataframe):
    """Create a NumPy risk/complexity score using local working variables"""
    local_weight = 0.5
    global_read_weight = 1.0
    global_write_weight = 2.5
    error_weight = 4.0

    dataframe = dataframe.copy()
    dataframe["ScopeScore"] = np.round(
        dataframe["LocalVariables"] * local_weight
        + dataframe["GlobalReads"] * global_read_weight
        + dataframe["GlobalWrites"] * global_write_weight
        + dataframe["NameErrors"] * error_weight,
        2
    )
    return dataframe


def build_summary(dataframe):
    """Return a text summary. All helper variables here are local"""
    total_events = len(dataframe)
    total_errors = int(dataframe["NameErrors"].sum())
    average_score = float(np.mean(dataframe["ScopeScore"]))
    global_writes = int(dataframe["GlobalWrites"].sum())

    return(
        f"Events analysed: {total_events}\n"
        f"Total NameErrors: {total_errors}\n"
        f"Average scope score: {average_score:.2f}\n"
        f"Global writes observed: {global_writes}\n"
        f"Dashboard opened: {dashboard_open_count} time(s)"
    )


def plot_by_function(dataframe):
    """Matplotlib chart: average scope score by function"""
    chart_data = (
        dataframe.groupby("FunctionName")["ScopeScore"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))
    chart_data.plot(kind="bar")
    plt.title("Average Scope Score by Function")
    plt.ylabel("Average Scope Score")
    plt.xlabel("Function")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def plot_scope_types(dataframe):
    """Matplotlib chart: number of events by scope type"""
    counts = dataframe["ScopeType"].value_counts()

    plt.figure(figsize=(7, 5))
    plt.bar(counts.index, counts.values)
    plt.title("Events by Scope Type")
    plt.ylabel("Number of Events")
    plt.xlabel("Scope Type")
    plt.tight_layout()
    plt.show()


def main():
    increment_open_count()

    data = load_data() # local to main()
    data = add_scope_score(data)

    window = tk.Tk()
    window.title(APP_TITLE)
    window.geometry("760x500")

    title = tk.Label(
        window,
        text="VARIABLE SCOPE ANALYTICS LAB",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=18)

    summary_box = tk.Text(window, width=78, height=10)
    summary_box.pack(padx=20, pady=10)
    summary_box.insert("1.0", build_summary(data))
    summary_box.config(state="disabled")

    button_frame = tk.Frame(window)
    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="Plot Function Scope Score",
        width=25,
        command=lambda: plot_by_function(data)
    ).grid(row=0, column=0, padx=8)

    tk.Button(
        button_frame,
        text="Plot Scope Types",
        width=25,
        command=lambda: plot_scope_types(data)
    ).grid(row=0, column=1, padx=8)

    tk.Button(
        window,
        text="Explain Scope",
        command=lambda: messagebox.showinfo(
            "Scope reminder",
            "Local variables belong to a function. Global variables live at top level. "
            "Use the narrowest scope that still does the job."
        )
    ).pack(pady=8)

    window.mainloop()


if __name__ == "__main__":
    main()