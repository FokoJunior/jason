# Système d'Évaluation des Enseignants

Un système complet d'évaluation des enseignants développé en Python avec PostgreSQL, Flask et CustomTkinter.

## 🎯 Description

Ce système permet aux étudiants d'évaluer leurs enseignants selon différents critères, aux enseignants de consulter leurs évaluations et statistiques, et aux administrateurs de gérer l'ensemble du système.

## 🏗️ Architecture

### Diagramme de Classes

Le système est basé sur un diagramme de classes UML avec les entités suivantes :

- **Utilisateur** : Classe de base pour tous les utilisateurs

  - **Étudiant** : Peut créer et consulter des évaluations
  - **Enseignant** : Peut consulter ses évaluations et statistiques
  - **Administrateur** : Gère le système et génère des rapports
- **Cours** : Représente les cours enseignés
- **Évaluation** : Contient les notes et commentaires sur un enseignant
- **Enseignement** : Lie les enseignants aux cours

### Cas d'Utilisation

1. **Étudiant**

   - Évaluer un enseignant
   - Consulter ses évaluations
   - Rechercher des cours
2. **Enseignant**

   - Consulter les évaluations reçues
   - Voir ses statistiques de performance
   - Générer des rapports
3. **Administrateur**

   - Gérer les utilisateurs
   - Consulter toutes les évaluations
   - Générer des rapports globaux
   - Exporter les données

## 🛠️ Technologies Utilisées

- **Backend** : Python 3.8+
- **Base de données** : PostgreSQL
- **API** : Flask avec CORS
- **Interface graphique** : CustomTkinter
- **Visualisation** : Matplotlib, Seaborn
- **Traitement des données** : Pandas, NumPy

## 📋 Prérequis

- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd systeme-evaluation-enseignants
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration de la base de données

#### Option A : Utiliser les paramètres par défaut

Le système utilise par défaut :

- Host : localhost
- Port : 5432
- Base de données : evaluation_enseignants
- Utilisateur : postgres
- Mot de passe : password

#### Option B : Configuration personnalisée

Créer un fichier `.env` à la racine du projet :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=evaluation_enseignants
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
SECRET_KEY=votre_cle_secrete
DEBUG=True
```

### 4. Initialiser la base de données

```bash
python database_init.py
```

Cette commande va :

- Créer la base de données PostgreSQL
- Créer toutes les tables nécessaires
- Insérer des données d'exemple

### 5. Vérifier l'installation

```bash
python -c "from models import DatabaseConnection; print('Connexion OK' if DatabaseConnection.get_connection() else 'Erreur de connexion')"
```

## 🎮 Utilisation

### Interface Graphique

Lancer l'interface graphique :

```bash
python interface_graphique.py
```

#### Comptes de test disponibles :

- **Administrateur** : ADMIN001 / admin123
- **Enseignant** : ENS001 / enseignant123
- **Étudiant** : ETU001 / etudiant123

### API REST

Lancer l'API Flask :

```bash
python api.py
```

L'API sera accessible sur `http://localhost:5000`

#### Endpoints principaux :

**Authentification :**

- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion
- `GET /api/auth/profile` - Profil utilisateur

**Étudiants :**

- `GET /api/student/evaluations` - Mes évaluations
- `POST /api/student/evaluations` - Créer une évaluation
- `GET /api/student/courses` - Cours disponibles

**Enseignants :**

- `GET /api/teacher/evaluations` - Évaluations reçues
- `GET /api/teacher/statistics` - Statistiques
- `GET /api/teacher/report` - Rapport de performance

**Administrateurs :**

- `GET /api/admin/users` - Tous les utilisateurs
- `GET /api/admin/evaluations` - Toutes les évaluations
- `GET /api/admin/statistics` - Statistiques globales
- `POST /api/admin/export` - Exporter les données

## 📊 Critères d'Évaluation

Le système évalue les enseignants selon 12 critères (note de 1 à 5) :

1. **Clarté du cours** - Qualité de l'explication
2. **Ponctualité** - Respect des horaires
3. **Pédagogie** - Méthodes d'enseignement
4. **Disponibilité** - Accessibilité aux étudiants
5. **Maîtrise de la matière** - Expertise du sujet
6. **Respect des étudiants** - Attitude envers les étudiants
7. **Gestion du temps** - Organisation du cours
8. **Appréciation stimulée** - Motivation des étudiants
9. **Utilisation des outils** - Technologies et supports
10. **Approche interactive** - Participation des étudiants
11. **Cohérence avec les objectifs** - Alignement pédagogique
12. **Utilité professionnelle** - Application pratique

## 🗄️ Structure de la Base de Données

### Tables principales :

- **utilisateurs** : Informations des utilisateurs
- **cours** : Catalogue des cours
- **enseignements** : Attribution cours-enseignants
- **evaluations** : Évaluations des enseignants

### Index créés pour optimiser les performances :

- `idx_evaluations_etudiant`
- `idx_evaluations_enseignant`
- `idx_evaluations_cours`
- `idx_evaluations_date`

## 🔧 Fonctionnalités Avancées

### Statistiques et Rapports

- **Moyennes par critère** : Calcul automatique des moyennes
- **Graphiques interactifs** : Visualisation avec Matplotlib
- **Rapports PDF** : Export des rapports (à implémenter)
- **Export JSON** : Données exportables

### Sécurité

- **Authentification** : Sessions sécurisées
- **Autorisation** : Contrôle d'accès par rôle
- **Validation** : Vérification des données d'entrée
- **Chiffrement** : Mots de passe sécurisés

### Interface Utilisateur

- **Thème sombre/clair** : Personnalisation de l'apparence
- **Interface responsive** : Adaptation à différentes tailles d'écran
- **Navigation intuitive** : Onglets organisés par fonctionnalité
- **Feedback utilisateur** : Messages d'erreur et de succès

## 🐛 Dépannage

### Problèmes courants :

1. **Erreur de connexion PostgreSQL**

   ```
   Solution : Vérifier que PostgreSQL est démarré et les paramètres de connexion
   ```
2. **Module non trouvé**

   ```
   Solution : Installer les dépendances avec pip install -r requirements.txt
   ```
3. **Erreur de port déjà utilisé**

   ```
   Solution : Changer le port dans api.py ou arrêter le processus qui utilise le port
   ```
4. **Interface graphique ne s'affiche pas**

   ```
   Solution : Vérifier l'installation de CustomTkinter et les dépendances graphiques
   ```

## 📈 Améliorations Futures

- [ ]  Interface web avec React/Vue.js
- [ ]  Notifications en temps réel
- [ ]  Système de commentaires anonymes
- [ ]  Rapports PDF automatiques
- [ ]  Intégration avec les systèmes d'information universitaires
- [ ]  API mobile pour applications mobiles
- [ ]  Système de notifications par email
- [ ]  Tableau de bord avec métriques avancées

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Développé pour un projet académique
- Basé sur les diagrammes UML fournis
- Architecture modulaire et extensible

## 📞 Support

Pour toute question ou problème :

- Créer une issue sur GitHub
- Consulter la documentation technique
- Vérifier les logs d'erreur

---

**Note** : Ce système est conçu pour un environnement éducatif et respecte les bonnes pratiques de développement et de sécurité.
