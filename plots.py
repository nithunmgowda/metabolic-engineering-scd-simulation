from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from model import ModelState, compute_fluxes, sensitivity_analysis


def plot_sensitivity(df: pd.DataFrame) -> tuple[plt.Figure, list[plt.Axes]]:
    """Generate the required sensitivity plots as a single figure with 4 subplots."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    axes = axes.ravel()

    x = df["PPP_fraction"].to_numpy()

    y_nadph = df["NADPH"].to_numpy()
    y_ros = df["ROS"].to_numpy()
    y_atp = df["ATP"].to_numpy()
    y_bpg = df["2,3-BPG"].to_numpy()

    axes[0].plot(x, y_nadph, color="#2e8b57", marker="o")
    axes[0].set_title("PPP flux vs NADPH")
    axes[0].set_xlabel("PPP fraction")
    axes[0].set_ylabel("NADPH")

    axes[1].plot(x, y_ros, color="#d9534f", marker="o")
    axes[1].set_title("PPP flux vs ROS")
    axes[1].set_xlabel("PPP fraction")
    axes[1].set_ylabel("ROS")

    axes[2].plot(x, y_atp, color="#337ab7", marker="o")
    axes[2].set_title("PPP flux vs ATP")
    axes[2].set_xlabel("PPP fraction")
    axes[2].set_ylabel("ATP")

    axes[3].plot(x, y_bpg, color="#f0ad4e", marker="o")
    axes[3].set_title("PPP flux vs 2,3-BPG")
    axes[3].set_xlabel("PPP fraction")
    axes[3].set_ylabel("2,3-BPG")

    for ax in axes:
        ax.grid(True, linestyle="--", alpha=0.4)

    return fig, axes


def create_comparison_plot(scenario_df: pd.DataFrame) -> plt.Figure:
    """Create a simple grouped bar chart comparing the three model states."""
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
    ax.grid(True, linestyle="--", alpha=0.3)
    return fig


def create_pathway_figure(current_state: ModelState) -> plt.Figure:
    """Create a simple pathway schematic with current flux values annotated."""
    fig, ax = plt.subplots(figsize=(10, 5))
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
        ax.text(x, y, text, ha="center", va="center", fontsize=11, bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))

    ax.annotate('', xy=(0.35, 0.55), xytext=(0.18, 0.75), arrowprops=dict(arrowstyle='->', color='black'))
    ax.annotate('', xy=(0.35, 0.20), xytext=(0.18, 0.75), arrowprops=dict(arrowstyle='->', color='black'))
    ax.annotate('', xy=(0.60, 0.55), xytext=(0.35, 0.55), arrowprops=dict(arrowstyle='->', color='black'))
    ax.annotate('', xy=(0.60, 0.20), xytext=(0.35, 0.20), arrowprops=dict(arrowstyle='->', color='black'))
    ax.annotate('', xy=(0.75, 0.20), xytext=(0.60, 0.20), arrowprops=dict(arrowstyle='->', color='black'))
    ax.annotate('', xy=(0.70, 0.55), xytext=(0.45, 0.55), arrowprops=dict(arrowstyle='->', color='black'))

    ax.text(0.20, 0.80, f"Current glycolysis flux: {flux['glycolysis_flux']:.2f}", fontsize=10)
    ax.text(0.20, 0.12, f"Current PPP flux: {flux['ppp_flux']:.2f}", fontsize=10)
    ax.text(0.52, 0.75, f"Current ATP: {flux['ATP']:.2f}", fontsize=10)
    ax.text(0.52, 0.12, f"Current NADPH: {flux['NADPH']:.2f}", fontsize=10)
    ax.text(0.76, 0.12, f"Current ROS: {flux['ROS']:.2f}", fontsize=10)
    ax.text(0.70, 0.75, f"Current 2,3-BPG: {flux['2,3-BPG']:.2f}", fontsize=10)

    return fig


__all__ = ["plot_sensitivity", "create_comparison_plot", "create_pathway_figure"]
