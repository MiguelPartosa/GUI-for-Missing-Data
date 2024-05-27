import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import filedialog
from tkinter import ttk  # for the rounded button
from tkinter import messagebox  # for feedback
BGCOL = "#053F2A"  # main bg col
METHODLIST = ['Remove rows with missing data', r'Fill by column average (mean)',
              'Fill by linear interpolation', r'Fill by global constant (i.e. \'0\' or NA)']
GLOBALCONST = 'NA'


def findCsv():  # find csv
    global file_path
    file_path = filedialog.askopenfilename(title="Select a CSV File",
                                           filetypes=[("CSV Files", "*.csv"),
                                                      ("All Files", "*.*")])  # Filter for CSV files
    if not file_path:
        print("Selected file:", file_path)
        FileSelected = False
        find_button.config(text="Find File")
    else:
        print("Selected file:", file_path)
        FileSelected = True
        find_button.config(text="Selected File: "+file_path.split("/")[-1])

    # update other conditions to disable execute button
    CheckToggles()
    CheckCSV()


class ToggleButton():
    def __init__(self, master, text, default_state=False, **kwargs):
        self.var = tk.BooleanVar(value=default_state)
        self.button = tk.Checkbutton(
            master, text=text, variable=self.var, command=CheckToggles,
            bg=BGCOL, fg="white", selectcolor="#55833F", font=("helvetica", 10),
            state="disabled")
        self.button.pack(**kwargs)  # already packing

    def GetState(self):
        return self.var.get()

    def ChangeState(self, val):
        if val:
            self.button.config(state="normal")
        else:
            self.button.config(state="disabled")


def CheckToggles():  # checks if there are toggled checkboxes
    # Turn off execute button if there are no options selected
    global file_path, ToggleInstances
    if (any(object.var.get() is True for object in ToggleInstances) and file_path):
        BtnExecute.config(state='normal')
    else:
        BtnExecute.config(state='disabled')


def CheckCSV():  # checks if there is a chosen csv
    # Turn off goggles if there is none
    global file_path
    if not file_path:
        print("No")
        for Button in (ToggleInstances):
            Button.ChangeState(False)
    else:
        print("Yes")
        for Button in (ToggleInstances):
            Button.ChangeState(True)


# Functional code

# Option 1: remove rows with missing data
# Option 2: Fill by column average (mean)
# Option 3: Linear Interpolation
# Option 4: Fill by global constant
def Option1(csv, Out):  # dropp row
    print("ran ")
    try:
        df = pd.read_csv(csv)
        print(df)
        df.dropna(inplace=True)
        df.to_csv(Out, index=False)
        print("\n\n", df)
        print(f"Columns with missing data removed. Saved to {Out}\n\n")
    except Exception as e:
        print(f"An error occurred: {e}")


def Option2(csv, Out):  # mean
    try:
        df = pd.read_csv(csv)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col].fillna(df[col].mean(), inplace=True)
        df.to_csv(Out, index=False)
        print(
            f"Missing values filled with column averages. Saved to {Out}\n\n")
    except Exception as e:
        print(f"An error occurred: {e}")


def Option3(csv, Out):  # linear interpolation
    try:
        df = pd.read_csv(csv)
        # to avoid columns that have text
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col].interpolate(method='linear', inplace=True)
        df.to_csv(Out, index=False)
        print(
            f"Missing values filled with linear interpolation. Saved to {Out}\n\n")
    except Exception as e:
        print(f"Errorr: {e}")


def Option4(csv, Out):  # Constant
    try:
        df = pd.read_csv(csv)
        # will not avoid columns that have strings because it doesn't need calcu
        df.fillna(GLOBALCONST, inplace=True)
        df.to_csv(Out, index=False)
        print(
            f"Missing values filled with '{GLOBALCONST}'. Saved to {Out}\n\n")
    except Exception as e:
        print(f"An error occurred: {e}")

# Execute Button


def show_popup(message):  # for user feedback, wow hci! I used a function for flexibility of expanding the program
    messagebox.showinfo("Execution Status:", message)


def Execute():
    global ToggleInstances
    switch_dict = [Option1, Option2, Option3, Option4]  # list of functions

    for index, button in enumerate(ToggleInstances):
        if button.GetState():
            switch_dict[index](file_path, file_path.rsplit(
                '/', 1)[0] + '/' + f"Method{index+1}.csv")

    show_popup("Files Generated in same directory as csv.")


# GUI and application
root = tk.Tk()
root.title("Missing Data Handler")
root.geometry("300x400")
root.resizable(False, False)
root.configure(bg=BGCOL)
iconpath = r"c:\Users\Miguel\Documents\VSCode\School\CS 35 Data Mining\Exercise 1\DataIcon.ico"
root.iconbitmap("DataIcon.ico")

# Labels
tk.Label(font=("Helvetica", 15),
         fg='white', bg=BGCOL, text="Missing Data Handler", anchor='w').pack()  # Title 2

tk.Label(font=("Helvetica", 7),
         fg='white', bg=BGCOL, text="by Miguel Partosa | an exercise in cs 35 Data Mining", anchor='w',
         wraplength=200).pack()  # info and subtitle

tk.Label(font=("Helvetica", 7),
         fg='white', bg=BGCOL, text="CSV Directory*", anchor='w', justify="left", width=25, padx=10,
         wraplength=200).pack()  # label1

# Button for finding file
FileSelected = False
file_path = ""
find_button = tk.Button(root, text="Find File",
                        command=findCsv, width=30, anchor='w')
find_button.pack()

# List of options to run
ToggleInstances = []

for button in range(4):
    CreateButton = ToggleButton(
        root, f"Method {button+1}", padx=40, pady=5, anchor='w')
    # for description of method
    tk.Label(font=("Helvetica", 7),
             fg='white', bg=BGCOL, text=METHODLIST[button], anchor='w', justify="left", width=20, padx=30,
             wraplength=200).pack()  # label1
    # adding direct objects to list to reference when executing
    ToggleInstances.append(CreateButton)


# This Button has to be special
# Style for rounded button
style = ttk.Style()
style.configure("Rounded.TButton", borderwidth=0,
                relief="flat", background=BGCOL, font=("Helvetica", 15))

BtnExecute = ttk.Button(root, text="Fix Data & Generate Files", style="Rounded.TButton",
                        command=Execute, state='disabled')

BtnExecute.pack(padx=0, pady=20, side='bottom',
                anchor='center')

# 4 options for the 4 methods that allows the user to handle the missing data
# 5 menus including a run all button

# open file and give the options to solve the missing data
# Open this in a new file


root.mainloop()  # start application
try:
    input("press anything to continue")
except:
    pass
