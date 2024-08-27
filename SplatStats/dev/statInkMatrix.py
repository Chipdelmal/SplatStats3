# !/usr/bin/env python3

import numpy as np
from os import path
from glob import glob
from random import shuffle
import SplatStats as splat
import matplotlib.pyplot as plt

(six, USR) = (1, 'dsk')
SSON = [
    'Drizzle Season 2022', 'Chill Season 2022', ' Fresh 2022', 'Sizzle Season 2022',
    'Drizzle Season 2023', 'Chill Season 2023', ' Fresh 2023', 'Sizzle Season 2023',
    'Drizzle Season 2024', 'Chill Season 2024', ' Fresh 2024', 'Sizzle Season 2024',
]
SEASON = SSON[six]
###############################################################################
# Get files and set font
###############################################################################
if USR=='lab':
    DATA_PATH = '/Users/sanchez.hmsc/Sync/BattlesDocker/'
elif USR=='lap':
    DATA_PATH = '/Users/sanchez.hmsc/Documents/SyncMega/BattlesDocker'
else:
    DATA_PATH = '/home/chipdelmal/Documents/Sync/BattlesDocker/'
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
###############################################################################
# Parse Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
###############################################################################
# Filter by Constraints
###############################################################################
# for gmode in ('Tower Control', 'Splat Zones', 'Turf War', 'Clam Blitz', 'Rainmaker'):
fltrs = (btls['season']==SEASON, ) # btls['mode']==gmode)
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
tauW = np.zeros((len(matrix), len(matrix)))
for (ix, wp) in enumerate(names):
    winsDiff = matrix[ix]/matrix[:,ix]
    tauW[ix] = winsDiff
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
###############################################################################
# Matrices
###############################################################################
(TITLE, RAN) = (True, 0.75)
COLS = (
    ('#B400FF', '#1D07AC'), ('#D01D79', '#1D07AC'), ('#6BFF00', '#1D07AC')
)
# Re-Arrange Stuff ------------------------------------------------------------
tauX = np.copy(tauW)-1
sorting = list(np.argsort([np.sum(r>0) for r in tauX]))[::-1]
# sorting = list(np.argsort([np.sum(r) for r in tauX]))[::-1]
tauS = tauX[sorting][:,sorting]
namS = [names[i] for i in sorting]
counts = [np.sum(r>0) for r in tauS]
(tot, mns, sds) = (
    np.sum(tauS, axis=1), np.mean(tauS, axis=1), np.std(tauS, axis=1)
)
totMat = totalM[sorting]
lLabs = ['{} ({})'.format(n, c) for (n, c) in zip(namS, counts)]
tLabs = ['({:03d}k) {}'.format(c, n) for (n, c) in zip(namS, [int(i) for i in totMat/1e3])]
# rLabs = ['{:02d} ({:03d}k)'.format(t, s) for (t, s) in zip(counts, [int(i) for i in totMat/1e3])]
pal = splat.colorPaletteFromHexList([COLS[six][0], '#FFFFFF', COLS[six][1]])
(fig, ax) = plt.subplots(figsize=(20, 20))
im = ax.matshow(tauS, vmin=-RAN, vmax=RAN, cmap=pal)
ax.set_xticks(np.arange(0, len(namS)))
ax.set_yticks(np.arange(0, len(namS)))
ax.set_xticklabels(tLabs, rotation=90, fontsize=12.5)
ax.set_yticklabels(lLabs, fontsize=12.5)
yLims = ax.get_ylim()
# ax2 = ax.twinx()
# ax2 = fig.add_subplot(111, sharex=ax, frameon=False)
# ax2.matshow(tauS, vmin=-RAN, vmax=RAN, cmap=pal)
# ax2.yaxis.tick_right()
# ax2.set_ylim(*yLims)
# ax2.set_xticks(np.arange(0, len(namS)))
# ax2.set_xticklabels(namS, rotation=90, fontsize=12.5)
# ax2.set_yticks(np.arange(0, len(namS)))
# ax2.set_yticklabels(rLabs, fontsize=12.5)
# fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.2)
if TITLE:
    ax.set_title(SEASON, fontsize=50, y=-.06)
fName = '{} Weapon Matrix.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Frequency Analysis
###############################################################################
wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: (x[1], x[2], x[3]) for (_, x) in sorted(wpnSortZip)[::]}
wlRatio = [i[1]/i[0] for i in wpnsDict.values()]
# Polar barchart --------------------------------------------------------------
nItems = len(wlRatio)
itr = zip(
    [nItems-i for i in range(nItems)], wpnsDict.keys(), wlRatio
)
labels = ['{:02d}. {} ({}%)'.format(ix, n, int(f*100)) for (ix, n, f) in itr]
COLORS = splat.ALL_COLORS
shuffle(COLORS)
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels, [i[0] for i in wpnsDict.values()],
    yRange=(0, 1e6), rRange=(0, 90), ticksStep=4,
    colors=[c+'DD' for c in COLORS],
    edgecolor='#00000088', linewidth=0,
    figAx=(fig, ax),
    ticksFmt={
        'lw': 1, 'range': (-.2, 1), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.1e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 3.75, 
        'ha': 'left', 'fmt': '{:.1f}'
    }
)
xlabels = ax.get_xticklabels()
for txt in xlabels:
    lab = txt.get_text()
    txt.set_text('{:.2f}M'.format(float(lab)/1e6))
