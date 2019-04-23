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
    attendances = data[["email", "events"]]
    data.pop("events")

    attendances, uniques = get_attendances(attendances)
    attendances = pd.DataFrame(attendances)
    attendances["description"] = ""
    events = pd.DataFrame({"name": list(uniques)})
    events = events.assign(month="", year="", description="", CLY_sponsored="", location="")

    results = os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), "results")
    if not os.path.exists(results):
        os.makedirs(results)

    data.to_csv(os.path.join(results, "alumni.csv"), index = False)
    events.to_csv(os.path.join(results, "events.csv"), index = False)
    attendances.to_csv(os.path.join(results, "attendances.csv"), index = False)

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    parse_file(filename)
    label.config(text="Successfully Converted CSV Files.")

def AlumnusAction(event=None):
    file = open(os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), "alumnus_template.csv"), "w")
    file.write("first_name,last_name,email,phone,location,college,yale_degree,other_degrees,linkedin,employer,employed_field,recommender,description")
    file.close()
    label.config(text="Successfully Downloaded Alumnus Template.")

def StudentAction(event=None):
    file = open(os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), "student_template.csv"), "w")
    file.write("first_name,last_name,email,year")
    file.close()
    label.config(text="Successfully Downloaded Student Template.")

root = tk.Tk()
root.geometry("500x300")
button = tk.Button(root, text='Convert Alumnus Template', command=UploadAction, height=5, width=50)
alumnus_button = tk.Button(root, text='Download Alumnus Template', command=AlumnusAction, height=5, width=50)
student_button = tk.Button(root, text='Download Student Template', command=StudentAction, height=5, width=50)
label = tk.Label(root, text="Upload a CSV file containing\na comma-delimited column with events.")
button.pack()
alumnus_button.pack()
student_button.pack()
label.pack()

root.mainloop()
