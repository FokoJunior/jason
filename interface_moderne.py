import customtkinter as ctk
from tkinter import messagebox, ttk
import datetime
from datetime import datetime
from models import *
from config import Config
from components import ModernTable, InfoCard, ModernForm, ModernChart, ModernSearch, ModernNotification
from pages import EvaluationFormPage, MyEvaluationsPage, TeacherStatsPage, UserManagementPage, GlobalStatsPage

# Configuration de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernAppBar(ctk.CTkFrame):
    """AppBar moderne et dynamique"""
    
    def __init__(self, parent, user, on_logout):
        super().__init__(parent, height=70, fg_color="#1a1a1a", corner_radius=0)
        self.pack(fill="x", padx=0, pady=0)
        self.pack_propagate(False)
        
        # Logo et titre
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="🎓 Système d'Évaluation",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")
        
        # Informations utilisateur à droite
        user_frame = ctk.CTkFrame(self, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=15)
        
        # Icône selon le statut
        icons = {
            'étudiant': '👨‍🎓',
            'enseignant': '👨‍🏫', 
            'administrateur': '👨‍💼'
        }
        icon = icons.get(user.statut, '👤')
        
        # Nom et statut de l'utilisateur
        user_info = ctk.CTkLabel(
            user_frame,
            text=f"{icon} {user.nom_prenom}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        user_info.pack(side="left", padx=10)
        
        # Statut
        status_label = ctk.CTkLabel(
            user_frame,
            text=f"({user.statut})",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        status_label.pack(side="left", padx=5)
        
        # Heure actuelle
        self.time_label = ctk.CTkLabel(
            user_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.time_label.pack(side="left", padx=20)
        
        # Bouton de déconnexion
        logout_btn = ctk.CTkButton(
            user_frame,
            text="🚪 Déconnexion",
            command=on_logout,
            width=120,
            height=35,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        logout_btn.pack(side="left", padx=10)
        
        # Mettre à jour l'heure
        self.update_time()
    
    def update_time(self):
        """Mettre à jour l'heure affichée"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"🕐 {current_time}")
        self.after(1000, self.update_time)

class ModernSidebar(ctk.CTkFrame):
    """Sidebar moderne avec navigation"""
    
    def __init__(self, parent, user, on_nav):
        super().__init__(parent, width=280, fg_color="#2d2d2d", corner_radius=0)
        self.pack(side="left", fill="y", padx=0, pady=0)
        self.pack_propagate(False)
        
        self.user = user
        self.on_nav = on_nav
        self.active_button = None
        
        # Titre du menu
        title_label = ctk.CTkLabel(
            self,
            text="📋 Navigation",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=30, padx=20)
        
        # Créer les boutons selon le type d'utilisateur
        if user.statut == 'étudiant':
            self.create_student_menu()
        elif user.statut == 'enseignant':
            self.create_teacher_menu()
        elif user.statut == 'administrateur':
            self.create_admin_menu()
    
    def create_menu_button(self, text, command, icon="📄"):
        """Créer un bouton de menu stylisé"""
        btn = ctk.CTkButton(
            self,
            text=f"{icon} {text}",
            command=lambda: self.handle_nav(command),
            width=240,
            height=50,
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff",
            corner_radius=10
        )
        btn.pack(pady=8, padx=20)
        return btn
    
    def handle_nav(self, command):
        """Gérer la navigation et mettre à jour l'apparence"""
        # Réinitialiser tous les boutons
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color="#3a3a3a")
        
        # Mettre en surbrillance le bouton actif
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == command.__name__:
                widget.configure(fg_color="#007acc")
                break
        
        # Appeler la fonction de navigation
        command()
    
    def create_student_menu(self):
        """Menu pour les étudiants"""
        menu_items = [
            ("Tableau de bord", self.show_dashboard, "📊"),
            ("Évaluer un enseignant", self.show_evaluation_form, "📝"),
            ("Mes évaluations", self.show_my_evaluations, "📋"),
            ("Rechercher des cours", self.show_course_search, "🔍"),
            ("Mon profil", self.show_profile, "👤")
        ]
        
        for text, command, icon in menu_items:
            self.create_menu_button(text, command, icon)
    
    def create_teacher_menu(self):
        """Menu pour les enseignants"""
        menu_items = [
            ("Tableau de bord", self.show_dashboard, "📊"),
            ("Mes évaluations reçues", self.show_received_evaluations, "📋"),
            ("Mes statistiques", self.show_teacher_stats, "📈"),
            ("Mes cours", self.show_teacher_courses, "📚"),
            ("Mon profil", self.show_profile, "👤")
        ]
        
        for text, command, icon in menu_items:
            self.create_menu_button(text, command, icon)
    
    def create_admin_menu(self):
        """Menu pour les administrateurs"""
        menu_items = [
            ("Tableau de bord", self.show_dashboard, "📊"),
            ("Gestion des utilisateurs", self.show_user_management, "👥"),
            ("Toutes les évaluations", self.show_all_evaluations, "📋"),
            ("Statistiques globales", self.show_global_stats, "📈"),
            ("Rapports", self.show_reports, "📄"),
            ("Mon profil", self.show_profile, "👤")
        ]
        
        for text, command, icon in menu_items:
            self.create_menu_button(text, command, icon)
    
    # Méthodes de navigation
    def show_dashboard(self): self.on_nav("dashboard")
    def show_evaluation_form(self): self.on_nav("evaluation_form")
    def show_my_evaluations(self): self.on_nav("my_evaluations")
    def show_course_search(self): self.on_nav("course_search")
    def show_profile(self): self.on_nav("profile")
    def show_received_evaluations(self): self.on_nav("received_evaluations")
    def show_teacher_stats(self): self.on_nav("teacher_stats")
    def show_teacher_courses(self): self.on_nav("teacher_courses")
    def show_user_management(self): self.on_nav("user_management")
    def show_all_evaluations(self): self.on_nav("all_evaluations")
    def show_global_stats(self): self.on_nav("global_stats")
    def show_reports(self): self.on_nav("reports")

class ModernDashboard(ctk.CTk):
    """Dashboard moderne avec AppBar et Sidebar"""
    
    def __init__(self, user):
        super().__init__()
        
        self.user = user
        self.current_page = None
        self.content_area = None
        
        # Configuration de la fenêtre
        self.title("Système d'Évaluation des Enseignants")
        self.geometry("1600x900")
        self.configure(fg_color="#1a1a1a")
        
        # Centrer la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1600 // 2)
        y = (self.winfo_screenheight() // 2) - (900 // 2)
        self.geometry(f"1600x900+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # AppBar
        self.appbar = ModernAppBar(self, self.user, self.logout)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Sidebar
        self.sidebar = ModernSidebar(main_frame, self.user, self.navigate_to)
        
        # Zone de contenu
        self.content_area = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Afficher la page par défaut
        self.show_dashboard()
    
    def navigate_to(self, page):
        """Navigation vers une page"""
        self.clear_content()
        
        if page == "dashboard":
            self.show_dashboard()
        elif page == "evaluation_form":
            self.show_evaluation_form()
        elif page == "my_evaluations":
            self.show_my_evaluations()
        elif page == "course_search":
            self.show_course_search()
        elif page == "profile":
            self.show_profile()
        elif page == "received_evaluations":
            self.show_received_evaluations()
        elif page == "teacher_stats":
            self.show_teacher_stats()
        elif page == "teacher_courses":
            self.show_teacher_courses()
        elif page == "user_management":
            self.show_user_management()
        elif page == "all_evaluations":
            self.show_all_evaluations()
        elif page == "global_stats":
            self.show_global_stats()
        elif page == "reports":
            self.show_reports()
    
    def clear_content(self):
        """Vider la zone de contenu"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Afficher le tableau de bord"""
        # Titre
        title = ctk.CTkLabel(
            self.content_area,
            text="📊 Tableau de Bord",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)
        
        # Cartes d'informations
        cards_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=20)
        
        # Carte de bienvenue
        welcome_card = ctk.CTkFrame(cards_frame, fg_color="#3a3a3a", corner_radius=15)
        welcome_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            welcome_card,
            text=f"👋 Bienvenue, {self.user.nom_prenom} !",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=20)
        
        ctk.CTkLabel(
            welcome_card,
            text=f"Rôle : {self.user.statut} | Année : {self.user.annee_academique}",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        ).pack(pady=10)
        
        # Statistiques rapides
        stats_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        # Charger les statistiques selon le rôle
        if self.user.statut == 'étudiant':
            self.load_student_dashboard_stats(stats_frame)
        elif self.user.statut == 'enseignant':
            self.load_teacher_dashboard_stats(stats_frame)
        elif self.user.statut == 'administrateur':
            self.load_admin_dashboard_stats(stats_frame)
    
    def load_student_dashboard_stats(self, parent):
        """Charger les statistiques du tableau de bord étudiant"""
        # Carte des évaluations
        eval_card = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=15)
        eval_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            eval_card,
            text="📝 Mes Évaluations",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=15)
        
        # Charger les évaluations de l'étudiant
        evaluations = self.user.consulterEvaluations()
        count = len(evaluations)
        
        ctk.CTkLabel(
            eval_card,
            text=f"{count} évaluation(s)",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CAF50"
        ).pack(pady=10)
        
        # Carte des cours
        course_card = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=15)
        course_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            course_card,
            text="📚 Cours Disponibles",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=15)
        
        # Charger les cours
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cours")
                course_count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                
                ctk.CTkLabel(
                    course_card,
                    text=f"{course_count} cours",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#2196F3"
                ).pack(pady=10)
        except:
            ctk.CTkLabel(
                course_card,
                text="N/A",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#888888"
            ).pack(pady=10)
    
    def load_teacher_dashboard_stats(self, parent):
        """Charger les statistiques du tableau de bord enseignant"""
        # Carte des évaluations reçues
        eval_card = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=15)
        eval_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            eval_card,
            text="📊 Évaluations Reçues",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=15)
        
        # Charger les évaluations reçues
        evaluations = self.user.consulterEvaluationsRecues()
        count = len(evaluations)
        
        ctk.CTkLabel(
            eval_card,
            text=f"{count} évaluation(s)",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF9800"
        ).pack(pady=10)
        
        # Carte de la moyenne
        avg_card = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=15)
        avg_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            avg_card,
            text="⭐ Moyenne Globale",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=15)
        
        # Calculer la moyenne
        if evaluations:
            total = sum(eval_obj.calculerMoyenneGlobale() for eval_obj in evaluations)
            avg = total / len(evaluations)
            avg_text = f"{avg:.2f}/5"
            avg_color = "#4CAF50" if avg >= 4.0 else "#FF9800" if avg >= 3.0 else "#F44336"
        else:
            avg_text = "N/A"
            avg_color = "#888888"
        
        ctk.CTkLabel(
            avg_card,
            text=avg_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=avg_color
        ).pack(pady=10)
    
    def load_admin_dashboard_stats(self, parent):
        """Charger les statistiques du tableau de bord administrateur"""
        # Carte des utilisateurs
        users_card = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=15)
        users_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            users_card,
            text="👥 Utilisateurs",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=15)
        
        # Charger le nombre d'utilisateurs
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM utilisateurs")
                user_count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                
                ctk.CTkLabel(
                    users_card,
                    text=f"{user_count} utilisateurs",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#2196F3"
                ).pack(pady=10)
        except:
            ctk.CTkLabel(
                users_card,
                text="N/A",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#888888"
            ).pack(pady=10)
        
        # Carte des évaluations
        eval_card = ctk.CTkFrame(parent, fg_color="#3a3a3a", corner_radius=15)
        eval_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            eval_card,
            text="📋 Évaluations",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=15)
        
        # Charger le nombre d'évaluations
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM evaluations")
                eval_count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                
                ctk.CTkLabel(
                    eval_card,
                    text=f"{eval_count} évaluations",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#4CAF50"
                ).pack(pady=10)
        except:
            ctk.CTkLabel(
                eval_card,
                text="N/A",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#888888"
            ).pack(pady=10)
    
    def logout(self):
        """Déconnexion"""
        if messagebox.askokcancel("🚪 Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.destroy()
            # Retourner à la fenêtre de connexion
            login_window = ModernLoginWindow()
            login_window.run()
    
    # Méthodes pour les pages avec les nouvelles implémentations
    def show_evaluation_form(self):
        """Afficher le formulaire d'évaluation"""
        self.clear_content()
        EvaluationFormPage(self.content_area, self.user)
    
    def show_my_evaluations(self):
        """Afficher mes évaluations"""
        self.clear_content()
        MyEvaluationsPage(self.content_area, self.user)
    
    def show_teacher_stats(self):
        """Afficher les statistiques de l'enseignant"""
        self.clear_content()
        TeacherStatsPage(self.content_area, self.user)
    
    def show_user_management(self):
        """Afficher la gestion des utilisateurs"""
        self.clear_content()
        UserManagementPage(self.content_area, self.user)
    
    def show_global_stats(self):
        """Afficher les statistiques globales"""
        self.clear_content()
        GlobalStatsPage(self.content_area, self.user)
    
    # Méthodes temporaires pour les autres pages
    def show_course_search(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="🔍 Recherche de cours", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        # TODO: Implémenter la recherche de cours
    
    def show_profile(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="👤 Mon profil", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        # TODO: Implémenter l'affichage du profil
    
    def show_received_evaluations(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="📊 Évaluations reçues", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        # TODO: Implémenter l'affichage des évaluations reçues
    
    def show_teacher_courses(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="📚 Mes cours", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        # TODO: Implémenter l'affichage des cours
    
    def show_all_evaluations(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="📋 Toutes les évaluations", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        # TODO: Implémenter l'affichage de toutes les évaluations
    
    def show_reports(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="📄 Rapports", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
        # TODO: Implémenter l'affichage des rapports

class ModernLoginWindow(ctk.CTk):
    """Fenêtre de connexion moderne"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Système d'Évaluation des Enseignants - Connexion")
        self.geometry("600x500")
        self.configure(fg_color="#1a1a1a")
        self.resizable(False, False)
        
        # Centrer la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"600x500+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Titre principal
        title_label = ctk.CTkLabel(
            self, 
            text="🎓 Système d'Évaluation des Enseignants",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=40)
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            self,
            text="Connectez-vous pour accéder au système",
            font=ctk.CTkFont(size=16),
            text_color="#cccccc"
        )
        subtitle_label.pack(pady=10)
        
        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(self, fg_color="#2d2d2d", corner_radius=20)
        form_frame.pack(pady=40, padx=60, fill="both", expand=True)
        
        # Identifiant
        ctk.CTkLabel(form_frame, text="👤 Identifiant:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#ffffff").pack(pady=(30, 10))
        
        self.login_entry = ctk.CTkEntry(
            form_frame, 
            width=400,
            height=50,
            placeholder_text="Entrez votre identifiant...",
            font=ctk.CTkFont(size=14),
            fg_color="#3a3a3a",
            border_color="#007acc",
            text_color="#ffffff"
        )
        self.login_entry.pack(pady=(0, 20))
        
        # Mot de passe
        ctk.CTkLabel(form_frame, text="🔒 Mot de passe:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#ffffff").pack(pady=(0, 10))
        
        self.password_entry = ctk.CTkEntry(
            form_frame, 
            width=400,
            height=50,
            show="*",
            placeholder_text="Entrez votre mot de passe...",
            font=ctk.CTkFont(size=14),
            fg_color="#3a3a3a",
            border_color="#007acc",
            text_color="#ffffff"
        )
        self.password_entry.pack(pady=(0, 30))
        
        # Bouton de connexion
        login_button = ctk.CTkButton(
            form_frame,
            text="🚀 Se connecter",
            command=self.login,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#007acc",
            hover_color="#005a9e"
        )
        login_button.pack(pady=20)
        
        # Informations de test
        info_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        info_frame.pack(pady=30)
        
        ctk.CTkLabel(info_frame, text="📋 Comptes de test:", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#ffffff").pack()
        
        test_accounts = [
            "👨‍💼 ADMIN001 / admin123",
            "👨‍🏫 ENS001 / enseignant123", 
            "👨‍🎓 ETU001 / etudiant123"
        ]
        
        for account in test_accounts:
            ctk.CTkLabel(info_frame, text=account, 
                        font=ctk.CTkFont(size=12),
                        text_color="#888888").pack(pady=2)
        
        # Lier la touche Entrée
        self.bind('<Return>', lambda event: self.login())
        
        # Focus sur le premier champ
        self.login_entry.focus()
    
    def login(self):
        """Authentification de l'utilisateur"""
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not login or not password:
            messagebox.showerror("❌ Erreur", "Veuillez remplir tous les champs.")
            return
        
        # Afficher un indicateur de chargement
        self.config(cursor="wait")
        self.update()
        
        try:
            # Tentative de connexion
            user = Utilisateur()
            if user.seConnecter(login, password):
                # Créer l'utilisateur approprié selon le statut
                if user.statut == 'étudiant':
                    current_user = Etudiant()
                    current_user.__dict__.update(user.__dict__)
                    welcome_msg = f"👨‍🎓 Bienvenue, {user.nom_prenom} !"
                elif user.statut == 'enseignant':
                    current_user = Enseignant()
                    current_user.__dict__.update(user.__dict__)
                    welcome_msg = f"👨‍🏫 Bienvenue, {user.nom_prenom} !"
                elif user.statut == 'administrateur':
                    current_user = Administrateur()
                    current_user.__dict__.update(user.__dict__)
                    welcome_msg = f"👨‍💼 Bienvenue, {user.nom_prenom} !"
                else:
                    messagebox.showerror("❌ Erreur", "Statut utilisateur invalide.")
                    return
                
                # Ouvrir le dashboard moderne
                self.withdraw()
                dashboard = ModernDashboard(current_user)
                dashboard.mainloop()
                
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
            self.config(cursor="")
    
    def run(self):
        """Lancer l'application"""
        self.mainloop()

def main():
    """Fonction principale"""
    login_window = ModernLoginWindow()
    login_window.run()

if __name__ == "__main__":
    main() 