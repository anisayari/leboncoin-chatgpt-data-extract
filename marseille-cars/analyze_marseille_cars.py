#!/usr/bin/env python3
"""Analyse des annonces voitures de Marseille avec visualisations Plotly."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import plotly.express as px


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    default_input = base_dir.parent / "marseille-cars.csv"
    default_output = base_dir / "outputs"

    parser = argparse.ArgumentParser(
        description="Genere des visualisations Plotly pour marseille-cars.csv."
    )
    parser.add_argument("--input", type=Path, default=default_input, help="CSV d'entree")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=default_output,
        help="Dossier de sortie des visualisations",
    )
    parser.add_argument(
        "--top-brands", type=int, default=12, help="Nombre de marques a afficher"
    )
    parser.add_argument(
        "--top-models", type=int, default=20, help="Nombre de modeles a afficher"
    )
    parser.add_argument(
        "--min-brand-listings",
        type=int,
        default=10,
        help="Seuil min d'annonces pour calculer les marques les plus cheres",
    )
    return parser.parse_args()


def save_figure(fig, output_dir: Path, name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{name}.html"
    png_path = output_dir / f"{name}.png"

    fig.write_html(str(html_path), include_plotlyjs="cdn")
    try:
        fig.write_image(str(png_path), width=1400, height=800, scale=2)
        print(f"[OK] HTML + PNG: {name}")
    except Exception:
        print(f"[OK] HTML: {name} (PNG non exporte, installer kaleido)")


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV introuvable: {csv_path}")

    df = pd.read_csv(csv_path)
    for col in ["annee", "km", "prix_eur"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["marque"] = df["marque"].astype(str).str.strip()
    df["modele"] = df["modele"].astype(str).str.strip()
    df = df.dropna(subset=["marque", "modele", "prix_eur", "km", "annee"])
    df = df[(df["prix_eur"] > 0) & (df["km"] >= 0)]
    return df


def main() -> None:
    args = parse_args()
    df = load_data(args.input)
    output_dir = args.output_dir

    print(f"CSV charge: {args.input}")
    print(f"Lignes: {len(df)} | Marques: {df['marque'].nunique()} | Modeles: {df['modele'].nunique()}")

    top_brands = df["marque"].value_counts().head(args.top_brands).reset_index()
    top_brands.columns = ["marque", "annonces"]
    fig = px.bar(
        top_brands,
        x="marque",
        y="annonces",
        title=f"Top {args.top_brands} marques les plus representees",
        text_auto=True,
        color="annonces",
        color_continuous_scale="Blues",
    )
    fig.update_layout(template="plotly_white", xaxis_title="Marque", yaxis_title="Nb annonces")
    save_figure(fig, output_dir, "01_marques_plus_representees")

    top_models = df["modele"].value_counts().head(args.top_models).reset_index()
    top_models.columns = ["modele", "annonces"]
    fig = px.bar(
        top_models,
        x="modele",
        y="annonces",
        title=f"Top {args.top_models} modeles les plus representes",
        text_auto=True,
        color="annonces",
        color_continuous_scale="Teal",
    )
    fig.update_layout(template="plotly_white", xaxis_title="Modele", yaxis_title="Nb annonces")
    save_figure(fig, output_dir, "02_modeles_plus_representes")

    top_brand_names = top_brands["marque"].head(min(8, len(top_brands))).tolist()
    brand_model_counts = (
        df[df["marque"].isin(top_brand_names)]
        .groupby(["marque", "modele"], as_index=False)
        .size()
        .rename(columns={"size": "annonces"})
        .sort_values(["marque", "annonces"], ascending=[True, False])
        .groupby("marque", as_index=False)
        .head(6)
    )
    fig = px.treemap(
        brand_model_counts,
        path=["marque", "modele"],
        values="annonces",
        title="Modeles les plus publies par marque (top marques)",
        color="annonces",
        color_continuous_scale="Mint",
    )
    fig.update_layout(template="plotly_white")
    save_figure(fig, output_dir, "03_modeles_par_marque_treemap")

    expensive_brands = (
        df.groupby("marque", as_index=False)
        .agg(prix_moyen=("prix_eur", "mean"), annonces=("id", "count"))
        .query("annonces >= @args.min_brand_listings")
        .sort_values("prix_moyen", ascending=False)
        .head(args.top_brands)
    )
    fig = px.bar(
        expensive_brands,
        x="marque",
        y="prix_moyen",
        title=(
            "Marques les plus cheres (prix moyen, "
            f"minimum {args.min_brand_listings} annonces)"
        ),
        text_auto=".0f",
        color="prix_moyen",
        color_continuous_scale="OrRd",
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Marque",
        yaxis_title="Prix moyen (EUR)",
    )
    save_figure(fig, output_dir, "04_marques_plus_cheres")

    top_models_list = df["modele"].value_counts().head(args.top_models).index.tolist()
    price_by_model = df[df["modele"].isin(top_models_list)].copy()
    fig = px.box(
        price_by_model,
        x="modele",
        y="prix_eur",
        color="modele",
        title=f"Variance des prix par modele (top {args.top_models})",
        points=False,
    )
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="Modele",
        yaxis_title="Prix (EUR)",
    )
    save_figure(fig, output_dir, "05_variance_prix_par_modele")

    fig = px.histogram(
        df,
        x="km",
        nbins=40,
        title="Distribution du kilometrage",
        color_discrete_sequence=["#2a9d8f"],
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Kilometrage",
        yaxis_title="Nb annonces",
    )
    save_figure(fig, output_dir, "06_distribution_km")

    scatter_df = df.copy()
    top_scatter_brands = scatter_df["marque"].value_counts().head(8).index
    scatter_df["marque_cluster"] = scatter_df["marque"].where(
        scatter_df["marque"].isin(top_scatter_brands), "Autres"
    )
    fig = px.scatter(
        scatter_df,
        x="km",
        y="prix_eur",
        color="marque_cluster",
        title="Relation prix vs kilometrage",
        opacity=0.65,
        hover_data=["marque", "modele", "annee"],
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Kilometrage",
        yaxis_title="Prix (EUR)",
    )
    save_figure(fig, output_dir, "07_prix_vs_km")

    fig = px.histogram(
        df,
        x="prix_eur",
        nbins=50,
        title="Distribution des prix",
        color_discrete_sequence=["#e76f51"],
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Prix (EUR)",
        yaxis_title="Nb annonces",
    )
    save_figure(fig, output_dir, "08_distribution_prix")

    print(f"Visualisations generees dans: {output_dir}")


if __name__ == "__main__":
    main()

