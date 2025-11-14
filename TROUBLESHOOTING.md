# 🔧 Guide de Dépannage

## ✅ Problèmes Résolus

### 1. Erreur 404 - Modèle Claude
**Problème :** `model: claude-3-5-sonnet-20241022` retournait 404
**Solution :** Corrigé vers `claude-3-5-sonnet-20240620` (le vrai modèle disponible)

## 🚨 Actions Requises

### 2. API Brave - Rate Limit (429)

**Problème actuel :**
```
⚠ Search API error: 429 Client Error: Too Many Requests
```

**Solutions :**

#### Option A : Utiliser une clé API Brave valide (Recommandé)
1. Allez sur https://brave.com/search/api/
2. Créez un compte gratuit
3. Obtenez votre clé API (gratuit : 2000 requêtes/mois)
4. Ajoutez-la dans `.env` ou `config.json` :

```bash
# .env
BRAVE_API_KEY=votre_clé_brave_ici
```

OU

```json
// config.json
{
  "brave_api_key": "votre_clé_brave_ici"
}
```

#### Option B : Le système utilisera DuckDuckGo en fallback
Si vous n'avez pas de clé Brave, le système utilisera automatiquement DuckDuckGo (gratuit, mais moins performant).

**Aucune action requise**, mais les résultats seront moins précis.

### 3. Configuration Gmail (Optionnel)

Le message suivant est normal si vous n'avez pas configuré Gmail API :
```
⚠️  Gmail credentials not found!
For now, using SMTP fallback...
```

**Pour l'instant, le système utilise SMTP** (méthode simple). Pour configurer Gmail API plus tard :

1. Suivez les étapes dans `API_KEYS_SETUP.md`
2. Téléchargez `gmail_credentials.json`
3. Placez-le à la racine du projet

## 🔄 Appliquer les Corrections

Sur votre machine :

```bash
# Récupérer les corrections
git pull

# Relancer l'application
./start_web.sh
```

## ✅ Vérification de la Configuration

Vérifiez votre fichier `config.json` :

```json
{
    "anthropic_api_key": "sk-ant-xxxxx",  // ✅ Doit être votre vraie clé
    "brave_api_key": "BSA-xxxxx",         // ⚠️ Optionnel mais recommandé
    "sender_name": "Votre Nom",
    "sender_email": "votre-email@example.com",
    "sender_phone": "Votre Téléphone",
    "sender_website": "www.chronos.studio",
    "database_path": "chronos_outreach.db",
    "gmail_credentials_path": "gmail_credentials.json",
    "smtp": {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "votre-email@gmail.com",
        "password": "votre-app-password"
    }
}
```

## 🧪 Test Rapide

Après avoir récupéré les corrections :

1. **Test de l'API Claude** :
   - Allez dans Settings
   - Vérifiez que votre clé Anthropic est configurée
   - Le système devrait maintenant utiliser `claude-3-5-sonnet-20240620`

2. **Test de Recherche** :
   - Allez dans Research
   - Essayez une recherche (ex: "Premium Gin")
   - Si vous avez une clé Brave : devrait fonctionner normalement
   - Sans clé Brave : utilisera DuckDuckGo (moins de résultats)

## 📋 Résumé des Corrections

| Problème | Statut | Action |
|----------|--------|--------|
| Modèle Claude 404 | ✅ Corrigé | `git pull` |
| API Brave 429 | ⚠️ Config requise | Ajouter clé ou ignorer |
| Gmail credentials | ℹ️ Optionnel | SMTP fonctionne |

## 💡 Notes Importantes

- **Le système fonctionne sans Brave API** (fallback DuckDuckGo)
- **SMTP fonctionne sans Gmail API** (méthode simple)
- **Seule la clé Anthropic est obligatoire**

## 🆘 Toujours des Problèmes ?

Si après `git pull` vous avez encore des erreurs :

1. Vérifiez votre clé Anthropic dans `config.json`
2. Vérifiez les logs dans la console
3. Consultez `chronos_outreach.log` pour les détails
4. Partagez les erreurs pour assistance

---

Mise à jour : 2025-11-14
