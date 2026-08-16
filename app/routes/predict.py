"""PredEntreVar – Route prédiction /api/predict"""
from flask import Blueprint, request, jsonify, render_template
from app.services.ml_service import ml_service, SECTEURS_VALIDES
from app.models.models import Prediction
from app import db

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict')
def predict_page():
    return render_template('predict.html', secteurs=SECTEURS_VALIDES)

@predict_bp.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requis'}), 400

    secteur = data.get('secteur', '')
    if secteur not in SECTEURS_VALIDES:
        return jsonify({'error': f'Secteur invalide. Secteurs valides : {SECTEURS_VALIDES}'}), 400

    try:
        taux_cho = float(data.get('taux_chomage', 7.0))
        if not (0 <= taux_cho <= 25):
            return jsonify({'error': 'taux_chomage doit être entre 0 et 25'}), 400
        annee = int(data.get('annee', 2025))
        if not (2025 <= annee <= 2030):
            return jsonify({'error': 'annee doit être entre 2025 et 2030'}), 400
        nuitees = float(data.get('nuitees', 15000.0))
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

    result = ml_service.predict(secteur, annee, taux_cho, nuitees)

    # Logger la prédiction en BDD
    try:
        log = Prediction(secteur=secteur, annee_cible=annee,
                         taux_chomage_hyp=taux_cho,
                         valeur_predite=result['prediction'],
                         intervalle_bas=result['ci_low'],
                         intervalle_haut=result['ci_high'])
        db.session.add(log)
        db.session.commit()
    except Exception:
        pass  # Le logging n'est pas bloquant

    return jsonify(result), 200

@predict_bp.route('/api/predict/all')
def api_predict_all():
    """Prédictions pour tous les secteurs (dashboard comparatif)."""
    try:
        annee    = int(request.args.get('annee', 2025))
        chomage  = float(request.args.get('chomage', 6.5))
        nuitees  = float(request.args.get('nuitees', 15000))
        results  = ml_service.get_predictions_for_all_sectors(annee, chomage, nuitees)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
