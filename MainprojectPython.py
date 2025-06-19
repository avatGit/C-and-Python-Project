import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

FILE = "gestion_rooms.json"

def initialiser_rooms():
    if not os.path.exists(FILE):
        data = {
            "rooms": [{"numero": i+1, "occupant": None, "initial_condition": "clean"} for i in range(100)],
            "problemes": [],
            "reparations": []
        }
        with open(FILE, "w") as fichier:
            json.dump(data, fichier, indent=4)

def load_data():
    initialiser_rooms()
    if not os.path.exists(FILE):
        return {"rooms": [], "reparations": [], "problemes": []}
    
    with open(FILE, "r") as fichier:
        data = json.load(fichier)
        if "problemes" not in data:
            data["problemes"] = []
        if "reparations" not in data:
            data["reparations"] = []
        if "rooms" not in data:
            data["rooms"] = []
        return data

def save_data(data):
    with open(FILE, "w") as fichier:
        json.dump(data, fichier, indent=4)

class RoomManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Management")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.iconbitmap("room.ico")
        
        self.bg_color = "#b2d5f4"
        self.text_bg_color = "#d9ecff"
        
        self.style = ttkb.Style(theme='morph')
        self.style.configure('.', background=self.bg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color)
        
        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ici En-tête
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        header_label = ttk.Label(
            header_frame, 
            text="ROOM MANAGEMENT", 
            font=('Helvetica', 16, 'bold'),
            foreground='white',
            background='#343a40',
            anchor="center",
            padding=20
        )
        header_label.pack(fill=tk.X, expand=True)
        
        # Contenu de la frame
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Les principaux Boutons
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttkb.Button(
            btn_frame, 
            text="🔑 Assign a room", 
            command=self.assign_room, 
            bootstyle="primary",
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        ttkb.Button(
            btn_frame, 
            text="⚠ Report a problem", 
            command=self.report_probleme, 
            bootstyle="danger",
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        ttkb.Button(
            btn_frame, 
            text="🚪 Free up a room", 
            command=self.check_out, 
            bootstyle="success",
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        btn_frame2 = ttk.Frame(content_frame)
        btn_frame2.pack(fill=tk.X, pady=(0, 20))
        
        ttkb.Button(
            btn_frame2, 
            text="🔧 Show repairs", 
            command=self.show_repairs, 
            bootstyle="secondary",
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        ttkb.Button(
            btn_frame2, 
            text="👤 Show occupants", 
            command=self.show_occupants, 
            bootstyle="primary",
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        ttkb.Button(
            btn_frame2, 
            text="❌ Leave", 
            command=root.destroy, 
            bootstyle="danger",
            width=15
        ).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # la Zone de texte :
        text_frame = ttk.Frame(content_frame, relief=tk.SUNKEN, borderwidth=1)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_font = Font(family="Consolas", size=10)
        
        self.info_text = tk.Text(
            text_frame, 
            height=20, 
            wrap=tk.WORD, 
            font=text_font,
            bg="#f8f9fa",
            padx=10,
            pady=10
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        # En bas de la page
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        ttk.Label(
            footer_frame, 
            text="© 2025 Residence - All rights reserved", 
            foreground="#6c757d"
        ).pack(side=tk.RIGHT)
        
        # Initialiser les données
        self.data = load_data()
        
        # Message de bienvenue!!!!
        welcome_msg = "Welcome to the Room Management System\n\n"
        welcome_msg += "Use the buttons above to:\n"
        welcome_msg += "1. Assign a room to a guest\n"
        welcome_msg += "2. Report a problem in a room\n"
        welcome_msg += "3. Free up a room\n"
        welcome_msg += "4. View current repairs\n"
        welcome_msg += "5. See the list of occupants\n\n"
        welcome_msg += "Current status: system ready"
        
        self.update_info_text(welcome_msg)
        
    def update_info_text(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED)
        
    def assign_room(self):
        self.data = load_data()
        available = [c["numero"] for c in self.data["rooms"] if c["occupant"] is None]
        
        room_window = ttkb.Toplevel(self.root)
        room_window.title("Assign a Room")
        room_window.geometry("500x300")
        
        main_frame = ttk.Frame(room_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            main_frame, 
            text=f"Available rooms: {', '.join(map(str, available[:20]))}",
            font=('Helvetica', 10, 'bold')
        ).pack(pady=(10, 5))
        
        if len(available) > 20:
            ttk.Label(
                main_frame, 
                text=f"... ({len(available)-20} more rooms available)",
                foreground="#6c757d"
            ).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Room number:").pack(pady=5)
        
        room_entry = ttk.Entry(main_frame, font=('Helvetica', 12))
        room_entry.pack(pady=5, ipady=5)
        
        def on_assign():
            try:
                numero = int(room_entry.get())
                if numero < 1 or numero > 100:
                    messagebox.showerror("Error", "Invalid room number. Must be between 1 and 100.")
                    return
                
                room = self.data["rooms"][numero-1]
                if room["occupant"] is not None:
                    messagebox.showerror("Error", "This room is already occupied.")
                    return
                
                client_window = ttkb.Toplevel(room_window)
                client_window.title("Customer Details")
                client_window.geometry("400x400")
                
                client_frame = ttk.Frame(client_window)
                client_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                ttk.Label(client_frame, text="Last name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
                last_name_entry = ttk.Entry(client_frame, font=('Helvetica', 12))
                last_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
                
                ttk.Label(client_frame, text="First name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
                first_name_entry = ttk.Entry(client_frame, font=('Helvetica', 12))
                first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
                
                ttk.Label(client_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
                phone_entry = ttk.Entry(client_frame, font=('Helvetica', 12))
                phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
                
                ttk.Label(client_frame, text="Room condition:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
                condition_entry = ttk.Entry(client_frame, font=('Helvetica', 12))
                condition_entry.insert(0, "clean")
                condition_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
                
                def on_client_submit():
                    last_name = last_name_entry.get()
                    first_name = first_name_entry.get()
                    phone = phone_entry.get()
                    initial_condition = condition_entry.get()
                    
                    if not last_name or not first_name:
                        messagebox.showerror("Error", "First and last name are required.")
                        return
                    
                    room["occupant"] = {
                        "last_name": last_name,
                        "first_name": first_name,
                        "phone": phone
                    }
                    room["initial_condition"] = initial_condition
                    
                    save_data(self.data)
                    messagebox.showinfo("Success", f"Room {numero} assigned to {first_name} {last_name}.")
                    client_window.destroy()
                    room_window.destroy()
                    self.show_occupants()
                
                submit_btn = ttkb.Button(
                    client_frame, 
                    text="Confirm Assignment", 
                    command=on_client_submit,
                    bootstyle="success"
                )
                submit_btn.grid(row=4, column=0, columnspan=2, pady=20, sticky=tk.EW)
                
                client_frame.columnconfigure(1, weight=1)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
        
        assign_btn = ttkb.Button(
            main_frame, 
            text="Next →", 
            command=on_assign,
            bootstyle="primary"
        )
        assign_btn.pack(pady=20, ipady=5)
        
        main_frame.columnconfigure(0, weight=1)

    def report_probleme(self):
        self.data = load_data()
        
        room_window = ttkb.Toplevel(self.root)
        room_window.title("Report Problem")
        room_window.geometry("500x300")
        
        main_frame = ttk.Frame(room_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            main_frame, 
            text="Room Number:", 
            font=('Helvetica', 10)
        ).pack(pady=5)
        
        room_entry = ttk.Entry(main_frame, font=('Helvetica', 12))
        room_entry.pack(pady=5, ipady=5)
        
        def on_report():
            try:
                num = int(room_entry.get())
                if num < 1 or num > 100:
                    messagebox.showerror("Error", "Invalid room number. Must be between 1 and 100.")
                    return
                
                room = self.data["rooms"][num-1]
                if room["occupant"] is None:
                    messagebox.showerror("Error", "This room is not occupied.")
                    return
                
                problem_window = ttkb.Toplevel(room_window)
                problem_window.title("Problem Description")
                problem_window.geometry("500x300")
                
                problem_frame = ttk.Frame(problem_window)
                problem_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                ttk.Label(
                    problem_frame, 
                    text="Describe the problem:", 
                    font=('Helvetica', 10)
                ).pack(pady=5)
                
                problem_entry = ttk.Entry(problem_frame, font=('Helvetica', 12), width=40)
                problem_entry.pack(pady=5, ipady=5)
                
                def on_problem_submit():
                    probleme_type = problem_entry.get()
                    if not probleme_type:
                        messagebox.showerror("Error", "Please describe the problem.")
                        return
                    
                    self.data["problemes"].append({
                        "room_number": num,
                        "description": probleme_type,
                        "status": "reported"
                    })
                    save_data(self.data)
                    messagebox.showinfo("Success", f"Problem reported for room {num}.")
                    problem_window.destroy()
                    room_window.destroy()
                    self.show_repairs()
                
                submit_btn = ttkb.Button(
                    problem_frame, 
                    text="Submit Report", 
                    command=on_problem_submit,
                    bootstyle="danger"
                )
                submit_btn.pack(pady=20, ipady=5)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
        
        report_btn = ttkb.Button(
            main_frame, 
            text="Next →", 
            command=on_report,
            bootstyle="primary"
        )
        report_btn.pack(pady=20, ipady=5)

    def check_out(self):
        self.data = load_data()
        
        room_window = ttkb.Toplevel(self.root)
        room_window.title("Check Out")
        room_window.geometry("500x400")
        
        main_frame = ttk.Frame(room_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            main_frame, 
            text="Room number:", 
            font=('Helvetica', 10)
        ).pack(pady=5)
        
        room_entry = ttk.Entry(main_frame, font=('Helvetica', 12))
        room_entry.pack(pady=5, ipady=5)
        
        def on_check_out():
            try:
                room_numb = int(room_entry.get())
                if room_numb < 1 or room_numb > 100:
                    messagebox.showerror("Error", "Invalid room number. Must be between 1 and 100.")
                    return
                
                room = self.data["rooms"][room_numb-1]
                if room["occupant"] is None:
                    messagebox.showerror("Error", "This room is not occupied.")
                    return
                
                room_problems = [p for p in self.data["problemes"] if p["room_number"] == room_numb and p["status"] != "resolved"]
                final_condition = ""
                
                if room_problems:
                    problem_list = "\n".join([f"- {p['description']} (status: {p['status']})" for p in room_problems])
                    response = messagebox.askyesno(
                        "Warning", 
                        f"!!! Problems detected in this room !!!\n\n{problem_list}\n\nDo you want to proceed with checkout?"
                    )
                    if not response:
                        messagebox.showinfo("Info", "Checkout canceled.")
                        room_window.destroy()
                        return
                    
                    final_condition = room_problems[0]['description']
                    messagebox.showinfo("Info", f"Problem '{final_condition}' will be recorded as exit condition")
                else:
                    final_condition = simpledialog.askstring("Room Condition", "Room condition at checkout:")
                    if final_condition is None:
                        room_window.destroy()
                        return
                
                initial_condition = room.get("initial_condition", "").strip().lower()
                final_condition = final_condition.strip().lower()
                
                if initial_condition != final_condition:
                    description = f"Problem: {final_condition}" if room_problems else f"Condition changed: '{initial_condition}' to '{final_condition}'"
                    responsible = room["occupant"]
                    self.data["reparations"].append({
                        "room": room_numb,
                        "description": description,
                        "status": "pending",
                        "responsible": responsible
                    })
                    messagebox.showinfo(
                        "Repair Required", 
                        f"Repair required. Customer {responsible['first_name']} {responsible['last_name']} may be responsible."
                    )
                
                for p in self.data["problemes"]:
                    if p["room_number"] == room_numb:
                        p["status"] = "resolved"
                
                room["occupant"] = None
                save_data(self.data)
                messagebox.showinfo("Success", f"Room {room_numb} successfully checked out.")
                room_window.destroy()
                self.show_occupants()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
        
        checkout_btn = ttkb.Button(
            main_frame, 
            text="Check Out", 
            command=on_check_out,
            bootstyle="success"
        )
        checkout_btn.pack(pady=20, ipady=5)

    def show_repairs(self):
        self.data = load_data()
        reparations = self.data.get("reparations", [])
        
        if not reparations:
            self.update_info_text("No repairs reported.")
            return
        
        info_text = "List of current repairs:\n\n"
        for rep in reparations:
            info_text += f"- Room {rep['room']}: {rep['description']}\n"
            if "responsible" in rep:
                r = rep["responsible"]
                info_text += f"   Customer: {r['first_name']} {r['last_name']} ({r['phone']})\n"
            info_text += f"   Status: {rep['status']}\n\n"
        
        self.update_info_text(info_text)
        
        def remove_repair():
            room_num = simpledialog.askinteger("Remove Repair", "Enter room number to remove from repairs:")
            if room_num is not None:
                self.data["reparations"] = [r for r in self.data["reparations"] if r["room"] != room_num]
                
                for p in self.data["problemes"]:
                    if p["room_number"] == room_num:
                        p["status"] = "resolved"
                
                save_data(self.data)
                messagebox.showinfo("Success", f"Room {room_num} removed from repair list.")
                self.show_repairs()
        
        ttkb.Button(
            self.main_frame, 
            text="Remove Repair", 
            command=remove_repair,
            bootstyle="danger"
        ).pack(pady=5)

    def show_occupants(self):
        self.data = load_data()
        info_text = "List of current occupants:\n\n"
        info_text += "Room  | Name\n"
        info_text += "------|-----------------\n"
        
        occupied = 0
        for c in self.data["rooms"]:
            if c["occupant"] is not None:
                info_text += f"{c['numero']:5} | {c['occupant']['first_name']} {c['occupant']['last_name']}\n"
                occupied += 1
        
        info_text += f"\nTotal: {occupied} occupied rooms out of 100"
        self.update_info_text(info_text)

if __name__ == "__main__":
    root = ttkb.Window(themename="morph")
    app = RoomManagementApp(root)
    root.mainloop()