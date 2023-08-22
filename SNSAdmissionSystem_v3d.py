"""
SNS Admission System
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import random
import pandas as pd
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

class ImageManager:
    def __init__(self):
        self.image_references = []

    def create_image(self, image_path):
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        self.image_references.append(image_tk)
        return image_tk

class SchoolAdmissionsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SNS Student Admissions System")
        self.root.geometry("1024x768")

        self.image_manager = ImageManager()
        self.original_image = Image.open("SNSLogo1.jpg")
        self.background_image = self.image_manager.create_image("SNSLogo1.jpg")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relx=0.5, rely=1, anchor="s")  # Positioned at the bottom

        self.num_students_var = tk.StringVar()
        self.age_range_var = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        self.apply_washout_effect()

        inputs_frame = tk.Frame(self.root)
        inputs_frame.place(relx=0.5, rely=0.1, anchor="n")  # Positioned at the top

        self.create_input_labels(inputs_frame)
        self.create_input_entries(inputs_frame)
        self.create_input_buttons(inputs_frame)

    def create_input_labels(self, frame):
        tk.Label(frame, text="Enter number of students to select:").pack()
        tk.Label(frame, text="Enter age range (min-max):").pack()

    def create_input_entries(self, frame):
        self.num_students_entry = tk.Entry(frame, textvariable=self.num_students_var)
        self.num_students_entry.pack(side="left")
        self.age_range_entry = tk.Entry(frame, textvariable=self.age_range_var)
        self.age_range_entry.insert(tk.END, "3-4")
        self.age_range_entry.pack(side="left")

    def create_input_buttons(self, frame):
        tk.Button(frame, text="Set Inputs", command=self.set_inputs).pack(side="left", padx=10)
        tk.Button(frame, text="Load Excel File", command=self.load_excel_file).pack(side="left", padx=10)
        tk.Button(frame, text="Select Students", command=self.select_students).pack(side="left", padx=10)

    def apply_washout_effect(self):
        original_image = Image.open("SNSLogo1.jpg")
        washed_out_image = original_image.copy()
        washed_out_image.putalpha(60)
        self.washout_image = ImageTk.PhotoImage(washed_out_image)

    def set_inputs(self):
        try:
            num_students = int(self.num_students_var.get())
            age_range_str = self.age_range_var.get()
            age_range = tuple(map(int, age_range_str.split('-')))

            if num_students <= 0 or age_range[0] >= age_range[1]:
                raise ValueError

            messagebox.showinfo("Inputs Set", "Inputs have been set successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid inputs")

    def load_excel_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                messagebox.showinfo("Excel File Loaded", "Excel file loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file:\n{str(e)}")

    def select_students(self):
        if not self.num_students_var.get() or not self.age_range_var.get() or not hasattr(self, 'df'):
            messagebox.showerror("Error", "Please set the inputs and load the Excel file")
            return

        try:
            num_students = int(self.num_students_var.get())
            age_range = tuple(map(int, self.age_range_var.get().split('-')))
            self.selected_students = self.process_data(self.df, num_students, age_range)
            self.display_selected_students()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def process_data(self, dataframe, num_students, age_range):
        boys = dataframe[dataframe['Gender'] == 'M']
        girls = dataframe[dataframe['Gender'] == 'F']

        boys_count = girls_count = num_students // 2

        selected_boys = boys.sample(min(boys_count, len(boys)), replace=False).reset_index(drop=True)
        selected_girls = girls.sample(min(girls_count, len(girls)), replace=False).reset_index(drop=True)

        selected_ages = random.choices(range(age_range[0], age_range[1] + 1), k=num_students)

        selected_students = pd.concat([selected_boys, selected_girls], ignore_index=True)
        selected_students['Age'] = selected_ages

        return selected_students

    def display_selected_students(self):
        results_window = tk.Toplevel(self.root)
        results_window.title("Selected Students Results")

        self.create_results_label(results_window)
        self.create_results_text(results_window)
        self.create_save_buttons(results_window)

    def create_results_label(self, window):
        results_label = tk.Label(window, text="Selected Students:")
        results_label.pack()

    def create_results_text(self, window):
        results_text = tk.Text(window, height=10, width=50)
        results_text.pack()
        results_text.config(state=tk.NORMAL)
        results_text.insert(tk.END, self.selected_students.to_string(index=False))
        results_text.config(state=tk.DISABLED)

    def create_save_buttons(self, window):
        save_csv_button = tk.Button(window, text="Save as CSV", command=self.save_csv)
        save_csv_button.pack()

        save_excel_button = tk.Button(window, text="Save as Excel", command=self.save_excel)
        save_excel_button.pack()

    def save_csv(self):
        if self.selected_students is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.selected_students.to_csv(file_path, index=False)
                messagebox.showinfo("CSV Saved", "CSV file saved successfully")

    def save_excel(self):
        if self.selected_students is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                self.selected_students.to_excel(file_path, index=False)
                messagebox.showinfo("Excel Saved", "Excel file saved successfully")

def main():
    root = ThemedTk(theme="arc")
    app = SchoolAdmissionsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
