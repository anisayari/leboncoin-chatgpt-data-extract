#!/usr/bin/env python3
"""Analyse des annonces appartements Paris avec visualisations Plotly."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import plotly.express as px


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Analyse tous les CSV du dossier appartement-paris et genere des graphes."
    )
    parser.add_argument(
        "--input-glob",
        default="*.csv",
        help="Pattern de CSV a charger depuis appartement-paris (ex: *.csv)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base_dir / "outputs",
        help="Dossier de sortie des visualisations",
    )
    parser.add_argument(
        "--min-arr-listings",
        type=int,
        default=2,
        help="Seuil mini d'annonces pour les comparaisons par arrondissement",
    )
    parser.add_argument(
        "--max-price",
        type=float,
        default=225000.0,
        help="Prix max conserve dans l'analyse (EUR).",
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
        print(f"[OK] HTML: {name} (PNG non exporte, installer kaleido==0.2.1)")


def to_numeric(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def load_data(base_dir: Path, input_glob: str) -> tuple[pd.DataFrame, list[Path]]:
    csv_files = sorted(base_dir.glob(input_glob))
    csv_files = [p for p in csv_files if p.is_file()]
    if not csv_files:
        raise FileNotFoundError(f"Aucun CSV trouve avec le pattern {input_glob} dans {base_dir}")

    frames = []
    for csv_path in csv_files:
        df = pd.read_csv(csv_path)
        df["source_csv"] = csv_path.name
        frames.append(df)

    df_all = pd.concat(frames, ignore_index=True)

    required_cols = [
        "id",
        "prix",
        "surface_m2",
        "nb_pieces",
        "nb_chambres",
        "dpe",
        "arrondissement",
        "type_vendeur",
        "date_publication",
        "lien",
    ]
    missing = [c for c in required_cols if c not in df_all.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes: {missing}")

    for col in ["prix", "surface_m2", "nb_pieces", "nb_chambres"]:
        df_all[col] = to_numeric(df_all[col])

    df_all["date_publication"] = pd.to_datetime(df_all["date_publication"], errors="coerce")
    df_all["arrondissement"] = df_all["arrondissement"].astype(str).str.strip()
    df_all["dpe"] = df_all["dpe"].astype(str).str.strip().str.upper()
    df_all["dpe"] = df_all["dpe"].replace({"": "NA", "NAN": "NA"})
    df_all["type_vendeur"] = df_all["type_vendeur"].astype(str).str.strip().str.lower()
    df_all["type_vendeur"] = df_all["type_vendeur"].replace({"": "unknown", "nan": "unknown"})

    # Garder la derniere version de chaque annonce id.
    df_all = df_all.sort_values("date_publication").drop_duplicates(subset=["id"], keep="last")

    df = df_all[(df_all["prix"] > 0) & (df_all["surface_m2"] > 0)].copy()
    df["prix_m2"] = df["prix"] / df["surface_m2"]

    return df, csv_files


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    output_dir = args.output_dir
    df, csv_files = load_data(base_dir, args.input_glob)
    df = df[df["prix"] <= args.max_price].copy()

    print("CSV charges:")
    for csv_path in csv_files:
        print(f"- {csv_path}")
    print(
        "Lignes uniques (id dedupe): "
        f"{len(df)} | Arrondissements: {df['arrondissement'].nunique()} | "
        f"Prix median: {df['prix'].median():.0f} EUR | Surface mediane: {df['surface_m2'].median():.0f} m2 | "
        f"Cap prix: <= {args.max_price:.0f} EUR"
    )

    by_arr_count = (
        df["arrondissement"]
        .value_counts()
        .rename_axis("arrondissement")
        .reset_index(name="annonces")
        .sort_values("arrondissement")
    )
    fig = px.bar(
        by_arr_count,
        x="arrondissement",
        y="annonces",
        title="Annonces par arrondissement",
        text_auto=True,
        color="annonces",
        color_continuous_scale="Blues",
    )
    fig.update_layout(template="plotly_white", xaxis_title="Arrondissement", yaxis_title="Nb annonces")
    save_figure(fig, output_dir, "01_annonces_par_arrondissement")

    by_arr_price = (
        df.groupby("arrondissement", as_index=False)
        .agg(annonces=("id", "count"), prix_m2_median=("prix_m2", "median"))
        .query("annonces >= @args.min_arr_listings")
        .sort_values("prix_m2_median", ascending=False)
    )
    fig = px.bar(
        by_arr_price,
        x="arrondissement",
        y="prix_m2_median",
        title=(
            "Prix median au m2 par arrondissement "
            f"(min {args.min_arr_listings} annonces)"
        ),
        text_auto=".0f",
        color="prix_m2_median",
        color_continuous_scale="OrRd",
        hover_data=["annonces"],
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Arrondissement",
        yaxis_title="Prix median au m2 (EUR)",
    )
    save_figure(fig, output_dir, "02_prix_m2_par_arrondissement")

    fig = px.histogram(
        df,
        x="prix",
        nbins=35,
        title="Distribution des prix",
        color_discrete_sequence=["#e76f51"],
    )
    fig.update_layout(template="plotly_white", xaxis_title="Prix (EUR)", yaxis_title="Nb annonces")
    save_figure(fig, output_dir, "03_distribution_prix")

    fig = px.histogram(
        df,
        x="surface_m2",
        nbins=30,
        title="Distribution des surfaces",
        color_discrete_sequence=["#2a9d8f"],
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Surface (m2)",
        yaxis_title="Nb annonces",
    )
    save_figure(fig, output_dir, "04_distribution_surface")

    scatter_df = df.copy()
    top_arrs = scatter_df["arrondissement"].value_counts().head(8).index
    scatter_df["arrondissement_group"] = scatter_df["arrondissement"].where(
        scatter_df["arrondissement"].isin(top_arrs), "Autres"
    )
    fig = px.scatter(
        scatter_df,
        x="surface_m2",
        y="prix",
        color="arrondissement_group",
        title="Prix vs surface",
        opacity=0.7,
        hover_data=["arrondissement", "nb_pieces", "nb_chambres", "type_vendeur", "dpe"],
    )
    fig.update_layout(template="plotly_white", xaxis_title="Surface (m2)", yaxis_title="Prix (EUR)")
    save_figure(fig, output_dir, "05_prix_vs_surface")

    box_df = df[df["nb_pieces"].notna()].copy()
    box_df["nb_pieces"] = box_df["nb_pieces"].astype(int).astype(str)
    fig = px.box(
        box_df,
        x="nb_pieces",
        y="prix_m2",
        color="nb_pieces",
        title="Variance du prix au m2 par nombre de pieces",
        points=False,
    )
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="Nombre de pieces",
        yaxis_title="Prix au m2 (EUR)",
    )
    save_figure(fig, output_dir, "06_variance_prix_m2_par_pieces")

    dpe_order = ["A", "B", "C", "D", "E", "F", "G", "N", "V", "NA"]
    dpe_counts = df["dpe"].value_counts().rename_axis("dpe").reset_index(name="annonces")
    dpe_counts["dpe"] = pd.Categorical(dpe_counts["dpe"], categories=dpe_order, ordered=True)
    dpe_counts = dpe_counts.sort_values("dpe")
    fig = px.bar(
        dpe_counts,
        x="dpe",
        y="annonces",
        title="Repartition DPE",
        text_auto=True,
        color="annonces",
        color_continuous_scale="Teal",
    )
    fig.update_layout(template="plotly_white", xaxis_title="DPE", yaxis_title="Nb annonces")
    save_figure(fig, output_dir, "07_repartition_dpe")

    seller_counts = (
        df["type_vendeur"].value_counts().rename_axis("type_vendeur").reset_index(name="annonces")
    )
    fig = px.pie(
        seller_counts,
        names="type_vendeur",
        values="annonces",
        title="Repartition type vendeur",
        hole=0.4,
    )
    fig.update_layout(template="plotly_white")
    save_figure(fig, output_dir, "08_repartition_type_vendeur")

    print(f"Visualisations generees dans: {output_dir}")


if __name__ == "__main__":
    main()
