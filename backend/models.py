from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text, Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()
class Utilisateur(Base):
    __tablename__ = "utilisateur"
    id_utilisateur: int = Column(Integer, primary_key=True, index=True)
    nom_utilisateur: str = Column(String(50), index=True)
    email: str = Column(String(50), unique=True, index=True)
    numero_tl: str= Column(String(10), index=True)
    adresse: str = Column(String(50), index=True)
    genre: str= Column(String(10), index=True)
    date_de_naissance: date = Column(Date)
    mot_de_passe: str = Column(String(255))
    
    patient = relationship("Patient", back_populates="utilisateur", uselist=False)
    employer = relationship("Employer", back_populates="utilisateur", uselist=False)
    admin = relationship("Admin", back_populates="utilisateur", uselist=False)
    
class Employer(Base):
    __tablename__ = "employer"
    id_employer: int = Column(Integer, primary_key=True, index=True)
    id_utilisateur: int = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), index=True)
    role: str = Column(String(50), index=True)
    salaire: int = Column(Integer, index=True)
    statut: str= Column(String(50), index=True)
    
    utilisateur = relationship("Utilisateur", back_populates="employer")
    medecin = relationship("Medecin", back_populates="employer", uselist=False)
    demandes_conge = relationship("DemandeConge", back_populates="employer")
    
class Medecin(Base):
    __tablename__ = "medecin"
    id_medecin: int = Column(Integer, primary_key=True, index=True)
    id_employer: int = Column(Integer, ForeignKey("employer.id_employer"), index=True)
    specialite: str = Column(String(50), index=True)
    
    employer = relationship("Employer", back_populates="medecin")
    patients = relationship("Patient", back_populates="medecin")

class Admin(Base):
    __tablename__ = "admin"
    id_admin: int = Column(Integer, primary_key=True, index=True)
    id_utilisateur: int = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), index=True)
    
    utilisateur = relationship("Utilisateur", back_populates="admin")
    
class Patient(Base):
    __tablename__ = "patient"
    id_patient: int = Column(Integer, primary_key=True, index=True)
    id_utilisateur: int = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), index=True)
    medecin_traitant: int = Column(Integer, ForeignKey("medecin.id_medecin"), index=True)
    couverture_medicale: str = Column(String(50), index=True)
    
    utilisateur = relationship("Utilisateur", back_populates="patient")
    medecin = relationship("Medecin", back_populates="patients")
    dossier = relationship("DossierMedical", back_populates="patient", uselist=False)

class DemandeConge(Base):
    __tablename__ = "demande_conge"
    id_demande: int = Column(Integer, primary_key=True, index=True)
    id_employer: int = Column(Integer, ForeignKey("employer.id_employer"), index=True)
    type_conge: str = Column(String(50), index=True)
    date_debut_conge: date = Column(Date)
    date_fin_conge: date = Column(Date)
    
    employer = relationship("Employer", back_populates="demandes_conge")

class RDV(Base):
    __tablename__ = "RDV"
    id_RDV = Column(Integer, primary_key=True, index=True)
    date_rdv = Column(Date)
    heure_rdv = Column(Time) # Nouvelle colonne
    statut = Column(String(50))
    id_patient = Column(Integer, ForeignKey("patient.id_patient"))
    id_medecin = Column(Integer, ForeignKey("medecin.id_medecin"))
    
    # Relations
    patient = relationship("Patient")
    medecin = relationship("Medecin")
    visites = relationship("Visite", back_populates="rdv")

class Visite(Base):
    __tablename__ = "Visite"
    id_visite = Column(Integer, primary_key=True, index=True)
    id_RDV = Column(Integer, ForeignKey("RDV.id_RDV"))
    date_visite = Column(Date, default=datetime.datetime.now)
    type_visite = Column(String(50))
    poids = Column(Float)
    temperature = Column(Float)
    tension_max = Column(Float)
    tension_min = Column(Float)

    rdv = relationship("RDV", back_populates="visites")
    


class Facture(Base):
    __tablename__ = "facture"
    id_facture = Column(Integer, primary_key=True, index=True)
    id_visite = Column(Integer, ForeignKey("Visite.id_visite"))
    id_acte = Column(Integer, ForeignKey("acte_medical.id_acte"))
    date_facture = Column(Date)
    montant = Column(Float)
    avance = Column(Float, default=0.0)
    reste = Column(Float)
    etat = Column(String(20)) # Payé, En attente, Partiel

    visite = relationship("Visite")
    acte = relationship("ActeMedical", back_populates="factures")
    
class Catalogue(Base):
    __tablename__ = "catalogue"
    id_catalogue = Column(Integer, primary_key=True, index=True)
    nom_catalogue = Column(String(100), nullable=False)
    description = Column(String(255))

    tarifs = relationship("Tarifier", back_populates="catalogue")

class ActeMedical(Base):
    __tablename__ = "acte_medical"
    id_acte = Column(Integer, primary_key=True, index=True)
    nom_acte = Column(String(100), nullable=False)
    code_acte = Column(String(20), unique=True) # Ex: C, CS, APC


    tarifs = relationship("Tarifier", back_populates="acte")
    factures = relationship("Facture", back_populates="acte")

