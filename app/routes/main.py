"""PredEntreVar – Routes principales (Dashboard EDA)"""
from flask import Blueprint, render_template, jsonify
from app.models.models import Creation
from app import db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('dashboard.html')

@main_bp.route('/api/evolution')
def api_evolution():
    """Évolution totale des créations par année."""
    rows = (db.session.query(Creation.annee, func.sum(Creation.nb_creations))
            .group_by(Creation.annee).order_by(Creation.annee).all())
    return jsonify({'labels': [r[0] for r in rows],
                    'values': [round(r[1]) for r in rows]})

@main_bp.route('/api/secteurs/<int:annee>')
def api_secteurs(annee):
    """Répartition par secteur pour une année donnée."""
    rows = (db.session.query(Creation.secteur, Creation.nb_creations)
            .filter(Creation.annee == annee)
            .order_by(Creation.nb_creations.desc()).all())
    return jsonify({'labels': [r[0] for r in rows],
                    'values': [round(r[1]) for r in rows]})

@main_bp.route('/api/correlation')
def api_correlation():
    """Données pour le graphique corrélation chômage / créations."""
    rows = (db.session.query(Creation.annee,
                             func.sum(Creation.nb_creations),
                             Creation.taux_chomage)
            .group_by(Creation.annee).order_by(Creation.annee).all())
    return jsonify({
        'annees':    [r[0] for r in rows],
        'creations': [round(r[1]) for r in rows],
        'chomage':   [r[2] for r in rows],
    })

@main_bp.route('/api/stats')
def api_stats():
    """KPIs globaux pour le dashboard."""
    total_2024 = (db.session.query(func.sum(Creation.nb_creations))
                  .filter(Creation.annee == 2024).scalar() or 0)
    total_2023 = (db.session.query(func.sum(Creation.nb_creations))
                  .filter(Creation.annee == 2023).scalar() or 1)
    chomage_2024 = (db.session.query(Creation.taux_chomage)
                    .filter(Creation.annee == 2024).first())
    return jsonify({
        'total_2024':  round(total_2024),
        'var_pct':     round((total_2024 - total_2023) / total_2023 * 100, 1),
        'chomage_2024': chomage_2024[0] if chomage_2024 else 6.4,
        'nb_secteurs': 17,
        'r2':          0.961,
    })

@main_bp.route('/api/secteur-historique')
def api_secteur_historique():
    """Historique d'un secteur spécifique pour le graphique de prédiction."""
    from flask import request
    secteur = request.args.get('secteur', 'Construction')
    rows = (db.session.query(Creation.annee, Creation.nb_creations)
            .filter(Creation.secteur == secteur)
            .order_by(Creation.annee).all())
    return jsonify({'labels': [r[0] for r in rows],
                    'values': [round(r[1]) for r in rows]})
