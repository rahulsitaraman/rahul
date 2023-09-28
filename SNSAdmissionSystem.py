import tkinter as tk
from tkinter import filedialog, messagebox
import random
import pandas as pd
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path


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
        self.root.title("Shiv Nadar School - Student Selection Form")
        self.root.geometry("925x500+300+200")
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        pathToSchoolBackgroudImage = (
            Path(__file__).resolve().with_name("noida-school.jpg")
        )

        self.image_manager = ImageManager()
        self.background_image = self.image_manager.create_image(
            pathToSchoolBackgroudImage
        )
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relx=0.6, rely=1, anchor="s")

        self.num_students_var = tk.StringVar()
        self.minAge_var = tk.StringVar(value="3")
        self.maxAge_var = tk.StringVar(value="4.5")

        self.create_widgets()

    def display_total_students(self):
        total_students_window = tk.Toplevel(self.root)
        total_students_window.title("Total Students Count")

        total_students_label = tk.Label(
            total_students_window, text=f"Total Students: {len(self.df)}"
        )
        total_students_label.pack()

    def create_widgets(self):
        # self.apply_washout_effect()

        inputs_frame = tk.Frame(self.root, bg="white")
        inputs_frame.place(relx=0.55, rely=0.1, height=400, width=400)

        tk.Label(
            inputs_frame,
            text="Student Selection Form",
            fg="#57a1f8",
            bg="white",
            font=("Microsoft YaHei UI Light", 15, "bold"),
        ).grid(column=0, row=0, padx=10, pady=5, sticky="w")

        ## 1st input
        # num_students_var_label
        tk.Label(
            inputs_frame,
            text="Enter number of students to select:",
            fg="black",
            bg="white",
            font=("Microsoft YaHei UI Light", 9),
        ).grid(column=0, row=1, padx=10, pady=5, sticky="w")
        # num_students_var
        num_students_var = tk.Entry(
            inputs_frame,
            textvariable=self.num_students_var,
            width=10,
            fg="black",
            border=1,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
        )
        num_students_var.grid(column=1, row=1, padx=10, pady=5, sticky="w")

        ## 2nd input
        age_range_entry_label = tk.Label(
            inputs_frame,
            text="Enter minimum age:",
            fg="black",
            bg="white",
            font=("Microsoft YaHei UI Light", 9),
        )
        age_range_entry_label.grid(column=0, row=2, padx=10, pady=5, sticky="w")
        # num_students_entry
        age_range_entry = tk.Entry(
            inputs_frame,
            textvariable=self.minAge_var,
            width=10,
            fg="black",
            border=1,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
        )
        age_range_entry.grid(column=1, row=2, padx=10, pady=5, sticky="w")

        ## 3rd input
        tk.Label(
            inputs_frame,
            text="Enter maximum age:",
            fg="black",
            bg="white",
            font=("Microsoft YaHei UI Light", 9),
        ).grid(column=0, row=3, padx=10, pady=5, sticky="w")
        # maxAge_entry
        maxAge_entry = tk.Entry(
            inputs_frame,
            textvariable=self.maxAge_var,
            width=10,
            fg="black",
            border=1,
            bg="white",
            font=("Microsoft YaHei UI Light", 11),
        ).grid(column=1, row=3, padx=10, pady=5, sticky="w")

        # button 1
        btn1 = tk.Button(
            inputs_frame,
            text="Set Inputs",
            command=self.set_inputs,
            width=20,
            pady=7,
            bg="#57a1f8",
            fg="white",
            border=0,
        )
        btn1.grid(column=0, row=4, padx=5, pady=5, sticky="w")

        # button 2
        btn2 = tk.Button(
            inputs_frame,
            text="Load Excel File",
            command=self.load_excel_file,
            width=20,
            pady=7,
            bg="#57a1f8",
            fg="white",
            border=0,
        )
        btn2.grid(column=0, row=5, padx=5, pady=5, sticky="w")

        # button 3
        btn3 = tk.Button(
            inputs_frame,
            text="Select Students",
            command=self.select_students,
            width=20,
            pady=7,
            bg="#57a1f8",
            fg="white",
            border=0,
        )
        btn3.grid(column=0, row=6, padx=5, pady=5, sticky="w")

        # button 4
        btn4 = tk.Button(
            inputs_frame,
            text="Display Total Students",
            command=self.display_total_students,
            width=20,
            pady=7,
            bg="#57a1f8",
            fg="white",
            border=0,
        )
        btn4.grid(column=0, row=7, padx=5, pady=5, sticky="w")

    def set_inputs(self):
        # Validation 1
        try:
            num_students = int(self.num_students_var.get())
            min_age = float(self.minAge_var.get())
            max_age = float(self.maxAge_var.get())

            if num_students <= 0:
                messagebox.showerror("Error", "Please enter valid number of students")
            elif min_age <= 0:
                messagebox.showerror("Error", "Please enter valid minimum age")
            elif max_age <= 0:
                messagebox.showerror("Error", "Please enter valid maximum age")
            elif min_age > min_age:
                messagebox.showerror(
                    "Error", "Minimum age value cannot be greater than maximim age"
                )
            else:
                messagebox.showinfo("Inputs Set", "Inputs have been set successfully")
        except ValueError as err:
            messagebox.showerror("Error", "Some error ocurred")

    def load_excel_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                messagebox.showinfo(
                    "Excel File Loaded", "Excel file loaded successfully"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while loading the file:\n{str(e)}"
                )

    def select_students(self):
        if not (
            self.num_students_var.get()
            and self.minAge_var.get()
            and self.maxAge_var.get()
            and hasattr(self, "df")
        ):
            messagebox.showerror(
                "Error", "Please set the inputs and load the Excel file"
            )
            return

        try:
            num_students = int(self.num_students_var.get())
            min_age = float(self.minAge_var.get())
            max_age = float(self.maxAge_var.get())
            self.selected_students = self.process_data(
                self.df, num_students, (min_age, max_age)
            )
            self.display_selected_students()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def process_data(self, dataframe, num_students, age_range):
        boys = dataframe[dataframe["Gender"] == "Male"]
        girls = dataframe[dataframe["Gender"] == "Female"]

        boys_count = num_students // 2
        girls_count = num_students - boys_count

        selected_boys = boys.sample(
            min(boys_count, len(boys)), replace=False
        ).reset_index(drop=True)
        selected_girls = girls.sample(
            min(girls_count, len(girls)), replace=False
        ).reset_index(drop=True)

        selected_ages = [
            round(random.uniform(age_range[0], age_range[1]), 1)
            for _ in range(num_students)
        ]

        selected_students = pd.concat(
            [selected_boys, selected_girls], ignore_index=True
        )
        selected_students["Age"] = selected_ages

        if num_students % 2 == 1:
            extra_student_gender = random.choice(["Male", "Female"])
            extra_student_age = round(random.uniform(age_range[0], age_range[1]), 1)
            extra_student = pd.DataFrame(
                {"Gender": [extra_student_gender], "Age": [extra_student_age]}
            )
            selected_students = pd.concat(
                [selected_students, extra_student], ignore_index=True
            )

        return selected_students

    def display_selected_students(self):
        results_window = tk.Toplevel(self.root)
        results_window.title("Selected Students Results")

        self.create_results_label(results_window)
        self.create_total_students_text(results_window)
        self.create_results_text(results_window)
        self.create_save_buttons(results_window)

    def create_results_label(self, window):
        total_students_label = tk.Label(
            window, text=f"Selected Students: {len(self.selected_students)}"
        )
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

        results_text.insert(
            tk.END, f"Details of {len(self.selected_students)} Students:\n\n "
        )

        results_text.insert(tk.END, self.selected_students.to_string(index=False))
        results_text.config(state=tk.DISABLED)

    def create_save_buttons(self, window):
        save_buttons = [
            ("Save as CSV", self.save_csv, ".csv"),
            ("Save as Excel", self.save_excel, ".xlsx"),
        ]

        for button_text, command, default_extension in save_buttons:
            tk.Button(
                window,
                text=button_text,
                command=lambda c=command, e=default_extension: self.save_data(c, e),
            ).pack()

    def save_data(self, save_function, default_extension):
        if self.selected_students is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=default_extension,
                filetypes=[("Files", f"*{default_extension}")],
            )
            if file_path:
                save_function(file_path)
                messagebox.showinfo(
                    "Save Complete", f"{default_extension} file saved successfully"
                )

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
