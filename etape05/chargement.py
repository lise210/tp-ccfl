import os
import csv
from pathlib import Path

from sqlalchemy.engine import Connection
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


CHEMIN_SITES = Path("data/sites.csv")
CHEMIN_MATERIEL = Path("sorties/materiel_propre.csv")
CHEMIN_ASSOCIATIONS = Path("sorties/associations_propre.csv")
CHEMIN_RESERVATIONS = Path("sorties/reservations_propre.csv")


def lire_csv(chemin: Path) -> list[dict[str, str]]:
    with chemin.open(encoding="utf-8-sig", newline="") as fichier:
        return list(csv.DictReader(fichier))

