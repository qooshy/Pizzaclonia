# PizzaClonia(TM) - Challenge de Pentest

> "Every slice brings us closer."

Un challenge CTF en 3 étapes enchaînées autour d'une pizzeria alien-cultiste.

\---

## Lancement

```bash
docker compose up --build
```

Accès : http://localhost:8000

\---

## Architecture

```

  web (FastAPI) - port 8000 exposé   
   /static/js/app.js (forensic)   
   /staff-only  (IDOR)            
   /api/delivery-check  (SSRF)    

                    réseau Docker interne uniquement

  internal (Flask) - port 5000       
  NON EXPOSÉ à l'extérieur           
   /members  (données exfiltrées) 
   /flag                          

```

\---

## Chaîne d'exploitation

### ÉTAPE 1 - Forensic JS (DevTools)

1. Ouvrir http://localhost:8000
2. DevTools  onglet **Sources**  `app.js`
3. Repérer le tableau `\_ref` avec des fragments base64 :

```javascript
   const \_ref = \["Y2ww", "bmUt", "YjN0YQ=="];
   ```

4. Dans la Console DevTools :

```javascript
   \_ref.map(atob).join("")
   //  "cl0n3-b3ta"
   ```

5. Accéder à : `http://localhost:8000/staff-only?token=cl0n3-b3ta`

\---

### ÉTAPE 2 - IDOR

1. Le portail staff liste les commandes via `/api/orders?token=cl0n3-b3ta`
2. Accéder à **chaque commande par son ID** : `/api/orders/1`, `/api/orders/2`...
3. **Aucune vérification d'identité** - les clones se font mutuellement confiance
4. La commande **#4** (Haut Prêtre ZX-9) contient la clé API interne :

```
   internal\_key: CULT-API-7731-ZETA
   ```

\---

### ÉTAPE 3 - SSRF

1. Dans le portail staff  section "Vérification Zone de Livraison"
2. Entrer l'URL du service interne (non joignable depuis le browser) :

```
   http://internal:5000/members?api_key=CULT-API-7731-ZETA
   ```

3. Le serveur web effectue la requête à notre place  retourne la liste complète des membres
4. Pour le flag :

```
   http://internal:5000/flag?api_key=CULT-API-7731-ZETA
   ```

**FLAG** : `FLAG{ssrf\_p1zz4\_cl0n14\_3xf1ltr4t10n\_c0mpl3t3\_}`

\---

## Vulnérabilités \& correctifs

### Forensic - Secret dans JS côté client

**Problème** : Les secrets ne doivent jamais être dans le code client.  
**Correctif** : Auth server-side via session, cookie httpOnly, ou flux OAuth. Jamais de token en clair ou reconstituable dans le JS.

### IDOR - Absence de contrôle d'accès par ressource

**Problème** : `/api/orders/{id}` ne vérifie pas que le token appartient au propriétaire de la commande.  
**Correctif** : Lier chaque ressource à un utilisateur et vérifier l'appartenance côté serveur avant tout accès.

### SSRF - Requête HTTP côté serveur vers URL arbitraire

**Problème** : `address\_url` est fetchée sans validation  accès au réseau interne.  
**Correctif** : Allowlist stricte des domaines autorisés, bloquer les IP privées (RFC 1918), ne jamais exposer ce genre d'endpoint sans validation.

\---

## Notes techniques

* no PHP  (Python uniquement)
* Docker Compose  (2 services, réseau isolé)
* Lancement immédiat : `docker compose up --build`
* Interface cohérente  (thème alien kitsch, Orbitron + Crimson Pro)
* Aucun outil externe requis pour le forensic  (DevTools natif)

