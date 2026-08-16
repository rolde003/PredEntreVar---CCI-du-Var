"""PredEntreVar – Modèles SQLAlchemy"""
from app import db
from datetime import datetime

class Creation(db.Model):
    """Données INSEE SIDE – créations d'entreprises par secteur et année."""
    __tablename__ = 'creations'
    id              = db.Column(db.Integer, primary_key=True)
    annee           = db.Column(db.Integer, nullable=False)
    secteur         = db.Column(db.String(120), nullable=False)
    nb_creations    = db.Column(db.Float, nullable=False)
    taux_chomage    = db.Column(db.Float)
    nuitees_milliers = db.Column(db.Float)
    __table_args__  = (db.UniqueConstraint('annee', 'secteur'),)

    def to_dict(self):
        return {'annee': self.annee, 'secteur': self.secteur,
                'nb_creations': self.nb_creations,
                'taux_chomage': self.taux_chomage,
                'nuitees_milliers': self.nuitees_milliers}

class Prediction(db.Model):
    """Log des prédictions réalisées via l'interface."""
    __tablename__ = 'predictions'
    id                 = db.Column(db.Integer, primary_key=True)
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)
    secteur            = db.Column(db.String(120), nullable=False)
    annee_cible        = db.Column(db.Integer, nullable=False)
    taux_chomage_hyp   = db.Column(db.Float, nullable=False)
    valeur_predite     = db.Column(db.Float, nullable=False)
    intervalle_bas     = db.Column(db.Float)
    intervalle_haut    = db.Column(db.Float)
    modele             = db.Column(db.String(50), default='Ridge')

class ModelMetric(db.Model):
    """Historique des entraînements du modèle."""
    __tablename__ = 'model_metrics'
    id          = db.Column(db.Integer, primary_key=True)
    trained_at  = db.Column(db.DateTime, default=datetime.utcnow)
    algorithme  = db.Column(db.String(80))
    rmse        = db.Column(db.Float)
    mae         = db.Column(db.Float)
    r2          = db.Column(db.Float)
    n_train     = db.Column(db.Integer)
