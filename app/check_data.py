from pydantic import BaseModel
from enum import Enum


class GeneStatus(str, Enum):
    NOT_MUTATED = "NOT_MUTATED"
    MUTATED = "MUTATED"


class GenderStatus(str, Enum):
    Male = "Male"
    Female = "Female"


class Patient(BaseModel):
    IDH1: GeneStatus
    TP53: GeneStatus
    ATRX: GeneStatus
    PTEN: GeneStatus
    EGFR: GeneStatus
    CIC: GeneStatus
    MUC16: GeneStatus
    PIK3CA: GeneStatus
    NF1: GeneStatus
    PIK3R1: GeneStatus
    FUBP1: GeneStatus
    RB1: GeneStatus
    NOTCH1: GeneStatus
    BCOR: GeneStatus
    CSMD3: GeneStatus
    SMARCA4: GeneStatus
    GRIN2A: GeneStatus
    IDH2: GeneStatus
    FAT4: GeneStatus
    PDGFRA: GeneStatus
    Age_at_diagnosis: str
    Gender: GenderStatus
