import tkinter as tk
from tkinter import ttk, messagebox

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


def show_threat_chart():
    # Display the number of incidents for each human threat
    counts = df["ThreatType"].value_counts().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar")
    plt.title("Human Threat Incidents by Type")
    plt.xlabel("Threat Type")
    plt.ylabel("Number of Incidents")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()


def show_average_risk_chart():
    # Display average risk score for each threat type
    average_risk = (
        df.groupby("ThreatType")["RiskScore"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    average_risk.plot(kind="bar")
    plt.title("Average Risk Score by Human Threat")
    plt.xlabel("Threat Type")
    plt.ylabel("Average Risk Score")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()


def show_high_risk():
    # Show incidents with a risk score of 16 or above
    high_risk = df[df["RiskScore"] >= 16]

    output.delete("1.0", tk.END)

    if high_risk.empty:
        output.insert(tk.END, "no high-risk incidents found.")
        return

    for _, row in high_risk.iterrows():
        output.insert(
            tk.END,
            f"#{row['IncidentID']} | {row['Department']} | "
            f"{row['ThreatType']} | Risk {row['RiskScore']}\n"
        )


def show_summary():
    # Use pandas and NumPy to create a quick SOC-style summary
    total = len(df)
    mean_risk = np.mean(df["RiskScore"].to_numpy())
    highest = df.loc[df["RiskScore"].idxmax()]

    output.delete("1.0", tk.END)
    output.insert(tk.END, f"Total incidents: {total}\n")
    output.insert(tk.END, f"Mean risk score: {mean_risk:.2f}\n")
    output.insert(
        tk.END,
        f"Highest risk: #{highest['IncidentID']} - "
        f"{highest['ThreatType']} ({highest['RiskScore']})\n"
    )
    output.insert(
        tk.END,
        f"Recommended control: #{highest['RecommendedControl']}\n"
    )


# ---------------- TKINTER GUI ----------------
root = tk.Tk()
root.title("Human Threat Analytics Dashboard")
root.geometry("820x560")

title = tk.Label(
    root,
    text="HUMAN THREAT ANALYTICS DASHBOARD",
    font=("Arial", 20, "bold")
)
title.pack(pady=14)

subtitle = tk.Label(
    root,
    text="Analyse fictional incidents using pandas, NumPy, Matplotlib and Tkinter"
)
subtitle.pack()

button_frame = ttk.Frame(root)
button_frame.pack(pady=16)

ttk.Button(
    button_frame,
    text="Summary",
    command=show_summary
).grid(row=0, column=0, padx=5)

ttk.Button(
    button_frame,
    text="Threat Chart",
    command=show_threat_chart
).grid(row=0, column=1, padx=5)

ttk.Button(
    button_frame,
    text="Average Risk Chart",
    command=show_average_risk_chart
).grid(row=0, column=2, padx=5)

ttk.Button(
    button_frame,
    text="High-Risk Incidents",
    command=show_high_risk
).grid(row=0, column=3, padx=5)

output = tk.Text(root, width=92, height=20)
output.pack(padx=18, pady=10)

show_summary()

root.mainloop()