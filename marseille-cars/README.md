# Analyse Data: Marche auto Marseille

Source: `marseille-cars.csv`

## Resume executif

Cette extraction contient `2300` annonces, `40` marques et `617` modeles.
Le marche est fortement concentre sur quelques marques generalistes (Peugeot, Renault, Citroen, Volkswagen), avec une dispersion de prix importante selon la marque, le modele, l'annee et le kilometrage.

## Methodologie

Le script:

1. Charge le CSV.
2. Convertit `annee`, `km`, `prix_eur` en numerique.
3. Filtre les lignes invalides (`prix_eur <= 0`, `km < 0`, valeurs manquantes).
4. Genere des visualisations Plotly en `.html` (interactif) et `.png` (image).

## Chiffres cles (dataset actuel)

- Volume: `2300` annonces
- Marques uniques: `40`
- Modeles uniques: `617`
- Prix moyen: `21 879 EUR`
- Prix median: `18 390 EUR`
- Quartiles prix (Q1 / Q3): `13 397.5 EUR` / `24 415 EUR`
- Kilometrage moyen: `70 283 km`
- Kilometrage median: `57 056 km`
- Quartiles km (Q1 / Q3): `27 941.5 km` / `92 000 km`
- Annee mediane: `2021`
- Correlation prix vs km: `-0.345` (relation negative moderee)

## Lecture business des resultats

### 1) Marques les plus representees

Top volume annonces:
- Peugeot: `455`
- Renault: `390`
- Citroen: `236`
- Volkswagen: `230`
- BMW / Audi / Toyota / Mercedes suivent ensuite.

Interpretation: l'offre locale est dominee par des marques generalistes francaises et allemandes.

### 2) Modeles les plus representes

Top modeles:
- 208 (`88`)
- Clio (`79`)
- C3 (`74`)
- Captur (`68`)
- 2008 (`65`)

Interpretation: predominance des citadines et SUV compacts, adaptes a un usage urbain/periurbain.

### 3) Marques les plus cheres (prix moyen, min 10 annonces)

Top prix moyen:
- Porsche: `~105k EUR`
- Land Rover: `~62k EUR`
- Volvo: `~51k EUR`
- Cupra: `~41k EUR`
- Mercedes: `~33k EUR`

Interpretation: un segment premium/luxe existe mais reste minoritaire en volume.

### 4) Variance de prix par modele

La variance est elevee sur les modeles a forte diffusion (ex: 208, Clio, Golf), ce qui suggere des ecarts forts d'annee, finition et kilometrage.

### 5) Kilometrage et prix

La relation negative prix-km est nette, mais non parfaite. A kilometrage equivalent, l'effet marque/modele/annee peut rester determinant.

## Limites et qualite des donnees

- Incoherence de casse sur certaines marques (`Bmw` vs `BMW`) qui peut biaiser certains classements.
- Presence de valeurs extremement elevees sur le prix, a interpretrer avec prudence.
- Le dataset evolue dans le temps, donc les conclusions peuvent changer a chaque nouvelle extraction.

## Visualisations disponibles

Le script genere:

- `01_marques_plus_representees`
- `02_modeles_plus_representes`
- `03_modeles_par_marque_treemap`
- `04_marques_plus_cheres`
- `05_variance_prix_par_modele`
- `06_distribution_km`
- `07_prix_vs_km`
- `08_distribution_prix`

Sorties dans `marseille-cars/outputs/`:
- `.html` interactif
- `.png` image statique

## Prerequis

```bash
python3 -m pip install -r requirements.txt
```

## Execution

Depuis la racine du projet:

```bash
python3 marseille-cars/analyze_marseille_cars.py \
  --input marseille-cars.csv \
  --output-dir marseille-cars/outputs
```

## Reutilisation pour d'autres datasets

Ce dossier sert de template. Pour un CSV immobilier:

1. Creer un dossier dedie (ex: `marseille-real-estate/`).
2. Copier l'approche script + README + `outputs/`.
3. Adapter les KPIs et les graphes au metier immobilier (prix/m2, surface, typologie, quartier, etc.).
