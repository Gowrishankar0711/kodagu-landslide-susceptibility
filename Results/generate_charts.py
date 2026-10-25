"""Regenerate compact result charts from the accompanying CSV tables.
Requires Matplotlib. No model predictions or training data are reconstructed.
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "charts"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "svg.fonttype": "none", "svg.hashsalt": "kodagu-results"})

def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def finish(fig, name, note):
    fig.text(.10, .025, note, fontsize=8, color="#475569")
    fig.subplots_adjust(left=.11, right=.97, bottom=.22, top=.85)
    fig.savefig(OUT / name, format="svg", metadata={"Date": None})
    plt.close(fig)

metrics = rows("model_performance.csv")
fig, ax = plt.subplots(figsize=(7.4, 3.8))
values = [float(r["ROC_AUC"]) for r in metrics]
bars = ax.bar(["AHP*", "RF", "ANN"], values, color=["#94a3b8", "#0f766e", "#2563eb"], width=.55)
ax.set(ylim=(0, 1.08), ylabel="ROC–AUC", title="Kodagu | ROC–AUC summary")
ax.set_yticks(np.arange(0, 1.01, .2))
ax.grid(axis="y", alpha=.15)
ax.set_axisbelow(True)
ax.bar_label(bars, labels=[f"{v:.4f}" for v in values], padding=5)
finish(fig, "roc_auc_comparison.svg", "*AHP: separate inventory/background evaluation. RF/ANN: test subset.")

fig, ax = plt.subplots(figsize=(7.4, 4))
keys = ["Accuracy_Percent", "Precision_Percent", "Recall_Percent", "F1_Percent"]
x = np.arange(4)
for i, (r, color) in enumerate(zip(metrics[1:], ["#0f766e", "#2563eb"])):
    vals = [float(r[k]) for k in keys]
    bars = ax.bar(x + (i-.5)*.36, vals, .36, label=r["Model"], color=color)
    ax.bar_label(bars, labels=[f"{v:.2f}" for v in vals], padding=3, fontsize=8)
ax.set(xticks=x, xticklabels=["Accuracy", "Precision", "Recall", "F1"], ylim=(0, 108),
       ylabel="Percent", title="Kodagu | ML test performance")
ax.set_yticks(np.arange(0,101,20))
ax.legend(loc="upper center", bbox_to_anchor=(.5,1.03), ncol=2, frameon=False)
ax.grid(axis="y", alpha=.15)
ax.set_axisbelow(True)
finish(fig, "ml_metrics_comparison.svg", "70:30 split. Precision, recall and F1 describe the landslide class.")

classes = rows("susceptibility_area_statistics.csv")
fig, ax = plt.subplots(figsize=(7.4, 4))
models = ["AHP", "Random Forest", "ANN"]
bottom = np.zeros(3)
for category, color in zip(["Low","Moderate","High"], ["#81b29a","#f2cc8f","#c85555"]):
    vals = np.array([float(next(r["Area_Percent"] for r in classes
                    if r["Model"]==m and r["Susceptibility"]==category)) for m in models])
    ax.barh(["AHP", "RF", "ANN"], vals, left=bottom, label=category, color=color, height=.55)
    for y, v, left in zip(range(3), vals, bottom):
        ax.text(left+v/2, y, f"{v:.2f}%", ha="center", va="center", fontsize=9,
                color="white" if category=="High" else "#17202a")
    bottom += vals
ax.invert_yaxis()
ax.set(xlim=(0,100), xlabel="Share of each model's analysed area (%)",
       title="Kodagu | Susceptibility class distribution")
ax.set_title("Kodagu | Susceptibility class distribution", pad=32)
ax.legend(loc="lower center", bbox_to_anchor=(.5,1.01), ncol=3, frameon=False)
finish(fig, "class_distribution.svg", "AHP: rounded reported percentages (99.99% total). Class thresholds may differ.")

agreement = rows("model_agreement_statistics.csv")
fig, ax = plt.subplots(figsize=(7.4,3.8))
vals = [float(r["Percentage"]) for r in agreement]
bars = ax.barh(["All three agree","Exactly two agree","All three disagree"], vals,
              color=["#0f766e","#94a3b8","#c85555"], height=.55)
ax.invert_yaxis()
ax.set(xlim=(0,80), xlabel="Share of common analysed cells (%)",
       title="Kodagu | Agreement between AHP, RF and ANN")
ax.bar_label(bars, labels=[f"{v:.2f}%" for v in vals], padding=4)
fig.subplots_adjust(left=.27)
# Wider left margin accommodates the full agreement labels.
fig.text(.10,.025,"Overall class agreement; separate from the 2.99% high-susceptibility intersection.",
         fontsize=8,color="#475569")
fig.subplots_adjust(left=.27,right=.97,bottom=.23,top=.85)
fig.savefig(OUT/"model_agreement.svg",format="svg",metadata={"Date":None})
plt.close(fig)
print("Created four comparison charts.")
