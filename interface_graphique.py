import customtkinter as ctk
from tkinter import messagebox, ttk
try:
    import matplotlib.pyplot as plt
    import matplotlib.backends.backend_tkagg as tkagg
    from matplotlib.figure import Figure
    import seaborn as sns
    import pandas as pd
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib non disponible - Les graphiques seront désactivés")

from datetime import datetime
from models import *
from config import Config

# Configuration de CustomTkinter
ctk.set_appearance_mode(Config.THEME)
ctk.set_default_color_theme(Config.COLOR_THEME)

class LoginWindow:
    """Fenêtre de connexion améliorée"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Système d'Évaluation des Enseignants - Connexion")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
        
        self.current_user = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur améliorée"""
        # Titre principal
        title_label = ctk.CTkLabel(
            self.root, 
            text="🎓 Système d'Évaluation des Enseignants",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=30)
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            self.root,
            text="Connectez-vous pour accéder au système",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=5)
        
        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        form_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        # Identifiant
        ctk.CTkLabel(form_frame, text="👤 Identifiant:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(0, 5))
        self.login_entry = ctk.CTkEntry(
            form_frame, 
            width=300,
            height=40,
            placeholder_text="Entrez votre identifiant..."
        )
        self.login_entry.pack(pady=(0, 15))
        
        # Mot de passe
        ctk.CTkLabel(form_frame, text="🔒 Mot de passe:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(0, 5))
        self.password_entry = ctk.CTkEntry(
            form_frame, 
            width=300,
            height=40,
            show="*",
            placeholder_text="Entrez votre mot de passe..."
        )
        self.password_entry.pack(pady=(0, 20))
        
        # Bouton de connexion
        login_button = ctk.CTkButton(
            form_frame,
            text="🚀 Se connecter",
            command=self.login,
            width=200,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        login_button.pack(pady=10)
        
        # Informations de test
        info_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        info_frame.pack(pady=20)
        
        ctk.CTkLabel(info_frame, text="📋 Comptes de test:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack()
        
        test_accounts = [
            "👨‍💼 ADMIN001 / admin123",
            "👨‍🏫 ENS001 / enseignant123", 
            "👨‍🎓 ETU001 / etudiant123"
        ]
        
        for account in test_accounts:
            ctk.CTkLabel(info_frame, text=account, 
                        font=ctk.CTkFont(size=11),
                        text_color="gray").pack(pady=2)
        
        # Lier la touche Entrée
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus sur le premier champ
        self.login_entry.focus()
    
    def login(self):
        """Authentification de l'utilisateur avec gestion d'erreurs améliorée"""
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not login or not password:
            messagebox.showerror("❌ Erreur", "Veuillez remplir tous les champs.")
            return
        
        # Afficher un indicateur de chargement
        self.root.config(cursor="wait")
        self.root.update()
        
        try:
            # Tentative de connexion
            user = Utilisateur()
            if user.seConnecter(login, password):
                # Créer l'utilisateur approprié selon le statut
                if user.statut == 'étudiant':
                    self.current_user = Etudiant()
                    self.current_user.__dict__.update(user.__dict__)
                    welcome_msg = f"👨‍🎓 Bienvenue, {user.nom_prenom} !"
                elif user.statut == 'enseignant':
                    self.current_user = Enseignant()
                    self.current_user.__dict__.update(user.__dict__)
                    welcome_msg = f"👨‍🏫 Bienvenue, {user.nom_prenom} !"
                elif user.statut == 'administrateur':
                    self.current_user = Administrateur()
                    self.current_user.__dict__.update(user.__dict__)
                    welcome_msg = f"👨‍💼 Bienvenue, {user.nom_prenom} !"
                else:
                    messagebox.showerror("❌ Erreur", "Statut utilisateur invalide.")
                    return
                
                # Ouvrir le tableau de bord approprié
                self.root.withdraw()
                dashboard = DashboardWindow(self.current_user)
                dashboard.show()
                
                # Message de bienvenue
                messagebox.showinfo("✅ Connexion réussie", welcome_msg)
            else:
                messagebox.showerror("❌ Échec de connexion", 
                                   "Identifiants incorrects.\n\nVérifiez votre identifiant et mot de passe.")
        except Exception as e:
            messagebox.showerror("❌ Erreur système", 
                               f"Erreur lors de la connexion :\n{str(e)}")
        finally:
            # Restaurer le curseur
            self.root.config(cursor="")
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()

class DashboardWindow:
    """Fenêtre du tableau de bord avec menu à gauche"""
    
    def __init__(self, user):
        self.user = user
        self.root = ctk.CTkToplevel()
        self.root.title(f"Tableau de Bord - {user.nom_prenom}")
        self.root.geometry("1400x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1400x800+{x}+{y}")
        
        self.current_frame = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur avec menu à gauche"""
        # Frame principal horizontal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Barre de titre
        title_frame = ctk.CTkFrame(main_frame, height=60)
        title_frame.pack(fill="x", padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        # Icône selon le statut
        icons = {
            'étudiant': '👨‍🎓',
            'enseignant': '👨‍🏫', 
            'administrateur': '👨‍💼'
        }
        icon = icons.get(self.user.statut, '👤')
        
        ctk.CTkLabel(
            title_frame,
            text=f"{icon} {self.user.nom_prenom} ({self.user.statut})",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=20, pady=15)
        
        # Bouton de déconnexion
        logout_button = ctk.CTkButton(
            title_frame,
            text="🚪 Déconnexion",
            command=self.logout,
            width=120
        )
        logout_button.pack(side="right", padx=20, pady=15)
        
        # Frame horizontal pour le contenu
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Menu à gauche
        self.create_left_menu(content_frame)
        
        # Zone de contenu à droite
        self.content_area = ctk.CTkFrame(content_frame)
        self.content_area.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Afficher la page par défaut
        self.show_default_page()
    
    def create_left_menu(self, parent):
        """Créer le menu à gauche"""
        menu_frame = ctk.CTkFrame(parent, width=250)
        menu_frame.pack(side="left", fill="y", padx=(0, 10))
        menu_frame.pack_propagate(False)
        
        # Titre du menu
        ctk.CTkLabel(
            menu_frame,
            text="📋 Menu",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Créer les boutons du menu selon le type d'utilisateur
        if self.user.statut == 'étudiant':
            self.create_student_menu(menu_frame)
        elif self.user.statut == 'enseignant':
            self.create_teacher_menu(menu_frame)
        elif self.user.statut == 'administrateur':
            self.create_admin_menu(menu_frame)
    
    def create_student_menu(self, parent):
        """Menu pour les étudiants"""
        menu_items = [
            ("📝 Évaluer un enseignant", self.show_evaluation_form),
            ("📊 Mes évaluations", self.show_my_evaluations),
            ("🔍 Rechercher des cours", self.show_course_search),
            ("👤 Mon profil", self.show_profile)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                parent,
                text=text,
                command=command,
                width=220,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(pady=5, padx=15)
    
    def create_teacher_menu(self, parent):
        """Menu pour les enseignants"""
        menu_items = [
            ("📊 Mes évaluations reçues", self.show_received_evaluations),
            ("📈 Mes statistiques", self.show_teacher_stats),
            ("📚 Mes cours", self.show_teacher_courses),
            ("👤 Mon profil", self.show_profile)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                parent,
                text=text,
                command=command,
                width=220,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(pady=5, padx=15)
    
    def create_admin_menu(self, parent):
        """Menu pour les administrateurs"""
        menu_items = [
            ("👥 Gestion des utilisateurs", self.show_user_management),
            ("📋 Toutes les évaluations", self.show_all_evaluations),
            ("📊 Statistiques globales", self.show_global_stats),
            ("📄 Rapports", self.show_reports),
            ("👤 Mon profil", self.show_profile)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                parent,
                text=text,
                command=command,
                width=220,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(pady=5, padx=15)
    
    def show_default_page(self):
        """Afficher la page par défaut"""
        if self.user.statut == 'étudiant':
            self.show_evaluation_form()
        elif self.user.statut == 'enseignant':
            self.show_received_evaluations()
        elif self.user.statut == 'administrateur':
            self.show_user_management()
    
    def clear_content_area(self):
        """Vider la zone de contenu"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_evaluation_form(self):
        """Afficher le formulaire d'évaluation"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📝 Évaluer un enseignant",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame de sélection
        selection_frame = ctk.CTkFrame(self.content_area)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(selection_frame, text="🎯 Sélectionner un enseignant et un cours:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Combobox pour les enseignants
        ctk.CTkLabel(selection_frame, text="👨‍🏫 Enseignant:").pack(pady=5)
        self.teacher_combobox = ctk.CTkComboBox(selection_frame, values=self.get_teachers_list())
        self.teacher_combobox.pack(pady=5)
        
        # Combobox pour les cours
        ctk.CTkLabel(selection_frame, text="📚 Cours:").pack(pady=5)
        self.course_combobox = ctk.CTkComboBox(selection_frame, values=self.get_courses_list())
        self.course_combobox.pack(pady=5)
        
        # Frame pour les critères d'évaluation
        criteria_frame = ctk.CTkFrame(self.content_area)
        criteria_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(criteria_frame, text="⭐ Critères d'évaluation (1-5):", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Créer les sliders pour chaque critère
        self.criteria_sliders = {}
        criteria_labels = {
            'clarte_cours': 'Clarté du cours',
            'ponctualite': 'Ponctualité',
            'pedagogie': 'Pédagogie',
            'disponibilite': 'Disponibilité',
            'maitrise_matiere': 'Maîtrise de la matière',
            'respect_etudiants': 'Respect des étudiants',
            'temps': 'Gestion du temps',
            'appreciation_stimulee': 'Appréciation stimulée',
            'utilisation_outils': 'Utilisation des outils',
            'approche_interactive': 'Approche interactive',
            'coherence_objectif': 'Cohérence avec les objectifs',
            'utilite_professionnelle': 'Utilité professionnelle'
        }
        
        for i, (key, label) in enumerate(criteria_labels.items()):
            frame = ctk.CTkFrame(criteria_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=label, width=200).pack(side="left", padx=10)
            
            slider = ctk.CTkSlider(frame, from_=1, to=5, number_of_steps=4)
            slider.pack(side="left", padx=10, fill="x", expand=True)
            slider.set(3)  # Valeur par défaut
            
            value_label = ctk.CTkLabel(frame, text="3", width=30)
            value_label.pack(side="right", padx=10)
            
            # Lier le slider à la mise à jour du label
            slider.configure(command=lambda val, label=value_label: label.configure(text=str(int(val))))
            
            self.criteria_sliders[key] = slider
        
        # Zone de commentaire
        comment_frame = ctk.CTkFrame(self.content_area)
        comment_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(comment_frame, text="💬 Commentaire général:").pack(pady=5)
        self.comment_text = ctk.CTkTextbox(comment_frame, height=100)
        self.comment_text.pack(fill="x", padx=10, pady=5)
        
        # Bouton de soumission
        submit_button = ctk.CTkButton(
            self.content_area,
            text="✅ Soumettre l'évaluation",
            command=self.submit_evaluation,
            width=200
        )
        submit_button.pack(pady=20)
    
    def show_my_evaluations(self):
        """Afficher les évaluations de l'étudiant"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📊 Mes évaluations",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Rafraîchir",
            command=self.refresh_evaluations,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Treeview pour afficher les évaluations
        self.evaluations_tree = ttk.Treeview(self.content_area, columns=("Date", "Enseignant", "Cours", "Moyenne"), show="headings")
        self.evaluations_tree.heading("Date", text="Date")
        self.evaluations_tree.heading("Enseignant", text="Enseignant")
        self.evaluations_tree.heading("Cours", text="Cours")
        self.evaluations_tree.heading("Moyenne", text="Moyenne")
        
        self.evaluations_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les évaluations
        self.load_evaluations()
    
    def show_received_evaluations(self):
        """Afficher les évaluations reçues par l'enseignant"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📊 Mes évaluations reçues",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Rafraîchir",
            command=self.refresh_received_evaluations,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Treeview pour afficher les évaluations
        self.received_evaluations_tree = ttk.Treeview(self.content_area, columns=("Date", "Étudiant", "Cours", "Moyenne", "Commentaire"), show="headings")
        self.received_evaluations_tree.heading("Date", text="Date")
        self.received_evaluations_tree.heading("Étudiant", text="Étudiant")
        self.received_evaluations_tree.heading("Cours", text="Cours")
        self.received_evaluations_tree.heading("Moyenne", text="Moyenne")
        self.received_evaluations_tree.heading("Commentaire", text="Commentaire")
        
        self.received_evaluations_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les évaluations reçues
        self.load_received_evaluations()
    
    def show_teacher_stats(self):
        """Afficher les statistiques de l'enseignant"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📈 Mes statistiques",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Rafraîchir",
            command=self.refresh_teacher_stats,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Zone de texte pour les statistiques
        self.stats_text = ctk.CTkTextbox(self.content_area, height=400)
        self.stats_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les statistiques
        self.load_teacher_stats_text()
    
    def show_user_management(self):
        """Afficher la gestion des utilisateurs"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="👥 Gestion des utilisateurs",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)
        
        add_user_button = ctk.CTkButton(
            buttons_frame,
            text="➕ Ajouter un utilisateur",
            command=self.add_user,
            width=150
        )
        add_user_button.pack(side="left", padx=5)
        
        refresh_users_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Rafraîchir",
            command=self.refresh_users,
            width=100
        )
        refresh_users_button.pack(side="left", padx=5)
        
        # Treeview pour afficher les utilisateurs
        self.users_tree = ttk.Treeview(self.content_area, columns=("ID", "Nom", "Statut", "Année"), show="headings")
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Nom", text="Nom")
        self.users_tree.heading("Statut", text="Statut")
        self.users_tree.heading("Année", text="Année académique")
        
        self.users_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les utilisateurs
        self.load_users()
    
    def show_all_evaluations(self):
        """Afficher toutes les évaluations"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📋 Toutes les évaluations",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Rafraîchir",
            command=self.refresh_all_evaluations,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Treeview pour afficher toutes les évaluations
        self.all_evaluations_tree = ttk.Treeview(self.content_area, columns=("Date", "Étudiant", "Enseignant", "Cours", "Moyenne"), show="headings")
        self.all_evaluations_tree.heading("Date", text="Date")
        self.all_evaluations_tree.heading("Étudiant", text="Étudiant")
        self.all_evaluations_tree.heading("Enseignant", text="Enseignant")
        self.all_evaluations_tree.heading("Cours", text="Cours")
        self.all_evaluations_tree.heading("Moyenne", text="Moyenne")
        
        self.all_evaluations_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger toutes les évaluations
        self.load_all_evaluations()
    
    def show_global_stats(self):
        """Afficher les statistiques globales"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📊 Statistiques globales",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Rafraîchir",
            command=self.refresh_global_stats,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Zone de texte pour les statistiques
        self.global_stats_text = ctk.CTkTextbox(self.content_area, height=400)
        self.global_stats_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les statistiques globales
        self.load_global_stats_text()
    
    def show_reports(self):
        """Afficher les rapports"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="📄 Rapports",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(self.content_area)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)
        
        generate_report_button = ctk.CTkButton(
            buttons_frame,
            text="📊 Générer rapport global",
            command=self.generate_global_report,
            width=150
        )
        generate_report_button.pack(side="left", padx=5)
        
        export_data_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Exporter données (JSON)",
            command=self.export_data,
            width=150
        )
        export_data_button.pack(side="left", padx=5)
        
        # Zone de texte pour afficher les rapports
        self.reports_text = ctk.CTkTextbox(self.content_area, height=400)
        self.reports_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def show_profile(self):
        """Afficher le profil utilisateur"""
        self.clear_content_area()
        
        # Titre
        title_label = ctk.CTkLabel(
            self.content_area,
            text="👤 Mon profil",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Informations du profil
        profile_frame = ctk.CTkFrame(self.content_area)
        profile_frame.pack(fill="x", padx=20, pady=10)
        
        profile_info = [
            f"ID: {self.user.id}",
            f"Nom: {self.user.nom_prenom}",
            f"Statut: {self.user.statut}",
            f"Année académique: {self.user.annee_academique}"
        ]
        
        for info in profile_info:
            ctk.CTkLabel(profile_frame, text=info, font=ctk.CTkFont(size=14)).pack(pady=5)
    
    # Méthodes utilitaires
    def get_teachers_list(self):
        """Récupérer la liste des enseignants"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nom_prenom FROM utilisateurs 
                    WHERE statut = 'enseignant' 
                    ORDER BY nom_prenom
                """)
                teachers = cursor.fetchall()
                cursor.close()
                conn.close()
                
                return [f"{teacher[0]} - {teacher[1]}" for teacher in teachers]
        except Exception as e:
            print(f"Erreur lors de la récupération des enseignants: {e}")
        return []
    
    def get_courses_list(self):
        """Récupérer la liste des cours"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT code_cours, titre FROM cours 
                    ORDER BY titre
                """)
                courses = cursor.fetchall()
                cursor.close()
                conn.close()
                
                return [f"{course[0]} - {course[1]}" for course in courses]
        except Exception as e:
            print(f"Erreur lors de la récupération des cours: {e}")
        return []
    
    def submit_evaluation(self):
        """Soumettre une évaluation"""
        # Récupérer les valeurs des sliders
        evaluation_data = {}
        for key, slider in self.criteria_sliders.items():
            evaluation_data[key] = int(slider.get())
        
        # Récupérer le commentaire
        evaluation_data['commentaire_general'] = self.comment_text.get("1.0", "end-1c")
        
        # Récupérer l'enseignant et le cours sélectionnés
        teacher_selection = self.teacher_combobox.get()
        course_selection = self.course_combobox.get()
        
        if not teacher_selection or not course_selection:
            messagebox.showerror("❌ Erreur", "Veuillez sélectionner un enseignant et un cours.")
            return
        
        teacher_id = teacher_selection.split(" - ")[0]
        course_code = course_selection.split(" - ")[0]
        
        # Créer l'évaluation
        evaluation = Evaluation(
            date_evaluation=datetime.now().date(),
            id_etudiant=self.user.id,
            id_enseignant=teacher_id,
            code_cours=course_code,
            **evaluation_data
        )
        
        # Sauvegarder l'évaluation
        if evaluation.sauvegarder():
            messagebox.showinfo("✅ Succès", "Évaluation soumise avec succès!")
            # Réinitialiser le formulaire
            self.reset_evaluation_form()
        else:
            messagebox.showerror("❌ Erreur", "Erreur lors de la soumission de l'évaluation.")
    
    def reset_evaluation_form(self):
        """Réinitialiser le formulaire d'évaluation"""
        # Réinitialiser les sliders
        for slider in self.criteria_sliders.values():
            slider.set(3)
        
        # Réinitialiser le commentaire
        self.comment_text.delete("1.0", "end")
    
    def load_evaluations(self):
        """Charger les évaluations de l'étudiant"""
        # Vider le treeview
        for item in self.evaluations_tree.get_children():
            self.evaluations_tree.delete(item)
        
        # Charger les évaluations
        evaluations = self.user.consulterEvaluations()
        for evaluation in evaluations:
            moyenne = evaluation.calculerMoyenneGlobale()
            self.evaluations_tree.insert("", "end", values=(
                evaluation.date_evaluation,
                evaluation.id_enseignant,
                evaluation.code_cours,
                f"{moyenne:.2f}"
            ))
    
    def load_received_evaluations(self):
        """Charger les évaluations reçues par l'enseignant"""
        # Vider le treeview
        for item in self.received_evaluations_tree.get_children():
            self.received_evaluations_tree.delete(item)
        
        # Charger les évaluations reçues
        evaluations = self.user.consulterEvaluationsRecues()
        for evaluation in evaluations:
            moyenne = evaluation.calculerMoyenneGlobale()
            commentaire = evaluation.commentaire_general or ""
            self.received_evaluations_tree.insert("", "end", values=(
                evaluation.date_evaluation,
                evaluation.id_etudiant,
                evaluation.code_cours,
                f"{moyenne:.2f}",
                commentaire[:50] + "..." if len(commentaire) > 50 else commentaire
            ))
    
    def load_teacher_stats_text(self):
        """Charger les statistiques de l'enseignant en texte"""
        stats = self.user.obtenirStatistiquesEvaluation()
        if stats:
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", f"📊 Statistiques pour {self.user.nom_prenom}\n\n")
            self.stats_text.insert("end", f"Nombre d'évaluations : {stats['nombre_evaluations']}\n")
            self.stats_text.insert("end", f"Moyenne globale : {stats['moyenne_globale']:.2f}/5\n\n")
            
            if 'criteres' in stats:
                self.stats_text.insert("end", "Moyennes par critère :\n")
                for critere, moyenne in stats['criteres'].items():
                    self.stats_text.insert("end", f"- {critere} : {moyenne:.2f}/5\n")
        else:
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", "Aucune évaluation disponible")
    
    def load_users(self):
        """Charger les utilisateurs"""
        # Vider le treeview
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Charger les utilisateurs
        users = self.user.gererUtilisateurs()
        for user in users:
            self.users_tree.insert("", "end", values=(
                user.id,
                user.nom_prenom,
                user.statut,
                user.annee_academique
            ))
    
    def load_all_evaluations(self):
        """Charger toutes les évaluations"""
        # Vider le treeview
        for item in self.all_evaluations_tree.get_children():
            self.all_evaluations_tree.delete(item)
        
        # Charger toutes les évaluations
        evaluations = self.user.consulterToutesEvaluations()
        for evaluation in evaluations:
            moyenne = evaluation.calculerMoyenneGlobale()
            self.all_evaluations_tree.insert("", "end", values=(
                evaluation.date_evaluation,
                getattr(evaluation, 'nom_etudiant', ''),
                getattr(evaluation, 'nom_enseignant', ''),
                getattr(evaluation, 'titre_cours', ''),
                f"{moyenne:.2f}"
            ))
    
    def load_global_stats_text(self):
        """Charger les statistiques globales en texte"""
        stats = self.user.genererRapportGlobal()
        if stats:
            self.global_stats_text.delete("1.0", "end")
            # Correction de l'erreur KeyError
            date_gen = stats.get('date_generation', 'Date inconnue')
            self.global_stats_text.insert("1.0", f"📊 Statistiques globales - {date_gen}\n\n")
            
            if 'statistiques_utilisateurs' in stats:
                self.global_stats_text.insert("end", "Statistiques des utilisateurs :\n")
                for statut, count in stats['statistiques_utilisateurs'].items():
                    self.global_stats_text.insert("end", f"- {statut} : {count}\n")
            
            self.global_stats_text.insert("end", f"\nTotal évaluations : {stats.get('total_evaluations', 0)}\n")
            self.global_stats_text.insert("end", f"Total cours : {stats.get('total_cours', 0)}\n")
        else:
            self.global_stats_text.delete("1.0", "end")
            self.global_stats_text.insert("1.0", "Aucune donnée disponible")
    
    def generate_global_report(self):
        """Générer un rapport global"""
        rapport = self.user.genererRapportGlobal()
        if rapport:
            # Afficher le rapport dans la zone de texte
            self.reports_text.delete("1.0", "end")
            date_gen = rapport.get('date_generation', 'Date inconnue')
            self.reports_text.insert("1.0", f"📊 Rapport Global - {date_gen}\n\n")
            self.reports_text.insert("end", f"Statistiques des utilisateurs:\n")
            for statut, count in rapport['statistiques_utilisateurs'].items():
                self.reports_text.insert("end", f"- {statut}: {count}\n")
            self.reports_text.insert("end", f"\nTotal évaluations: {rapport.get('total_evaluations', 0)}\n")
            self.reports_text.insert("end", f"Total cours: {rapport.get('total_cours', 0)}\n")
        else:
            messagebox.showerror("❌ Erreur", "Erreur lors de la génération du rapport.")
    
    def export_data(self):
        """Exporter les données"""
        filename = self.user.exporterDonnees('json')
        if filename:
            messagebox.showinfo("✅ Succès", f"Données exportées dans {filename}")
        else:
            messagebox.showerror("❌ Erreur", "Erreur lors de l'export des données.")
    
    # Méthodes de rafraîchissement
    def refresh_evaluations(self):
        self.load_evaluations()
    
    def refresh_received_evaluations(self):
        self.load_received_evaluations()
    
    def refresh_teacher_stats(self):
        self.load_teacher_stats_text()
    
    def refresh_users(self):
        self.load_users()
    
    def refresh_all_evaluations(self):
        self.load_all_evaluations()
    
    def refresh_global_stats(self):
        self.load_global_stats_text()
    
    def add_user(self):
        """Ajouter un utilisateur (à implémenter)"""
        messagebox.showinfo("ℹ️ Info", "Fonctionnalité d'ajout d'utilisateur à implémenter.")
    
    def logout(self):
        """Déconnexion"""
        self.root.destroy()
        login_window = LoginWindow()
        login_window.run()
    
    def on_closing(self):
        """Gestion de la fermeture de la fenêtre"""
        if messagebox.askokcancel("🚪 Quitter", "Voulez-vous vraiment quitter?"):
            self.root.destroy()
    
    def show(self):
        """Afficher la fenêtre"""
        self.root.deiconify()
        self.root.focus_force()

def main():
    """Fonction principale"""
    login_window = LoginWindow()
    login_window.run()

if __name__ == "__main__":
    main() 