import customtkinter as ctk
from tkinter import messagebox
from components import ModernTable, InfoCard, ModernForm, ModernChart, ModernSearch, ModernNotification
from models import *
from config import Config
import datetime

class EvaluationFormPage:
    """Page du formulaire d'évaluation moderne"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface"""
        # Titre
        title = ctk.CTkLabel(
            self.parent,
            text="📝 Évaluer un Enseignant",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Formulaire d'évaluation
        self.form = ModernForm(main_frame, "Formulaire d'évaluation")
        self.form.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Charger les cours disponibles
        self.load_courses()
        
        # Ajouter les champs
        self.form.add_field("Cours", "combobox", values=self.course_options)
        self.form.add_field("Enseignant", "combobox", values=self.teacher_options)
        
        # Critères d'évaluation
        criteria = Config.CRITERES_EVALUATION
        for criterion in criteria:
            self.form.add_field(
                criterion.replace('_', ' ').title(),
                "slider",
                from_=1,
                to=5,
                number_of_steps=4,
                command=lambda x, c=criterion: self.update_criterion_value(c, x)
            )
        
        # Commentaire
        self.form.add_field("Commentaire", "textbox", placeholder_text="Ajoutez votre commentaire...")
        
        # Boutons
        buttons_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=30, pady=20)
        
        # Bouton d'évaluation
        evaluate_btn = ctk.CTkButton(
            buttons_frame,
            text="📝 Soumettre l'évaluation",
            command=self.submit_evaluation,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        evaluate_btn.pack(side="left", padx=10)
        
        # Bouton de réinitialisation
        reset_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Réinitialiser",
            command=self.reset_form,
            width=150,
            height=50,
            font=ctk.CTkFont(size=14),
            fg_color="#FF9800",
            hover_color="#e68900"
        )
        reset_btn.pack(side="left", padx=10)
        
        # Stocker les valeurs des critères
        self.criterion_values = {}
    
    def load_courses(self):
        """Charger les cours et enseignants disponibles"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                
                # Charger les cours
                cursor.execute("SELECT nom_cours, code_cours FROM cours")
                courses = cursor.fetchall()
                self.course_options = [f"{course[1]} - {course[0]}" for course in courses]
                
                # Charger les enseignants
                cursor.execute("SELECT nom_prenom, identifiant FROM utilisateurs WHERE statut = 'enseignant'")
                teachers = cursor.fetchall()
                self.teacher_options = [f"{teacher[0]} ({teacher[1]})" for teacher in teachers]
                
                cursor.close()
                conn.close()
            else:
                self.course_options = ["Aucun cours disponible"]
                self.teacher_options = ["Aucun enseignant disponible"]
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.course_options = ["Erreur de chargement"]
            self.teacher_options = ["Erreur de chargement"]
    
    def update_criterion_value(self, criterion, value):
        """Mettre à jour la valeur d'un critère"""
        self.criterion_values[criterion] = value
    
    def submit_evaluation(self):
        """Soumettre l'évaluation"""
        values = self.form.get_values()
        
        # Validation
        if not values.get("Cours") or not values.get("Enseignant"):
            ModernNotification.show(self.parent, "Veuillez sélectionner un cours et un enseignant.", "error")
            return
        
        # Créer l'évaluation
        try:
            evaluation = Evaluation()
            evaluation.identifiant_etudiant = self.user.identifiant
            evaluation.code_cours = values["Cours"].split(" - ")[0]
            evaluation.identifiant_enseignant = values["Enseignant"].split("(")[1].split(")")[0]
            evaluation.commentaire = values.get("Commentaire", "")
            
            # Ajouter les notes des critères
            for criterion, value in self.criterion_values.items():
                setattr(evaluation, criterion, value)
            
            # Sauvegarder
            if evaluation.sauvegarderEvaluation():
                ModernNotification.show(self.parent, "Évaluation soumise avec succès !", "success")
                self.reset_form()
            else:
                ModernNotification.show(self.parent, "Erreur lors de la sauvegarde.", "error")
                
        except Exception as e:
            ModernNotification.show(self.parent, f"Erreur: {str(e)}", "error")
    
    def reset_form(self):
        """Réinitialiser le formulaire"""
        for field in self.form.fields.values():
            if hasattr(field, 'delete'):
                field.delete(0, 'end')
            elif hasattr(field, 'set'):
                field.set("")
            elif hasattr(field, 'set'):
                field.set(1)  # Pour les sliders
        
        self.criterion_values = {}

