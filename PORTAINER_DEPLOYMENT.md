# 🐙 Déploiement Portainer - ShroomLoc

Ce guide explique comment déployer ShroomLoc sur Portainer en utilisant les fichiers de configuration automatisés.

## 📋 Prérequis

- Portainer installé et configuré
- Accès Docker sur le nœud cible
- Fichier : `docker-compose.yml`

## 🚀 Déploiement

### 1. Créer une nouvelle Stack dans Portainer

1. Connectez-vous à Portainer
2. Allez dans **Stacks** → **Add Stack**
3. Nommez votre stack : `shroomloc`

### 2. Configuration de la Stack

#### Méthode A : Upload (Recommandé)
1. Choisissez **Upload**
2. Uploadez le fichier `docker-compose.yml`

#### Méthode B : Git Repository
1. Choisissez **Repository**
2. URL : `https://github.com/ShrooML-Team/ShroomLoc.git`
3. Compose file path : `docker-compose.yml`

### 3. Variables d'environnement

Dans la section **Environment variables**, ajoutez les variables souhaitées :

```
IMAGE_TAG=latest
HOST_PORT=63001
```

### 4. Variables configurables

| Variable | Description | Défaut | Exemple |
|----------|-------------|---------|---------|
| `IMAGE_TAG` | Version de l'image Docker | `latest` | `v0.2.3`, `main` |
| `HOST_PORT` | Port exposé sur l'hôte | `8000` | `8080`, `9000` |
| `API_PORT` | Port interne du conteneur | `8000` | `8000` |
| `CONTAINER_NAME` | Nom du conteneur | `shroomloc-api` | `my-shroomloc` |
| `RESTART_POLICY` | Politique de redémarrage | `unless-stopped` | `always`, `no` |
| `DATA_PATH` | Chemin des données dans le conteneur | `/app/data` | `/app/data` |

### 5. Déploiement final

1. Cliquez sur **Deploy the stack**
2. Attendez que les conteneurs se lancent
3. Vérifiez dans **Containers** que `shroomloc-api` est **running**

## 🔍 Vérification

L'application sera accessible sur :
- **API** : `http://[IP-SERVEUR]:[HOST_PORT]`
- **Documentation** : `http://[IP-SERVEUR]:[HOST_PORT]/docs`

Example : `http://192.168.1.100:8000/docs`

## 🔄 Mise à jour

### Via Portainer UI
1. Allez dans **Stacks** → `shroomloc`
2. Cliquez sur **Editor**
3. Modifiez `IMAGE_TAG` si nécessaire
4. Cliquez sur **Update the stack**
5. Cochez **Re-pull image and redeploy**

### Via API Portainer
```bash
curl -X POST "http://portainer:9000/api/stacks/[STACK_ID]/redeploy" \
     -H "Authorization: Bearer [TOKEN]"
```

## 🛠️ Configuration avancée

### Variables personnalisées

Ajoutez dans les variables d'environnement Portainer :

```env
# Base de données personnalisée
DATABASE_URL=sqlite:///./data/shroomloc.db

# Monitoring personnalisé
HEALTHCHECK_INTERVAL=60s
HEALTHCHECK_RETRIES=5
```

### Multi-environnement

Créez plusieurs stacks avec des variables différentes :

- **Production** : `IMAGE_TAG=latest`, `HOST_PORT=8000`
- **Staging** : `IMAGE_TAG=dev`, `HOST_PORT=8001`  
- **Test** : `IMAGE_TAG=pr-123`, `HOST_PORT=8002`

## 🔐 Sécurité

### Variables sensibles
Pour les variables sensibles, utilisez les **Secrets** de Portainer :
1. **Secrets** → **Add secret**
2. Dans le docker-compose, référencez avec `secrets:`

### Réseau privé
```yaml
networks:
  shroomloc-network:
    driver: bridge
    internal: true
```

## 🚨 Troubleshooting

### Conteneur ne démarre pas
1. Vérifiez les logs dans **Containers** → `shroomloc-api` → **Logs**
2. Vérifiez les variables d'environnement
3. Vérifiez la disponibilité de l'image

### Port déjà utilisé
Changez `HOST_PORT` dans les variables d'environnement.

### Problème d'image
```bash
# Vérifiez la disponibilité
docker pull ghcr.io/shrooml-team/shroomloc:latest
```