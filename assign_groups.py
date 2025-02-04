import tkinter as tk
import random
import pandas as pd  # Import pandas for reading Excel files

# Define groups with colors (background, text color)
groups = [
    ("Greenspace", "#90EE90", "black"),  # Light Green
    ("Raspberry Pi", "#C7053D", "white"),  # Raspberry Pi Red
    ("Food Waste", "#FFFACD", "black"),  # Light Yellow
    ("Carbon", "#2C2C2C", "white")  # Charcoal Gray
]

# Placeholder for students (you'll add students later)
students = []

# Function to load student names from an Excel file
def load_students_from_excel(file_path):
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        if "Name" in df.columns:
            students.extend(df["Name"].dropna().tolist())
        else:
            print("Error: Excel sheet does not contain a 'Name' column.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")

# Function to manually add students
def add_students_manually():
    global students
    students = [
        "Student 1", "Student 2", "Student 3", "Student 4", "Student 5",  # Add student names here
        # Add more students as needed
    ]

# Define the method to choose the student source
def choose_student_source(source="manual"):
    if source == "excel":
        load_students_from_excel("students.xlsx")  # Specify the path to your Excel file
    else:
        add_students_manually()  # Manually add the students

# Create main window
window = tk.Tk()
window.title("Group Assignment")
window.geometry("900x400")

# Assign Students Button
assign_button = tk.Button(window, text="Assign Students to Groups", font=("Helvetica", 14))
assign_button.pack(pady=10)

# Frame to hold groups
grid_frame = tk.Frame(window)
grid_frame.pack()

# Store group labels
group_frames = {}

# Function to display all groups first
def show_groups():
    # Create a label for each group
    for i, (group_name, group_color, text_color) in enumerate(groups):
        # Create a frame for each group
        group_frame = tk.Frame(grid_frame, bg=group_color, padx=10, pady=10, width=200, height=150)
        group_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        # Group name label
        group_label = tk.Label(group_frame, text=group_name, font=("Helvetica", 16, "bold"), 
                               bg=group_color, fg=text_color)
        group_label.pack()

        # Create label for student names
        member_label = tk.Label(group_frame, text="", font=("Helvetica", 12), bg=group_color, fg=text_color, justify="left")
        member_label.pack()

        # Store group label for updating later
        group_frames[group_name] = member_label

    # After showing groups, start assigning students
    window.after(500, assign_students)

# Track assigned student index and group index
current_student_index = 0
current_group_index = 0

# Function to assign students one by one to groups
def assign_students():
    global current_student_index, current_group_index

    if current_group_index >= len(groups):
        return  # Stop when all groups are processed

    group_name = groups[current_group_index][0]
    member_label = group_frames[group_name]
    
    if current_student_index < len(students):
        # Assign a student to the current group
        student = students[current_student_index]
        current_student_index += 1
        member_label.config(text=member_label.cget("text") + student + "\n")
        window.after(500, assign_students)  # Delay to assign the next student
    else:
        # If all students are assigned to the current group, move to the next group
        current_group_index += 1
        current_student_index = 0  # Reset student index for the next group
        window.after(500, assign_students)  # Proceed with the next group

# Button action: Show groups first, then assign students
assign_button.config(command=lambda: [assign_button.config(state=tk.DISABLED), show_groups()])

# You can set the student source here
choose_student_source("manual")  # Change to "excel" to load from an Excel file

# Run GUI
window.mainloop()
