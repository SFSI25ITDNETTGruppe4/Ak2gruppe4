"""Tkinter-klient for arbeidskravet i Python og database.

GUI-et dekker brukerkravene i oppgaven: varelager, ordrer, ordredetaljer,
kunder, status mot API og fakturagenerering via backend.

For å kjøre GUI-et må disse avhengighetene være installert:
- requests
- python-dotenv

GUI-et leser API_BASE_URL fra .env, eller bruker live-URL som standard.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
from dotenv import load_dotenv

# =====================================================
# CONFIG
# =====================================================

load_dotenv()

# Default til live API for å unngå localhost-feil når backend ikke kjører lokalt.
# Kan overstyres med miljøvariabelen API_BASE_URL.
API_BASE_URL = os.getenv("API_BASE_URL", "https://ak2gruppe4.onrender.com").rstrip("/")

# =====================================================
# FARGEPALETT
# Sentralisert – endre her for å justere hele appens utseende.
# =====================================================
COLORS = {
    "header_bg":  "#1a2742",   # mørk marineblå – header og navbar
    "nav_active": "#2563eb",   # klar blå – aktiv nav-knapp
    "nav_hover":  "#2d4a80",   # mellomblå – kolonne-hover
    "content_bg": "#ffffff",   # hvit bakgrunn for innholdssone
    "row_odd":    "#f0f4f8",   # lys blågrå – annenhver rad (zebra)
    "row_even":   "#ffffff",   # hvit – annenhver rad (zebra)
    "ok":         "#16a34a",   # grønn – suksessmelding
    "error":      "#dc2626",   # rød – feilmelding
    "warning":    "#d97706",   # oransje – advarsel
    "status_bg":  "#f1f5f9",   # lys bakgrunn i statusfelt
    "status_fg":  "#64748b",   # grå standardtekst i statusfelt
}

# =====================================================
# MAIN WINDOW
# =====================================================

# denne klassen samler hele GUI-løsningen i ett vindu. Den er delt inn i faner
# for varelager, ordrer, kunder og API-status, slik at hvert krav i oppgaven
# kan demonstreres fra samme program.

class VarehusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Varehus Lager & Ordre System")
        self.root.geometry("1200x720")
        # Vindusbakgrunn satt til header-fargen slik at topp-/sidefeltene
        # går i ett med header og navbar.
        self.root.configure(bg=COLORS["header_bg"])

        # Stil – konfigureres via _apply_styles() som bruker COLORS-paletten
        self._apply_styles()

        # Mørk header med appnavn og gruppenavn
        self._build_header()

        # Navbar
        self.create_navbar()

        # Statusfelt nederst – pakkes FØR content_frame slik at det alltid er
        # synlig selv når content_frame fyller resten av vinduet (expand=True).
        self._status_var = tk.StringVar(value="Klar")
        self._status_label = tk.Label(
            root,
            textvariable=self._status_var,
            anchor=tk.W,
            bg=COLORS["status_bg"],
            fg=COLORS["status_fg"],
            padx=12,
            pady=4,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
        )
        self._status_label.pack(side=tk.BOTTOM, fill=tk.X)
        self._notify_job = None  # holder referanse til auto-reset-timer

        # Main content area
        self.content_frame = tk.Frame(root, bg=COLORS["content_bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 6))

        # Start with varelager tab
        self.show_varelager()

    def _build_header(self):
        """Bygg toppfelt med appnavn og gruppenavn.

        Bruker tk.Frame med fast høyde (pack_propagate=False) for et
        rent, ikke-utvidbart header-område.
        """
        header = tk.Frame(self.root, bg=COLORS["header_bg"], height=52)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)  # behold høyden selv om innholdet er lite

        tk.Label(
            header,
            text="  🏭  Varehus Lager & Ordre System",
            bg=COLORS["header_bg"],
            fg="#ffffff",
            font=("Segoe UI", 14, "bold"),
            anchor=tk.W,
        ).pack(side=tk.LEFT, padx=16, fill=tk.Y)

        tk.Label(
            header,
            text="Gruppe 4 – AK2  ",
            bg=COLORS["header_bg"],
            fg="#94a3b8",
            font=("Segoe UI", 10),
        ).pack(side=tk.RIGHT, padx=4, fill=tk.Y)
    
    def _apply_styles(self):
        """Konfigurer ttk-stiler for hele applikasjonen med COLORS-paletten."""
        s = ttk.Style()
        s.theme_use("clam")

        # Treeview-rader: ren bakgrunn og lesbar skrift
        s.configure(
            "Treeview",
            background=COLORS["content_bg"],
            foreground="#1e293b",
            rowheight=26,
            fieldbackground=COLORS["content_bg"],
            font=("Segoe UI", 10),
        )
        # Kolonneoverskrifter: mørk bakgrunn som matcher header
        s.configure(
            "Treeview.Heading",
            background=COLORS["header_bg"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(6, 4),
        )
        s.map("Treeview.Heading",
              background=[("active", COLORS["nav_hover"])])
        s.map("Treeview",
              background=[("selected", COLORS["nav_active"])],
              foreground=[("selected", "#ffffff")])

        # Knapper og entry-felt
        s.configure("TButton", font=("Segoe UI", 10), padding=(10, 5))
        s.configure("TEntry",  font=("Segoe UI", 10), padding=(6, 4))

    def create_navbar(self):
        """Opprett navigasjonsmeny med aktiv-markering.

        Bruker vanlige tk.Button (ikke ttk) fordi ttk ikke støtter
        bakgrunnsfarger på alle plattformer. Referanser lagres i
        self._nav_buttons slik at _set_active_nav() kan farge dem.
        """
        self._nav_buttons = {}  # key → tk.Button – brukes til aktiv-markering

        navbar = tk.Frame(self.root, bg=COLORS["header_bg"], height=40)
        navbar.pack(fill=tk.X, side=tk.TOP)
        navbar.pack_propagate(False)

        nav_items = [
            ("varelager", "📦  Varelager",  self.show_varelager),
            ("ordrer",    "📋  Ordrer",      self.show_ordrer),
            ("kunder",    "👥  Kunder",      self.show_kunder),
            ("status",    "🏥  API Status",  self.show_status),
        ]
        for key, label, cmd in nav_items:
            btn = tk.Button(
                navbar,
                text=label,
                bg=COLORS["header_bg"],
                fg="#cbd5e1",
                activebackground=COLORS["nav_hover"],
                activeforeground="#ffffff",
                relief=tk.FLAT,
                bd=0,
                padx=18,
                pady=8,
                font=("Segoe UI", 10),
                cursor="hand2",
                command=cmd,
            )
            btn.pack(side=tk.LEFT)
            self._nav_buttons[key] = btn

    def _set_active_nav(self, key):
        """Marker aktiv navigasjonsknapp med klar blå bakgrunn."""
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.config(bg=COLORS["nav_active"], fg="#ffffff")
            else:
                btn.config(bg=COLORS["header_bg"], fg="#cbd5e1")
    
    def clear_content(self):
        """Tøm content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _fill_tree(self, tree, rows):
        """Tøm og fyll Treeview med zebra-striper (annenhver rad farges).

        Alle tabeller i appen bruker denne hjelperen slik at stripingen
        er konsistent. Tags 'odd' og 'even' må være definert på treet
        på forhånd (gjøres rett etter at Treeview opprettes).
        """
        tree.delete(*tree.get_children())
        for i, row in enumerate(rows):
            # Annenhver rad får ulik bakgrunn via tag
            tag = "odd" if i % 2 == 0 else "even"
            tree.insert("", tk.END, values=row, tags=(tag,))

    @staticmethod
    def _to_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _notify(self, message, level="info"):
        """Vis tilbakemelding i statusfeltet i stedet for popup-dialoger.

        level: 'info' = grønn, 'error' = rød, 'warning' = oransje.
        Meldingen nullstilles automatisk til 'Klar' etter 4 sekunder.
        """
        colors = {"info": "green", "error": "red", "warning": "darkorange"}
        self._status_label.config(foreground=colors.get(level, "black"))
        self._status_var.set(message)
        # Avbryt eventuell pågående timer slik at nye meldinger ikke kuttes kort
        if self._notify_job:
            self.root.after_cancel(self._notify_job)
        self._notify_job = self.root.after(4000, lambda: self._status_var.set("Klar"))
    
    # =====================================================
    # TAB: VARELAGER
    # =====================================================
    
    def show_varelager(self):
        """Vise varelager liste"""
        self.clear_content()
        self._set_active_nav("varelager")  # marker aktiv fane i navbar
        
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
        # Sett zebra-stripefarger via tags (brukes av _fill_tree)
        self.varelager_tree.tag_configure("odd",  background=COLORS["row_odd"])
        self.varelager_tree.tag_configure("even", background=COLORS["row_even"])
        
        # Scroll bar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.varelager_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.varelager_tree.config(yscroll=scrollbar.set)
        
        # Last data
        self.update_varelager()
    
    def update_varelager(self):
        """Hent varelager fra API"""
        try:
            # Oppgavekrav: GUI-et skal vise varenummer, navn, antall og pris.
            response = requests.get(f"{API_BASE_URL}/api/varelager", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                self._notify(data.get("message", "Ukjent feil"), "error")
                return
            
            # Bygg radliste og fyll tabell med zebra-striper via _fill_tree
            rows = [
                (v["VNr"], v["Betegnelse"], v["Antall"],
                 f"{self._to_float(v.get('Pris')):.2f}")
                for v in data.get("items", [])
            ]
            self._fill_tree(self.varelager_tree, rows)
            
            self._notify(f"Lastet {len(data.get('items', []))} varer", "info")
        
        except requests.exceptions.RequestException as e:
            self._notify(f"Tilkoblingsfeil: {str(e)}", "error")
    
    # =====================================================
    # TAB: ORDRER
    # =====================================================
    
    def show_ordrer(self):
        """Vise ordrer liste"""
        self.clear_content()
        self._set_active_nav("ordrer")  # marker aktiv fane i navbar
        
        ttk.Label(self.content_frame, text="📋 Ordrer", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Knapper
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Oppdater", command=self.update_ordrer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Se detaljer", command=self.show_ordrer_detaljer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generer faktura (PDF)", command=self.generate_faktura_pdf).pack(side=tk.LEFT, padx=5)
        
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
        # Sett zebra-stripefarger via tags (brukes av _fill_tree)
        self.ordrer_tree.tag_configure("odd",  background=COLORS["row_odd"])
        self.ordrer_tree.tag_configure("even", background=COLORS["row_even"])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.ordrer_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ordrer_tree.config(yscroll=scrollbar.set)
        
        # Last data
        self.update_ordrer()
    
    def update_ordrer(self):
        """Hent ordrer fra API"""
        try:
            # denne funksjonen henter ordreliste fra backend og fyller tabellen i GUI-et.
            response = requests.get(f"{API_BASE_URL}/api/ordrer", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                self._notify(data.get("message", "Ukjent feil"), "error")
                return
            
            # Bygg radliste og fyll tabell med zebra-striper via _fill_tree
            rows = [
                (o["OrdreNr"], o["OrdreDato"], o["SendtDato"],
                 o["BetaltDato"], o["KNr"])
                for o in data.get("items", [])
            ]
            self._fill_tree(self.ordrer_tree, rows)
            
            self._notify(f"Lastet {len(data.get('items', []))} ordrer", "info")
        
        except requests.exceptions.RequestException as e:
            self._notify(f"Tilkoblingsfeil: {str(e)}", "error")
    
    def show_ordrer_detaljer(self):
        """Vis detaljer for valgt ordre"""
        selected = self.ordrer_tree.selection()
        if not selected:
            self._notify("Velg en ordre først", "warning")
            return
        
        ordreNr = self.ordrer_tree.item(selected[0])["values"][0]
        
        try:
            # Oppgavekrav: valgt ordre skal vise kunde, varer, antall og summer.
            response = requests.get(f"{API_BASE_URL}/api/ordrer/{ordreNr}", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                self._notify(data.get("message", "Ukjent feil"), "error")
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
            
            # løkken legger inn hver ordrelinje i detaljtabellen slik at bruker ser
            # hvilke varer som er solgt, hvor mange og hva hver linje koster.
            # Zebra-striper i detalj-vinduets tabell
            tree.tag_configure("odd",  background=COLORS["row_odd"])
            tree.tag_configure("even", background=COLORS["row_even"])
            for i, linje in enumerate(data.get("linjer", [])):
                tree.insert("", tk.END, tags=("odd" if i % 2 == 0 else "even",), values=(
                    linje["VNr"],
                    linje["Betegnelse"],
                    linje["Antall"],
                    f"{self._to_float(linje.get('Pris')):.2f}",
                    f"{self._to_float(linje.get('LinjeSum')):.2f}"
                ))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Totaler
            totaler = data["totaler"]
            total_text = (
                f"Subtotal: {self._to_float(totaler.get('total_før_moms')):.2f} kr\n"
                f"Moms (25%): {self._to_float(totaler.get('moms_25_prosent')):.2f} kr\n"
                f"TOTAL: {self._to_float(totaler.get('total_med_moms')):.2f} kr"
            )
            ttk.Label(detail_window, text=total_text, font=("Arial", 11, "bold")).pack(padx=10, pady=10)
            self._notify(f"Viser detaljer for ordre #{ordreNr}", "info")
        
        except requests.exceptions.RequestException as e:
            self._notify(f"Tilkoblingsfeil: {str(e)}", "error")

    def generate_faktura_pdf(self):
        """Generer og lagre PDF-faktura for valgt ordre"""
        selected = self.ordrer_tree.selection()
        if not selected:
            self._notify("Velg en ordre først", "warning")
            return

        ordreNr = self.ordrer_tree.item(selected[0])["values"][0]

        try:
            # Oppgavekrav: faktura skal kunne genereres fra GUI for valgt ordre.
            response = requests.post(f"{API_BASE_URL}/api/ordrer/{ordreNr}/faktura", timeout=20)
            if response.status_code >= 400:
                try:
                    data = response.json()
                    message = data.get("message", "Ukjent feil")
                except Exception:
                    message = f"HTTP {response.status_code}"
                self._notify(message, "error")
                return

            faktura_nr = response.headers.get("X-Invoice-Number", f"faktura-{ordreNr}")
            filename = filedialog.asksaveasfilename(
                title="Lagre faktura",
                defaultextension=".pdf",
                initialfile=f"{faktura_nr}.pdf",
                filetypes=[("PDF filer", "*.pdf")],
            )

            if not filename:
                return

            with open(filename, "wb") as out_file:
                out_file.write(response.content)

            self._notify(f"Faktura lagret: {filename}", "info")
        except requests.exceptions.RequestException as e:
            self._notify(f"Tilkoblingsfeil: {str(e)}", "error")
    
    # =====================================================
    # TAB: KUNDER
    # =====================================================
    
    def show_kunder(self):
        """Vise kunder liste"""
        self.clear_content()
        self._set_active_nav("kunder")  # marker aktiv fane i navbar

        # denne fanen dekker kundedelen av oppgaven: vise kunder, legge til kunde
        # og slette kunde via API-et.

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
        # Sett zebra-stripefarger via tags (brukes av _fill_tree)
        self.kunder_tree.tag_configure("odd",  background=COLORS["row_odd"])
        self.kunder_tree.tag_configure("even", background=COLORS["row_even"])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.kunder_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.kunder_tree.config(yscroll=scrollbar.set)
        
        # Last data
        self.update_kunder()
    
    def update_kunder(self):
        """Hent kunder fra API"""
        try:
            # Backend-ruten bruker Stored Procedure, som er et eksplisitt krav i oppgaven.
            response = requests.get(f"{API_BASE_URL}/api/kunder", timeout=5)
            data = response.json()
            
            if not data.get("ok"):
                self._notify(data.get("message", "Ukjent feil"), "error")
                return
            
            # Bygg radliste og fyll tabell med zebra-striper via _fill_tree
            rows = [
                (k["KNr"], k["Navn"], k["Adresse"],
                 k["Postnummer"], k["By"])
                for k in data.get("items", [])
            ]
            self._fill_tree(self.kunder_tree, rows)
            
            self._notify(f"Lastet {len(data.get('items', []))} kunder", "info")
        
        except requests.exceptions.RequestException as e:
            self._notify(f"Tilkoblingsfeil: {str(e)}", "error")
    
    def add_kunde(self):
        """Legg til ny kunde"""
        # denne funksjonen åpner et enkelt skjema for å opprette kunde fra GUI-et.
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
            # den indre funksjonen sender skjemaet til backend, som gjør selve
            # valideringen og opprettelsen i databasen.
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
                    self._notify(f"Kunde lagt til (ID: {data['KNr']})", "info")
                    add_window.destroy()
                    self.update_kunder()
                else:
                    self._notify(data.get("message", "Ukjent feil"), "error")
            
            except requests.exceptions.RequestException as e:
                self._notify(f"Tilkoblingsfeil: {str(e)}", "error")
        
        ttk.Button(add_window, text="Lagre", command=save_kunde).pack(pady=10)
    
    def delete_kunde(self):
        """Slett valgt kunde"""
        # sletting krever at en kunde er valgt, og backend passer på at kunder
        # med eksisterende ordrer ikke kan fjernes.
        selected = self.kunder_tree.selection()
        if not selected:
            self._notify("Velg en kunde først", "warning")
            return
        
        KNr = self.kunder_tree.item(selected[0])["values"][0]
        
        if messagebox.askyesno("Bekreft", f"Slett kunde #{KNr}?"):
            try:
                response = requests.delete(f"{API_BASE_URL}/api/kunder/{KNr}", timeout=5)
                data = response.json()
                
                if data.get("ok"):
                    self._notify("Kunde slettet", "info")
                    self.update_kunder()
                else:
                    self._notify(data.get("message", "Ukjent feil"), "error")
            
            except requests.exceptions.RequestException as e:
                self._notify(f"Tilkoblingsfeil: {str(e)}", "error")
    
    # =====================================================
    # TAB: STATUS
    # =====================================================
    
    def show_status(self):
        """Vise API status"""
        self.clear_content()
        self._set_active_nav("status")  # marker aktiv fane i navbar

        # denne funksjonen gjør det enkelt å teste om miljøvariabler og database
        # er riktig satt opp på maskinen ved å kalle /health/db.
        
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
