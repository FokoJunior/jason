import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime

class ModernTable(ctk.CTkFrame):
    """Tableau moderne avec style personnalisé"""
    
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent, fg_color="#2d2d2d", corner_radius=10)
        
        # Configuration du style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Style pour le Treeview
        style.configure(
            "Treeview",
            background="#3a3a3a",
            foreground="#ffffff",
            fieldbackground="#3a3a3a",
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        
        style.configure(
            "Treeview.Heading",
            background="#007acc",
            foreground="#ffffff",
            borderwidth=0,
            font=("Segoe UI", 11, "bold")
        )
        
        style.map(
            "Treeview",
            background=[("selected", "#007acc")],
            foreground=[("selected", "#ffffff")]
        )
        
        # Créer le Treeview
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        # Configurer les colonnes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def insert_data(self, data):
        """Insérer des données dans le tableau"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insérer les nouvelles données
        for row in data:
            self.tree.insert("", "end", values=row)
    
    def get_selected(self):
        """Obtenir l'élément sélectionné"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])["values"]
        return None

class InfoCard(ctk.CTkFrame):
    """Carte d'information moderne"""
    
    def __init__(self, parent, title, value, icon="📊", color="#007acc", **kwargs):
        super().__init__(parent, fg_color="#3a3a3a", corner_radius=15, **kwargs)
        
        # Titre
        title_label = ctk.CTkLabel(
            self,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(20, 10))
        
        # Valeur
        value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 20))

class ModernForm(ctk.CTkFrame):
    """Formulaire moderne"""
    
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, fg_color="#2d2d2d", corner_radius=15, **kwargs)
        
        # Titre du formulaire
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Frame pour les champs
        self.fields_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.fields_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.fields = {}
    
    def add_field(self, label, field_type="entry", **kwargs):
        """Ajouter un champ au formulaire"""
        # Label
        label_widget = ctk.CTkLabel(
            self.fields_frame,
            text=label,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        label_widget.pack(pady=(10, 5), anchor="w")
        
        # Champ
        if field_type == "entry":
            field = ctk.CTkEntry(
                self.fields_frame,
                width=400,
                height=40,
                font=ctk.CTkFont(size=14),
                fg_color="#3a3a3a",
                border_color="#007acc",
                text_color="#ffffff",
                **kwargs
            )
        elif field_type == "combobox":
            field = ctk.CTkComboBox(
                self.fields_frame,
                width=400,
                height=40,
                font=ctk.CTkFont(size=14),
                fg_color="#3a3a3a",
                border_color="#007acc",
                text_color="#ffffff",
                **kwargs
            )
        elif field_type == "textbox":
            field = ctk.CTkTextbox(
                self.fields_frame,
                width=400,
                height=100,
                font=ctk.CTkFont(size=14),
                fg_color="#3a3a3a",
                border_color="#007acc",
                text_color="#ffffff",
                **kwargs
            )
        elif field_type == "slider":
            field = ctk.CTkSlider(
                self.fields_frame,
                width=400,
                **kwargs
            )
        
        field.pack(pady=(0, 15))
        
        # Stocker la référence
        self.fields[label] = field
        
        return field
    
    def get_values(self):
        """Obtenir toutes les valeurs du formulaire"""
        values = {}
        for label, field in self.fields.items():
            if isinstance(field, ctk.CTkTextbox):
                values[label] = field.get("1.0", "end-1c")
            elif isinstance(field, ctk.CTkSlider):
                values[label] = int(field.get())
            else:
                values[label] = field.get()
        return values

class ModernChart(ctk.CTkFrame):
    """Graphique moderne avec matplotlib"""
    
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, fg_color="#2d2d2d", corner_radius=15, **kwargs)
        
        # Titre
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Frame pour le graphique
        self.chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_bar_chart(self, data, labels, title="", color="#007acc"):
        """Créer un graphique en barres"""
        # Vider le frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#2d2d2d')
        ax.set_facecolor('#2d2d2d')
        
        bars = ax.bar(labels, data, color=color, alpha=0.8)
        
        # Personnaliser le graphique
        ax.set_title(title, color='white', fontsize=16, fontweight='bold')
        ax.set_xlabel('Catégories', color='white', fontsize=12)
        ax.set_ylabel('Valeurs', color='white', fontsize=12)
        
        # Personnaliser les axes
        ax.tick_params(axis='x', colors='white', rotation=45)
        ax.tick_params(axis='y', colors='white')
        
        # Personnaliser la grille
        ax.grid(True, alpha=0.3, color='white')
        
        # Ajouter les valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', color='white')
        
        plt.tight_layout()
        
        # Intégrer dans l'interface
        canvas = tkagg.FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_pie_chart(self, data, labels, title=""):
        """Créer un graphique circulaire"""
        # Vider le frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('#2d2d2d')
        ax.set_facecolor('#2d2d2d')
        
        colors = ['#007acc', '#4CAF50', '#FF9800', '#F44336', '#9C27B0']
        
        wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%',
                                          colors=colors[:len(data)], startangle=90)
        
        # Personnaliser le titre
        ax.set_title(title, color='white', fontsize=16, fontweight='bold', pad=20)
        
        # Personnaliser les labels
        for text in texts:
            text.set_color('white')
            text.set_fontsize(12)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        
        # Intégrer dans l'interface
        canvas = tkagg.FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