ax.set_xticklabels(xlabels, rotation=0, fontsize=8)
ax.set_title(SEASON, fontsize=25, x=.25, y=.5)
fName = 'PolarHalf - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')




###############################################################################
# Code Dominance Matrix
###############################################################################
# wpnsNames = None
# btls = btlsFiltered.iloc[0:3]
# btlsNum = btls.shape[0]
# # Get weapons used by each team, and who won ---------------------------------
# (alpha, bravo, winAlpha) = (
#     btls[[f'A{i}-weapon' for i in range(1, 5)]],
#     btls[[f'B{i}-weapon' for i in range(1, 5)]],
#     list(btls['win'])
# )
# # Get all the weapons used, and sort them if needed --------------------------
# if not wpnsNames:
#     wpnsSet = (set(alpha.stack()) | set(bravo.stack()))
#     wpnsNames = sorted(list(wpnsSet))
# wpnsNumbr = len(wpnsNames)
# # Generate matrix ------------------------------------------------------------
# domMtx = np.zeros((wpnsNumbr, wpnsNumbr))
# bix = 0
# for bix in range(btlsNum):
#     # Get names for weapons in both teams ------------------------------------
#     (wpnsNmA, wpnsNmB) = (list(alpha.iloc[bix]), list(bravo.iloc[bix]))
#     # Get indices for weapons in both teams ----------------------------------
#     (wpnsIxA, wpnsIxB) = (
#         [wpnsNames.index(w) for w in wpnsNmA],
#         [wpnsNames.index(w) for w in wpnsNmB]
#     )
#     if winAlpha[bix]:
#         # Team Alpha won -----------------------------------------------------
#         for ixA in wpnsIxA:
#             for ixB in wpnsIxB:
#                 domMtx[ixA, ixB] = domMtx[ixA, ixB] + 1
#     else:
#         # Team Bravo won -----------------------------------------------------
#         for ixB in wpnsIxB:
#             for ixA in wpnsIxA:
#                 domMtx[ixB, ixA] = domMtx[ixB, ixA] + 1
# domMtx.T


# # Vectorize (encode) the weapons used by each team in the battles ---------
# vct = DictVectorizer(sparse=False)

# (wpnsDA, wpnsDB) = (
#     [dict(Counter(alpha.iloc[i])) for i in range(alpha.shape[0])],
#     [dict(Counter(bravo.iloc[i])) for i in range(bravo.shape[0])]
# )


# wpnsDA

# (wpnsVA, wpnsVB) = (
#     vct.fit_transform(wpnsDA), 
#     vct.fit_transform(wpnsDB)
# )

# wpnsNames = list(vct.get_feature_names_out())
# wpnsNumbr = len(wpnsNames)


# ix = 0

# alpha.iloc[ix]
# wpnsDA[ix]
# wpix = [jx for (jx, i) in enumerate(wpnsVA[ix]) if (i>=1)]
# [wpnsNames[n] for n in wpix]

# bravo.iloc[ix]
# wpnsDB[ix]
# wpnsVB[ix]
# wpix = [jx for (jx, i) in enumerate(wpnsVB[ix]) if (i>=1)]
# [wpnsNames[n] for n in wpix]


# (bAWpns, bBWpns) = (wpnsDA[ix], wpnsDB[ix])
# (bAVctr, bBVctr) = (wpnsVA[ix], wpnsVB[ix])

# domMtx = np.zeros((wpnsNumbr, wpnsNumbr))
# for ix in range(btlsNum):
#     (bAWpns, bBWpns) = (wpnsDA[ix], wpnsDB[ix])
#     (bAVctr, bBVctr) = (wpnsVA[ix], wpnsVB[ix])
#     if winAlpha[ix]:
#         # Alpha won -------------------------------------------------------
#         rxs = splat.flatten([[wpnsNames.index(wpn)]*bBWpns[wpn] for wpn in bBWpns])
#         # rxs = [wpnsNames.index(wpn) for wpn in bBWpns]
#         for rx in rxs:
#             domMtx[rx] = domMtx[rx]+bAVctr
#     else:
#         # Bravo won -------------------------------------------------------
#         rxs = splat.flatten([[wpnsNames.index(wpn)]*bAWpns[wpn] for wpn in bAWpns])
#         # rxs = [wpnsNames.index(wpn) for wpn in bAWpns]
#         for rx in rxs:
#             domMtx[rx] = domMtx[rx]+bBVctr
# # Transpose and return ----------------------------------------------------
# domMtx = domMtx.T 
