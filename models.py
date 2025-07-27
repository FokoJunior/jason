import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config import Config
import json

class DatabaseConnection:
    """Classe pour gérer la connexion à la base de données PostgreSQL"""
    
    @staticmethod
    def get_connection():
        try:
            connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                client_encoding='utf8'
            )
            return connection
        except Exception as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return None

class Utilisateur:
    """Classe de base pour tous les utilisateurs du système"""
    
    def __init__(self, id=None, nom_prenom=None, sexe=None, mot_de_passe=None, 
                 annee_academique=None, statut=None):
        self.id = id
        self.nom_prenom = nom_prenom
        self.sexe = sexe
        self.mot_de_passe = mot_de_passe
        self.annee_academique = annee_academique
        self.statut = statut
    
    def seConnecter(self, login, motDePasse):
        """Authentification d'un utilisateur"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM utilisateurs 
                    WHERE id = %s AND mot_de_passe = %s
                """, (login, motDePasse))
                user_data = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if user_data:
                    self.__dict__.update(dict(user_data))
                    return True
            return False
        except Exception as e:
            print(f"Erreur lors de la connexion: {e}")
            return False
    
    def modifierMotDePasse(self, ancienMdp, nouveauMdp):
        """Modification du mot de passe"""
        try:
            if self.mot_de_passe != ancienMdp:
                return False
            
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE utilisateurs 
                    SET mot_de_passe = %s 
                    WHERE id = %s
                """, (nouveauMdp, self.id))
                conn.commit()
                cursor.close()
                conn.close()
                self.mot_de_passe = nouveauMdp
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la modification du mot de passe: {e}")
            return False
    
    def obtenirProfil(self):
        """Récupération du profil utilisateur"""
        return self
    
    def mettreAJourProfil(self, donnees):
        """Mise à jour du profil utilisateur"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE utilisateurs 
                    SET nom_prenom = %s, sexe = %s, annee_academique = %s
                    WHERE id = %s
                """, (donnees.get('nom_prenom'), donnees.get('sexe'), 
                     donnees.get('annee_academique'), self.id))
                conn.commit()
                cursor.close()
                conn.close()
                
                # Mise à jour des attributs locaux
                for key, value in donnees.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la mise à jour du profil: {e}")
            return False

class Etudiant(Utilisateur):
    """Classe Étudiant héritant de Utilisateur"""
    
    def __init__(self, id=None, nom_prenom=None, sexe=None, mot_de_passe=None,
                 annee_academique=None, statut='étudiant', niveau=None, filiere=None):
        super().__init__(id, nom_prenom, sexe, mot_de_passe, annee_academique, statut)
        self.niveau = niveau
        self.filiere = filiere
    
    def creerEvaluation(self, idEnseignant, codeCours):
        """Création d'une nouvelle évaluation"""
        evaluation = Evaluation()
        evaluation.id_etudiant = self.id
        evaluation.id_enseignant = idEnseignant
        evaluation.code_cours = codeCours
        evaluation.date_evaluation = datetime.now().date()
        return evaluation
    
    def consulterEvaluations(self):
        """Consultation des évaluations de l'étudiant"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM evaluations 
                    WHERE id_etudiant = %s 
                    ORDER BY date_evaluation DESC
                """, (self.id,))
                evaluations_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                evaluations = []
                for data in evaluations_data:
                    eval_obj = Evaluation()
                    eval_obj.__dict__.update(dict(data))
                    evaluations.append(eval_obj)
                return evaluations
            return []
        except Exception as e:
            print(f"Erreur lors de la consultation des évaluations: {e}")
            return []
    
    def modifierEvaluation(self, idEvaluation):
        """Modification d'une évaluation existante"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM evaluations 
                    WHERE id_evaluation = %s AND id_etudiant = %s
                """, (idEvaluation, self.id))
                evaluation_data = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if evaluation_data:
                    evaluation = Evaluation()
                    evaluation.__dict__.update(dict(evaluation_data))
                    return evaluation
            return None
        except Exception as e:
            print(f"Erreur lors de la modification de l'évaluation: {e}")
            return None
    
    def rechercherCours(self):
        """Recherche de cours disponibles"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT DISTINCT c.* FROM cours c
                    JOIN enseignements e ON c.code_cours = e.code_cours
                    WHERE e.annee_academique = %s
                """, (self.annee_academique,))
                cours_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                cours = []
                for data in cours_data:
                    cours_obj = Cours()
                    cours_obj.__dict__.update(dict(data))
                    cours.append(cours_obj)
                return cours
            return []
        except Exception as e:
            print(f"Erreur lors de la recherche de cours: {e}")
            return []
    
    def obtenirCoursInscrits(self):
        """Récupération des cours où l'étudiant est inscrit"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT DISTINCT c.* FROM cours c
                    JOIN enseignements e ON c.code_cours = e.code_cours
                    WHERE e.annee_academique = %s
                """, (self.annee_academique,))
                cours_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                cours = []
                for data in cours_data:
                    cours_obj = Cours()
                    cours_obj.__dict__.update(dict(data))
                    cours.append(cours_obj)
                return cours
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des cours inscrits: {e}")
            return []

