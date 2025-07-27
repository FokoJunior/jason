import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from models import *
from config import Config

# Configuration de CustomTkinter
ctk.set_appearance_mode(Config.THEME)
ctk.set_default_color_theme(Config.COLOR_THEME)

class LoginWindow:
    """Fenêtre de connexion"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Système d'Évaluation des Enseignants - Connexion")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
        
        self.current_user = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Titre
        title_label = ctk.CTkLabel(
            self.root, 
            text="Système d'Évaluation des Enseignants",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(self.root)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Identifiant
        ctk.CTkLabel(form_frame, text="Identifiant:").pack(pady=5)
        self.login_entry = ctk.CTkEntry(form_frame, width=250)
        self.login_entry.pack(pady=5)
        
        # Mot de passe
        ctk.CTkLabel(form_frame, text="Mot de passe:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(form_frame, width=250, show="*")
        self.password_entry.pack(pady=5)
        
        # Bouton de connexion
        login_button = ctk.CTkButton(
            form_frame,
            text="Se connecter",
            command=self.login,
            width=200
        )
        login_button.pack(pady=20)
        
        # Lier la touche Entrée
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus sur le premier champ
        self.login_entry.focus()
    
    def login(self):
        """Authentification de l'utilisateur"""
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not login or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
        
        # Tentative de connexion
        user = Utilisateur()
        if user.seConnecter(login, password):
            self.current_user = user
            
            # Créer l'utilisateur approprié selon le statut
            if user.statut == 'étudiant':
                self.current_user = Etudiant()
                self.current_user.__dict__.update(user.__dict__)
            elif user.statut == 'enseignant':
                self.current_user = Enseignant()
                self.current_user.__dict__.update(user.__dict__)
            elif user.statut == 'administrateur':
                self.current_user = Administrateur()
                self.current_user.__dict__.update(user.__dict__)
            
            # Ouvrir le tableau de bord approprié
            self.root.withdraw()
            dashboard = DashboardWindow(self.current_user)
            dashboard.show()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects.")
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()

