from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model import ModelState, compute_fluxes


def plot_sensitivity(df: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    axes = axes.ravel()

    x = df["PPP_fraction"].to_numpy()

    axes[0].plot(x, df["NADPH"].to_numpy(), color="#2e8b57", marker="o")
    axes[0].set_title("PPP fraction vs NADPH")
    axes[0].set_xlabel("PPP fraction")
    axes[0].set_ylabel("NADPH")
    axes[0].grid(True, linestyle="--", alpha=0.4)

    axes[1].plot(x, df["ROS"].to_numpy(), color="#d9534f", marker="o")
    axes[1].set_title("PPP fraction vs ROS")
    axes[1].set_xlabel("PPP fraction")
    axes[1].set_ylabel("ROS")
    axes[1].grid(True, linestyle="--", alpha=0.4)

    axes[2].plot(x, df["ATP"].to_numpy(), color="#337ab7", marker="o")
    axes[2].set_title("PPP fraction vs ATP")
    axes[2].set_xlabel("PPP fraction")
    axes[2].set_ylabel("ATP")
    axes[2].grid(True, linestyle="--", alpha=0.4)

    axes[3].plot(x, df["2,3-BPG"].to_numpy(), color="#f0ad4e", marker="o")
    axes[3].set_title("PPP fraction vs 2,3-BPG")
    axes[3].set_xlabel("PPP fraction")
    axes[3].set_ylabel("2,3-BPG")
    axes[3].grid(True, linestyle="--", alpha=0.4)

    return fig, axes


def create_comparison_plot(scenario_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(scenario_df))
    width = 0.15

    metrics = ["ATP", "NADPH", "ROS", "2,3-BPG"]
    colors = ["#4c78a8", "#54a24b", "#e45756", "#f58518"]

    for i, metric in enumerate(metrics):
        ax.bar(x + (i - 1.5) * width, scenario_df[metric].to_numpy(), width=width, label=metric, color=colors[i])

    ax.set_xticks(x)
    ax.set_xticklabels(scenario_df["Scenario"], rotation=20, ha="right")
    ax.set_ylabel("Normalized/arbitrary units")
    ax.set_title("Normal vs SCD-like vs Simulated Intervention")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.3, axis="y")
    return fig


def create_pathway_figure(current_state: ModelState) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    flux = compute_fluxes(current_state)

    nodes = [
        (0.10, 0.75, "GLUCOSE"),
        (0.25, 0.55, "Glycolysis"),
        (0.25, 0.20, "PPP"),
        (0.50, 0.55, "ATP"),
        (0.50, 0.20, "NADPH"),
        (0.75, 0.20, "Antioxidant\nprotection"),
        (0.70, 0.55, "2,3-BPG\nbranch"),
    ]

    for x, y, text in nodes:
        ax.text(x, y, text, ha="center", va="center", fontsize=10,
                bbox=dict(facecolor="lightyellow", edgecolor="black", boxstyle="round,pad=0.4"))

    ax.annotate("", xy=(0.20, 0.55), xytext=(0.15, 0.73),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.annotate("", xy=(0.20, 0.20), xytext=(0.15, 0.77),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.annotate("", xy=(0.40, 0.55), xytext=(0.30, 0.55),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.annotate("", xy=(0.40, 0.20), xytext=(0.30, 0.20),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.annotate("", xy=(0.65, 0.20), xytext=(0.55, 0.20),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.annotate("", xy=(0.65, 0.55), xytext=(0.40, 0.55),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax.text(0.05, 0.92, f"Glycolysis flux: {flux['glycolysis_flux']:.2f}", fontsize=9, weight="bold")
    ax.text(0.05, 0.88, f"PPP flux: {flux['ppp_flux']:.2f}", fontsize=9, weight="bold")
    ax.text(0.55, 0.92, f"ATP: {flux['ATP']:.2f}", fontsize=9, weight="bold")
    ax.text(0.55, 0.88, f"NADPH: {flux['NADPH']:.2f}", fontsize=9, weight="bold")
    ax.text(0.55, 0.84, f"ROS: {flux['ROS']:.2f}", fontsize=9, weight="bold")
    ax.text(0.55, 0.80, f"2,3-BPG: {flux['2,3-BPG']:.2f}", fontsize=9, weight="bold")

    return fig
