"""PredEntreVar – Service Machine Learning
Auteur : IBOVI Rolde Chadrac | CCI du Var | Mastère Data & IA 2025-2026
"""
import joblib
import numpy as np
import pandas as pd

SECTEURS_VALIDES = [
    "Agriculture, sylviculture et peche",
    "Industries extractives",
    "Industrie manufacturiere",
    "Energie, eau, gaz",
    "Construction",
    "Commerce ; reparation automobiles",
    "Transports et entreposage",
    "Hebergement et restauration",
    "Information et communication",
    "Activites financieres et assurance",
    "Activites immobilieres",
    "Activites specialisees, scientifiques et techniques",
    "Activites de services administratifs et de soutien",
    "Enseignement",
    "Sante humaine et action sociale",
    "Arts, spectacles et activites recreatives",
    "Autres activites de services",
]

class MLService:
    def __init__(self):
        self.model        = None
        self.scaler       = None
        self.feature_cols = None
        self.rmse         = 193.1
        self.r2           = 0.961
        self.mae          = 141.7
        self._loaded      = False

    def load_model(self, path='models/ridge_model.joblib'):
        try:
            bundle            = joblib.load(path)
            self.model        = bundle['model']
            self.scaler       = bundle['scaler']
            self.feature_cols = bundle['feature_cols']
            self.r2           = bundle.get('r2', self.r2)
            self.rmse         = bundle.get('rmse', self.rmse)
            self.mae          = bundle.get('mae', self.mae)
            self._loaded      = True
            print(f"✓ Modèle Ridge chargé | R²={self.r2} | RMSE={self.rmse}")
        except Exception as e:
            print(f"⚠ Erreur chargement modèle : {e}")

    def predict(self, secteur, annee, taux_chomage, nuitees=15000.0):
        if not self._loaded:
            raise RuntimeError("Modèle non chargé. Appelez load_model() d'abord.")

        # Construire le vecteur de features
        row = pd.DataFrame({c: [0.0] for c in self.feature_cols})
        row['annee_norm']        = (annee - 2012) / 12
        row['taux_chomage']      = taux_chomage
        row['nuitees_milliers']  = nuitees

        # Encoder le secteur (one-hot)
        col_key = 'sect_' + secteur
        # Cherche la colonne correspondante (correspondance partielle)
        for col in self.feature_cols:
            if secteur[:10] in col or col_key[:15] in col:
                row[col] = 1.0
                break

        # Standardiser et prédire
        X_scaled = self.scaler.transform(row[self.feature_cols])
        pred = float(self.model.predict(X_scaled)[0])
        pred = max(0.0, pred)

        margin = 1.96 * self.rmse  # Intervalle de confiance 95%
        return {
            'prediction':   round(pred),
            'ci_low':       round(max(0, pred - margin)),
            'ci_high':      round(pred + margin),
            'r2':           self.r2,
            'rmse':         self.rmse,
            'mae':          self.mae,
            'secteur':      secteur,
            'annee':        annee,
            'taux_chomage': taux_chomage,
        }

    def get_predictions_for_all_sectors(self, annee=2025, taux_chomage=6.5, nuitees=15000.0):
        """Prédictions pour tous les secteurs – utile pour le dashboard."""
        results = []
        for s in SECTEURS_VALIDES:
            try:
                r = self.predict(s, annee, taux_chomage, nuitees)
                results.append({'secteur': s, 'prediction': r['prediction'],
                                'ci_low': r['ci_low'], 'ci_high': r['ci_high']})
            except Exception:
                pass
        return sorted(results, key=lambda x: -x['prediction'])

# Instance globale chargée au démarrage Flask
ml_service = MLService()
