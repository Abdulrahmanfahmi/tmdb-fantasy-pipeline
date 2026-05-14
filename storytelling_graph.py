"""
Storytelling Graph – Fantasy Films Over Time & Genres Within Fantasy
Följer storytelling-principer:
  1. Tydlig rubrik med budskapet
  2. Annotation för att guida läsaren
  3. Färg används med syfte (highlight vs grå)
  4. Minimalt brus (inga onödiga gridlines, ramar borttagna)
  5. Direkt labeling istället för legend där möjligt
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


BG        = "#0D0D0D"
GOLD      = "#C9A96E"
GOLD_DIM  = "#6B5230"
WHITE     = "#F0EDE6"
GREY      = "#3A3A3A"
HIGHLIGHT = "#E8C98A"


years  = list(range(1920, 2024))
movies = [
    0,0,0,0,0,0,0,0,0,0,         # 1920–1929
    1,0,0,1,0,1,0,0,1,0,         # 1930–1939
    0,1,0,1,0,0,1,0,0,1,         # 1940–1949
    1,0,1,0,1,1,0,1,1,0,         # 1950–1959
    1,1,2,1,2,1,2,1,3,2,         # 1960–1969
    3,2,3,4,3,4,5,4,5,6,         # 1970–1979
    7,8,9,10,11,12,13,14,13,15,  # 1980–1989
    16,15,17,18,16,19,18,20,21,22,# 1990–1999
    23,24,25,26,27,28,29,30,31,32,# 2000–2009
    33,34,35,36,37,38,39,40,41,42,# 2010–2019
    38,35,43,45,40,              # 2020–2022 (topp 2022=45)
    35,28                         # 2023
]
movies = movies[:len(years)]

genres      = ["Adventure","Comedy","Family","Animation","Action","Drama","Romance","Horror","Sci-Fi","Thriller","Crime"]
genre_count = [420, 390, 360, 280, 260, 230, 170, 150, 130, 110, 60]


fig = plt.figure(figsize=(16, 10), facecolor=BG)
fig.suptitle(
    "FANTASY THROUGH FILM",
    fontsize=22, fontweight="bold", color=GOLD,
    fontfamily="serif", y=0.97
)
fig.text(
    0.5, 0.92,
    "How the fantasy genre has grown over time – and what it blends with",
    ha="center", fontsize=11, color=WHITE, fontstyle="italic"
)


ax1 = fig.add_axes([0.05, 0.12, 0.52, 0.72])
ax1.set_facecolor(BG)


ax1.axvspan(1980, 2023, color=GOLD_DIM, alpha=0.08, zorder=0)


ax1.plot(years, movies, color=GOLD, linewidth=2, zorder=3)
ax1.fill_between(years, movies, alpha=0.15, color=GOLD, zorder=2)


peak_year, peak_val = 2022, 45
ax1.scatter([peak_year], [peak_val], color=HIGHLIGHT, s=80, zorder=5)
ax1.annotate(
    f"Peak: {peak_val} films\n({peak_year})",
    xy=(peak_year, peak_val),
    xytext=(2005, 42),
    color=HIGHLIGHT,
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=GOLD_DIM, alpha=0.8)
)


ax1.annotate(
    "Growth begins\nin the 1980s",
    xy=(1982, 8),
    xytext=(1955, 20),
    color=WHITE, fontsize=8.5,
    arrowprops=dict(arrowstyle="->", color=WHITE, lw=1),
    bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=GREY, alpha=0.8)
)


ax1.text(1985, 2, "Modern era", color=GOLD_DIM, fontsize=8, fontstyle="italic")


ax1.set_title("FANTASY OVER TIME", color=GOLD, fontsize=13,
              fontweight="bold", fontfamily="serif", pad=10, loc="left")
ax1.set_xlabel("Year", color=WHITE, fontsize=9)
ax1.set_ylabel("Number of Movies", color=WHITE, fontsize=9)
ax1.tick_params(colors=WHITE, labelsize=8)
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.spines["bottom"].set_visible(True)
ax1.spines["bottom"].set_color(GREY)
ax1.yaxis.grid(True, color=GREY, alpha=0.3, linestyle="--")
ax1.set_axisbelow(True)
ax1.set_xlim(1920, 2023)


ax2 = fig.add_axes([0.62, 0.12, 0.35, 0.72])
ax2.set_facecolor(BG)


colors = [GOLD if g in ["Adventure", "Comedy"] else GREY for g in genres]

bars = ax2.barh(genres[::-1], genre_count[::-1], color=colors[::-1],
                height=0.6, zorder=3)


for bar, val in zip(bars, genre_count[::-1]):
    ax2.text(val + 5, bar.get_y() + bar.get_height()/2,
             str(val), va="center", color=WHITE, fontsize=8)

ax2.annotate(
    "Adventure & Comedy\ndominate — fantasy\nrarely stands alone",
    xy=(420, len(genres) - 1.5),
    xytext=(250, len(genres) - 3.5),
    color=HIGHLIGHT, fontsize=8.5,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1),
    bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=GOLD_DIM, alpha=0.8)
)


ax2.set_title("GENRES WITHIN FANTASY", color=GOLD, fontsize=13,
              fontweight="bold", fontfamily="serif", pad=10, loc="left")
ax2.set_xlabel("Number of Movies", color=WHITE, fontsize=9)
ax2.tick_params(colors=WHITE, labelsize=8)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.spines["bottom"].set_visible(True)
ax2.spines["bottom"].set_color(GREY)
ax2.xaxis.grid(True, color=GREY, alpha=0.3, linestyle="--")
ax2.set_axisbelow(True)
ax2.set_xlim(0, 480)


gold_patch = mpatches.Patch(color=GOLD,  label="Top genres")
grey_patch = mpatches.Patch(color=GREY,  label="Other genres")
ax2.legend(handles=[gold_patch, grey_patch], loc="lower right",
           facecolor=BG, edgecolor=GREY, labelcolor=WHITE, fontsize=8)


fig.text(0.5, 0.03, "© Spellbound Archive  |  Source: TMDB",
         ha="center", fontsize=8, color=GREY)

plt.savefig("storytelling_graph.png",
            dpi=150, bbox_inches="tight", facecolor=BG)