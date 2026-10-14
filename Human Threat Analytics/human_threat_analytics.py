import tkinter as tk
from tkinter import ttk

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

    return data

df = load_data()

def filtered_data():
    # Return rows matching the selected department and threat
    data = df.copy()

    department = department_var.get()
    threat = threat_var.get()

    if department != "All":
        data = data[data["Department"] == department]

    if threat != "All":
        data = data[data["ThreatType"] == threat]

    return data

def update_table():
    # Refresh the Treeview using the selected filters
    for item in table.get_children():
        table.delete(item)

    data = filtered_data()

    for _, row in data.iterrows():
        table.insert(
            "",
            tk.END,
            values=(
                row["IncidentID"],
                row["Department"],
                row["ThreatType"],
                row["RiskScore"],
                row["RecommendedControl"]
            )
        )

    status_label.config(text=f"Showing {len(data)} incident(s)")


def show_filtered_chart():
    # Plot incident counts for the filtered dataset
    data = filtered_data()

    if data.empty:
        return

    counts = data["ThreatType"].value_counts()

    plt.figure(figsize=(7, 4))
    counts.plot(kind="bar")
    plt.title("Filtered Human Threat Incidents")
    plt.xlabel("Threat Type")
    plt.ylabel("Incidents")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()


def show_risk_box():
    # Display statistics for the currently filtered data
    data = filtered_data()

    output.delete("1.0", tk.END)

    if data.empty:
        output.insert(tk.END, "No incidents match the filters.")
        return

    risks = data["RiskScore"].to_numpy()

    output.insert(tk.END, f"Mean risk: {np.mean(risks):.2f}\n")
    output.insert(tk.END, f"Median risk: {np.median(risks):.2f}\n")
    output.insert(tk.END, f"Maximum risk: {np.max(risks)}\n")
    output.insert(tk.END, f"Minimum risk: {np.min(risks)}\n")


# ---------------- TKINTER GUI ----------------
root = tk.Tk()
root.title("Human Threat Analytics Dashboard")
root.geometry("980x650")

tk.Label(
    root,
    text="HUMAN THREAT FILTER DASHBOARD",
    font=("Arial", 20, "bold")
).pack(pady=12)

filters = ttk.Frame(root)
filters.pack(pady=8)

department_var = tk.StringVar(value="All")
threat_var = tk.StringVar(value="All")

departments = ["All"] + sorted(df["Department"].unique().tolist())
threats = ["All"] + sorted(df["ThreatType"].unique().tolist())

ttk.Label(filters, text="Department:").grid(row=0, column=0, padx=4)
ttk.Combobox(
    filters,
    textvariable=department_var,
    values=departments,
    state="readonly",
    width=18
).grid(row=0, column=1, padx=4)

ttk.Label(filters, text="Threat:").grid(row=0, column=2, padx=4)
ttk.Combobox(
    filters,
    textvariable=threat_var,
    values=threats,
    state="readonly",
    width=22
).grid(row=0, column=3, padx=4)

ttk.Button(
    filters,
    text="Apply Filter",
    command=update_table
).grid(row=0, column=4, padx=5)

ttk.Button(
    filters,
    text="Show Chart",
    command=show_filtered_chart
).grid(row=0, column=5, padx=5)

ttk.Button(
    filters,
    text="Risk Statistics",
    command=show_risk_box
).grid(row=0, column=6, padx=5)

columns = ("ID", "Department", "Threat", "Risk", "Control")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for column in columns:
    table.heading(column, text=column)

table.column("ID", width=50)
table.column("Department", width=110)
table.column("Threat", width=160)
table.column("Risk", width=70)
table.column("Control", width=180)

table.pack(fill="both", expand=True, padx=15, pady=10)

status_label = ttk.Label(root, text="")
status_label.pack()

output = tk.Text(root, height=6, width=105)
output.pack(padx=15, pady=10)

update_table()

root.mainloop()
