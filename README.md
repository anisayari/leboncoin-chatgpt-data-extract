# Leboncoin ChatGPT Data Extract

> WARNING
> Ce repository existe uniquement parce que Leboncoin dement qu'il est possible d'utiliser son app ChatGPT pour extraire des donnees structurees de son site.
> Ce contenu est publie a but strictement informationnel.
> Parce que mentir, ce n'est pas acceptable.

Ce repository contient des jeux de donnees extraits depuis l'app ChatGPT de Leboncoin, ainsi que des analyses reproductibles (Python + Plotly).

## Contexte

J'ai voulu avertir que ce type d'application pouvait porter des risques pour la securite des donnees.
Leboncoin dement et qualifie ces affirmations d'infondees.
Au lieu de traiter le signalement sur le fond, ils ont prefere balayer ces alertes.
Voici les preuves concretes que c'est possible, avec des donnees extraites, des scripts et des visualisations reproductibles.

D'autant plus: entre mes premiers essais et mes essais apres le tweet, ils ont bien renforce la securite de leur app.
Donc dementir publiquement tout en prenant le point en interne, c'est ethically questionable.

- Tweet de signalement public: [DFintelligence sur X](https://x.com/DFintelligence/status/2021459351248982444?s=20)
- Article mentionnant le dementi: [Numerama](https://www.numerama.com/cyberguerre/2177379-leboncoin-vient-il-de-ruiner-des-annees-defforts-avec-son-appli-chatgpt-on-leur-a-pose-la-question.html)

### Captures

Capture de mon tweet:

![Capture tweet DFintelligence](tweet-dfintelligence.png)

Capture du dementi:

![Capture dementi Leboncoin](leboncoin-dement.png)

Captures des mesures / garde-fous observes apres:

![Capture mesure 1](mesure1.png)

![Capture mesure 2](mesure2.png)

PS: la prochaine fois, moins de deni et plus de remise en question.

## Organisation du repo

Regle: **1 dossier = 1 analyse**.

- `marseille-cars/`: analyse des annonces auto sur Marseille
- `appartement-paris/`: analyse des annonces immobilieres sur Paris

Chaque dossier d'analyse contient:

1. Un script Python d'analyse.
2. Le(s) CSV dans le dossier de l'analyse.
3. Un `README.md` metier (methodo + lecture des resultats).
4. Un dossier `outputs/` avec les visualisations (`.html` et `.png`).

## Ajouter une nouvelle analyse (ex: immobilier)

1. Creer un dossier dedie, par exemple `marseille-real-estate/`.
2. Ajouter un script `analyze_*.py` qui lit un CSV et produit des visualisations.
3. Ajouter un `README.md` en francais avec la lecture data.
4. Ecrire les sorties dans `outputs/`.

## Exemples de visualisations par analyse

### Marseille Cars

Ce qu'on peut apprendre:
- quelles marques dominent le marche local,
- comment le prix evolue en fonction du kilometrage.

![Marseille cars - marques les plus representees](marseille-cars/outputs/01_marques_plus_representees.png)

![Marseille cars - prix vs km](marseille-cars/outputs/07_prix_vs_km.png)

### Appartement Paris

Ce qu'on peut apprendre:
- quels arrondissements concentrent l'offre,
- ou le prix au m2 est le plus eleve.

![Appartement Paris - annonces par arrondissement](appartement-paris/outputs/01_annonces_par_arrondissement.png)

![Appartement Paris - prix m2 par arrondissement](appartement-paris/outputs/02_prix_m2_par_arrondissement.png)

## Lancer les analyses

```bash
python3 -m pip install -r requirements.txt

python3 marseille-cars/analyze_marseille_cars.py \
  --input marseille-cars/marseille-cars.csv \
  --output-dir marseille-cars/outputs

python3 appartement-paris/analyze_paris_apartments.py \
  --output-dir appartement-paris/outputs
```