class MyEvaluationsPage:
    """Page des évaluations de l'étudiant"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface"""
        # Titre
        title = ctk.CTkLabel(
            self.parent,
            text="📋 Mes Évaluations",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)
        
        # Barre de recherche
        self.search = ModernSearch(self.parent, "Rechercher dans mes évaluations...")
        self.search.pack(fill="x", padx=30, pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Tableau des évaluations
        columns = ["Cours", "Enseignant", "Date", "Moyenne", "Actions"]
        self.table = ModernTable(main_frame, columns)
        self.table.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Charger les données
        self.load_evaluations()
    
    def load_evaluations(self):
        """Charger les évaluations de l'étudiant"""
        try:
            evaluations = self.user.consulterEvaluations()
            
            # Convertir en format pour le tableau
            table_data = []
            for eval_obj in evaluations:
                # Calculer la moyenne
                moyenne = eval_obj.calculerMoyenneGlobale()
                
                # Formater la date
                date_str = eval_obj.date_evaluation.strftime("%d/%m/%Y") if eval_obj.date_evaluation else "N/A"
                
                table_data.append([
                    eval_obj.code_cours,
                    eval_obj.identifiant_enseignant,
                    date_str,
                    f"{moyenne:.2f}/5",
                    "📝 Modifier | 🗑️ Supprimer"
                ])
            
            self.table.insert_data(table_data)
            
        except Exception as e:
            ModernNotification.show(self.parent, f"Erreur lors du chargement: {str(e)}", "error")

class TeacherStatsPage:
    """Page des statistiques de l'enseignant"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface"""
        # Titre
        title = ctk.CTkLabel(
            self.parent,
            text="📈 Mes Statistiques",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Cartes de statistiques
        self.create_stats_cards(main_frame)
        
        # Graphiques
        self.create_charts(main_frame)
    
    def create_stats_cards(self, parent):
        """Créer les cartes de statistiques"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        try:
            # Obtenir les statistiques
            stats = self.user.obtenirStatistiquesEvaluation()
            
            # Créer les cartes
            cards_data = [
                ("Total Évaluations", stats.get('total_evaluations', 0), "#2196F3"),
                ("Moyenne Globale", f"{stats.get('moyenne_globale', 0):.2f}/5", "#4CAF50"),
                ("Note la plus élevée", f"{stats.get('note_max', 0):.1f}/5", "#FF9800"),
                ("Note la plus basse", f"{stats.get('note_min', 0):.1f}/5", "#F44336")
            ]
            
            for title, value, color in cards_data:
                card = InfoCard(stats_frame, title, value, color=color)
                card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                
        except Exception as e:
            ModernNotification.show(self.parent, f"Erreur lors du chargement des statistiques: {str(e)}", "error")
    
    def create_charts(self, parent):
        """Créer les graphiques"""
        charts_frame = ctk.CTkFrame(parent, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, pady=20)
        
        try:
            # Graphique des moyennes par critère
            stats = self.user.obtenirStatistiquesEvaluation()
            
            if 'moyennes_criteres' in stats:
                criteria = list(stats['moyennes_criteres'].keys())
                values = list(stats['moyennes_criteres'].values())
                
                chart = ModernChart(charts_frame, "Moyennes par critère")
                chart.pack(fill="both", expand=True, padx=20, pady=20)
                chart.create_bar_chart(values, criteria, "Moyennes par critère d'évaluation")
            
        except Exception as e:
            ModernNotification.show(self.parent, f"Erreur lors de la création des graphiques: {str(e)}", "error")

class UserManagementPage:
    """Page de gestion des utilisateurs (admin)"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface"""
        # Titre
        title = ctk.CTkLabel(
            self.parent,
            text="👥 Gestion des Utilisateurs",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)
        
        # Barre d'outils
        toolbar_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=30, pady=10)
        
        # Barre de recherche
        self.search = ModernSearch(toolbar_frame, "Rechercher un utilisateur...")
        self.search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton d'ajout
        add_btn = ctk.CTkButton(
            toolbar_frame,
            text="➕ Ajouter un utilisateur",
            command=self.show_add_user_form,
            width=200,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        add_btn.pack(side="right", padx=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Tableau des utilisateurs
        columns = ["Identifiant", "Nom", "Statut", "Année", "Actions"]
        self.table = ModernTable(main_frame, columns)
        self.table.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Charger les données
        self.load_users()
    
    def load_users(self):
        """Charger la liste des utilisateurs"""
        try:
            # Obtenir tous les utilisateurs
            all_users = self.user.consulterTousUtilisateurs()
            
            # Convertir en format pour le tableau
            table_data = []
            for user in all_users:
                table_data.append([
                    user.identifiant,
                    user.nom_prenom,
                    user.statut,
                    user.annee_academique,
                    "✏️ Modifier | 🗑️ Supprimer"
                ])
            
            self.table.insert_data(table_data)
            
        except Exception as e:
            ModernNotification.show(self.parent, f"Erreur lors du chargement: {str(e)}", "error")
    
    def show_add_user_form(self):
        """Afficher le formulaire d'ajout d'utilisateur"""
        # Créer une nouvelle fenêtre
        form_window = ctk.CTkToplevel()
        form_window.title("Ajouter un utilisateur")
        form_window.geometry("500x600")
        form_window.configure(fg_color="#1a1a1a")
        
        # Centrer la fenêtre
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"500x600+{x}+{y}")
        
        # Formulaire
        form = ModernForm(form_window, "Nouvel utilisateur")
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Champs
        form.add_field("Identifiant", "entry", placeholder_text="Ex: ETU001")
        form.add_field("Nom et Prénom", "entry", placeholder_text="Ex: Jean Dupont")
        form.add_field("Genre", "combobox", values=["M", "F"])
        form.add_field("Mot de passe", "entry", show="*", placeholder_text="Mot de passe")
        form.add_field("Année académique", "entry", placeholder_text="Ex: 2024-2025")
        form.add_field("Statut", "combobox", values=["étudiant", "enseignant", "administrateur"])
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_window, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Sauvegarder",
            command=lambda: self.save_user(form, form_window),
            width=150,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Annuler",
            command=form_window.destroy,
            width=150,
            height=40,
            fg_color="#F44336",
            hover_color="#d32f2f"
        )
        cancel_btn.pack(side="left", padx=10)
    
    def save_user(self, form, window):
        """Sauvegarder le nouvel utilisateur"""
        values = form.get_values()
        
        # Validation
        required_fields = ["Identifiant", "Nom et Prénom", "Mot de passe", "Statut"]
        for field in required_fields:
            if not values.get(field):
                ModernNotification.show(window, f"Le champ '{field}' est obligatoire.", "error")
                return
        
        try:
            # Créer l'utilisateur
            user = Utilisateur()
            user.identifiant = values["Identifiant"]
            user.nom_prenom = values["Nom et Prénom"]
            user.genre = values.get("Genre", "M")
            user.mot_de_passe = values["Mot de passe"]
            user.annee_academique = values.get("Année académique", "2024-2025")
            user.statut = values["Statut"]
            
            # Sauvegarder
            if user.creerUtilisateur():
                ModernNotification.show(window, "Utilisateur créé avec succès !", "success")
                window.destroy()
                self.load_users()  # Recharger la liste
            else:
                ModernNotification.show(window, "Erreur lors de la création.", "error")
                
        except Exception as e:
            ModernNotification.show(window, f"Erreur: {str(e)}", "error")

class GlobalStatsPage:
    """Page des statistiques globales (admin)"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface"""
        # Titre
        title = ctk.CTkLabel(
            self.parent,
            text="📊 Statistiques Globales",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Charger les statistiques
        self.load_global_stats(main_frame)
    
    def load_global_stats(self, parent):
        """Charger les statistiques globales"""
        try:
            # Obtenir le rapport global
            rapport = self.user.genererRapportGlobal()
            
            if rapport:
                # Cartes de statistiques
                stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
                stats_frame.pack(fill="x", pady=20)
                
                cards_data = [
                    ("Total Utilisateurs", rapport.get('total_utilisateurs', 0), "#2196F3"),
                    ("Total Évaluations", rapport.get('total_evaluations', 0), "#4CAF50"),
                    ("Total Cours", rapport.get('total_cours', 0), "#FF9800"),
                    ("Date de génération", rapport.get('date_generation', 'N/A'), "#9C27B0")
                ]
                
                for title, value, color in cards_data:
                    card = InfoCard(stats_frame, title, value, color=color)
                    card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                
                # Graphiques
                charts_frame = ctk.CTkFrame(parent, fg_color="transparent")
                charts_frame.pack(fill="both", expand=True, pady=20)
                
                # Répartition des utilisateurs
                if 'statistiques_utilisateurs' in rapport:
                    users_data = list(rapport['statistiques_utilisateurs'].values())
                    users_labels = list(rapport['statistiques_utilisateurs'].keys())
                    
                    chart = ModernChart(charts_frame, "Répartition des utilisateurs")
                    chart.pack(fill="both", expand=True, padx=20, pady=20)
                    chart.create_pie_chart(users_data, users_labels, "Répartition par statut")
            
        except Exception as e:
            ModernNotification.show(self.parent, f"Erreur lors du chargement des statistiques: {str(e)}", "error") 