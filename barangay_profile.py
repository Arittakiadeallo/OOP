from tkinter import *
import sqlite3
from tkinter import ttk

root = Tk()
root.title('Barangay Profile CRUD')
root.geometry("500x500")
root.configure(bg="lightblue")

# Connect to SQLite database
conn = sqlite3.connect('barangay_profile.db')
c = conn.cursor()

def submit():
    conn = sqlite3.connect('G:/aritta/akd/barangay_profile.db')
    c = conn.cursor()
    c.execute("INSERT INTO barangay_residents VALUES(:name,:age,:sex,:contact_number,:barangay,:committee,:role)",
            {
              'name': name.get(),
              'age': age.get(),
              'sex': sex.get(),
              'contact_number': contact_number.get(),
              'barangay': barangay.get(),
              'committee': committee_combobox.get(),
              'role': role_combobox.get(),
             })
    conn.commit()
    conn.close()

    # Clear input fields after submission
    name.delete(0, END)
    age.delete(0, END)
    sex.delete(0, END)
    contact_number.delete(0, END)
    barangay.delete(0, END)
    committee_combobox.set('')
    role_combobox.set('')

def query():
    conn = sqlite3.connect('G:/aritta/akd/barangay_profile.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM barangay_residents")
    records = c.fetchall()

    print_records = ''
    for record in records:
        print_records += f"{record[0]} {record[1]} {record[2]} {record[3]} {record[4]} {record[5]} {record[6]}\n"
    
    query_table=Label(root,text=print_records)
    query_table.grid(row=30,column=1,columnspan=3)

    conn.commit()
    conn.close()

    
def delete():
    conn = sqlite3.connect('G:/aritta/akd/barangay_profile.db')
    c = conn.cursor()
    
    record_id = delete_box.get()
    if record_id:
        c.execute("DELETE FROM barangay_residents WHERE oid = ?", (record_id,))
        conn.commit()
        conn.close()
    else:
        print("Please provide an ID.")

def update():
    conn = sqlite3.connect('G:/aritta/akd/barangay_profile.db')
    c = conn.cursor()    
    record_id = delete_box.get()

    c.execute("""UPDATE barangay_residents SET
        name = :name,
        age = :age,
        sex = :sex,
        contact_number = :contact_number,
        barangay = :barangay,
        committee = :committee,
        role = :role
        WHERE oid = :oid""",
        {
            'name': name_editor.get(),
            'age': age_editor.get(),
            'sex': sex_editor.get(),
            'contact_number': contact_number_editor.get(),
            'barangay': barangay_editor.get(),
            'committee': committee_combobox_editor.get(),
            'role': role_combobox_editor.get(),
            'oid': record_id
        })

    conn.commit()
    conn.close()

def edit():
    editor = Tk()
    editor.title('Update Resident Record')
    editor.geometry("1000x1000")

    conn = sqlite3.connect('G:/aritta/akd/barangay_profile.db')
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("SELECT * FROM barangay_residents WHERE oid = ?", (record_id,))
    records = c.fetchall()

    if records:
        global name_editor, age_editor, sex_editor, contact_number_editor, barangay_editor, committee_combobox_editor, role_combobox_editor

        name_editor = Entry(editor, width=30, bg="lightyellow")
        name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
        age_editor = Entry(editor, width=30, bg="lightyellow")
        age_editor.grid(row=1, column=1, padx=20)
        sex_editor = Entry(editor, width=30, bg="lightyellow")
        sex_editor.grid(row=2, column=1, padx=20)
        contact_number_editor = Entry(editor, width=30, bg="lightyellow")
        contact_number_editor.grid(row=3, column=1, padx=20)
        barangay_editor = Entry(editor, width=30, bg="lightyellow")
        barangay_editor.grid(row=4, column=1, padx=20)

        role_combobox_editor = ttk.Combobox(editor, width=30, values=["Barangay Captain", "Barangay Kagawad", "Barangay Secretary", "Barangay Treasurer", "SK Chairman", "Sk Secretary", "Sk Treasurer"], state="readonly")
        role_combobox_editor.grid(row=7, column=1, padx=20)
        committee_combobox_editor = ttk.Combobox(editor, width=30, values=["BARANGAY DEVELOPMENT COUNCIL (BDC)","APPROVAL OF BARANGAY DEVELOPMENT PLANS.", "BARANGAY PHYSICAL FITNESS AND SPORTS DEVELOPMENT COUNCIL.", "BARANGAY PEACE AND ORDER COMMITTEE.", "BARANGAY ECOLOGICAL SOLID WASTE MANAGEMENT COMMITTEE.", "LOCAL COUNCIL FOR THE PROTECTION OF CHILDREN.", "BARANGAY ANTI-DRUG ABUSE COUNCIL."], state="readonly")
        committee_combobox_editor.grid(row=6, column=1, padx=20)

        name_label = Label(editor, text="Name", bg="lightblue", fg="black")
        name_label.grid(row=0, column=0)
        age_label = Label(editor, text="Age", bg="lightblue", fg="black")
        age_label.grid(row=1, column=0)
        sex_label = Label(editor, text="sex", bg="lightblue", fg="black")
        sex_label.grid(row=2, column=0)
        contact_number_label = Label(editor, text="Contact No.", bg="lightblue", fg="black")
        contact_number_label.grid(row=3, column=0)
        barangay_label = Label(editor, text="Barangay", bg="lightblue", fg="black")
        barangay_label.grid(row=4, column=0)
        committee_label = Label(editor, text="committee", bg="lightblue", fg="black")
        committee_label.grid(row=6, column=0)
        role_label = Label(editor, text="Role", bg="lightblue", fg="black")
        role_label.grid(row=7, column=0)
        
        for record in records:
            name_editor.insert(0, record[0])
            age_editor.insert(0, record[1])
            sex_editor.insert(0, record[2])
            contact_number_editor.insert(0, record[3])
            barangay_editor.insert(0, record[4])
            committee_combobox_editor.insert(0, record[5])
            role_combobox_editor.set(record[6])

        save_btn = Button(editor, text="Save Record", command=update, bg="lightblue", fg="black")
        save_btn.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

    else:
        print("Record not found.")
    conn.commit()
    conn.close()

# Input fields for resident information
name = Entry(root, width=30, bg="lightyellow")
name.grid(row=0, column=1, padx=20)
age = Entry(root, width=30, bg="lightyellow")
age.grid(row=1, column=1, padx=20)
sex = Entry(root, width=30, bg="lightyellow")
sex.grid(row=2, column=1, padx=20)
contact_number = Entry(root, width=30, bg="lightyellow")
contact_number.grid(row=3, column=1, padx=20)
barangay = Entry(root, width=30, bg="lightyellow")
barangay.grid(row=4, column=1, padx=20)

# Dropdown for selecting role
role_combobox = ttk.Combobox(root, width=30, values=["Barangay Captain", "Barangay Kagawad", "Barangay Secretary", "Barangay Treasurer", "SK Chairman", "Sk Kagawad", "Sk Secretary", " Sk Treasurer"], state="readonly")
role_combobox.grid(row=7, column=1, padx=20)
committee_combobox = ttk.Combobox(root, width=30, values=["BARANGAY DEVELOPMENT COUNCIL (BDC)","APPROVAL OF BARANGAY DEVELOPMENT PLANS.", "BARANGAY PHYSICAL FITNESS AND SPORTS DEVELOPMENT COUNCIL.", "BARANGAY PEACE AND ORDER COMMITTEE.", "BARANGAY ECOLOGICAL SOLID WASTE MANAGEMENT COMMITTEE.", "LOCAL COUNCIL FOR THE PROTECTION OF CHILDREN.", "BARANGAY ANTI-DRUG ABUSE COUNCIL."], state="readonly")
committee_combobox.grid(row=6, column=1, padx=20)

# Labels for the input fields
name_label = Label(root, text="Name", bg="lightblue", fg="black")
name_label.grid(row=0, column=0)
age_label = Label(root, text="Age", bg="lightblue", fg="black")
age_label.grid(row=1, column=0)
sex_label = Label(root, text="sex", bg="lightblue", fg="black")
sex_label.grid(row=2, column=0)
contact_number_label = Label(root, text="Contact No.", bg="lightblue", fg="black")
contact_number_label.grid(row=3, column=0)
barangay_label = Label(root, text="Barangay", bg="lightblue", fg="black")
barangay_label.grid(row=4, column=0)
committee_label = Label(root, text="committee", bg="lightblue", fg="black")
committee_label.grid(row=6, column=0)
role_label = Label(root, text="Role", bg="lightblue", fg="black")
role_label.grid(row=7, column=0)

# Buttons for submit, edit, query, delete
submit_btn = Button(root, text="New", command=submit, bg="lightgreen", fg="black")
submit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

edit_btn = Button(root, text="Edit", command=edit, bg="lightgreen", fg="black")
edit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

query_btn = Button(root, text="View", command=query, bg="lightgreen", fg="black")
query_btn.grid(row=8, column=2, columnspan=2, pady=10, padx=10, ipadx=50)

delete_btn = Button(root, text="Remove", command=delete, bg="lightgreen", fg="black")
delete_btn.grid(row=9, column=2, columnspan=2, pady=10, padx=10, ipadx=50)

delete_box = Entry(root, width=30, bg="lightgreen")
delete_box.grid(row=10, column=1, padx=30)

delete_box_label = Label(root, text="Select ID No.", bg="lightblue", fg="black")
delete_box_label.grid(row=10, column=0)

# Query label to display records
query_label = Label(root, text="", bg="lightblue", fg="black")
query_label.grid(row=15, column=0, columnspan=4)

root.mainloop()