class DashboardWindow:
    """Fenêtre du tableau de bord"""
    
    def __init__(self, user):
        self.user = user
        self.root = ctk.CTkToplevel()
        self.root.title(f"Tableau de Bord - {user.nom_prenom}")
        self.root.geometry("1200x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1200x700+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Barre de titre
        title_frame = ctk.CTkFrame(self.root)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            title_frame,
            text=f"Bienvenue, {self.user.nom_prenom} ({self.user.statut})",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=20, pady=10)
        
        # Bouton de déconnexion
        logout_button = ctk.CTkButton(
            title_frame,
            text="Déconnexion",
            command=self.logout,
            width=100
        )
        logout_button.pack(side="right", padx=20, pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Créer les onglets selon le type d'utilisateur
        if self.user.statut == 'étudiant':
            self.create_student_tabs(main_frame)
        elif self.user.statut == 'enseignant':
            self.create_teacher_tabs(main_frame)
        elif self.user.statut == 'administrateur':
            self.create_admin_tabs(main_frame)
    
    def create_student_tabs(self, parent):
        """Création des onglets pour les étudiants"""
        tabview = ctk.CTkTabview(parent)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Onglet Évaluer un enseignant
        evaluate_tab = tabview.add("Évaluer un enseignant")
        self.create_evaluation_form(evaluate_tab)
        
        # Onglet Mes évaluations
        my_evaluations_tab = tabview.add("Mes évaluations")
        self.create_my_evaluations_view(my_evaluations_tab)
        
        # Onglet Rechercher des cours
        search_courses_tab = tabview.add("Rechercher des cours")
        self.create_course_search_view(search_courses_tab)
    
    def create_teacher_tabs(self, parent):
        """Création des onglets pour les enseignants"""
        tabview = ctk.CTkTabview(parent)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Onglet Mes évaluations reçues
        evaluations_tab = tabview.add("Mes évaluations reçues")
        self.create_received_evaluations_view(evaluations_tab)
        
        # Onglet Statistiques
        stats_tab = tabview.add("Statistiques")
        self.create_teacher_stats_view(stats_tab)
        
        # Onglet Mes cours
        courses_tab = tabview.add("Mes cours")
        self.create_teacher_courses_view(courses_tab)
    
    def create_admin_tabs(self, parent):
        """Création des onglets pour les administrateurs"""
        tabview = ctk.CTkTabview(parent)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Onglet Gestion des utilisateurs
        users_tab = tabview.add("Gestion des utilisateurs")
        self.create_user_management_view(users_tab)
        
        # Onglet Toutes les évaluations
        all_evaluations_tab = tabview.add("Toutes les évaluations")
        self.create_all_evaluations_view(all_evaluations_tab)
        
        # Onglet Statistiques globales
        global_stats_tab = tabview.add("Statistiques globales")
        self.create_global_stats_view(global_stats_tab)
        
        # Onglet Rapports
        reports_tab = tabview.add("Rapports")
        self.create_reports_view(reports_tab)
    
    def create_evaluation_form(self, parent):
        """Formulaire d'évaluation pour les étudiants"""
        # Frame de sélection
        selection_frame = ctk.CTkFrame(parent)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(selection_frame, text="Sélectionner un enseignant et un cours:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Combobox pour les enseignants
        ctk.CTkLabel(selection_frame, text="Enseignant:").pack(pady=5)
        self.teacher_combobox = ctk.CTkComboBox(selection_frame, values=self.get_teachers_list())
        self.teacher_combobox.pack(pady=5)
        
        # Combobox pour les cours
        ctk.CTkLabel(selection_frame, text="Cours:").pack(pady=5)
        self.course_combobox = ctk.CTkComboBox(selection_frame, values=self.get_courses_list())
        self.course_combobox.pack(pady=5)
        
        # Frame pour les critères d'évaluation
        criteria_frame = ctk.CTkFrame(parent)
        criteria_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(criteria_frame, text="Critères d'évaluation (1-5):", 
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
        comment_frame = ctk.CTkFrame(parent)
        comment_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(comment_frame, text="Commentaire général:").pack(pady=5)
        self.comment_text = ctk.CTkTextbox(comment_frame, height=100)
        self.comment_text.pack(fill="x", padx=10, pady=5)
        
        # Bouton de soumission
        submit_button = ctk.CTkButton(
            parent,
            text="Soumettre l'évaluation",
            command=self.submit_evaluation,
            width=200
        )
        submit_button.pack(pady=20)
    
    def create_my_evaluations_view(self, parent):
        """Vue des évaluations de l'étudiant"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Mes évaluations:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="Rafraîchir",
            command=self.refresh_evaluations,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Treeview pour afficher les évaluations
        self.evaluations_tree = ttk.Treeview(parent, columns=("Date", "Enseignant", "Cours", "Moyenne"), show="headings")
        self.evaluations_tree.heading("Date", text="Date")
        self.evaluations_tree.heading("Enseignant", text="Enseignant")
        self.evaluations_tree.heading("Cours", text="Cours")
        self.evaluations_tree.heading("Moyenne", text="Moyenne")
        
        self.evaluations_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les évaluations
        self.load_evaluations()
    
    def create_received_evaluations_view(self, parent):
        """Vue des évaluations reçues pour les enseignants"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Évaluations reçues:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="Rafraîchir",
            command=self.refresh_received_evaluations,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Treeview pour afficher les évaluations
        self.received_evaluations_tree = ttk.Treeview(parent, columns=("Date", "Étudiant", "Cours", "Moyenne", "Commentaire"), show="headings")
        self.received_evaluations_tree.heading("Date", text="Date")
        self.received_evaluations_tree.heading("Étudiant", text="Étudiant")
        self.received_evaluations_tree.heading("Cours", text="Cours")
        self.received_evaluations_tree.heading("Moyenne", text="Moyenne")
        self.received_evaluations_tree.heading("Commentaire", text="Commentaire")
        
        self.received_evaluations_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les évaluations reçues
        self.load_received_evaluations()
    
    def create_teacher_stats_view(self, parent):
        """Vue des statistiques pour les enseignants"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Statistiques d'évaluation:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="Rafraîchir",
            command=self.refresh_teacher_stats,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Frame pour les statistiques
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Créer le graphique
        self.create_teacher_stats_chart(stats_frame)
    
    def create_user_management_view(self, parent):
        """Vue de gestion des utilisateurs pour les administrateurs"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Gestion des utilisateurs:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)
        
        add_user_button = ctk.CTkButton(
            buttons_frame,
            text="Ajouter un utilisateur",
            command=self.add_user,
            width=150
        )
        add_user_button.pack(side="left", padx=5)
        
        refresh_users_button = ctk.CTkButton(
            buttons_frame,
            text="Rafraîchir",
            command=self.refresh_users,
            width=100
        )
        refresh_users_button.pack(side="left", padx=5)
        
        # Treeview pour afficher les utilisateurs
        self.users_tree = ttk.Treeview(parent, columns=("ID", "Nom", "Statut", "Année"), show="headings")
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Nom", text="Nom")
        self.users_tree.heading("Statut", text="Statut")
        self.users_tree.heading("Année", text="Année académique")
        
        self.users_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger les utilisateurs
        self.load_users()
    
    def create_all_evaluations_view(self, parent):
        """Vue de toutes les évaluations pour les administrateurs"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Toutes les évaluations:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="Rafraîchir",
            command=self.refresh_all_evaluations,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Treeview pour afficher toutes les évaluations
        self.all_evaluations_tree = ttk.Treeview(parent, columns=("Date", "Étudiant", "Enseignant", "Cours", "Moyenne"), show="headings")
        self.all_evaluations_tree.heading("Date", text="Date")
        self.all_evaluations_tree.heading("Étudiant", text="Étudiant")
        self.all_evaluations_tree.heading("Enseignant", text="Enseignant")
        self.all_evaluations_tree.heading("Cours", text="Cours")
        self.all_evaluations_tree.heading("Moyenne", text="Moyenne")
        
        self.all_evaluations_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Charger toutes les évaluations
        self.load_all_evaluations()
    
    def create_global_stats_view(self, parent):
        """Vue des statistiques globales pour les administrateurs"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Statistiques globales:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="Rafraîchir",
            command=self.refresh_global_stats,
            width=100
        )
        refresh_button.pack(pady=10)
        
        # Frame pour les statistiques
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Créer le graphique
        self.create_global_stats_chart(stats_frame)
    
    def create_reports_view(self, parent):
        """Vue des rapports pour les administrateurs"""
        # Frame pour les contrôles
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(controls_frame, text="Génération de rapports:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)
        
        generate_report_button = ctk.CTkButton(
            buttons_frame,
            text="Générer rapport global",
            command=self.generate_global_report,
            width=150
        )
        generate_report_button.pack(side="left", padx=5)
        
        export_data_button = ctk.CTkButton(
            buttons_frame,
            text="Exporter données (JSON)",
            command=self.export_data,
            width=150
        )
        export_data_button.pack(side="left", padx=5)
        
        # Zone de texte pour afficher les rapports
        self.reports_text = ctk.CTkTextbox(parent, height=400)
        self.reports_text.pack(fill="both", expand=True, padx=20, pady=10)
    
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
            messagebox.showerror("Erreur", "Veuillez sélectionner un enseignant et un cours.")
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
            messagebox.showinfo("Succès", "Évaluation soumise avec succès!")
            # Réinitialiser le formulaire
            self.reset_evaluation_form()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la soumission de l'évaluation.")
    
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
                evaluation.nom_etudiant,
                evaluation.nom_enseignant,
                evaluation.titre_cours,
                f"{moyenne:.2f}"
            ))
    
    def create_teacher_stats_chart(self, parent):
        """Créer le graphique des statistiques de l'enseignant"""
        # Obtenir les statistiques
        stats = self.user.obtenirStatistiquesEvaluation()
        if not stats:
            ctk.CTkLabel(parent, text="Aucune évaluation disponible").pack(pady=20)
            return
        
        # Créer le graphique
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Graphique des moyennes par critère
        criteres = list(stats['criteres'].keys())
        valeurs = list(stats['criteres'].values())
        
        ax1.bar(criteres, valeurs, color='skyblue')
        ax1.set_title('Moyennes par critère')
        ax1.set_ylabel('Note moyenne')
        ax1.tick_params(axis='x', rotation=45)
        
        # Graphique circulaire du nombre d'évaluations
        ax2.pie([stats['nombre_evaluations']], labels=['Évaluations'], autopct='%1.0f')
        ax2.set_title(f'Nombre total d\'évaluations: {stats["nombre_evaluations"]}')
        
        plt.tight_layout()
        
        # Intégrer le graphique dans l'interface
        canvas = tkagg.FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_global_stats_chart(self, parent):
        """Créer le graphique des statistiques globales"""
        # Obtenir les statistiques globales
        stats = self.user.genererStatistiquesGlobales()
        if not stats:
            ctk.CTkLabel(parent, text="Aucune donnée disponible").pack(pady=20)
            return
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Graphique des moyennes globales par critère
        criteres = list(stats.keys())
        valeurs = [stats[critere]['moyenne'] for critere in criteres]
        
        ax.bar(criteres, valeurs, color='lightcoral')
        ax.set_title('Moyennes globales par critère')
        ax.set_ylabel('Note moyenne')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Intégrer le graphique dans l'interface
        canvas = tkagg.FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def generate_global_report(self):
        """Générer un rapport global"""
        rapport = self.user.genererRapportGlobal()
        if rapport:
            # Afficher le rapport dans la zone de texte
            self.reports_text.delete("1.0", "end")
            self.reports_text.insert("1.0", f"Rapport Global - {rapport['date_generation']}\n\n")
            self.reports_text.insert("end", f"Statistiques des utilisateurs:\n")
            for statut, count in rapport['statistiques_utilisateurs'].items():
                self.reports_text.insert("end", f"- {statut}: {count}\n")
            self.reports_text.insert("end", f"\nTotal évaluations: {rapport['total_evaluations']}\n")
            self.reports_text.insert("end", f"Total cours: {rapport['total_cours']}\n")
        else:
            messagebox.showerror("Erreur", "Erreur lors de la génération du rapport.")
    
    def export_data(self):
        """Exporter les données"""
        filename = self.user.exporterDonnees('json')
        if filename:
            messagebox.showinfo("Succès", f"Données exportées dans {filename}")
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'export des données.")
    
    # Méthodes de rafraîchissement
    def refresh_evaluations(self):
        self.load_evaluations()
    
    def refresh_received_evaluations(self):
        self.load_received_evaluations()
    
    def refresh_teacher_stats(self):
        # Recréer le graphique
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkTabview):
                        for tab in child.winfo_children():
                            if isinstance(tab, ctk.CTkFrame):
                                self.create_teacher_stats_chart(tab)
    
    def refresh_users(self):
        self.load_users()
    
    def refresh_all_evaluations(self):
        self.load_all_evaluations()
    
    def refresh_global_stats(self):
        # Recréer le graphique
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkTabview):
                        for tab in child.winfo_children():
                            if isinstance(tab, ctk.CTkFrame):
                                self.create_global_stats_chart(tab)
    
    def add_user(self):
        """Ajouter un utilisateur (à implémenter)"""
        messagebox.showinfo("Info", "Fonctionnalité d'ajout d'utilisateur à implémenter.")
    
    def logout(self):
        """Déconnexion"""
        self.root.destroy()
        login_window = LoginWindow()
        login_window.run()
    
    def on_closing(self):
        """Gestion de la fermeture de la fenêtre"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
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