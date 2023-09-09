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
        self.background_image = self.image_manager.create_image("SNSLogo1.jpg")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relx=0.5, rely=1, anchor="s")

        self.num_students_var = tk.StringVar()
        self.age_range_var = tk.StringVar(value="3-4.5")

        self.create_widgets()
        
    def display_total_students(self):
        total_students_window = tk.Toplevel(self.root)
        total_students_window.title("Total Students Count")

        total_students_label = tk.Label(total_students_window, text=f"Total Students: {len(self.df)}")
        total_students_label.pack()


    def create_widgets(self):
        self.apply_washout_effect()

        inputs_frame = tk.Frame(self.root)
        inputs_frame.place(relx=0.5, rely=0.1, anchor="n")

        self.create_input_labels(inputs_frame)
        self.create_input_entries(inputs_frame)
        self.create_input_buttons(inputs_frame)

    def create_input_labels(self, frame):
        for label_text in ["Enter number of students to select:", "Enter age range (min-max):"]:
            tk.Label(frame, text=label_text).pack()

    def create_input_entries(self, frame):
        self.num_students_entry = tk.Entry(frame, textvariable=self.num_students_var)
        self.num_students_entry.pack(side="left")
        self.age_range_entry = tk.Entry(frame, textvariable=self.age_range_var)
        self.age_range_entry.pack(side="left")

    def create_input_buttons(self, frame):
        button_texts = ["Set Inputs", "Load Excel File", "Select Students", "Display Total Students"]
        button_commands = [self.set_inputs, self.load_excel_file, self.select_students, self.display_total_students]

        for text, command in zip(button_texts, button_commands):
            tk.Button(frame, text=text, command=command).pack(side="left", padx=10)


    def apply_washout_effect(self):
        original_image = Image.open("SNSLogo1.jpg")
        washed_out_image = original_image.copy()
        washed_out_image.putalpha(60)
        self.washout_image = ImageTk.PhotoImage(washed_out_image)

    def set_inputs(self):
        try:
            num_students = int(self.num_students_var.get())
            min_age, max_age = map(float, self.age_range_var.get().split('-'))

            if num_students <= 0 or min_age >= max_age:
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
        if not (self.num_students_var.get() and self.age_range_var.get() and hasattr(self, 'df')):
            messagebox.showerror("Error", "Please set the inputs and load the Excel file")
            return

        try:
            num_students = int(self.num_students_var.get())
            min_age, max_age = map(float, self.age_range_var.get().split('-'))
            self.selected_students = self.process_data(self.df, num_students, (min_age, max_age))
            self.display_selected_students()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def process_data(self, dataframe, num_students, age_range):
        boys = dataframe[dataframe['Gender'] == 'Male']
        girls = dataframe[dataframe['Gender'] == 'Female']

        boys_count = num_students // 2
        girls_count = num_students - boys_count

        selected_boys = boys.sample(min(boys_count, len(boys)), replace=False).reset_index(drop=True)
        selected_girls = girls.sample(min(girls_count, len(girls)), replace=False).reset_index(drop=True)

        selected_ages = [round(random.uniform(age_range[0], age_range[1]), 1) for _ in range(num_students)]
        
        selected_students = pd.concat([selected_boys, selected_girls], ignore_index=True)
        selected_students['Age'] = selected_ages

        if num_students % 2 == 1:
            extra_student_gender = random.choice(['Male', 'Female'])
            extra_student_age = round(random.uniform(age_range[0], age_range[1]), 1)
            extra_student = pd.DataFrame({'Gender': [extra_student_gender], 'Age': [extra_student_age]})
            selected_students = pd.concat([selected_students, extra_student], ignore_index=True)

        return selected_students

    def display_selected_students(self):
        results_window = tk.Toplevel(self.root)
        results_window.title("Selected Students Results")

        self.create_results_label(results_window)
        self.create_total_students_text(results_window)
        self.create_results_text(results_window)
        self.create_save_buttons(results_window)

    def create_results_label(self, window):
        total_students_label = tk.Label(window, text=f"Selected Students: {len(self.selected_students)}")
        total_students_label.pack()
        tk.Label(window, text="Selected Students:").pack()
    
    def create_total_students_text(self, window):
        total_students_text = tk.Text(window, height=1, width=100)
        total_students_text.pack()
        total_students_text.config(state=tk.NORMAL)
        total_students_text.insert(tk.END, f"Total Students: {len(self.df)}")
        total_students_text.config(state=tk.DISABLED)

    def create_results_text(self, window):
        results_text = tk.Text(window, height=50, width=100)
        results_text.pack()
        results_text.config(state=tk.NORMAL)
    
        results_text.insert(tk.END, f"Details of {len(self.selected_students)} Students:\n\n ")
    
        results_text.insert(tk.END, self.selected_students.to_string(index=False))
        results_text.config(state=tk.DISABLED)

    def create_save_buttons(self, window):
        save_buttons = [
            ("Save as CSV", self.save_csv, ".csv"),
            ("Save as Excel", self.save_excel, ".xlsx")
        ]

        for button_text, command, default_extension in save_buttons:
            tk.Button(
                window, text=button_text, command=lambda c=command, e=default_extension: self.save_data(c, e)
            ).pack()

    def save_data(self, save_function, default_extension):
        if self.selected_students is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=[("Files", f"*{default_extension}")])
            if file_path:
                save_function(file_path)
                messagebox.showinfo("Save Complete", f"{default_extension} file saved successfully")

    def save_csv(self, file_path):
        self.selected_students.to_csv(file_path, index=False)

    def save_excel(self, file_path):
        self.selected_students.to_excel(file_path, index=False)

def main():
    root = ThemedTk(theme="clearlooks")
    app = SchoolAdmissionsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
