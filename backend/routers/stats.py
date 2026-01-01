from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from backend import database

router = APIRouter(
    prefix="/stats", 
    tags=["Tableau de Bord"]
)

@router.get("/alerte-epidemie")
def detecter_epidemie(db: Session = Depends(database.get_db)):
    sept_jours_avant = (datetime.now() - timedelta(days=7)).date()
    SEUIL_ALERTE = 5

    results = db.query(
        models.Symptome.nom_symptome,
        func.count(models.Visite.id_visite).label("total_cas")
    ).join(models.Signaler, models.Symptome.id_symptome == models.Signaler.id_symptome)\
     .join(models.Visite, models.Signaler.id_visite == models.Visite.id_visite)\
     .filter(models.Visite.date_visite >= sept_jours_avant)\
     .group_by(models.Symptome.nom_symptome)\
     .having(func.count(models.Visite.id_visite) >= SEUIL_ALERTE)\
     .all()

    return [{"nom_symptome": r.nom_symptome, "total_cas": r.total_cas} for r in results]

@router.get("/quotidien")
def get_stats_quotidien(date: str, db: Session = Depends(database.get_db)):
    # 1. Liste détaillée (inclut le compte via len())
    rdvs = db.query(models.RDV).filter(models.RDV.date_rdv == date).all()
    
    rdv_liste = [
        {
            "heure": r.heure_rdv.strftime("%H:%M") if r.heure_rdv else "--:--",
            "patient_nom": r.patient.utilisateur.nom_utilisateur if r.patient else "Inconnu",
            "statut": r.statut
        } for r in rdvs
    ]
    
    # 2. Chiffre d'Affaires
    ca = db.query(func.sum(models.Facture.montant)).filter(models.Facture.date_facture == date).scalar() or 0
    
    return {
        "rdv_count": len(rdvs),
        "ca_jour": ca,
        "rdv_liste": rdv_liste
    }