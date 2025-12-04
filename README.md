# SnakeSQL - Python Edition

![Version](https://img.shields.io/badge/version-2.0.1-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-red)

Un outil de test d'injection SQL avancé réécrit en Python.

## 📝 Crédits

- **Original Bash Script**: @ImKKingshuk - https://github.com/ImKKingshuk
- **Python Conversion**: 187ctf

## 🎯 Fonctionnalités

- **Détection automatique** de vulnérabilités SQL Injection
- **Blind SQL Injection** avec deux méthodes :
  - Time-based (basée sur le temps)
  - Boolean-based (basée sur les conditions booléennes)
- **Énumération** de bases de données, tables et colonnes
- **Extraction de données** caractère par caractère
- **Support des proxies** et configurations avancées
- **Génération de rapports** en plusieurs formats
- **User-Agent aléatoire** pour éviter la détection
- **Résumé détaillé** de l'exécution

## 📋 Prérequis

```bash
pip install requests
```

## 🚀 Installation

```bash
git clone <repository-url>
cd SnakeSQL
chmod +x stealthsql.py
```

## 💻 Utilisation

### Utilisation basique

```bash
python3 stealthsql.py
```

ou

```bash
./stealthsql.py
```

### Configuration interactive

Le script vous demandera de configurer :

1. **URL cible** - L'URL vulnérable à tester
2. **Cookie de session** (optionnel) - Pour les sessions authentifiées
3. **Token d'authentification** (optionnel) - Bearer token
4. **Proxy** (optionnel) - Pour router les requêtes
5. **Headers personnalisés** (optionnel) - Headers HTTP supplémentaires
6. **User-Agent** - Généré automatiquement ou personnalisé
7. **Type de SQLi** - Time-based (T) ou Boolean-based (B)
8. **Requête SQL** - La requête SQL à exécuter

### Exemple de workflow

```
1. Entrer l'URL : http://example.com/page.php?id=
2. Choisir le type : T (Time-based)
3. Entrer la requête : SELECT username FROM users
4. Le script va :
   - Détecter la vulnérabilité
   - Extraire les données
   - Proposer l'énumération
   - Générer un rapport
```

## 🔍 Types d'injection supportés

### Time-Based Blind SQL Injection
Exploite les délais dans les réponses pour détecter les conditions vraies/fausses.

### Boolean-Based Blind SQL Injection
Compare la longueur des réponses pour détecter les conditions vraies/fausses.

## 📊 Énumération

Le script peut énumérer :
- **Databases** - Liste toutes les bases de données
- **Tables** - Liste les tables d'une base de données
- **Columns** - Liste les colonnes d'une table

## 📄 Génération de rapports

Formats supportés :
- HTML
- JSON
- CSV

## ⚠️ Avertissement

Cet outil est destiné **uniquement à des fins éducatives** et pour des tests autorisés.

**N'utilisez cet outil que sur :**
- Vos propres applications
- Des systèmes pour lesquels vous avez une autorisation écrite
- Des environnements de test/CTF

L'utilisation non autorisée de cet outil sur des systèmes tiers est **illégale**.

## 🔧 Différences avec la version Bash

### Améliorations
- ✅ Code plus lisible et maintenable
- ✅ Meilleure gestion des erreurs
- ✅ Support natif des requêtes HTTP avec `requests`
- ✅ Pas de dépendances externes complexes (curl, jq, etc.)
- ✅ Portable sur tous les OS (Windows, Linux, macOS)

### Comportement identique
- ✅ Même algorithme d'extraction
- ✅ Mêmes payloads de détection
- ✅ Même interface utilisateur
- ✅ Même formatage de sortie

## 📚 Structure du code

```python
StealthSQL/
│
├── stealthsql.py      # Script principal
└── README.md          # Documentation
```

## 🐛 Dépannage

### Erreur : Module 'requests' non trouvé
```bash
pip install requests
```

### Erreur : Permission denied
```bash
chmod +x stealthsql.py
```

## 📖 Documentation technique

### Classe principale : `StealthSQL`

Méthodes principales :
- `detect_sqli()` - Détection de vulnérabilités
- `blind_sql_injection()` - Exploitation blind SQLi
- `get_query_output()` - Extraction caractère par caractère
- `enumerate()` - Énumération DB/tables/colonnes
- `generate_report()` - Génération de rapports

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation

## 📜 Licence

Ce projet est sous licence MIT.

## 👥 Auteurs

- **Original Bash Script** : @ImKKingshuk
- **Conversion Python** : 187ctf

---

**Rappel** : Utilisez cet outil de manière éthique et légale ! 🛡️
