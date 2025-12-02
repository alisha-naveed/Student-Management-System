import tkinter as tk
from tkinter import messagebox
import pyodbc
#window Creation
window=tk.Tk()
window.title("Student Management System")
window.geometry("200x300")
#Database connectivity
conn=pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-9V1EK77\\SQLEXPRESS;'
    'Trusted_Connection=Yes;'
)
Cursor=conn.cursor()
#Table creation
Cursor.execute('''
IF OBJECT_ID('students','U')IS NULL
CREATE TABLE students(
    id INT IDENTITY(1,1)PRIMARY KEY,
    name NVARCHAR(50),
    age INT,
    grade NVARCHAR(10)
)
''')
conn.commit()
labelid=tk.Label(window,text="Student ID")
labelid.pack()
entryid=tk.Entry(window)
entryid.pack()
label=tk.Label(window,text="Name")
label.pack()
entry1=tk.Entry(window)
entry1.pack()
label2=tk.Label(window,text="Age")
label2.pack()
entry2=tk.Entry(window)
entry2.pack()
label3=tk.Label(window,text="Grade")
label3.pack()
entry3=tk.Entry(window)
entry3.pack()
#Adding students
def add_students():
    name = entry1.get()
    age = entry2.get()
    grade = entry3.get()

    Cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
                   (name, age, grade))
    conn.commit()

    messagebox.showinfo("Success", "Student added successfully!")

    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
#View student details
def view_students():
    Cursor.execute("SELECT * FROM students")
    rows = Cursor.fetchall()

    if not rows:
        messagebox.showinfo("View Students", "No students found")
        return

    text = ""
    for r in rows:
        text += f"ID: {r.id}, Name: {r.name}, Age: {r.age}, Grade: {r.grade}\n"

    messagebox.showinfo("All Students", text)
#Update students
def update_students():
    student_id = entryid.get()
    name = entry1.get()
    age = entry2.get()
    grade = entry3.get()

    if not student_id:
        messagebox.showwarning("Error", "Enter ID to update")
        return

    Cursor.execute("UPDATE students SET name=?, age=?, grade=? WHERE id=?",
                   (name, age, grade, student_id))
    conn.commit()

    messagebox.showinfo("Updated", "Student updated successfully!")
#Delete students
def delete_students():
    student_id = entryid.get()

    if not student_id:
        messagebox.showwarning("Error", "Enter ID to delete")
        return

    Cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()

    messagebox.showinfo("Deleted", "Student deleted successfully!")

btn_style = {
    "font": ("Arial", 12, "bold"),
    "width": 18,
    "height": 1,
    "bd": 0,
    "relief": "flat",
    "fg": "white",
    "activeforeground": "white",
    "cursor": "hand2",
    "pady": 5
}

add_button = tk.Button(window, text="Add Student", command=add_students,
                       bg="#A3E6A5", activebackground="#45A049", **btn_style)
add_button.pack(pady=5)

view_button = tk.Button(window, text="View Student", command=view_students,
                        bg="#6AB4F1", activebackground="#1E88E5", **btn_style)
view_button.pack(pady=5)

update_button = tk.Button(window, text="Update Student", command=update_students,
                          bg="#F1B253", activebackground="#FB8C00", **btn_style)
update_button.pack(pady=5)

delete_button = tk.Button(window, text="Delete Student", command=delete_students,
                          bg="#F35C51", activebackground="#E53935", **btn_style)
delete_button.pack(pady=5)
window.mainloop()
