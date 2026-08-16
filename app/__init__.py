"""PredEntreVar – Factory Flask – IBOVI Rolde Chadrac – CCI du Var"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'predentrevar_secret_2026_cci_var'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(basedir, '..', 'predentrevar.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Charger le modèle ML
    from .services.ml_service import ml_service
    ml_service.load_model(
        os.path.join(basedir, '..', 'models', 'ridge_model.joblib')
    )
    
    # Enregistrer les blueprints
    from .routes.main import main_bp
    from .routes.predict import predict_bp
    from .routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(admin_bp)
    
    # Créer les tables au premier démarrage
    with app.app_context():
        db.create_all()
        _init_data(app)
    
    return app

def _init_data(app):
    """Importer les données CSV dans la BDD si vide."""
    from .models.models import Creation
    if Creation.query.count() == 0:
        import pandas as pd, os
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'creations_var.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                db.session.add(Creation(
                    annee=int(row['annee']),
                    secteur=row['secteur'],
                    nb_creations=float(row['nb_creations']),
                    taux_chomage=float(row['taux_chomage']),
                    nuitees_milliers=float(row['nuitees_milliers'])
                ))
            db.session.commit()
            print(f"✓ {len(df)} lignes importées dans la BDD")
