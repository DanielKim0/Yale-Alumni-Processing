import pandas as pd
import sys, os
import tkinter as tk
from tkinter import filedialog

def get_attendances(attendances):
    uniques = set()
    emails = []
    events = []
    for index, row in attendances.iterrows():
        if pd.notnull(row[1]):
            attended = row[1].split(", ")
            for event in attended:
                emails.append(row[0])
                events.append(event)
                uniques.add(event)
    return {"alumnus_email": emails, "event_name": events}, uniques

def parse_file(file):
    data = pd.read_csv(file)
    attendances = data[["email", "event"]]
    data.pop("event")

    attendances, uniques = get_attendances(attendances)
    attendances = pd.DataFrame(attendances)
    attendances["description"] = ""
    events = pd.DataFrame({"name": list(uniques)})
    events = events.assign(month="", year="", description="", CLY_sponsored="", location="")

    if not os.path.exists("results"):
        os.makedirs("results")

    data.to_csv(os.path.join("results", "alumni.csv"), index = False)
    events.to_csv(os.path.join("results", "events.csv"), index = False)
    attendances.to_csv(os.path.join("results", "attendances.csv"), index = False)

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    parse_file(filename)
    label.config(text="Success!")

root = tk.Tk()
button = tk.Button(root, text='Open', command=UploadAction, height=5, width=20)
label = tk.Label(root, text="Upload a CSV file containing\na comma-delimited column with events.")
button.pack()
label.pack()

root.mainloop()