class ModernStats(ctk.CTkFrame):
    """Affichage moderne des statistiques"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#2d2d2d", corner_radius=15, **kwargs)
        
        # Titre
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Statistiques",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=20)
        
        # Frame pour les statistiques
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def display_stats(self, stats_data):
        """Afficher les statistiques"""
        # Vider le frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Créer des cartes pour chaque statistique
        for i, (label, value) in enumerate(stats_data.items()):
            card = InfoCard(
                self.stats_frame,
                title=label,
                value=value,
                icon="📈"
            )
            card.pack(side="left", fill="both", expand=True, padx=10, pady=10)

class ModernSearch(ctk.CTkFrame):
    """Barre de recherche moderne"""
    
    def __init__(self, parent, placeholder="Rechercher...", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Frame de recherche
        search_frame = ctk.CTkFrame(self, fg_color="#3a3a3a", corner_radius=20)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Icône de recherche
        search_icon = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=ctk.CTkFont(size=16)
        )
        search_icon.pack(side="left", padx=15, pady=10)
        
        # Champ de recherche
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text=placeholder,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            text_color="#ffffff"
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        # Bouton de recherche
        search_button = ctk.CTkButton(
            search_frame,
            text="Rechercher",
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#007acc",
            hover_color="#005a9e"
        )
        search_button.pack(side="right", padx=15, pady=10)
    
    def get_search_term(self):
        """Obtenir le terme de recherche"""
        return self.search_entry.get().strip()

class ModernNotification(ctk.CTkFrame):
    """Notification moderne"""
    
    def __init__(self, parent, message, type="info", **kwargs):
        super().__init__(parent, fg_color="#3a3a3a", corner_radius=10, **kwargs)
        
        # Icône selon le type
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        icon = icons.get(type, "ℹ️")
        
        # Couleurs selon le type
        colors = {
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800",
            "info": "#2196F3"
        }
        color = colors.get(type, "#2196F3")
        
        # Icône
        icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(side="left", padx=15, pady=15)
        
        # Message
        message_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#ffffff"
        )
        message_label.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=15)
        
        # Bouton de fermeture
        close_button = ctk.CTkButton(
            self,
            text="×",
            width=30,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color="#555555",
            command=self.destroy
        )
        close_button.pack(side="right", padx=15, pady=15)
        
        # Auto-destruction après 5 secondes
        self.after(5000, self.destroy)
    
    @staticmethod
    def show(parent, message, type="info"):
        """Afficher une notification"""
        notification = ModernNotification(parent, message, type)
        notification.pack(fill="x", padx=20, pady=10)
        return notification 