#!/usr/bin/env python3
"""
Script de test local pour l'API ShroomLoc
Version standalone pour tester l'API localement
"""

import argparse
import sys
import urllib.request
import urllib.error
import time


def check_endpoint(url: str, timeout: int = 5) -> tuple[bool, str]:
    """Vérifie qu'un endpoint répond correctement"""
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


def main():
    parser = argparse.ArgumentParser(description="Test de santé local pour ShroomLoc API")
    parser.add_argument("--host", default="localhost", help="Hôte de l'API (défaut: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="Port de l'API (défaut: 8000)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🔍 Test de l'API ShroomLoc")
        print(f"📍 Host: {args.host}")
        print(f"🔌 Port: {args.port}")
        print("-" * 50)
    
    base_url = f"http://{args.host}:{args.port}"
    endpoints = ["/docs", "/openapi.json"]
    
    all_success = True
    start_time = time.time()
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        success, message = check_endpoint(url)
        if args.verbose:
            print(f"  {message}")
        if not success:
            all_success = False
    
    # Test endpoint avec auth (doit retourner 401)
    auth_url = f"{base_url}/mushrooms?latitude=45.0&longitude=2.0"
    try:
        urllib.request.urlopen(auth_url, timeout=5)
        if args.verbose:
            print(f"  ⚠️  {auth_url} - Pas d'auth requise (inattendu)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            if args.verbose:
                print(f"  ✅ {auth_url} - Auth requise (OK)")
        else:
            if args.verbose:
                print(f"  ❌ {auth_url} - Code: {e.code}")
            all_success = False
    except Exception as e:
        if args.verbose:
            print(f"  ❌ {auth_url} - Error: {str(e)}")
        all_success = False
    
    duration = time.time() - start_time
    
    if args.verbose:
        print(f"\n⏱️  Durée: {duration:.2f}s")
        print("=" * 50)
    
    if all_success:
        print("✨ API disponible et fonctionnelle !")
        sys.exit(0)
    else:
        print("❌ Problème détecté avec l'API !")
        if not args.verbose:
            print("Utilisez --verbose pour plus de détails")
        sys.exit(1)


if __name__ == "__main__":
    main()