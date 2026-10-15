import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV_FILE = "human_threat_incidents.csv"


def load_data():
    # load the fictional incident dataset and calculate a risk score
    data = pd.read_csv(CSV_FILE)

    # NumPy multiplies the likelihood and impact arrays
    data["RiskScore"] = np.multiply(
        data["Likelihood"].to_numpy(),
        data["Impact"].to_numpy()
    )

    # NumPy selects a risk band using multiple conditions
    conditions = [
        data["RiskScore"] >= 16,
        data["RiskScore"] > 8
    ]

    choices = ["High", "Medium"]

    data["RiskBand"] = np.select(
        conditions,
        choices,
        default="Low"
    )

    return data

df = load_data()

def refresh_table(data=None):
    if data is None:
        data = df

    for item in table.get_children():
        table.delete(item)

    for _, row in data.iterrows():
        table.insert(
            "",
            tk.END,
            values=(
                row["IncidentID"],
                row["Department"],
                row["ThreatType"],
                row["RiskScore"],
                row["RiskBand"],
                row["RecommendedControl"]
            )
        )

def show_priority_chart():
    # Plot how many incidents fall into each risk band
    order = ["Low", "Medium", "High"]
    counts = df["RiskBand"].value_counts().reindex(order, fill_value=0)

    plt.figure(figsize=(7, 4))
    counts.plot(kind="bar")
    plt.title("Incident Priority by Risk Band")
    plt.xlabel("Risk Band")
    plt.ylabel("Incidents")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
     

def show_control_chart():
    # Show how often each recommended control appears.
    controls = df["RecommendedControl"].value_counts()

    plt.figure(figsize=(8, 5))
    controls.plot(kind="barh")
    plt.title("Recommended Controls Across Incidents")
    plt.xlabel("Number of Incidents")
    plt.tight_layout()
    plt.show()


def show_high_priority():
    high = df[df["RiskBand"] == "High"]
    refresh_table(high)
    status.config(text=f"High-priority incidents: {len(high)}")


def show_all():
    refresh_table(df)
    status.config(text=f"All incidents: {len(df)}")


def export_analysis():
    # Export the analysed dataset with risk scores and risk bands
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save analysed incident report"
    )

    if filename:
        df.to_csv(filename, index=False)
        messagebox.showinfo(
            "Export complete",
            "The analysed incident report was saved."
        )


# ---------------- TKINTER GUI ----------------
root = tk.Tk()
root.title("Human Threat Analytics Dashboard")
root.geometry("1050x680")

tk.Label(
    root,
    text="HUMAN THREAT PRIORITY CENTRE",
    font=("Arial", 20, "bold")
).pack(pady=12)

buttons = ttk.Frame(root)
buttons.pack(pady=6)

tk.Button(
    buttons,
    text="All Incidents",
    command=show_all
).grid(row=0, column=0, padx=5)

ttk.Button(
    buttons,
    text="High Priority",
    command=show_high_priority
).grid(row=0, column=1, padx=5)

ttk.Button(
    buttons,
    text="Risk Band Chart",
    command=show_priority_chart
).grid(row=0, column=2, padx=5)

ttk.Button(
    buttons,
    text="Control Chart",
    command=show_control_chart
).grid(row=0, column=3, padx=5)

ttk.Button(
    buttons,
    text="Export Analysis",
    command=export_analysis
).grid(row=0, column=4, padx=5)

columns = (
    "ID",
    "Department",
    "Threat",
    "Risk",
    "Band",
    "Recommended Control"
)

table = ttk.Treeview(
    root, columns=columns,
    show="headings",
    height=20
)

for column in columns:
    table.heading(column, text=column)

table.column("ID", width=50)
table.column("Department", width=100)
table.column("Threat", width=150)
table.column("Risk", width=65)
table.column("Band", width=80)
table.column("Recommended Control", width=180)

table.pack(fill="both", expand=True, padx=15, pady=10)

status = ttk.Label(root, text="")
status.pack(pady=5)

show_all()

root.mainloop()
