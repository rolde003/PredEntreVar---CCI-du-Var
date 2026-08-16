"""PredEntreVar – Routes administration"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.models.models import Prediction, ModelMetric
from app.services.ml_service import ml_service
from app import db
import hashlib

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Mot de passe admin (hash SHA-256 de "PredEntreVar2026!")
ADMIN_HASH = hashlib.sha256(b'PredEntreVar2026!').hexdigest()

def check_auth():
    return session.get('admin_logged') == True

@admin_bp.route('/')
def admin_index():
    if not check_auth():
        return redirect(url_for('admin.login'))
    preds = Prediction.query.order_by(Prediction.created_at.desc()).limit(20).all()
    metrics = ModelMetric.query.order_by(ModelMetric.trained_at.desc()).limit(10).all()
    return render_template('admin.html',
                           predictions=preds, metrics=metrics,
                           ml=ml_service)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        pwd = request.form.get('password', '')
        if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_HASH:
            session['admin_logged'] = True
            return redirect(url_for('admin.admin_index'))
        error = 'Mot de passe incorrect'
    return render_template('login.html', error=error)

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect(url_for('main.index'))

@admin_bp.route('/api/metrics')
def api_metrics():
    if not check_auth():
        return jsonify({'error': 'Non autorisé'}), 401
    return jsonify({'r2': ml_service.r2, 'rmse': ml_service.rmse, 'mae': ml_service.mae})
