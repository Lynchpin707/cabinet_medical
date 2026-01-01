from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class UtilisateurCreate(BaseModel):
    nom_utilisateur: str 
    email: str 
    numero_tl: int 
    adresse: str 
    genre: str
    date_de_naissance: date
    mot_de_passe: str 

class UtilisateurUpdate(BaseModel):
    name: str
    email: str

class PatientCreate(UtilisateurCreate):
    medecin_traitant: Optional[int]
    couverture_medicale: Optional[str]
    
class EmployerCreate(UtilisateurCreate):
     
    role: str
    salaire : int
    statut: Optional[str]
    
class MedecinCreate(EmployerCreate):
    specialite: Optional[str]
    
class Utilisateur(UtilisateurCreate):
    id_utilisateur: int

    class Config:
        orm_mode = True # Pour Python 3.9 / Pydantic v1
        # ou from_attributes = True si vous utilisez Pydantic v2

class PatientOut(BaseModel):
    id_patient: int
    id_utilisateur: int
    medecin_traitant: Optional[int]
    couverture_medicale: Optional[str]

    class Config:
        orm_mode = True

class EmployerOut(BaseModel):
    id_employer: int
    id_utilisateur: int
    role: str
    salaire: int
    statut: Optional[str]

    class Config:
        orm_mode = True

class MedecinOut(BaseModel):
    id_medecin: int
    id_employer: int
    specialite: Optional[str]

    class Config:
        orm_mode = True     
        
class VisiteBase(BaseModel):
    type_visite: str
    poids: float
    temperature: float
    tension_max: float
    tension_min: float


class VisiteCreate(VisiteBase):
    id_RDV: int

class Visite(VisiteBase):
    id_visite: int
    date_visite: date

    class Config:
        from_attributes = True   
        
# --- RDV ---
class RDVBase(BaseModel):
    id_patient: int
    id_medecin: int
    date_rdv: date
    heure_rdv: time
    statut: str = "Prévu" # Valeur par défaut

class RDVCreate(RDVBase):
    pass

class RDV(RDVBase):
    id_RDV: int

    class Config:
        from_attributes = True 
        
# Ce que le Frontend envoie (Saisie minimale)
class FactureCreate(BaseModel):
    id_visite: int
    id_acte: int
    avance: float = 0.0

# Structure de base pour l'affichage (Lecture)
class FactureBase(BaseModel):
    id_visite: int
    id_acte: int
    date_facture: date
    montant: float
    avance: float
    reste: float 
    etat: str

# Ce que l'API renvoie 
class Facture(FactureBase):
    id_facture: int

    class Config:
        from_attributes = True

class ActeMedical(BaseModel):
    id_acte: int
    nom_acte: str
    type_acte: str

    class Config:
        from_attributes = True
        
# --- Acte Médical ---
class ActeMedicalBase(BaseModel):
    nom_acte: str
    code_acte: str

class ActeMedicalCreate(ActeMedicalBase):
    pass

class ActeMedical(ActeMedicalBase):
    id_acte: int
    class Config:
        from_attributes = True

# --- Catalogue ---
class CatalogueBase(BaseModel):
    nom_catalogue: str
    description: Optional[str] = None

class CatalogueCreate(CatalogueBase):
    pass

class Catalogue(CatalogueBase):
    id_catalogue: int
    class Config:
        from_attributes = True

# --- Tarification ---
class TarifierCreate(BaseModel):
    id_catalogue: int
    id_acte: int
    prix: float

class Tarifier(TarifierCreate):
    id_tarifier: int
    acte: Optional[ActeMedical]
    class Config:
        from_attributes = True
    
# --- Dossier Médical ---
class DossierMedicalBase(BaseModel):
    id_patient: int
    groupe_sanguin: Optional[str]
    date_creation: date

class DossierMedicalCreate(DossierMedicalBase):
    pass

class DossierMedical(DossierMedicalBase):
    id_dossier: int
    class Config:
        from_attributes = True

    # --- Liaisons ---
class AjoutAllergie(BaseModel):
    id_allergie: int
    severite: Optional[str] = "Inconnue"

class AjoutMaladie(BaseModel):
    id_maladie: int
    
# --- Médicaments & Analyses ---
class MedicamentCreate(BaseModel):
    nom_medicament: str
    forme: Optional[str]

class Medicament(MedicamentCreate):
    id_medicament: int
    class Config:
        from_attributes = True

# --- Ordonnance ---
class OrdonnanceCreate(BaseModel):
    id_visite: int
    instructions: Optional[str]

class Ordonnance(OrdonnanceCreate):
    id_ordonnance: int
    class Config:
        from_attributes = True

# --- Détails Prescription ---
class PrescriptionMedCreate(BaseModel):
    id_medicament: int
    posologie: str
    duree: str

class PrescriptionAnalyseCreate(BaseModel):
    id_analyse: int
    description: Optional[str]
    
# --- Employer ---
class EmployerBase(BaseModel):
    id_utilisateur: int
    date_embauche: date
    salaire: float

class EmployerCreate(EmployerBase):
    pass

class Employer(EmployerBase):
    id_employer: int
    class Config:
        from_attributes = True

# --- Medecin ---
class MedecinCreate(BaseModel):
    id_employer: int
    specialite: str
    grade: str

class Medecin(MedecinCreate):
    id_medecin: int
    class Config:
        from_attributes = True

# --- Demande de Congé ---
class DemandeCongeCreate(BaseModel):
    id_employer: int
    date_debut: date
    date_fin: date
    type_conge: str

class DemandeConge(DemandeCongeCreate):
    id_demande: int
    statut: str
    class Config:
        from_attributes = True
        
# --- Symptômes ---
class SymptomeBase(BaseModel):
    nom_symptome: str
    code_symptome: Optional[str]

class SymptomeCreate(SymptomeBase):
    pass

class Symptome(SymptomeBase):
    id_symptome: int
    class Config:
        from_attributes = True

# --- Détection (Liaison) ---
class DetectionCreate(BaseModel):
    id_symptome: int
    intensite: Optional[str] = "Modérée"