class Enseignant(Utilisateur):
    """Classe Enseignant héritant de Utilisateur"""
    
    def __init__(self, id=None, nom_prenom=None, sexe=None, mot_de_passe=None,
                 annee_academique=None, statut='enseignant', grade=None, specialite=None):
        super().__init__(id, nom_prenom, sexe, mot_de_passe, annee_academique, statut)
        self.grade = grade
        self.specialite = specialite
    
    def consulterEvaluationsRecues(self):
        """Consultation des évaluations reçues par l'enseignant"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM evaluations 
                    WHERE id_enseignant = %s 
                    ORDER BY date_evaluation DESC
                """, (self.id,))
                evaluations_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                evaluations = []
                for data in evaluations_data:
                    eval_obj = Evaluation()
                    eval_obj.__dict__.update(dict(data))
                    evaluations.append(eval_obj)
                return evaluations
            return []
        except Exception as e:
            print(f"Erreur lors de la consultation des évaluations reçues: {e}")
            return []
    
    def obtenirStatistiquesEvaluation(self):
        """Calcul des statistiques d'évaluation"""
        evaluations = self.consulterEvaluationsRecues()
        if not evaluations:
            return None
        
        stats = {
            'nombre_evaluations': len(evaluations),
            'moyenne_globale': 0,
            'criteres': {}
        }
        
        # Calcul des moyennes par critère
        criteres = Config.CRITERES_EVALUATION
        for critere in criteres:
            total = 0
            count = 0
            for eval_obj in evaluations:
                if hasattr(eval_obj, critere) and getattr(eval_obj, critere) is not None:
                    total += getattr(eval_obj, critere)
                    count += 1
            if count > 0:
                stats['criteres'][critere] = round(total / count, 2)
        
        # Calcul de la moyenne globale
        total_global = 0
        count_global = 0
        for eval_obj in evaluations:
            moyenne_eval = eval_obj.calculerMoyenneGlobale()
            if moyenne_eval > 0:
                total_global += moyenne_eval
                count_global += 1
        
        if count_global > 0:
            stats['moyenne_globale'] = round(total_global / count_global, 2)
        
        return stats
    
    def consulterCours(self):
        """Consultation des cours enseignés"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT DISTINCT code_cours FROM enseignements 
                    WHERE enseignants = %s AND annee_academique = %s
                """, (self.id, self.annee_academique))
                cours_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                return [row['code_cours'] for row in cours_data]
            return []
        except Exception as e:
            print(f"Erreur lors de la consultation des cours: {e}")
            return []
    
    def genererRapportPerformance(self):
        """Génération d'un rapport de performance"""
        stats = self.obtenirStatistiquesEvaluation()
        cours = self.consulterCours()
        
        rapport = {
            'enseignant': self.nom_prenom,
            'grade': self.grade,
            'specialite': self.specialite,
            'annee_academique': self.annee_academique,
            'statistiques': stats,
            'cours_enseignes': cours,
            'date_generation': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return rapport
    
    def obtenirRenseignements(self):
        """Récupération des renseignements d'enseignement"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM enseignements 
                    WHERE enseignants = %s AND annee_academique = %s
                """, (self.id, self.annee_academique))
                enseignements_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                enseignements = []
                for data in enseignements_data:
                    ens_obj = Enseignement()
                    ens_obj.__dict__.update(dict(data))
                    enseignements.append(ens_obj)
                return enseignements
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des renseignements: {e}")
            return []

