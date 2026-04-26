import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

# =====================================================
# CONFIG
# =====================================================

API_BASE_URL = "http://localhost:5000"  # Endre til https://ak2gruppe4.onrender.com for production

# =====================================================
# MAIN WINDOW
# =====================================================

class VarehusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Varehus Lager & Ordre System")
        self.root.geometry("1200x700")
        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Navbar
        self.create_navbar()
        
        # Main content area
        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Start with varelager tab
        self.show_varelager()
    
    def create_navbar(self):
        """Opprett navigasjonsmeny"""
        navbar = ttk.Frame(self.root)
        navbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(navbar, text="📦 Varelager", command=self.show_varelager).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="📋 Ordrer", command=self.show_ordrer).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="👥 Kunder", command=self.show_kunder).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="🏥 API Status", command=self.show_status).pack(side=tk.LEFT, padx=5)
    
    def clear_content(self):
        """Tøm content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # =====================================================
    # TAB: VARELAGER
    # =====================================================
    
    def show_varelager(self):
        """Vise varelager liste"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="📦 Varelager Oversikt", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Knapper
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Oppdater", command=self.update_varelager).pack(side=tk.LEFT, padx=5)
        
        # Tabel
        self.varelager_tree = ttk.Treeview(
            self.content_frame,
            columns=("VNr", "Betegnelse", "Antall", "Pris"),
            height=25
        )
        self.varelager_tree.column("#0", width=0, stretch=tk.NO)
        self.varelager_tree.column("VNr", anchor=tk.W, width=60)
        self.varelager_tree.column("Betegnelse", anchor=tk.W, width=300)
        self.varelager_tree.column("Antall", anchor=tk.CENTER, width=80)
        self.varelager_tree.column("Pris", anchor=tk.E, width=100)
        
        self.varelager_tree.heading("#0", text="", anchor=tk.W)
        self.varelager_tree.heading("VNr", text="Vare Nr", anchor=tk.W)
        self.varelager_tree.heading("Betegnelse", text="Navn", anchor=tk.W)
        self.varelager_tree.heading("Antall", text="Antall", anchor=tk.CENTER)
        self.varelager_tree.heading("Pris", text="Pris (kr)", anchor=tk.E)
        
        self.varelager_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scroll bar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.varelager_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.varelager_tree.config(yscroll=scrollbar.set)
        
        # Last data
        self.update_varelager()
    
    def update_varelager(self):
        """Hent varelager fra API"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/varelager", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                messagebox.showerror("API Error", data.get("message", "Ukjent feil"))
                return
            
            # Tøm tabel
            for item in self.varelager_tree.get_children():
                self.varelager_tree.delete(item)
            
            # Fyll med data
            for vare in data.get("items", []):
                self.varelager_tree.insert(
                    "",
                    tk.END,
                    values=(
                        vare["VNr"],
                        vare["Betegnelse"],
                        vare["Antall"],
                        f"{vare['Pris']:.2f}"
                    )
                )
            
            messagebox.showinfo("Suksess", f"Lastet {len(data.get('items', []))} varer")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Tilkoblingsfeil", f"Kan ikke koble til API: {str(e)}")
    
    # =====================================================
    # TAB: ORDRER
    # =====================================================
    
    def show_ordrer(self):
        """Vise ordrer liste"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="📋 Ordrer", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Knapper
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Oppdater", command=self.update_ordrer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Se detaljer", command=self.show_ordrer_detaljer).pack(side=tk.LEFT, padx=5)
        
        # Tabel
        self.ordrer_tree = ttk.Treeview(
            self.content_frame,
            columns=("OrdreNr", "OrdreDato", "SendtDato", "BetaltDato", "KNr"),
            height=25
        )
        self.ordrer_tree.column("#0", width=0, stretch=tk.NO)
        self.ordrer_tree.column("OrdreNr", anchor=tk.W, width=80)
        self.ordrer_tree.column("OrdreDato", anchor=tk.CENTER, width=120)
        self.ordrer_tree.column("SendtDato", anchor=tk.CENTER, width=120)
        self.ordrer_tree.column("BetaltDato", anchor=tk.CENTER, width=120)
        self.ordrer_tree.column("KNr", anchor=tk.CENTER, width=60)
        
        self.ordrer_tree.heading("OrdreNr", text="Ordre Nr", anchor=tk.W)
        self.ordrer_tree.heading("OrdreDato", text="Ordre Dato", anchor=tk.CENTER)
        self.ordrer_tree.heading("SendtDato", text="Sendt Dato", anchor=tk.CENTER)
        self.ordrer_tree.heading("BetaltDato", text="Betalt Dato", anchor=tk.CENTER)
        self.ordrer_tree.heading("KNr", text="Kunde Nr", anchor=tk.CENTER)
        
        self.ordrer_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.ordrer_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ordrer_tree.config(yscroll=scrollbar.set)
        
        # Last data
        self.update_ordrer()
    
    def update_ordrer(self):
        """Hent ordrer fra API"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/ordrer", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                messagebox.showerror("API Error", data.get("message", "Ukjent feil"))
                return
            
            # Tøm tabel
            for item in self.ordrer_tree.get_children():
                self.ordrer_tree.delete(item)
            
            # Fyll med data
            for ordre in data.get("items", []):
                self.ordrer_tree.insert(
                    "",
                    tk.END,
                    values=(
                        ordre["OrdreNr"],
                        ordre["OrdreDato"],
                        ordre["SendtDato"],
                        ordre["BetaltDato"],
                        ordre["KNr"]
                    )
                )
            
            messagebox.showinfo("Suksess", f"Lastet {len(data.get('items', []))} ordrer")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Tilkoblingsfeil", f"Kan ikke koble til API: {str(e)}")
    
    def show_ordrer_detaljer(self):
        """Vis detaljer for valgt ordre"""
        selected = self.ordrer_tree.selection()
        if not selected:
            messagebox.showwarning("Advarsel", "Velg en ordre først")
            return
        
        ordreNr = self.ordrer_tree.item(selected[0])["values"][0]
        
        try:
            response = requests.get(f"{API_BASE_URL}/api/ordrer/{ordreNr}", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                messagebox.showerror("API Error", data.get("message", "Ukjent feil"))
                return
            
            # Opprett detalj-vindu
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Ordre #{ordreNr} - Detaljer")
            detail_window.geometry("700x600")
            
            # Kundeinfo
            ordre = data["ordre"]
            kunde_text = f"Kunde: {ordre.get('Navn', 'N/A')}\n{ordre.get('Adresse', '')}\n{ordre.get('Postnummer', '')} {ordre.get('By', '')}"
            ttk.Label(detail_window, text=kunde_text, font=("Arial", 10)).pack(padx=10, pady=10)
            
            # Tabell for ordrelinjer
            tree = ttk.Treeview(detail_window, columns=("VNr", "Betegnelse", "Antall", "Pris", "Sum"), height=15)
            tree.column("#0", width=0)
            tree.column("VNr", width=50)
            tree.column("Betegnelse", width=250)
            tree.column("Antall", width=60)
            tree.column("Pris", width=80)
            tree.column("Sum", width=80)
            
            tree.heading("VNr", text="V-Nr")
            tree.heading("Betegnelse", text="Vare")
            tree.heading("Antall", text="Antall")
            tree.heading("Pris", text="Pris (kr)")
            tree.heading("Sum", text="Sum (kr)")
            
            for linje in data.get("linjer", []):
                tree.insert("", tk.END, values=(
                    linje["VNr"],
                    linje["Betegnelse"],
                    linje["Antall"],
                    f"{linje['Pris']:.2f}",
                    f"{linje['LinjeSum']:.2f}"
                ))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Totaler
            totaler = data["totaler"]
            total_text = (
                f"Subtotal: {totaler['total_før_moms']:.2f} kr\n"
                f"Moms (25%): {totaler['moms_25_prosent']:.2f} kr\n"
                f"TOTAL: {totaler['total_med_moms']:.2f} kr"
            )
            ttk.Label(detail_window, text=total_text, font=("Arial", 11, "bold")).pack(padx=10, pady=10)
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Tilkoblingsfeil", f"Kan ikke koble til API: {str(e)}")
    
    # =====================================================
    # TAB: KUNDER
    # =====================================================
    
    def show_kunder(self):
        """Vise kunder liste"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="👥 Kunder", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Knapper
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Oppdater", command=self.update_kunder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ny Kunde", command=self.add_kunde).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Slett", command=self.delete_kunde).pack(side=tk.LEFT, padx=5)
        
        # Tabel
        self.kunder_tree = ttk.Treeview(
            self.content_frame,
            columns=("KNr", "Navn", "Adresse", "Postnummer", "By"),
            height=25
        )
        self.kunder_tree.column("#0", width=0, stretch=tk.NO)
        self.kunder_tree.column("KNr", anchor=tk.W, width=50)
        self.kunder_tree.column("Navn", anchor=tk.W, width=200)
        self.kunder_tree.column("Adresse", anchor=tk.W, width=200)
        self.kunder_tree.column("Postnummer", anchor=tk.W, width=80)
        self.kunder_tree.column("By", anchor=tk.W, width=100)
        
        self.kunder_tree.heading("KNr", text="K-Nr", anchor=tk.W)
        self.kunder_tree.heading("Navn", text="Navn", anchor=tk.W)
        self.kunder_tree.heading("Adresse", text="Adresse", anchor=tk.W)
        self.kunder_tree.heading("Postnummer", text="Postnummer", anchor=tk.W)
        self.kunder_tree.heading("By", text="By", anchor=tk.W)
        
        self.kunder_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.kunder_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.kunder_tree.config(yscroll=scrollbar.set)
        
        # Last data
        self.update_kunder()
    
    def update_kunder(self):
        """Hent kunder fra API"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/kunder", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                messagebox.showerror("API Error", data.get("message", "Ukjent feil"))
                return
            
            # Tøm tabel
            for item in self.kunder_tree.get_children():
                self.kunder_tree.delete(item)
            
            # Fyll med data
            for kunde in data.get("items", []):
                self.kunder_tree.insert(
                    "",
                    tk.END,
                    values=(
                        kunde["KNr"],
                        kunde["Navn"],
                        kunde["Adresse"],
                        kunde["Postnummer"],
                        kunde["By"]
                    )
                )
            
            messagebox.showinfo("Suksess", f"Lastet {len(data.get('items', []))} kunder")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Tilkoblingsfeil", f"Kan ikke koble til API: {str(e)}")
    
    def add_kunde(self):
        """Legg til ny kunde"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Ny Kunde")
        add_window.geometry("400x300")
        
        # Input felter
        ttk.Label(add_window, text="Navn:").pack(padx=10, pady=5)
        navn_entry = ttk.Entry(add_window, width=40)
        navn_entry.pack(padx=10, pady=5)
        
        ttk.Label(add_window, text="Adresse:").pack(padx=10, pady=5)
        adresse_entry = ttk.Entry(add_window, width=40)
        adresse_entry.pack(padx=10, pady=5)
        
        ttk.Label(add_window, text="Postnummer:").pack(padx=10, pady=5)
        postnummer_entry = ttk.Entry(add_window, width=40)
        postnummer_entry.pack(padx=10, pady=5)
        
        ttk.Label(add_window, text="By:").pack(padx=10, pady=5)
        by_entry = ttk.Entry(add_window, width=40)
        by_entry.pack(padx=10, pady=5)
        
        def save_kunde():
            try:
                payload = {
                    "Navn": navn_entry.get(),
                    "Adresse": adresse_entry.get(),
                    "Postnummer": postnummer_entry.get(),
                    "By": by_entry.get()
                }
                
                response = requests.post(f"{API_BASE_URL}/api/kunder", json=payload, timeout=5)
                data = response.json()
                
                if data.get("ok"):
                    messagebox.showinfo("Suksess", f"Kunde lagt til (ID: {data['KNr']})")
                    add_window.destroy()
                    self.update_kunder()
                else:
                    messagebox.showerror("Feil", data.get("message", "Ukjent feil"))
            
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Tilkoblingsfeil", f"Kan ikke koble til API: {str(e)}")
        
        ttk.Button(add_window, text="Lagre", command=save_kunde).pack(pady=10)
    
    def delete_kunde(self):
        """Slett valgt kunde"""
        selected = self.kunder_tree.selection()
        if not selected:
            messagebox.showwarning("Advarsel", "Velg en kunde først")
            return
        
        KNr = self.kunder_tree.item(selected[0])["values"][0]
        
        if messagebox.askyesno("Bekreft", f"Slett kunde #{KNr}?"):
            try:
                response = requests.delete(f"{API_BASE_URL}/api/kunder/{KNr}", timeout=5)
                data = response.json()
                
                if data.get("ok"):
                    messagebox.showinfo("Suksess", "Kunde slettet")
                    self.update_kunder()
                else:
                    messagebox.showerror("Feil", data.get("message", "Ukjent feil"))
            
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Tilkoblingsfeil", f"Kan ikke koble til API: {str(e)}")
    
    # =====================================================
    # TAB: STATUS
    # =====================================================
    
    def show_status(self):
        """Vise API status"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="🏥 API Status", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        try:
            response = requests.get(f"{API_BASE_URL}/health/db", timeout=5)
            data = response.json()
            
            status_text = f"Status: {'✅ OK' if data.get('ok') else '❌ ERROR'}\n\nMessage:\n{data.get('message', 'N/A')}"
            
            if data.get("ok"):
                status_label = ttk.Label(self.content_frame, text=status_text, 
                                        font=("Arial", 11), foreground="green")
            else:
                status_label = ttk.Label(self.content_frame, text=status_text, 
                                        font=("Arial", 11), foreground="red")
            
            status_label.pack(padx=20, pady=20)
        
        except requests.exceptions.RequestException as e:
            error_label = ttk.Label(self.content_frame, 
                                   text=f"❌ Kan ikke koble til API\n\n{str(e)}", 
                                   font=("Arial", 11), foreground="red")
            error_label.pack(padx=20, pady=20)


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = VarehusApp(root)
    root.mainloop()
