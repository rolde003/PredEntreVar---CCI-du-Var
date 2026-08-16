"""PredEntreVar – Point d'entrée
Lancement : python run.py  →  http://localhost:5000
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "="*55)
    print("  PredEntreVar – CCI du Var – IBOVI Rolde Chadrac")
    print("  🌐  http://localhost:5000")
    print("  🔮  http://localhost:5000/predict")
    print("  🛠   http://localhost:5000/admin  (admin / PredEntreVar2026!)")
    print("="*55 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
