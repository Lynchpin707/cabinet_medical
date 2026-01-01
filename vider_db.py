from backend.database import engine
from sqlalchemy import text
from backend import models

def reset_db():
    connection = engine.connect()
    trans = connection.begin()
    try:
        # Désactiver les contraintes pour vider sans erreur
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        # Supprimer toutes les tables
        models.Base.metadata.drop_all(bind=engine)
        print("Base de données vidée.")
        
        # Recréer les tables
        models.Base.metadata.create_all(bind=engine)
        print("Tables recréées proprement.")
        
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        trans.commit()
    except Exception as e:
        trans.rollback()
        print(f"Erreur : {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    reset_db()