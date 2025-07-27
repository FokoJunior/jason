import psycopg2
from config import Config
from datetime import datetime

def create_database():
    """Création de la base de données et des tables"""
    
    # Connexion à PostgreSQL (sans spécifier de base de données)
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database='postgres'  # Base de données par défaut
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Création de la base de données si elle n'existe pas
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{Config.DB_NAME}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {Config.DB_NAME}")
            print(f"Base de données '{Config.DB_NAME}' créée avec succès.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de la création de la base de données: {e}")
        return False
    
    # Connexion à la nouvelle base de données
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Création de la table utilisateurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id VARCHAR(50) PRIMARY KEY,
                nom_prenom VARCHAR(100) NOT NULL,
                sexe VARCHAR(10) CHECK (sexe IN ('M', 'F')),
                mot_de_passe VARCHAR(255) NOT NULL,
                annee_academique VARCHAR(20),
                statut VARCHAR(20) CHECK (statut IN ('étudiant', 'enseignant', 'administrateur')) NOT NULL,
                niveau VARCHAR(20),
                filiere VARCHAR(50),
                grade VARCHAR(50),
                specialite VARCHAR(100),
                fonction VARCHAR(100),
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Création de la table cours
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cours (
                code_cours VARCHAR(20) PRIMARY KEY,
                titre VARCHAR(200) NOT NULL,
                type_cours VARCHAR(50),
                description TEXT,
                credits INTEGER DEFAULT 0,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Création de la table enseignements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enseignements (
                code_enseignement VARCHAR(50) PRIMARY KEY,
                annee_academique VARCHAR(20) NOT NULL,
                semestre VARCHAR(10) NOT NULL,
                enseignants VARCHAR(50) NOT NULL,
                code_cours VARCHAR(20) NOT NULL,
                commentaire TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (enseignants) REFERENCES utilisateurs(id),
                FOREIGN KEY (code_cours) REFERENCES cours(code_cours)
            )
        """)
        
        # Création de la table evaluations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id_evaluation SERIAL PRIMARY KEY,
                date_evaluation DATE NOT NULL DEFAULT CURRENT_DATE,
                clarte_cours INTEGER CHECK (clarte_cours >= 1 AND clarte_cours <= 5),
                ponctualite INTEGER CHECK (ponctualite >= 1 AND ponctualite <= 5),
                pedagogie INTEGER CHECK (pedagogie >= 1 AND pedagogie <= 5),
                disponibilite INTEGER CHECK (disponibilite >= 1 AND disponibilite <= 5),
                maitrise_matiere INTEGER CHECK (maitrise_matiere >= 1 AND maitrise_matiere <= 5),
                respect_etudiants INTEGER CHECK (respect_etudiants >= 1 AND respect_etudiants <= 5),
                temps INTEGER CHECK (temps >= 1 AND temps <= 5),
                appreciation_stimulee INTEGER CHECK (appreciation_stimulee >= 1 AND appreciation_stimulee <= 5),
                utilisation_outils INTEGER CHECK (utilisation_outils >= 1 AND utilisation_outils <= 5),
                approche_interactive INTEGER CHECK (approche_interactive >= 1 AND approche_interactive <= 5),
                coherence_objectif INTEGER CHECK (coherence_objectif >= 1 AND coherence_objectif <= 5),
                utilite_professionnelle INTEGER CHECK (utilite_professionnelle >= 1 AND utilite_professionnelle <= 5),
                commentaire_general TEXT,
                id_etudiant VARCHAR(50) NOT NULL,
                id_enseignant VARCHAR(50) NOT NULL,
                code_cours VARCHAR(20) NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_etudiant) REFERENCES utilisateurs(id),
                FOREIGN KEY (id_enseignant) REFERENCES utilisateurs(id),
                FOREIGN KEY (code_cours) REFERENCES cours(code_cours)
            )
        """)
        
        # Création d'index pour améliorer les performances
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_etudiant 
            ON evaluations(id_etudiant)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_enseignant 
            ON evaluations(id_enseignant)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_cours 
            ON evaluations(code_cours)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_date 
            ON evaluations(date_evaluation)
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Tables créées avec succès.")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la création des tables: {e}")
        return False

