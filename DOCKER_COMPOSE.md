# Docker Compose - ShroomLoc

Ce fichier Docker Compose vous permet de lancer facilement l'API ShroomLoc en utilisant l'image pré-construite hébergée sur GitHub Container Registry.

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose installés

### Lancement
```bash
# Démarrer l'application
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down
```

## 📋 Configuration

L'application sera accessible sur : http://localhost:8000

- **Documentation Swagger** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Variables d'environnement
Copiez `.env.example` vers `.env` pour personnaliser la configuration :
```bash
cp .env.example .env
```

## 🔐 Authentification par défaut

L'application crée automatiquement un utilisateur admin :
- **Username** : `admin`
- **Password** : `password123`

⚠️ **Important** : Changez ce mot de passe en production !

## 💾 Persistance des données

**Par défaut, aucune persistance n'est configurée** pour cette API car :
- Les données principales (champignons) sont stockées dans un fichier JSON statique
- La base SQLite ne contient que les comptes utilisateurs
- L'utilisateur admin par défaut est automatiquement recréé à chaque démarrage

### Si vous souhaitez persister les utilisateurs :

1. **Option simple** : Décommentez dans docker-compose.yml :
```yaml
volumes:
  - ./data/shroomloc.db:/app/shroomloc.db
```

2. **Créez d'abord le fichier** :
```bash
mkdir -p data
touch data/shroomloc.db
```

⚠️ **Attention** : Ne montez jamais tout le dossier `/app` car cela écrasera le code de l'application !

## 🔄 Mise à jour

Pour utiliser la dernière image :
```bash
docker-compose pull
docker-compose up -d
```

## 📊 Monitoring

L'application inclut un healthcheck qui vérifie automatiquement que l'API répond correctement.

Status du service :
```bash
docker-compose ps
```