class Administrateur(Utilisateur):
    """Classe Administrateur héritant de Utilisateur"""
    
    def __init__(self, id=None, nom_prenom=None, sexe=None, mot_de_passe=None,
                 annee_academique=None, statut='administrateur', fonction=None):
        super().__init__(id, nom_prenom, sexe, mot_de_passe, annee_academique, statut)
        self.fonction = fonction
    
    def genererRapportGlobal(self):
        """Génération d'un rapport global du système"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Statistiques des utilisateurs
                cursor.execute("SELECT statut, COUNT(*) FROM utilisateurs GROUP BY statut")
                stats_utilisateurs = dict(cursor.fetchall())
                
                # Statistiques des évaluations
                cursor.execute("SELECT COUNT(*) FROM evaluations")
                total_evaluations = cursor.fetchone()[0]
                
                # Statistiques des cours
                cursor.execute("SELECT COUNT(*) FROM cours")
                total_cours = cursor.fetchone()[0]
                
                cursor.close()
                conn.close()
                
                rapport = {
                    'date_generation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'statistiques_utilisateurs': stats_utilisateurs,
                    'total_evaluations': total_evaluations,
                    'total_cours': total_cours
                }
                
                return rapport
        except Exception as e:
            print(f"Erreur lors de la génération du rapport global: {e}")
            return None
    
    def consulterToutesEvaluations(self):
        """Consultation de toutes les évaluations du système"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT e.*, u1.nom_prenom as nom_etudiant, u2.nom_prenom as nom_enseignant
                    FROM evaluations e
                    JOIN utilisateurs u1 ON e.id_etudiant = u1.id
                    JOIN utilisateurs u2 ON e.id_enseignant = u2.id
                    ORDER BY e.date_evaluation DESC
                """)
                evaluations_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                evaluations = []
                for data in evaluations_data:
                    eval_obj = Evaluation()
                    eval_obj.__dict__.update(dict(data))
                    evaluations.append(eval_obj)
                return evaluations
            return []
        except Exception as e:
            print(f"Erreur lors de la consultation de toutes les évaluations: {e}")
            return []
    
    def gererUtilisateurs(self):
        """Gestion des utilisateurs du système"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT * FROM utilisateurs ORDER BY nom_prenom")
                utilisateurs_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                utilisateurs = []
                for data in utilisateurs_data:
                    if data['statut'] == 'étudiant':
                        user_obj = Etudiant()
                    elif data['statut'] == 'enseignant':
                        user_obj = Enseignant()
                    elif data['statut'] == 'administrateur':
                        user_obj = Administrateur()
                    else:
                        user_obj = Utilisateur()
                    
                    user_obj.__dict__.update(dict(data))
                    utilisateurs.append(user_obj)
                return utilisateurs
            return []
        except Exception as e:
            print(f"Erreur lors de la gestion des utilisateurs: {e}")
            return []
    
    def configurationSysteme(self):
        """Configuration du système"""
        # Cette méthode peut être utilisée pour configurer les paramètres du système
        pass
    
    def exporterDonnees(self, format_type):
        """Export des données dans différents formats"""
        if format_type.lower() == 'json':
            return self._exporterJSON()
        elif format_type.lower() == 'csv':
            return self._exporterCSV()
        else:
            return None
    
    def _exporterJSON(self):
        """Export des données au format JSON"""
        try:
            evaluations = self.consulterToutesEvaluations()
            utilisateurs = self.gererUtilisateurs()
            
            data = {
                'evaluations': [eval_obj.__dict__ for eval_obj in evaluations],
                'utilisateurs': [user_obj.__dict__ for user_obj in utilisateurs],
                'date_export': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            filename = f"export_evaluations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            return filename
        except Exception as e:
            print(f"Erreur lors de l'export JSON: {e}")
            return None
    
    def _exporterCSV(self):
        """Export des données au format CSV"""
        # Implémentation de l'export CSV
        pass
    
    def genererStatistiquesGlobales(self):
        """Génération de statistiques globales"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Statistiques par critère d'évaluation
                stats_globales = {}
                for critere in Config.CRITERES_EVALUATION:
                    cursor.execute(f"""
                        SELECT AVG({critere}) as moyenne, COUNT({critere}) as nombre
                        FROM evaluations 
                        WHERE {critere} IS NOT NULL
                    """)
                    result = cursor.fetchone()
                    if result:
                        stats_globales[critere] = {
                            'moyenne': round(result['moyenne'], 2) if result['moyenne'] else 0,
                            'nombre': result['nombre']
                        }
                
                cursor.close()
                conn.close()
                
                return stats_globales
        except Exception as e:
            print(f"Erreur lors de la génération des statistiques globales: {e}")
            return None

class Cours:
    """Classe Cours"""
    
    def __init__(self, code_cours=None, titre=None, type_cours=None):
        self.code_cours = code_cours
        self.titre = titre
        self.type_cours = type_cours
    
    def obtenirEvaluations(self):
        """Récupération des évaluations pour ce cours"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM evaluations 
                    WHERE code_cours = %s 
                    ORDER BY date_evaluation DESC
                """, (self.code_cours,))
                evaluations_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                evaluations = []
                for data in evaluations_data:
                    eval_obj = Evaluation()
                    eval_obj.__dict__.update(dict(data))
                    evaluations.append(eval_obj)
                return evaluations
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des évaluations du cours: {e}")
            return []
    
    def calculerMoyenneEvaluations(self):
        """Calcul de la moyenne des évaluations pour ce cours"""
        evaluations = self.obtenirEvaluations()
        if not evaluations:
            return 0
        
        total = 0
        count = 0
        for eval_obj in evaluations:
            moyenne = eval_obj.calculerMoyenneGlobale()
            if moyenne > 0:
                total += moyenne
                count += 1
        
        return round(total / count, 2) if count > 0 else 0
    
    def obtenirRenseignements(self):
        """Récupération des renseignements d'enseignement pour ce cours"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM enseignements 
                    WHERE code_cours = %s
                """, (self.code_cours,))
                enseignements_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                enseignements = []
                for data in enseignements_data:
                    ens_obj = Enseignement()
                    ens_obj.__dict__.update(dict(data))
                    enseignements.append(ens_obj)
                return enseignements
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des renseignements: {e}")
            return []
    
    def obtenirStatistiques(self):
        """Calcul des statistiques pour ce cours"""
        evaluations = self.obtenirEvaluations()
        if not evaluations:
            return None
        
        stats = {
            'nombre_evaluations': len(evaluations),
            'moyenne_globale': self.calculerMoyenneEvaluations(),
            'criteres': {}
        }
        
        # Calcul des moyennes par critère
        criteres = Config.CRITERES_EVALUATION
        for critere in criteres:
            total = 0
            count = 0
            for eval_obj in evaluations:
                if hasattr(eval_obj, critere) and getattr(eval_obj, critere) is not None:
                    total += getattr(eval_obj, critere)
                    count += 1
            if count > 0:
                stats['criteres'][critere] = round(total / count, 2)
        
        return stats
    
    def rechercherParTitre(self, titre):
        """Recherche de cours par titre"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM cours 
                    WHERE titre ILIKE %s
                """, (f'%{titre}%',))
                cours_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                cours = []
                for data in cours_data:
                    cours_obj = Cours()
                    cours_obj.__dict__.update(dict(data))
                    cours.append(cours_obj)
                return cours
            return []
        except Exception as e:
            print(f"Erreur lors de la recherche de cours: {e}")
            return []

class Evaluation:
    """Classe Evaluation"""
    
    def __init__(self, id_evaluation=None, date_evaluation=None, clarte_cours=None,
                 ponctualite=None, pedagogie=None, disponibilite=None, maitrise_matiere=None,
                 respect_etudiants=None, temps=None, appreciation_stimulee=None,
                 utilisation_outils=None, approche_interactive=None, coherence_objectif=None,
                 utilite_professionnelle=None, commentaire_general=None, id_etudiant=None,
                 id_enseignant=None, code_cours=None):
        self.id_evaluation = id_evaluation
        self.date_evaluation = date_evaluation
        self.clarte_cours = clarte_cours
        self.ponctualite = ponctualite
        self.pedagogie = pedagogie
        self.disponibilite = disponibilite
        self.maitrise_matiere = maitrise_matiere
        self.respect_etudiants = respect_etudiants
        self.temps = temps
        self.appreciation_stimulee = appreciation_stimulee
        self.utilisation_outils = utilisation_outils
        self.approche_interactive = approche_interactive
        self.coherence_objectif = coherence_objectif
        self.utilite_professionnelle = utilite_professionnelle
        self.commentaire_general = commentaire_general
        self.id_etudiant = id_etudiant
        self.id_enseignant = id_enseignant
        self.code_cours = code_cours
    
    def calculerMoyenneGlobale(self):
        """Calcul de la moyenne globale de l'évaluation"""
        criteres = Config.CRITERES_EVALUATION
        total = 0
        count = 0
        
        for critere in criteres:
            valeur = getattr(self, critere)
            if valeur is not None and 1 <= valeur <= 5:
                total += valeur
                count += 1
        
        return round(total / count, 2) if count > 0 else 0
    
    def validerEvaluation(self):
        """Validation de l'évaluation"""
        # Vérification que tous les champs obligatoires sont remplis
        if not all([self.id_etudiant, self.id_enseignant, self.code_cours]):
            return False
        
        # Vérification que les notes sont dans la plage valide (1-5)
        criteres = Config.CRITERES_EVALUATION
        for critere in criteres:
            valeur = getattr(self, critere)
            if valeur is not None and (valeur < 1 or valeur > 5):
                return False
        
        return True
    
    def sauvegarder(self):
        """Sauvegarde de l'évaluation en base de données"""
        if not self.validerEvaluation():
            return False
        
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                
                if self.id_evaluation is None:
                    # Insertion d'une nouvelle évaluation
                    cursor.execute("""
                        INSERT INTO evaluations (
                            date_evaluation, clarte_cours, ponctualite, pedagogie,
                            disponibilite, maitrise_matiere, respect_etudiants, temps,
                            appreciation_stimulee, utilisation_outils, approche_interactive,
                            coherence_objectif, utilite_professionnelle, commentaire_general,
                            id_etudiant, id_enseignant, code_cours
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id_evaluation
                    """, (
                        self.date_evaluation, self.clarte_cours, self.ponctualite,
                        self.pedagogie, self.disponibilite, self.maitrise_matiere,
                        self.respect_etudiants, self.temps, self.appreciation_stimulee,
                        self.utilisation_outils, self.approche_interactive,
                        self.coherence_objectif, self.utilite_professionnelle,
                        self.commentaire_general, self.id_etudiant, self.id_enseignant,
                        self.code_cours
                    ))
                    self.id_evaluation = cursor.fetchone()[0]
                else:
                    # Mise à jour d'une évaluation existante
                    cursor.execute("""
                        UPDATE evaluations SET
                            date_evaluation = %s, clarte_cours = %s, ponctualite = %s,
                            pedagogie = %s, disponibilite = %s, maitrise_matiere = %s,
                            respect_etudiants = %s, temps = %s, appreciation_stimulee = %s,
                            utilisation_outils = %s, approche_interactive = %s,
                            coherence_objectif = %s, utilite_professionnelle = %s,
                            commentaire_general = %s, id_etudiant = %s, id_enseignant = %s,
                            code_cours = %s
                        WHERE id_evaluation = %s
                    """, (
                        self.date_evaluation, self.clarte_cours, self.ponctualite,
                        self.pedagogie, self.disponibilite, self.maitrise_matiere,
                        self.respect_etudiants, self.temps, self.appreciation_stimulee,
                        self.utilisation_outils, self.approche_interactive,
                        self.coherence_objectif, self.utilite_professionnelle,
                        self.commentaire_general, self.id_etudiant, self.id_enseignant,
                        self.code_cours, self.id_evaluation
                    ))
                
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'évaluation: {e}")
            return False
    
    def modifier(self, id_eval):
        """Modification d'une évaluation existante"""
        self.id_evaluation = id_eval
        return self.sauvegarder()
    
    def supprimer(self):
        """Suppression d'une évaluation"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM evaluations WHERE id_evaluation = %s
                """, (self.id_evaluation,))
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'évaluation: {e}")
            return False
    
    def obtenirDetailsComplets(self):
        """Récupération des détails complets de l'évaluation"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT e.*, u1.nom_prenom as nom_etudiant, u2.nom_prenom as nom_enseignant,
                           c.titre as titre_cours
                    FROM evaluations e
                    JOIN utilisateurs u1 ON e.id_etudiant = u1.id
                    JOIN utilisateurs u2 ON e.id_enseignant = u2.id
                    JOIN cours c ON e.code_cours = c.code_cours
                    WHERE e.id_evaluation = %s
                """, (self.id_evaluation,))
                evaluation_data = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if evaluation_data:
                    self.__dict__.update(dict(evaluation_data))
                return self
        except Exception as e:
            print(f"Erreur lors de la récupération des détails: {e}")
            return None

