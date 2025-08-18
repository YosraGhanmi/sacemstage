import sys
import json
from sqlalchemy.orm import sessionmaker
from setup_database import engine, TransformerCalculation

def get_calculation_history(limit=10):
    """Récupérer l'historique des calculs"""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        calculations = session.query(TransformerCalculation)\
            .order_by(TransformerCalculation.created_at.desc())\
            .limit(limit)\
            .all()
        
        history = []
        for calc in calculations:
            history.append({
                'id': calc.id,
                'nom_client': calc.nom_client,
                'type_transformateur': calc.type_transformateur,
                'puissance_kva': calc.puissance_kva,
                'tension_primaire': calc.tension_primaire,
                'tension_secondaire': calc.tension_secondaire,
                'created_at': calc.created_at.isoformat() if calc.created_at else None,
                'resultats': calc.calculation_results
            })
        
        return history
        
    except Exception as e:
        print(f"Erreur lors de la récupération: {e}", file=sys.stderr)
        return []
    finally:
        session.close()

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    history = get_calculation_history(limit)
    print(json.dumps(history))
