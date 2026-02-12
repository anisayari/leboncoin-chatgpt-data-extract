# Leboncoin ChatGPT Data Extract

Ce repository contient des jeux de donnees extraits depuis l'app ChatGPT de Leboncoin, ainsi que des analyses reproductibles (Python + Plotly).

## Contexte

L'objectif est de documenter techniquement la possibilite d'extraction de donnees a grande echelle.

- Tweet de signalement public: [DFintelligence sur X](https://x.com/DFintelligence/status/2021459351248982444?s=20)
- Article mentionnant la position de Leboncoin: [Numerama](https://www.numerama.com/cyberguerre/2177379-leboncoin-vient-il-de-ruiner-des-annees-defforts-avec-son-appli-chatgpt-on-leur-a-pose-la-question.html)

Ce repo est publie pour apporter des elements concrets et verifiables (datasets + scripts + visualisations), dans l'espoir d'encourager une meilleure prise en compte des retours techniques. L'idee est simple: eviter la posture de l'autruche et traiter les signalements techniques de maniere directe.

## Organisation du repo

Regle: **1 dossier = 1 analyse**.

- `marseille-cars/`: analyse des annonces auto sur Marseille

Chaque dossier d'analyse contient:

1. Un script Python d'analyse.
2. Un `README.md` metier (methodo + lecture des resultats).
3. Un dossier `outputs/` avec les visualisations (`.html` et `.png`).

## Ajouter une nouvelle analyse (ex: immobilier)

1. Creer un dossier dedie, par exemple `marseille-real-estate/`.
2. Ajouter un script `analyze_*.py` qui lit un CSV et produit des visualisations.
3. Ajouter un `README.md` en francais avec la lecture data.
4. Ecrire les sorties dans `outputs/`.

## Lancer une analyse

```bash
python3 -m pip install -r requirements.txt
python3 marseille-cars/analyze_marseille_cars.py \
  --input marseille-cars.csv \
  --output-dir marseille-cars/outputs
```
