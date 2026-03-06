# ============================================================
# SIMPLE COMPLAINT REGISTRATION SYSTEM
# Python + Tkinter GUI + MySQL
# Clean, simple, and easy to understand
# ============================================================

import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk


# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RAHUL123",
        database="complaint_system"
    )


# ------------------------------------------------------------
# LOGIN WINDOW
# ------------------------------------------------------------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Complaint System - Login")
        self.root.geometry("420x350")
        self.root.configure(bg="#EAF0F1")

        title = Label(root, text="Login", font=("Arial", 22, "bold"), bg="#EAF0F1")
        title.pack(pady=20)

        frame = Frame(root, bg="#EAF0F1")
        frame.pack()

        Label(frame, text="Email:", bg="#EAF0F1", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.email = Entry(frame, width=30)
        self.email.grid(row=0, column=1, pady=5)

        Label(frame, text="Password:", bg="#EAF0F1", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.password = Entry(frame, width=30, show="*")
        self.password.grid(row=1, column=1, pady=5)

        Button(root, text="Login", width=20, bg="#3498DB", fg="white",
               command=self.login).pack(pady=15)

        Button(root, text="Register", width=20, bg="#2ECC71", fg="white",
               command=self.open_register).pack()

    def login(self):
        email = self.email.get()
        pwd = self.password.get()

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT user_id, role, password_hash FROM users WHERE email=%s", (email,))
            data = cur.fetchone()

            if data:
                user_id, role, real_pwd = data

                if pwd == real_pwd:
                    messagebox.showinfo("Login", "Login Successful!")

                    self.root.destroy()

                    if role == "admin":
                        r = Tk()
                        AdminWindow(r)
                        r.mainloop()
                    else:
                        r = Tk()
                        UserWindow(r, user_id)
                        r.mainloop()
                else:
                    messagebox.showerror("Error", "Incorrect Password!")
            else:
                messagebox.showerror("Error", "User not found!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_register(self):
        RegisterWindow()


# ------------------------------------------------------------
# REGISTER WINDOW
# ------------------------------------------------------------
class RegisterWindow:
    def __init__(self):
        self.root = Toplevel()
        self.root.title("Register")
        self.root.geometry("420x450")
        self.root.configure(bg="#FDFEFE")

        Label(self.root, text="Register", font=("Arial", 22, "bold"), bg="#FDFEFE").pack(pady=20)

        frame = Frame(self.root, bg="#FDFEFE")
        frame.pack()

        Label(frame, text="Full Name:", bg="#FDFEFE").grid(row=0, column=0, sticky="w")
        self.name = Entry(frame, width=30)
        self.name.grid(row=0, column=1, pady=5)

        Label(frame, text="Email:", bg="#FDFEFE").grid(row=1, column=0, sticky="w")
        self.email = Entry(frame, width=30)
        self.email.grid(row=1, column=1, pady=5)

        Label(frame, text="Phone:", bg="#FDFEFE").grid(row=2, column=0, sticky="w")
        self.phone = Entry(frame, width=30)
        self.phone.grid(row=2, column=1, pady=5)

        Label(frame, text="Password:", bg="#FDFEFE").grid(row=3, column=0, sticky="w")
        self.password = Entry(frame, width=30, show="*")
        self.password.grid(row=3, column=1, pady=5)

        Button(self.root, text="Register", bg="#2ECC71", fg="white", width=20,
               command=self.register).pack(pady=20)

    def register(self):
        name = self.name.get()
        email = self.email.get()
        phone = self.phone.get()
        password = self.password.get()

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO users (full_name, email, phone, password_hash, role)
                VALUES (%s, %s, %s, %s, 'citizen')
            """, (name, email, phone, password))

            conn.commit()

            messagebox.showinfo("Success", "Registered Successfully!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ------------------------------------------------------------
# USER WINDOW (FILE COMPLAINT)
# ------------------------------------------------------------
class UserWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

        self.root.title("File a Complaint")
        self.root.geometry("550x450")
        self.root.configure(bg="#EBF5FB")

        Label(root, text="Register Complaint", font=("Arial", 18, "bold"),
              bg="#EBF5FB").pack(pady=15)

        frame = Frame(root, bg="#EBF5FB")
        frame.pack()

        Label(frame, text="Title:", bg="#EBF5FB").grid(row=0, column=0, sticky="w")
        self.title = Entry(frame, width=40)
        self.title.grid(row=0, column=1, pady=5)

        Label(frame, text="Category:", bg="#EBF5FB").grid(row=1, column=0, sticky="w")
        self.cat_box = ttk.Combobox(frame, width=38)
        self.cat_box.grid(row=1, column=1, pady=5)
        self.load_categories()

        Label(frame, text="Description:", bg="#EBF5FB").grid(row=2, column=0, sticky="nw")
        self.desc = Text(frame, width=30, height=6)
        self.desc.grid(row=2, column=1, pady=5)

        Button(root, text="Submit Complaint", bg="#3498DB", fg="white",
               command=self.submit).pack(pady=20)

    def load_categories(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT name FROM categories")
            data = cur.fetchall()

            self.cat_box['values'] = [x[0] for x in data]
        except:
            pass

    def submit(self):
        title = self.title.get()
        category = self.cat_box.get()
        description = self.desc.get("1.0", END)

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT category_id FROM categories WHERE name=%s", (category,))
            cat_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO complaints (user_id, category_id, title, description, status)
                VALUES (%s, %s, %s, %s, 'Pending')
            """, (self.user_id, cat_id, title, description))

            conn.commit()

            messagebox.showinfo("Success", "Complaint Submitted!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ------------------------------------------------------------
# ADMIN WINDOW (VIEW + UPDATE)
# ------------------------------------------------------------
class AdminWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("700x450")

        Label(root, text="Admin Dashboard", font=("Arial", 20, "bold")).pack(pady=15)

        self.table = ttk.Treeview(root, columns=("ID", "Title", "Status"), height=12)
        self.table.pack()

        for col in ("ID", "Title", "Status"):
            self.table.heading(col, text=col)

        Button(root, text="Refresh", command=self.load).pack(pady=10)
        Button(root, text="Update Status", command=self.update_status).pack()

        self.load()

    def load(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT complaint_id, title, status FROM complaints")
        data = cur.fetchall()

        for d in data:
            self.table.insert("", END, values=d)

    def update_status(self):
        select = self.table.focus()
        if not select:
            messagebox.showwarning("Warning", "Select a complaint!")
            return

        cid = self.table.item(select)['values'][0]

        UpdateStatusWindow(cid)


# ------------------------------------------------------------
# UPDATE STATUS POPUP
# ------------------------------------------------------------
class UpdateStatusWindow:
    def __init__(self, cid):
        self.cid = cid

        self.root = Toplevel()
        self.root.title("Update Complaint Status")
        self.root.geometry("300x200")

        Label(self.root, text="New Status:").pack(pady=10)

        self.box = ttk.Combobox(self.root, values=["Pending", "In Progress", "Resolved", "Rejected"])
        self.box.pack(pady=5)

        Button(self.root, text="Save", command=self.save).pack(pady=10)

    def save(self):
        status = self.box.get()

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE complaints SET status=%s WHERE complaint_id=%s", (status, self.cid))
            conn.commit()
            messagebox.showinfo("Success", "Status Updated!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ------------------------------------------------------------
# START PROGRAM
# ------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    LoginWindow(root)
    root.mainloop()
