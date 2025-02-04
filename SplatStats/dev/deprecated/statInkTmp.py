# !/usr/bin/env python3

# https://github.com/fetus-hina/stat.ink/wiki/Spl3-%EF%BC%8D-CSV-Schema-%EF%BC%8D-Battle
# https://stat.ink/api-info/weapon3

from os import path
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from colour import Color
from matplotlib.ticker import EngFormatter
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import SplatStats as splat
import chord as chd
import matplotlib.colors as colors
from scipy.stats import entropy

(six, USR) = (0, 'lap')
SSON = ['Drizzle Season 2022', 'Chill Season 2022', 'Fresh Season 2023']
SEASON = SSON[six]
TOP = 20
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





# np.nanmean(entropy(tauW, axis=1))
sds = [np.nanstd(r[~np.isinf(r)]) for r in tauW]
(fig, ax) = plt.subplots(figsize=(2, 6))
ax.violinplot(sds, showmeans=True, showmedians=False, showextrema=False)
# ax.set_title(gmode)
ax.set_ylim(0, 1)
###############################################################################
# MatPlot
###############################################################################
# Unsorted --------------------------------------------------------------------
pal = splat.colorPaletteFromHexList(['#000000', '#FFFFFF', '#1D07AC'])
(fig, ax) = plt.subplots(figsize=(20, 20))
ax.matshow(tauW, vmin=.5, vmax=1.5, cmap=pal)
ax.set_xticks(np.arange(0, len(names)))
ax.set_yticks(np.arange(0, len(names)))
ax.set_xticklabels(names, rotation=90)
ax.set_yticklabels(names)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+'Matrix.png'),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
# Sorted ----------------------------------------------------------------------
tauX = np.copy(tauW)
# Most popular
sorting = list(np.argsort(totalM))[::-1]
# Most over
sorting = list(np.argsort([np.sum(r>=1) for r in tauX]))[::-1]

tauS = tauX[sorting][:,sorting]
namS = [names[i] for i in sorting]


pal = splat.colorPaletteFromHexList(['#000000', '#FFFFFF', '#1D07AC'])
(fig, ax) = plt.subplots(figsize=(20, 20))
ax.matshow(tauS, vmin=0.5, vmax=1.5, cmap=pal)
ax.set_xticks(np.arange(0, len(namS)))
ax.set_yticks(np.arange(0, len(namS)))
ax.set_xticklabels(namS, rotation=90)
ax.set_yticklabels(namS)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+'MatrixSorted.png'),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
# Sliced ----------------------------------------------------------------------
pal = splat.colorPaletteFromHexList(['#000000', '#FFFFFF', '#1D07AC'])
fig, ax = plt.subplots()
data1 = tauS.copy()
data1[6, :] = float('nan')
data2 = tauS.copy()
data2[:6, :] = float('nan')
im_1 = ax.imshow(data1, cmap='Reds')
im_2 = ax.imshow(data2, cmap='Blues')
im = np.vstack((im_1, im_2))
plt.show()
# Unknown ---------------------------------------------------------------------
tauW[tauW<=1]=0

