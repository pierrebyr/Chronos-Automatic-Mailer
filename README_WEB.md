# 🌐 Chronos Web Interface

## Interface Web Moderne et Professionnelle

Cette application dispose maintenant d'une interface web complète, moderne et professionnelle qui remplace l'interface en ligne de commande.

## 🚀 Lancement Rapide

### Linux/Mac
```bash
./start_web.sh
```

### Windows
```batch
start_web.bat
```

L'application sera accessible à : **http://localhost:8501**

## ✨ Fonctionnalités

### 📊 Dashboard
- Vue d'ensemble des métriques clés
- Graphiques interactifs
- Statistiques en temps réel
- Activités récentes
- Actions rapides

### 🔍 Recherche de Marques
- Formulaire interactif pour rechercher de nouvelles marques
- Filtrage par catégorie et limite
- Historique des recherches
- Statistiques de recherche

### 👥 Gestion des Prospects
- Tableau complet de tous les prospects
- Filtres avancés (catégorie, statut, recherche textuelle)
- Vue détaillée de chaque prospect
- Gestion des statuts (prospect → contacted → lead → client)
- Actions rapides (générer emails, voir analytics)

### 📝 Séquences d'Emails
- Génération par lot ou individuelle
- Prévisualisation des emails générés
- Suivi des prospects sans séquences
- Vue de toutes les séquences existantes
- Statut d'envoi pour chaque email

### 📤 Envoi d'Emails
- Sélection de l'email dans la séquence (1, 2, ou 3)
- Filtrage par catégorie
- Prévisualisation avant envoi
- Configuration du délai entre envois
- Mode test (simulation sans envoi réel)
- Confirmation de sécurité
- Barre de progression en temps réel
- Historique des envois

### ⏱️ Historique
- Timeline complète de toutes les activités
- Filtrage par période et type d'activité
- Vue groupée par date
- Icônes et couleurs par type d'activité
- Export en CSV

### 📊 Analytics
- Métriques de performance détaillées
- Graphiques interactifs (donut, funnel, treemap, heatmap)
- Analyse par catégorie
- Taux de complétion des séquences
- Activité des 30 derniers jours
- Insights clés automatiques

### ⚙️ Settings
- Configuration des clés API
- Informations de l'expéditeur
- Informations système
- Gestion de la base de données
- Documentation intégrée

## 🎨 Design

L'interface utilise un design system moderne avec :
- Palette de couleurs professionnelle (indigo/bleu)
- Typographie Inter
- Cards avec ombre et effets hover
- Sidebar sombre avec navigation claire
- Graphiques Plotly interactifs
- Animations fluides
- Design responsive

## 📋 Structure

```
Chronos-Automatic-Mailer/
├── app.py                 # Point d'entrée principal
├── web_styles.py          # Design system et CSS
├── pages/                 # Pages de l'application
│   ├── __init__.py
│   ├── dashboard.py       # Page d'accueil
│   ├── research.py        # Recherche de marques
│   ├── prospects.py       # Gestion des prospects
│   ├── email_sequences.py # Génération d'emails
│   ├── send_emails.py     # Envoi de campagnes
│   ├── history.py         # Historique d'activités
│   ├── analytics.py       # Analytics avancées
│   └── settings.py        # Configuration
├── database.py            # Base de données améliorée
├── main.py                # Logique métier
├── research_engine.py     # Moteur de recherche
├── email_generator.py     # Génération d'emails
└── email_sender.py        # Envoi d'emails
```

## 🔄 Migration depuis l'ancienne interface

L'ancienne interface CLI est toujours disponible via `main.py` :

```bash
# Ancienne méthode (toujours fonctionnelle)
python main.py research --category "Irish Whiskey" --limit 20
python main.py generate
python main.py send --email 1

# Nouvelle méthode (recommandée)
./start_web.sh
```

## 📈 Améliorations de la Base de Données

La base de données a été améliorée avec :
- **activity_log** : Historique complet de toutes les actions
- **tags** : Système de tags pour les prospects
- **campaigns** : Gestion de campagnes
- Métriques améliorées sur les emails (ouvertures, clics, réponses)
- Fonctions d'analytics avancées

## 💡 Conseils d'Utilisation

1. **Première utilisation** : Lancez le setup si pas encore fait
2. **Workflow recommandé** :
   - Dashboard → voir l'état général
   - Research → ajouter de nouveaux prospects
   - Email Sequences → générer les campagnes
   - Send Emails → lancer les envois
   - Analytics → analyser les performances

3. **Sécurité** : Utilisez le fichier `.env` pour stocker vos clés API
4. **Sauvegarde** : La base de données est dans `chronos_outreach.db`
5. **Logs** : Les logs sont dans `chronos_outreach.log`

## 🆘 Support

En cas de problème :
1. Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
2. Vérifiez la configuration : `config.json` et `.env`
3. Consultez les logs : `chronos_outreach.log`
4. Relancez le setup : `python setup.py`

## 📦 Dépendances Principales

- **Streamlit** : Framework web
- **Plotly** : Graphiques interactifs
- **Pandas** : Manipulation de données
- **Anthropic** : API Claude
- **SQLite** : Base de données

## 🎯 Prochaines Fonctionnalités

- Tracking des ouvertures et clics d'emails (intégration service tiers)
- Export PDF des rapports
- Modèles d'emails personnalisables
- A/B testing des sujets
- Intégration CRM
- Notifications push
- Mode multi-utilisateurs

---

Développé avec ❤️ et Claude AI
