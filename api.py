from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
import json
from models import *
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
CORS(app)

# Middleware pour vérifier l'authentification
def require_auth(f):
    """Décorateur pour vérifier l'authentification"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Non authentifié'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_role(role):
    """Décorateur pour vérifier le rôle de l'utilisateur"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != role:
                return jsonify({'error': 'Accès non autorisé'}), 403
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# Routes d'authentification
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentification d'un utilisateur"""
    try:
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        
        if not login or not password:
            return jsonify({'error': 'Login et mot de passe requis'}), 400
        
        # Tentative de connexion
        user = Utilisateur()
        if user.seConnecter(login, password):
            # Créer l'utilisateur approprié selon le statut
            if user.statut == 'étudiant':
                user_obj = Etudiant()
            elif user.statut == 'enseignant':
                user_obj = Enseignant()
            elif user.statut == 'administrateur':
                user_obj = Administrateur()
            else:
                user_obj = Utilisateur()
            
            user_obj.__dict__.update(user.__dict__)
            
            # Stocker les informations de session
            session['user_id'] = user_obj.id
            session['user_role'] = user_obj.statut
            session['user_name'] = user_obj.nom_prenom
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user_obj.id,
                    'nom_prenom': user_obj.nom_prenom,
                    'statut': user_obj.statut,
                    'annee_academique': user_obj.annee_academique
                }
            })
        else:
            return jsonify({'error': 'Identifiants incorrects'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Déconnexion d'un utilisateur"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/auth/profile', methods=['GET'])
@require_auth
def get_profile():
    """Récupérer le profil de l'utilisateur connecté"""
    try:
        user_id = session['user_id']
        user_role = session['user_role']
        
        # Créer l'utilisateur approprié
        if user_role == 'étudiant':
            user = Etudiant()
        elif user_role == 'enseignant':
            user = Enseignant()
        elif user_role == 'administrateur':
            user = Administrateur()
        else:
            user = Utilisateur()
        
        user.id = user_id
        profile = user.obtenirProfil()
        
        return jsonify({
            'success': True,
            'profile': {
                'id': profile.id,
                'nom_prenom': profile.nom_prenom,
                'sexe': profile.sexe,
                'annee_academique': profile.annee_academique,
                'statut': profile.statut,
                'niveau': getattr(profile, 'niveau', None),
                'filiere': getattr(profile, 'filiere', None),
                'grade': getattr(profile, 'grade', None),
                'specialite': getattr(profile, 'specialite', None),
                'fonction': getattr(profile, 'fonction', None)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Mettre à jour le profil de l'utilisateur connecté"""
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Créer l'utilisateur approprié
        user_role = session['user_role']
        if user_role == 'étudiant':
            user = Etudiant()
        elif user_role == 'enseignant':
            user = Enseignant()
        elif user_role == 'administrateur':
            user = Administrateur()
        else:
            user = Utilisateur()
        
        user.id = user_id
        
        if user.mettreAJourProfil(data):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Erreur lors de la mise à jour du profil'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes pour les étudiants
@app.route('/api/student/evaluations', methods=['GET'])
@require_auth
@require_role('étudiant')
def get_student_evaluations():
    """Récupérer les évaluations d'un étudiant"""
    try:
        user_id = session['user_id']
        student = Etudiant()
        student.id = user_id
        
        evaluations = student.consulterEvaluations()
        
        evaluations_data = []
        for eval_obj in evaluations:
            evaluations_data.append({
                'id_evaluation': eval_obj.id_evaluation,
                'date_evaluation': eval_obj.date_evaluation.isoformat() if eval_obj.date_evaluation else None,
                'id_enseignant': eval_obj.id_enseignant,
                'code_cours': eval_obj.code_cours,
                'moyenne_globale': eval_obj.calculerMoyenneGlobale(),
                'commentaire_general': eval_obj.commentaire_general
            })
        
        return jsonify({
            'success': True,
            'evaluations': evaluations_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/evaluations', methods=['POST'])
@require_auth
@require_role('étudiant')
def create_evaluation():
    """Créer une nouvelle évaluation"""
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Créer l'évaluation
        evaluation = Evaluation(
            date_evaluation=datetime.now().date(),
            id_etudiant=user_id,
            id_enseignant=data['id_enseignant'],
            code_cours=data['code_cours'],
            clarte_cours=data.get('clarte_cours'),
            ponctualite=data.get('ponctualite'),
            pedagogie=data.get('pedagogie'),
            disponibilite=data.get('disponibilite'),
            maitrise_matiere=data.get('maitrise_matiere'),
            respect_etudiants=data.get('respect_etudiants'),
            temps=data.get('temps'),
            appreciation_stimulee=data.get('appreciation_stimulee'),
            utilisation_outils=data.get('utilisation_outils'),
            approche_interactive=data.get('approche_interactive'),
            coherence_objectif=data.get('coherence_objectif'),
            utilite_professionnelle=data.get('utilite_professionnelle'),
            commentaire_general=data.get('commentaire_general')
        )
        
        if evaluation.sauvegarder():
            return jsonify({
                'success': True,
                'message': 'Évaluation créée avec succès'
            })
        else:
            return jsonify({'error': 'Erreur lors de la création de l\'évaluation'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/courses', methods=['GET'])
@require_auth
@require_role('étudiant')
def get_student_courses():
    """Récupérer les cours disponibles pour un étudiant"""
    try:
        user_id = session['user_id']
        student = Etudiant()
        student.id = user_id
        
        courses = student.rechercherCours()
        
        courses_data = []
        for course in courses:
            courses_data.append({
                'code_cours': course.code_cours,
                'titre': course.titre,
                'type_cours': course.type_cours
            })
        
        return jsonify({
            'success': True,
            'courses': courses_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes pour les enseignants
@app.route('/api/teacher/evaluations', methods=['GET'])
@require_auth
@require_role('enseignant')
def get_teacher_evaluations():
    """Récupérer les évaluations reçues par un enseignant"""
    try:
        user_id = session['user_id']
        teacher = Enseignant()
        teacher.id = user_id
        
        evaluations = teacher.consulterEvaluationsRecues()
        
        evaluations_data = []
        for eval_obj in evaluations:
            evaluations_data.append({
                'id_evaluation': eval_obj.id_evaluation,
                'date_evaluation': eval_obj.date_evaluation.isoformat() if eval_obj.date_evaluation else None,
                'id_etudiant': eval_obj.id_etudiant,
                'code_cours': eval_obj.code_cours,
                'moyenne_globale': eval_obj.calculerMoyenneGlobale(),
                'commentaire_general': eval_obj.commentaire_general,
                'clarte_cours': eval_obj.clarte_cours,
                'ponctualite': eval_obj.ponctualite,
                'pedagogie': eval_obj.pedagogie,
                'disponibilite': eval_obj.disponibilite,
                'maitrise_matiere': eval_obj.maitrise_matiere,
                'respect_etudiants': eval_obj.respect_etudiants,
                'temps': eval_obj.temps,
                'appreciation_stimulee': eval_obj.appreciation_stimulee,
                'utilisation_outils': eval_obj.utilisation_outils,
                'approche_interactive': eval_obj.approche_interactive,
                'coherence_objectif': eval_obj.coherence_objectif,
                'utilite_professionnelle': eval_obj.utilite_professionnelle
            })
        
        return jsonify({
            'success': True,
            'evaluations': evaluations_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teacher/statistics', methods=['GET'])
@require_auth
@require_role('enseignant')
def get_teacher_statistics():
    """Récupérer les statistiques d'un enseignant"""
    try:
        user_id = session['user_id']
        teacher = Enseignant()
        teacher.id = user_id
        
        stats = teacher.obtenirStatistiquesEvaluation()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teacher/courses', methods=['GET'])
@require_auth
@require_role('enseignant')
def get_teacher_courses():
    """Récupérer les cours d'un enseignant"""
    try:
        user_id = session['user_id']
        teacher = Enseignant()
        teacher.id = user_id
        
        courses = teacher.consulterCours()
        
        return jsonify({
            'success': True,
            'courses': courses
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teacher/report', methods=['GET'])
@require_auth
@require_role('enseignant')
def get_teacher_report():
    """Générer un rapport de performance pour un enseignant"""
    try:
        user_id = session['user_id']
        teacher = Enseignant()
        teacher.id = user_id
        
        report = teacher.genererRapportPerformance()
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes pour les administrateurs
@app.route('/api/admin/users', methods=['GET'])
@require_auth
@require_role('administrateur')
def get_all_users():
    """Récupérer tous les utilisateurs"""
    try:
        admin = Administrateur()
        admin.id = session['user_id']
        
        users = admin.gererUtilisateurs()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'nom_prenom': user.nom_prenom,
                'sexe': user.sexe,
                'annee_academique': user.annee_academique,
                'statut': user.statut,
                'niveau': getattr(user, 'niveau', None),
                'filiere': getattr(user, 'filiere', None),
                'grade': getattr(user, 'grade', None),
                'specialite': getattr(user, 'specialite', None),
                'fonction': getattr(user, 'fonction', None)
            })
        
        return jsonify({
            'success': True,
            'users': users_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/evaluations', methods=['GET'])
@require_auth
@require_role('administrateur')
def get_all_evaluations():
    """Récupérer toutes les évaluations"""
    try:
        admin = Administrateur()
        admin.id = session['user_id']
        
        evaluations = admin.consulterToutesEvaluations()
        
        evaluations_data = []
        for eval_obj in evaluations:
            evaluations_data.append({
                'id_evaluation': eval_obj.id_evaluation,
                'date_evaluation': eval_obj.date_evaluation.isoformat() if eval_obj.date_evaluation else None,
                'nom_etudiant': getattr(eval_obj, 'nom_etudiant', ''),
                'nom_enseignant': getattr(eval_obj, 'nom_enseignant', ''),
                'titre_cours': getattr(eval_obj, 'titre_cours', ''),
                'moyenne_globale': eval_obj.calculerMoyenneGlobale(),
                'commentaire_general': eval_obj.commentaire_general
            })
        
        return jsonify({
            'success': True,
            'evaluations': evaluations_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/statistics', methods=['GET'])
@require_auth
@require_role('administrateur')
def get_global_statistics():
    """Récupérer les statistiques globales"""
    try:
        admin = Administrateur()
        admin.id = session['user_id']
        
        stats = admin.genererStatistiquesGlobales()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/report', methods=['GET'])
@require_auth
@require_role('administrateur')
def get_global_report():
    """Générer un rapport global"""
    try:
        admin = Administrateur()
        admin.id = session['user_id']
        
        report = admin.genererRapportGlobal()
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/export', methods=['POST'])
@require_auth
@require_role('administrateur')
def export_data():
    """Exporter les données"""
    try:
        data = request.get_json()
        format_type = data.get('format', 'json')
        
        admin = Administrateur()
        admin.id = session['user_id']
        
        filename = admin.exporterDonnees(format_type)
        
        if filename:
            return jsonify({
                'success': True,
                'filename': filename
            })
        else:
            return jsonify({'error': 'Erreur lors de l\'export'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes communes
@app.route('/api/courses', methods=['GET'])
@require_auth
def get_courses():
    """Récupérer tous les cours"""
    try:
        conn = DatabaseConnection.get_connection()
        if conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM cours ORDER BY titre")
            courses_data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            courses = []
            for data in courses_data:
                courses.append(dict(data))
            
            return jsonify({
                'success': True,
                'courses': courses
            })
        else:
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teachers', methods=['GET'])
@require_auth
def get_teachers():
    """Récupérer tous les enseignants"""
    try:
        conn = DatabaseConnection.get_connection()
        if conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT id, nom_prenom, grade, specialite 
                FROM utilisateurs 
                WHERE statut = 'enseignant' 
                ORDER BY nom_prenom
            """)
            teachers_data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            teachers = []
            for data in teachers_data:
                teachers.append(dict(data))
            
            return jsonify({
                'success': True,
                'teachers': teachers
            })
        else:
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route de test
@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état de l'API"""
    return jsonify({
        'status': 'OK',
        'message': 'API d\'évaluation des enseignants opérationnelle'
    })

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000) 