class Tarifier(Base):
    __tablename__ = "tarifier"
    id_tarifier = Column(Integer, primary_key=True, index=True)
    id_catalogue = Column(Integer, ForeignKey("catalogue.id_catalogue"))
    id_acte = Column(Integer, ForeignKey("acte_medical.id_acte"))
    prix = Column(Float, nullable=False)

    catalogue = relationship("Catalogue", back_populates="tarifs")
    acte = relationship("ActeMedical", back_populates="tarifs")


# --- Tables de Référence ---
class Allergie(Base):
    __tablename__ = "allergie"
    id_allergie = Column(Integer, primary_key=True, index=True)
    nom_allergie = Column(String(100), nullable=False)
    dossiers = relationship("ContientAllerg", back_populates="allergie")

class Maladie(Base):
    __tablename__ = "maladie"
    id_maladie = Column(Integer, primary_key=True, index=True)
    nom_maladie = Column(String(100), nullable=False)
    dossiers = relationship("ContientMaladies", back_populates="maladie")

# --- Dossier Principal ---
class DossierMedical(Base):
    __tablename__ = "dossier_medical"
    id_dossier = Column(Integer, primary_key=True, index=True)
    id_patient = Column(Integer, ForeignKey("patient.id_patient"), unique=True)
    date_creation = Column(Date)
    groupe_sanguin = Column(String(5))

    patient = relationship("Patient", back_populates="dossier")
    allergies = relationship("ContientAllerg", back_populates="dossier")
    maladies = relationship("ContientMaladies", back_populates="dossier")

# --- Tables de Liaison (VIOLETTES dans votre MLD) ---
class ContientAllerg(Base):
    __tablename__ = "contient_allerg"
    id_dossier = Column(Integer, ForeignKey("dossier_medical.id_dossier"), primary_key=True)
    id_allergie = Column(Integer, ForeignKey("allergie.id_allergie"), primary_key=True)
    severite = Column(String(50)) # Optionnel, pour enrichir le MLD

    dossier = relationship("DossierMedical", back_populates="allergies")
    allergie = relationship("Allergie", back_populates="dossiers")

class ContientMaladies(Base):
    __tablename__ = "contient_maladies"
    id_dossier = Column(Integer, ForeignKey("dossier_medical.id_dossier"), primary_key=True)
    id_maladie = Column(Integer, ForeignKey("maladie.id_maladie"), primary_key=True)

    dossier = relationship("DossierMedical", back_populates="maladies")
    maladie = relationship("Maladie", back_populates="dossiers")

# --- Référentiels ---
class Medicament(Base):
    __tablename__ = "medicament"
    id_medicament = Column(Integer, primary_key=True, index=True)
    nom_medicament = Column(String(100), nullable=False)
    forme = Column(String(50)) # Ex: Comprimé, Sirop

class Analyse(Base):
    __tablename__ = "analyse"
    id_analyse = Column(Integer, primary_key=True, index=True)
    nom_analyse = Column(String(100), nullable=False)

# --- Ordonnance ---
class Ordonnance(Base):
    __tablename__ = "ordonnance"
    id_ordonnance = Column(Integer, primary_key=True, index=True)
    id_visite = Column(Integer, ForeignKey("Visite.id_visite"))
    instructions = Column(Text) # Conseils généraux

    visite = relationship("Visite")
    
    medicaments = relationship("PrescrireMed", back_populates="ordonnance")
    analyses = relationship("PrescrireAnalyse", back_populates="ordonnance")

# --- Tables de Liaison (Détails des prescriptions) ---
class PrescrireMed(Base):
    __tablename__ = "prescrire_med"
    id_ordonnance = Column(Integer, ForeignKey("ordonnance.id_ordonnance"), primary_key=True)
    id_medicament = Column(Integer, ForeignKey("medicament.id_medicament"), primary_key=True)
    posologie = Column(String(255)) 
    duree = Column(String(50))      

    ordonnance = relationship("Ordonnance", back_populates="medicaments")
    medicament = relationship("Medicament")

class PrescrireAnalyse(Base):
    __tablename__ = "prescrire_analyse"
    id_ordonnance = Column(Integer, ForeignKey("ordonnance.id_ordonnance"), primary_key=True)
    id_analyse = Column(Integer, ForeignKey("analyse.id_analyse"), primary_key=True)
    description = Column(Text)

    ordonnance = relationship("Ordonnance", back_populates="analyses")
    analyse = relationship("Analyse")
    
class Symptome(Base):
    __tablename__ = "symptome"
    id_symptome = Column(Integer, primary_key=True, index=True)
    nom_symptome = Column(String(100), nullable=False)
    code_symptome = Column(String(20)) # Ex: FEVP (Fièvre), TOUX

    visites = relationship("Detecter", back_populates="symptome")

class Detecter(Base):
    __tablename__ = "detecter"
    id_visite = Column(Integer, ForeignKey("Visite.id_visite"), primary_key=True)
    id_symptome = Column(Integer, ForeignKey("symptome.id_symptome"), primary_key=True)
    intensite = Column(String(50)) # Faible, Modérée, Forte

    visite = relationship("Visite") 
    symptome = relationship("Symptome", back_populates="visites")
    
class Signaler(Base):
    __tablename__ = "signaler"
    id_visite = Column(Integer, ForeignKey("Visite.id_visite", ondelete="CASCADE"), primary_key=True)
    id_symptome = Column(Integer, ForeignKey("symptome.id_symptome", ondelete="CASCADE"), primary_key=True)