# PredEntreVar – Guide d'installation Mac

## En 4 commandes, l'app tourne sur ton Mac 🚀

```bash
# 1. Dézipper et entrer dans le dossier
cd ~/Desktop
unzip IBOVI_ROLDE_CODE.zip
cd predentrevar_complet

# 2. Installer Python (si pas déjà fait : https://python.org)
# Vérifier : python3 --version  → doit afficher 3.10+

# 3. Installer les dépendances
pip3 install flask flask-sqlalchemy scikit-learn pandas numpy joblib

# 4. Lancer l'application
python3 run.py
```

## Ouvrir dans le navigateur

- **Dashboard EDA :**  http://localhost:5000
- **Simulateur :**      http://localhost:5000/predict
- **Admin :**           http://localhost:5000/admin

## Identifiants
| Rôle | Login | Mot de passe |
|------|-------|--------------|
| Admin | admin | PredEntreVar2026! |

## Structure du projet
```
predentrevar_complet/
├── run.py                    ← LANCER L'APP ICI : python3 run.py
├── requirements.txt          ← Dépendances Python
├── data/
│   └── creations_var.csv     ← Données INSEE SIDE (221 lignes)
├── models/
│   └── ridge_model.joblib    ← Modèle Ridge pré-entraîné (R²=0.961)
├── app/
│   ├── __init__.py           ← Configuration Flask + import BDD
│   ├── routes/
│   │   ├── main.py           ← Dashboard / API données
│   │   ├── predict.py        ← Formulaire + /api/predict
│   │   └── admin.py          ← Back-office
│   ├── services/
│   │   └── ml_service.py     ← ALGORITHME RIDGE – prédiction
│   ├── models/
│   │   └── models.py         ← Tables BDD (SQLAlchemy)
│   └── templates/
│       ├── base.html         ← Template de base Bootstrap
│       ├── dashboard.html    ← Dashboard avec graphiques Chart.js
│       ├── predict.html      ← Simulateur interactif
│       ├── admin.html        ← Back-office
│       └── login.html        ← Connexion admin
└── predentrevar.db           ← Base de données SQLite (créée automatiquement)
```

## Où se trouvent les choses clés ?

| Quoi | Fichier |
|------|---------|
| **Algorithme Ridge** (prédiction) | `app/services/ml_service.py` |
| **Base de données** SQLite | `predentrevar.db` (créé auto au 1er lancement) |
| **Données INSEE** | `data/creations_var.csv` |
| **Modèle entraîné** | `models/ridge_model.joblib` |
| **Route API** `/api/predict` | `app/routes/predict.py` |
| **Dashboard** graphiques | `app/routes/main.py` + `app/templates/dashboard.html` |
| **Simulateur** prédiction | `app/templates/predict.html` |

## Performances du modèle
| Métrique | Valeur |
|----------|--------|
| R² (jeu de test 20%) | **0,961** |
| RMSE | 193,1 créations |
| MAE | 141,7 créations |
| Jeu d'entraînement | 176 obs. (80%) |
| Jeu de test | 45 obs. (20%) |

## Si une erreur apparaît

```bash
# Erreur "No module named flask" → réinstaller
pip3 install flask flask-sqlalchemy scikit-learn pandas numpy joblib

# Erreur "port 5000 already in use" → changer le port
python3 run.py --port 8080
# Puis ouvrir http://localhost:8080

# Réinitialiser la BDD (si problème)
rm predentrevar.db
python3 run.py  # La recrée automatiquement
```

---
*Mastère Data et Intelligence Artificielle – Nexa Digital School 2025-2026*
*IBOVI Rolde Chadrac | CCI du Var – Toulon*