pad = 1.5
norm = colors.LogNorm(vmin=0.1, vmax=np.max(tauW))
colorPalette = splat.colorPaletteFromHexList(['#bdedf6', '#04067B'])
pColors = [colorPalette(norm(i)) for i in np.sum(tauW, axis=1)]
(fig, ax) = plt.subplots(figsize=(20, 20))
ax = chd.chord_modded(
    tauW, names, 
    ax=ax, rotate_names=[True]*len(names),
    fontcolor='k', chordwidth=.7, width=0.1, fontsize=4,
    extent=360, start_at=0, use_gradient=True, directed=False,
    cmap='plasma'
    # colors=pColors, 
)
ax.set_xlim(-pad, pad)
ax.set_ylim(-pad, pad)
ax.axis('off')
plt.savefig(
    path.join('/Users/sanchez.hmsc/Desktop', 'Chord.png'),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
# TESTS  ----------------------------------------------------------------------
(up, lo) = (np.triu(matrix, k=0), np.tril(matrix, k=0))
mat = np.copy(matrix)
np.fill_diagonal(mat, 0)
np.fill_diagonal(up, 0)
np.fill_diagonal(lo, 0)
###############################################################################
# Chord Analysis
###############################################################################
btlsFiltered = btls[fltrBool]
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
sums = np.sum(matrix, axis=1)

selfProb = np.diag(matrix.copy(), k=0)
norm = colors.LogNorm(vmin=1, vmax=np.max(matrix))
colorPalette = splat.colorPaletteFromHexList(['#bdedf6', '#04067B'])
pColors = [colorPalette(norm(i)) for i in sums]

cMat = matrix.copy()
np.fill_diagonal(cMat, 0)

pad = 1.5
(fig, ax) = plt.subplots(figsize=(10, 10))
ax = chd.chord_modded(
    cMat, names, 
    ax=ax, rotate_names=[True]*len(names),
    fontcolor='k', chordwidth=.7, width=0.1, fontsize=4,
    extent=360, start_at=0,
    colors=pColors, use_gradient=True
)
ax.set_xlim(-pad, pad)
ax.set_ylim(-pad, pad)
ax.axis('off')
fName = 'Chord.png'
plt.savefig(
    path.join('/Users/sanchez.hmsc/Desktop', fName),
    dpi=300, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')

plt.matshow(matrix)


names[0]
sums = np.sum(matrix, axis=1)
(minIx, maxIx) = (
    np.where(sums==sums.min())[0][0],
    np.where(sums==sums.max())[0][0]
)
[names[i] for i in (minIx, maxIx)]

###############################################################################
# Aggregate by date
###############################################################################
df['dummy'] = [1]*df.shape[0]
counts = df.groupby([df['period'].dt.date]).count()['dummy']
(fig, ax) = (plt.figure(), plt.axes())
ax.plot(list(counts))
df['mode'] = [splat.GAME_MODE[lob] for lob in df['mode']]




###############################################################################
# Stacked by type
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
gmodes = zip(
    ['Turf War', 'Splat Zones', 'Tower Control', 'Rainmaker', 'Clam Blitz'],
    ['FF', '99', '77', '55', '44'],
    [.2, .4, .5, .6, .8]
)
###############################################################################
# Frequency Analysis
###############################################################################
btlsFiltered = btls
(names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
# Calculating totals ----------------------------------------------------------
(totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
totalM = totalW + totalL
wpnsTriplets = zip(names, totalM, totalW, totalL)
wpnSortZip = zip(totalM, wpnsTriplets)
wpnsDict = {x[0]: np.array([0, 0, 0]) for (_, x) in sorted(wpnSortZip)[::]}
# Generate figure -------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})
gm = 'Turf War'
lum = -.15
cols = splat.ALL_COLORS
for (gm, ap, lum) in gmodes:
    # lum = (lum + 0.15)
    ###########################################################################
    # Filter by Constraints
    ###########################################################################
    fltrs = (btls['mode']==gm,)
    fltrBool = [all(i) for i in zip(*fltrs)]
    btlsFiltered = btls[fltrBool]
    (names, matrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
    (totalW, totalL) = (np.sum(matrix, axis=1), np.sum(matrix, axis=0))
    totalM = totalW + totalL
    for (ix, wpn) in enumerate(names):
        wpnsDict[wpn] = wpnsDict[wpn] + [totalM[ix], totalW[ix], totalL[ix]]

    colrs = []
    for c in splat.ALL_COLORS:
        cl = Color(c)
        cl.set_luminance(lum)
        colrs.append(cl.get_hex_l())

    (fig, ax) = splat.polarBarChart(
        wpnsDict.keys(), 
        [i[0] for i in wpnsDict.values()],
        figAx=(fig, ax),
        edgecolor='#00000088', linewidth=0.25,
        yRange=(0, 1.5e6), rRange=(0, 180), ticksStep=6,
        colors=[str(c)+ap for c in colrs],
        ticksFmt={
            'lw': 1, 'range': (-.2, 1), 
            'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.2e}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 4.25, 
            'ha': 'left', 'fmt': '{:.2f}'
        }
    )
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=7.5)
fName = 'PolarBroken.png'
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')


###############################################################################
# Win/Lose
###############################################################################
labels = ['{} ({}%)'.format(n, int(f*100)) for (n, f) in zip(wpnsDict.keys(), wlRatio)]
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels, 
    [i[0] for i in wpnsDict.values()],
    yRange=(0, 1.5e6), rRange=(0, 180), ticksStep=6,
    colors=[c+'DD' for c in splat.ALL_COLORS],
    edgecolor='#00000088', linewidth=0,
    figAx=(fig, ax),
    ticksFmt={
        'lw': 1, 'range': (-.2, 1), 
        'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.2e}'
    },
    labelFmt={
        'color': '#000000EE', 'fontsize': 4, 
        'ha': 'left', 'fmt': '{:.2f}'
    }
)
# (fig, ax) = splat.polarBarChart(
#     labels, 
#     [i[2] for i in wpnsDict.values()],
#     yRange=(0, 1.5e6), rRange=(0, 180), ticksStep=20,
#     figAx=(fig, ax),
#     colors=[c+'FF' for c in splat.ALL_COLORS],
#     edgecolor='#00000088', linewidth=0.25,
#     ticksFmt={
#         'lw': 1, 'range': (-.2, 1), 
#         'color': '#000000DD', 'fontsize': 1, 'fmt': '{:.2e}'
#     },
#     labelFmt={
#         'color': '#000000EE', 'fontsize': 4.25, 
#         'ha': 'left', 'fmt': '{:.2f}'
#     }
# )
# formatter1 = EngFormatter(places=1, unit="", sep="")
# ax.xaxis.set_major_formatter(formatter1)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=7.5)
# ax.set_xlabel('Number [Hz]')
fName = 'Polar.png'
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', 
    bbox_inches='tight'
)
plt.close('all')