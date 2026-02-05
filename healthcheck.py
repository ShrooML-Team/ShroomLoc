#!/usr/bin/env python3
"""
Script de healthcheck pour ShroomLoc API
Vérifie que l'application FastAPI répond correctement
"""

import sys
import time
import urllib.request
import urllib.error
import json
import os
from typing import Optional


def check_endpoint(url: str, timeout: int = 5) -> tuple[bool, str]:
    """
    Vérifie qu'un endpoint répond correctement
    
    Args:
        url: URL à tester
        timeout: Timeout en secondes
        
    Returns:
        Tuple (success, message)
    """
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            if response.getcode() == 200:
                return True, f"✅ {url} - OK ({response.getcode()})"
            else:
                return False, f"❌ {url} - Code: {response.getcode()}"
    except urllib.error.HTTPError as e:
        return False, f"❌ {url} - HTTP Error: {e.code}"
    except urllib.error.URLError as e:
        return False, f"❌ {url} - URL Error: {e.reason}"
    except Exception as e:
        return False, f"❌ {url} - Error: {str(e)}"


def check_api_health(host: str = "localhost", port: int = 8000) -> bool:
    """
    Vérifie la santé de l'API ShroomLoc
    
    Args:
        host: Hôte de l'API
        port: Port de l'API
        
    Returns:
        True si l'API est en bonne santé, False sinon
    """
    base_url = f"http://{host}:{port}"
    
    # Liste des endpoints à tester
    endpoints = [
        "/docs",           # Documentation Swagger
        "/openapi.json",   # Schéma OpenAPI
    ]
    
    print(f"🔍 Vérification de l'API ShroomLoc sur {base_url}")
    
    all_success = True
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        success, message = check_endpoint(url)
        print(f"  {message}")
        
        if not success:
            all_success = False
    
    # Test d'un endpoint avec authentification (sans credentials)
    # Doit retourner 401, ce qui indique que l'API fonctionne
    auth_url = f"{base_url}/mushrooms?latitude=45.0&longitude=2.0"
    try:
        urllib.request.urlopen(auth_url, timeout=5)
        print(f"  ⚠️  {auth_url} - Pas d'authentification requise (inattendu)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"  ✅ {auth_url} - Authentification requise (OK)")
        else:
            print(f"  ❌ {auth_url} - Code inattendu: {e.code}")
            all_success = False
    except Exception as e:
        print(f"  ❌ {auth_url} - Error: {str(e)}")
        all_success = False
    
    return all_success


def main():
    """Point d'entrée principal"""
    # Récupération des variables d'environnement
    host = os.getenv("HEALTHCHECK_HOST", "localhost")
    port = int(os.getenv("HEALTHCHECK_PORT", "8000"))
    
    # Arguments en ligne de commande
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print("Usage: python healthcheck.py [host] [port]")
            print("Variables d'environnement:")
            print("  HEALTHCHECK_HOST (défaut: localhost)")
            print("  HEALTHCHECK_PORT (défaut: 8000)")
            sys.exit(0)
        
        if len(sys.argv) >= 2:
            host = sys.argv[1]
        if len(sys.argv) >= 3:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print(f"❌ Port invalide: {sys.argv[2]}")
                sys.exit(1)
    
    # Vérification de la santé
    start_time = time.time()
    is_healthy = check_api_health(host, port)
    duration = time.time() - start_time
    
    print(f"\n⏱️  Durée: {duration:.2f}s")
    
    if is_healthy:
        print("🎉 L'API ShroomLoc est en bonne santé !")
        sys.exit(0)
    else:
        print("💥 L'API ShroomLoc a des problèmes de santé !")
        sys.exit(1)


if __name__ == "__main__":
    main()