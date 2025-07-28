#!/usr/bin/env python3
"""
Script principal du système d'évaluation des enseignants
Permet de lancer l'interface graphique ou l'API selon les besoins
"""

import sys
import os
import argparse
from config import Config

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    missing_deps = []
    
    # Vérifier les dépendances essentielles
    try:
        import psycopg2
        print("✅ psycopg2-binary installé")
    except ImportError:
        missing_deps.append("psycopg2-binary")
    
    try:
        import flask
        print("✅ Flask installé")
    except ImportError:
        missing_deps.append("flask")
    
    try:
        import customtkinter
        print("✅ CustomTkinter installé")
    except ImportError:
        missing_deps.append("customtkinter")
    
    # Vérifier les dépendances optionnelles
    try:
        import matplotlib
        print("✅ Matplotlib installé")
    except ImportError:
        print("⚠️  Matplotlib non installé (optionnel)")
    
    try:
        import pandas
        print("✅ Pandas installé")
    except ImportError:
        print("⚠️  Pandas non installé (optionnel)")
    
    if missing_deps:
        print(f"❌ Dépendances manquantes : {', '.join(missing_deps)}")
        return False
    
    print("✅ Toutes les dépendances essentielles sont installées")
    return True

def check_database():
    """Vérifier la connexion à la base de données"""
    try:
        from models import DatabaseConnection
        conn = DatabaseConnection.get_connection()
        if conn:
            conn.close()
            print("✅ Connexion à la base de données réussie")
            return True
        else:
            print("❌ Impossible de se connecter à la base de données")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données : {e}")
        return False

def initialize_database():
    """Initialiser la base de données"""
    try:
        print("🔄 Initialisation de la base de données...")
        from database_init import main as init_db
        init_db()
        print("✅ Base de données initialisée avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        return False

def launch_gui():
    """Lancer l'interface graphique"""
    try:
        print("🚀 Lancement de l'interface graphique...")
        from interface_graphique import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface : {e}")

def launch_api():
    """Lancer l'API Flask"""
    try:
        print("🚀 Lancement de l'API Flask...")
        print(f"📡 API accessible sur : http://localhost:5000")
        print("🔍 Documentation des endpoints : http://localhost:5000/api/health")
        from api import app
        app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'API : {e}")

def show_info():
    """Afficher les informations du système"""
    print("\n" + "="*60)
    print("🎓 SYSTÈME D'ÉVALUATION DES ENSEIGNANTS")
    print("="*60)
    print(f"📊 Version : 1.0.0")
    print(f"🐍 Python : {sys.version}")
    print(f"🗄️ Base de données : PostgreSQL")
    print(f"🎨 Interface : CustomTkinter")
    print(f"🌐 API : Flask")
    print("="*60)
    
    print("\n📋 Comptes de test disponibles :")
    print("   👨‍💼 Administrateur : ADMIN001 / admin123")
    print("   👨‍🏫 Enseignant     : ENS001 / enseignant123")
    print("   👨‍🎓 Étudiant       : ETU001 / etudiant123")
    print("="*60)

def show_help():
    """Afficher l'aide"""
    print("\n📖 AIDE - Système d'Évaluation des Enseignants")
    print("="*50)
    print("Usage : python main.py [OPTIONS]")
    print("\nOptions :")
    print("  --gui, -g          Lancer l'interface graphique")
    print("  --api, -a          Lancer l'API Flask")
    print("  --init, -i         Initialiser la base de données")
    print("  --check, -c        Vérifier l'installation")
    print("  --info, --version  Afficher les informations")
    print("  --help, -h         Afficher cette aide")
    print("\nExemples :")
    print("  python main.py --gui")
    print("  python main.py --api")
    print("  python main.py --init")
    print("  python main.py --check")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Système d'Évaluation des Enseignants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  python main.py --gui          # Lancer l'interface graphique
  python main.py --api          # Lancer l'API Flask
  python main.py --init         # Initialiser la base de données
  python main.py --check        # Vérifier l'installation
        """
    )
    
    parser.add_argument('--gui', '-g', action='store_true',
                       help='Lancer l\'interface graphique')
    parser.add_argument('--api', '-a', action='store_true',
                       help='Lancer l\'API Flask')
    parser.add_argument('--init', '-i', action='store_true',
                       help='Initialiser la base de données')
    parser.add_argument('--check', '-c', action='store_true',
                       help='Vérifier l\'installation')
    parser.add_argument('--info', action='store_true',
                       help='Afficher les informations du système')
    parser.add_argument('--version', action='store_true',
                       help='Afficher la version du système')
    
    args = parser.parse_args()
    
    # Si aucun argument, afficher l'aide
    if len(sys.argv) == 1:
        show_info()
        print("\n💡 Utilisez --help pour voir toutes les options disponibles ")
        return
    
    # Traitement des arguments
    if args.info or args.version:
        show_info()
        return
    
    
    if args.check:
        print("🔍 Vérification de l'installation...")
        deps_ok = check_dependencies()
        db_ok = check_database()
        
        if deps_ok and db_ok:
            print("\n✅ Installation correcte !")
            print("🎉 Le système est prêt à être utilisé.")
        else:
            print("\n❌ Problèmes détectés.")
            if not deps_ok:
                print("   - Installez les dépendances : pip install -r requirements.txt")
            if not db_ok:
                print("   - Vérifiez la configuration PostgreSQL")
                print("   - Lancez l'initialisation : python main.py --init")
        return
    
    if args.init:
        if check_dependencies():
            initialize_database()
        else:
            print("❌ Impossible d'initialiser sans les dépendances")
        return
    
    # Vérifications préalables pour le lancement
    if args.gui or args.api:
        print("🔍 Vérification de l'environnement...")
        
        if not check_dependencies():
            print("❌ Arrêt : dépendances manquantes")
            return
        
        if not check_database():
            print("⚠️  Attention : problème de connexion à la base de données")
            print("💡 Essayez : python main.py --init")
            response = input("Continuer quand même ? (y/N) : ")
            if response.lower() != 'y':
                return
    
    # Lancement des services
    if args.gui:
        launch_gui()
    elif args.api:
        launch_api()
    else:
        # Mode interactif si aucun argument spécifique
        show_info()
        print("\n🎯 Que souhaitez-vous faire ?")
        print("1. Lancer l'interface graphique")
        print("2. Lancer l'API Flask")
        print("3. Initialiser la base de données")
        print("4. Vérifier l'installation")
        print("5. Quitter")
        
        try:
            choice = input("\nVotre choix (1-5) : ").strip()
            
            if choice == '1':
                launch_gui()
            elif choice == '2':
                launch_api()
            elif choice == '3':
                initialize_database()
            elif choice == '4':
                print("🔍 Vérification de l'installation...")
                deps_ok = check_dependencies()
                db_ok = check_database()
                if deps_ok and db_ok:
                    print("✅ Installation correcte !")
                else:
                    print("❌ Problèmes détectés.")
            elif choice == '5':
                print("👋 Au revoir !")
            else:
                print("❌ Choix invalide")
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
        except Exception as e:
            print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main() 