class Enseignement:
    """Classe Enseignement"""
    
    def __init__(self, code_enseignement=None, annee_academique=None, semestre=None,
                 enseignants=None, code_cours=None, commentaire=None):
        self.code_enseignement = code_enseignement
        self.annee_academique = annee_academique
        self.semestre = semestre
        self.enseignants = enseignants
        self.code_cours = code_cours
        self.commentaire = commentaire
    
    def obtenirEvaluations(self):
        """Récupération des évaluations pour cet enseignement"""
        try:
            conn = DatabaseConnection.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT * FROM evaluations 
                    WHERE code_cours = %s AND id_enseignant = %s
                    ORDER BY date_evaluation DESC
                """, (self.code_cours, self.enseignants))
                evaluations_data = cursor.fetchall()
                cursor.close()
                conn.close()
                
                evaluations = []
                for data in evaluations_data:
                    eval_obj = Evaluation()
                    eval_obj.__dict__.update(dict(data))
                    evaluations.append(eval_obj)
                return evaluations
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des évaluations: {e}")
            return []
    
    def calculerPerformance(self):
        """Calcul de la performance de l'enseignement"""
        evaluations = self.obtenirEvaluations()
        if not evaluations:
            return None
        
        performance = {
            'nombre_evaluations': len(evaluations),
            'moyenne_globale': 0,
            'criteres': {}
        }
        
        # Calcul des moyennes par critère
        criteres = Config.CRITERES_EVALUATION
        for critere in criteres:
            total = 0
            count = 0
            for eval_obj in evaluations:
                if hasattr(eval_obj, critere) and getattr(eval_obj, critere) is not None:
                    total += getattr(eval_obj, critere)
                    count += 1
            if count > 0:
                performance['criteres'][critere] = round(total / count, 2)
        
        # Calcul de la moyenne globale
        total_global = 0
        count_global = 0
        for eval_obj in evaluations:
            moyenne_eval = eval_obj.calculerMoyenneGlobale()
            if moyenne_eval > 0:
                total_global += moyenne_eval
                count_global += 1
        
        if count_global > 0:
            performance['moyenne_globale'] = round(total_global / count_global, 2)
        
        return performance
    
    def obtenirEtudiants(self):
        """Récupération des étudiants inscrits à cet enseignement"""
        # Cette méthode peut être implémentée selon la structure de la base de données
        pass
    
    def planifierEvaluation(self):
        """Planification d'une évaluation pour cet enseignement"""
        # Cette méthode peut être utilisée pour planifier des évaluations
        pass 