def insert_sample_data():
    """Insertion de données d'exemple"""
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Insertion d'utilisateurs d'exemple avec tous les paramètres
        utilisateurs_exemple = [
            # Administrateur
            ('ADMIN001', 'Administrateur Principal', 'M', 'admin123', '2024-2025', 'administrateur', None, None, None, None, 'Directeur'),
            
            # Enseignants
            ('ENS001', 'Dr. Marie Dupont', 'F', 'enseignant123', '2024-2025', 'enseignant', None, None, 'Professeur', 'Informatique', None),
            ('ENS002', 'Dr. Jean Martin', 'M', 'enseignant123', '2024-2025', 'enseignant', None, None, 'Maître de Conférences', 'Mathématiques', None),
            ('ENS003', 'Dr. Sophie Bernard', 'F', 'enseignant123', '2024-2025', 'enseignant', None, None, 'Professeur', 'Physique', None),
            
            # Étudiants
            ('ETU001', 'Alice Dubois', 'F', 'etudiant123', '2024-2025', 'étudiant', 'L3', 'Informatique', None, None, None),
            ('ETU002', 'Thomas Leroy', 'M', 'etudiant123', '2024-2025', 'étudiant', 'L3', 'Informatique', None, None, None),
            ('ETU003', 'Emma Rousseau', 'F', 'etudiant123', '2024-2025', 'étudiant', 'M1', 'Mathématiques', None, None, None),
            ('ETU004', 'Lucas Moreau', 'M', 'etudiant123', '2024-2025', 'étudiant', 'M1', 'Physique', None, None, None),
        ]
        
        for user in utilisateurs_exemple:
            cursor.execute("""
                INSERT INTO utilisateurs (id, nom_prenom, sexe, mot_de_passe, annee_academique, 
                                       statut, niveau, filiere, grade, specialite, fonction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, user)
        
        # Insertion de cours d'exemple
        cours_exemple = [
            ('INFO101', 'Introduction à la Programmation', 'Cours Magistral'),
            ('INFO102', 'Structures de Données', 'Cours Magistral'),
            ('MATH101', 'Algèbre Linéaire', 'Cours Magistral'),
            ('MATH102', 'Calcul Différentiel', 'Cours Magistral'),
            ('PHYS101', 'Mécanique Classique', 'Cours Magistral'),
            ('PHYS102', 'Électromagnétisme', 'Cours Magistral'),
        ]
        
        for cours in cours_exemple:
            cursor.execute("""
                INSERT INTO cours (code_cours, titre, type_cours)
                VALUES (%s, %s, %s)
                ON CONFLICT (code_cours) DO NOTHING
            """, cours)
        
        # Insertion d'enseignements d'exemple
        enseignements_exemple = [
            ('ENS-INFO101-2024', '2024-2025', 'S1', 'ENS001', 'INFO101', 'Cours d\'introduction à la programmation'),
            ('ENS-INFO102-2024', '2024-2025', 'S2', 'ENS001', 'INFO102', 'Cours sur les structures de données'),
            ('ENS-MATH101-2024', '2024-2025', 'S1', 'ENS002', 'MATH101', 'Cours d\'algèbre linéaire'),
            ('ENS-MATH102-2024', '2024-2025', 'S2', 'ENS002', 'MATH102', 'Cours de calcul différentiel'),
            ('ENS-PHYS101-2024', '2024-2025', 'S1', 'ENS003', 'PHYS101', 'Cours de mécanique classique'),
            ('ENS-PHYS102-2024', '2024-2025', 'S2', 'ENS003', 'PHYS102', 'Cours d\'électromagnétisme'),
        ]
        
        for enseignement in enseignements_exemple:
            cursor.execute("""
                INSERT INTO enseignements (code_enseignement, annee_academique, semestre, 
                                        enseignants, code_cours, commentaire)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (code_enseignement) DO NOTHING
            """, enseignement)
        
        # Insertion d'évaluations d'exemple
        evaluations_exemple = [
            (datetime.now().date(), 4, 5, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 'Très bon cours', 'ETU001', 'ENS001', 'INFO101'),
            (datetime.now().date(), 5, 4, 5, 5, 4, 5, 4, 5, 4, 5, 4, 5, 'Excellent enseignant', 'ETU002', 'ENS001', 'INFO101'),
            (datetime.now().date(), 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 'Cours intéressant', 'ETU003', 'ENS002', 'MATH101'),
            (datetime.now().date(), 5, 5, 4, 4, 5, 4, 5, 4, 5, 4, 5, 4, 'Très pédagogue', 'ETU004', 'ENS003', 'PHYS101'),
        ]
        
        for evaluation in evaluations_exemple:
            cursor.execute("""
                INSERT INTO evaluations (date_evaluation, clarte_cours, ponctualite, pedagogie,
                                      disponibilite, maitrise_matiere, respect_etudiants, temps,
                                      appreciation_stimulee, utilisation_outils, approche_interactive,
                                      coherence_objectif, utilite_professionnelle, commentaire_general,
                                      id_etudiant, id_enseignant, code_cours)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, evaluation)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Données d'exemple insérées avec succès.")
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'insertion des données d'exemple: {e}")
        return False

def main():
    """Fonction principale pour initialiser la base de données"""
    print("Initialisation de la base de données...")
    
    if create_database():
        print("Base de données créée avec succès.")
        
        if insert_sample_data():
            print("Données d'exemple insérées avec succès.")
            print("\nConnexions de test:")
            print("- Administrateur: ADMIN001 / admin123")
            print("- Enseignant: ENS001 / enseignant123")
            print("- Étudiant: ETU001 / etudiant123")
        else:
            print("Erreur lors de l'insertion des données d'exemple.")
    else:
        print("Erreur lors de la création de la base de données.")

if __name__ == "__main__":
    main() 