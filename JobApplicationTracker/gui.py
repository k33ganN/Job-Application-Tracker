import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime
from db import init_db, add_application, list_applications, delete_application, update_application

app = tb.Window(themename="superhero")
app.title("Job Application Tracker")
app.geometry("900x500")

init_db()

# TABLE
columns = ("id", "company", "role", "status", "date")
tree = tb.Treeview(app, columns=columns, show="headings")
selected_id = None

tree.heading("id", text="ID")
tree.heading("company", text="Company")
tree.heading("role", text="Role")
tree.heading("status", text="Status")
tree.heading("date", text="Date Applied")

tree.column("id", width=60, anchor=CENTER)
tree.column("company", width=200, anchor=W)
tree.column("role", width=200, anchor=W)
tree.column("status", width=120, anchor=CENTER)
tree.column("date", width=120, anchor=CENTER)

tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

def refresh_table(status=None):
    tree.delete(*tree.get_children())
    for row in list_applications(status):
        tree.insert("", END, values=(row[0], row[1], row[2], row[4], row[3]))

refresh_table()

# FORM
form = tb.Frame(app)
form.pack(fill=X, padx=15, pady=10)

tb.Label(form, text="Company").grid(row=0, column=0, sticky=W, padx=5)
tb.Label(form, text="Role").grid(row=0, column=1, sticky=W, padx=5)
tb.Label(form, text="Status").grid(row=0, column=2, sticky=W, padx=5)

company_entry = tb.Entry(form, width=25)
role_entry = tb.Entry(form, width=25)
status_box = tb.Combobox(form, values=["applied", "interview", "rejected", "offer"], width=18)
status_box.set("applied")

company_entry.grid(row=1, column=0, padx=5, pady=5)
role_entry.grid(row=1, column=1, padx=5, pady=5)
status_box.grid(row=1, column=2, padx=5, pady=5)

def add_clicked():
    add_application(
        company_entry.get(),
        role_entry.get(),
        datetime.today().strftime("%Y-%m-%d"),
        status_box.get(),
        ""
    )
    refresh_table()
    company_entry.delete(0, END)
    role_entry.delete(0, END)

tb.Button(form, text="Add Application", command=add_clicked, bootstyle=SUCCESS)\
    .grid(row=1, column=3, padx=10)

#FILTER
def filter_status(event):
    val = filter_box.get()
    refresh_table(None if val == "all" else val)

filter_box = tb.Combobox(app, values=["all", "applied", "interview", "rejected", "offer"])
filter_box.set("all")
filter_box.pack(pady=5)
filter_box.bind("<<ComboboxSelected>>", filter_status)
tb.Label(app, text="Filter by Status:").pack()
filter_box.pack(pady=5)


#DELETE
def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select item", "Select an application first")
        return
    app_id = tree.item(selected[0])["values"][0]
    delete_application(app_id)
    refresh_table()

tb.Button(app, text="Delete Selected", bootstyle=DANGER, command=delete_selected).pack(pady=5)

def on_row_select(event):
    global selected_id
    selected = tree.selection()
    if not selected:
        return

    values = tree.item(selected[0])["values"]
    selected_id = values[0]

    company_entry.delete(0, END)
    company_entry.insert(0, values[1])

    role_entry.delete(0, END)
    role_entry.insert(0,values[2])

    status_box.set(values[3])

tree.bind("<<TreeviewSelect>>", on_row_select)

#UPDATE
def update_clicked():
    global selected_id
    if not selected_id:
        messagebox.showwarning("Selected", "Select an application first")
        return

    update_application(
        selected_id,
        company_entry.get(),
        role_entry.get(),
        status_box.get()        
    )

    refresh_table()
    selected_id = None

tb.Button(form, text="Update", bootstyle=WARNING, command=update_clicked)\
    .grid(row=1, column=4, padx=10)

app.mainloop()