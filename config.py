import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuration de la base de données PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'evaluation_enseignants')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'foko1234')

    # Configuration Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'votre_cle_secrete_ici')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Configuration de l'interface graphique
    THEME = "dark"  # ou "light"
    COLOR_THEME = "blue"  # ou "green", "dark-blue"

    # Configuration des évaluations
    CRITERES_EVALUATION = [
        'clarte_cours',
        'ponctualite',
        'pedagogie',
        'disponibilite',
        'maitrise_matiere',
        'respect_etudiants',
        'temps',
        'appreciation_stimulee',
        'utilisation_outils',
        'approche_interactive',
        'coherence_objectif',
        'utilite_professionnelle'
    ]

    # Messages d'erreur et de succès
    MESSAGES = {
        'connexion_reussie': 'Connexion réussie !',
        'connexion_echouee': 'Identifiants incorrects.',
        'evaluation_sauvegardee': 'Évaluation sauvegardée avec succès !',
        'evaluation_modifiee': 'Évaluation modifiée avec succès !',
        'evaluation_supprimee': 'Évaluation supprimée avec succès !',
        'utilisateur_cree': 'Utilisateur créé avec succès !',
        'utilisateur_modifie': 'Utilisateur modifié avec succès !',
        'utilisateur_supprime': 'Utilisateur supprimé avec succès !',
        'erreur_generique': 'Une erreur est survenue. Veuillez réessayer.',
        'champs_obligatoires': 'Tous les champs sont obligatoires.',
        'mot_de_passe_incorrect': 'L\'ancien mot de passe est incorrect.',
        'mots_de_passe_differents': 'Les nouveaux mots de passe ne correspondent pas.'
    } 