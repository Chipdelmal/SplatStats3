# !/usr/bin/env python3

from os import path, system
from glob import glob
import numpy as np
import pandas as pd
from random import shuffle
import matplotlib.pyplot as plt
from collections import Counter, OrderedDict
import SplatStats as splat


(six, USR) = (1, 'dsk')
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
fltrs = (btls['season']==SEASON, )
fltrBool = [all(i) for i in zip(*fltrs)]
btlsFiltered = btls[fltrBool]
###############################################################################
# Get Total Season Frequencies and Dominance Matrix
###############################################################################
(wpnFreq, wpnWLT, lbyFreq, lbyDaily) = (
    splat.getWeaponsFrequencies(btlsFiltered),
    splat.getWeaponsWLT(btlsFiltered),
    splat.getLobbyFrequencies(btlsFiltered),
    splat.countDailyLobbies(btlsFiltered)
)
lbyGaussDaily = splat.smoothCountDailyLobbies(lbyDaily)
(mNames, mMatrix) = splat.calculateDominanceMatrixWins(btlsFiltered)
(mWpnWins, mWpnLoss) = (np.sum(mMatrix, axis=1)/4, np.sum(mMatrix, axis=0)/4)
# Checks for consistency ------------------------------------------------------
tests = [
    np.sum(list(wpnFreq.values()))/8 == btlsFiltered.shape[0],
    np.sum(list(lbyFreq.values()))   == btlsFiltered.shape[0],
    np.sum(np.sum(wpnWLT[1][:,2]))   == np.sum(list(wpnFreq.values())),
    all(mWpnWins == wpnWLT[1][:,0]),
    all(mWpnLoss == wpnWLT[1][:,1]),
    all(wpnWLT[1][:,2] == mWpnWins+mWpnLoss)
]
assert(all(tests))
###############################################################################
# Calculate Auxiliary Metrics
###############################################################################
wpnsNum = len(mNames)
freqSorting = [mNames.index(w) for w in wpnFreq.keys()]
wpnWinRatio = wpnWLT[1][:,0]/wpnWLT[1][:,2]
###############################################################################
# Plot Total Frequencies
###############################################################################
itr = zip(
    [wpnsNum-i for i in range(wpnsNum)], wpnFreq.keys(),
    [wpnWinRatio[ix] for ix in freqSorting]
)
labels = ['{:02d}. {} ({}%)'.format(ix, n, int(f*100)) for (ix, n, f) in itr]
COLORS = splat.ALL_COLORS
shuffle(COLORS)
(fig, ax) = plt.subplots(
    figsize=(12, 12), subplot_kw={"projection": "polar"}
)
(fig, ax) = splat.polarBarChart(
    labels[::-1], list(wpnFreq.values())[::-1],
    yRange=(0, 3.0e5), rRange=(0, 180), ticksStep=4,
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
    txt.set_text('{:.0f}k'.format(float(lab)/1e3))
ax.set_xticklabels(xlabels, rotation=0, fontsize=8)
fName = 'Polar - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###########################################################################
# Weapon Matrix
###########################################################################
RAN = 0.75
COLS = (
    ('#B400FF', '#1D07AC'), ('#D01D79', '#1D07AC'), ('#6BFF00', '#1D07AC')
)
tauW = np.zeros((len(mMatrix), len(mMatrix)))
for (ix, wp) in enumerate(mNames):
    winsDiff = mMatrix[ix]/mMatrix[:,ix]
    tauW[ix] = winsDiff
tauX = np.copy(tauW)-1
sorting = list(np.argsort([np.sum(r>0) for r in tauX]))[::-1]
tauS = tauX[sorting][:,sorting]
namS = [mNames[i] for i in sorting]
counts = [np.sum(r>0) for r in tauS]
(tot, mns, sds) = (
    np.sum(tauS, axis=1), np.mean(tauS, axis=1), np.std(tauS, axis=1)
)
totMat = (mWpnWins+mWpnLoss)[sorting]
lLabs = ['{} ({})'.format(n, c) for (n, c) in zip(namS, counts)]
tLabs = ['({}k) {}'.format(c, n) for (n, c) in zip(namS, [int(i) for i in totMat/1e3])]
pal = splat.colorPaletteFromHexList([COLS[six][0], '#FFFFFF', COLS[six][1]])
(fig, ax) = plt.subplots(figsize=(20, 20))
im = ax.matshow(tauS, vmin=-RAN, vmax=RAN, cmap=pal)
ax.set_xticks(np.arange(0, len(namS)))
ax.set_yticks(np.arange(0, len(namS)))
ax.set_xticklabels(tLabs, rotation=90, fontsize=12.5)
ax.set_yticklabels(lLabs, fontsize=12.5)
yLims = ax.get_ylim()
fName = 'Matrix - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Type of Lobby
###############################################################################
(fig, ax) = plt.subplots(figsize=(0.4, 20))
(series, data) = (
    list(lbyFreq.keys()), 
    [[int(i)] for i in list(lbyFreq.values())]
)
data = [[i[0]/1000] for i in data]
(fig, ax) = splat.plotStackedBar(
    data, series, 
    labels=[i.replace(' ', '\n') for i in list(lbyFreq.keys())],
    figAx=(fig, ax),
    category_labels=False, 
    show_values=True, 
    value_format="{:.0f}k",
    colors=[
        '#2E0CB5', '#B400FF', '#6BFF00', '#525CF5', '#FDFF00', '#D01D79'
    ],
    fontsize=8.5, xTickOffset=0.7
)
ax.axis('off')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.text(
    -2.25, 0.5, 'Total matches: {:.0f}k'.format(np.sum(data)),
    fontsize=20,
    horizontalalignment='center',
    verticalalignment='center',
    transform=ax.transAxes,
    rotation=90
)
fName = 'Lobby - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')
###############################################################################
# Gaussian Lobby
###############################################################################
gModes = list(lbyDaily.columns)
gModesCols = ['#DE0B64FF', '#FDFF00FF', '#0D37C3FF', '#71DA0CFF', '#531BBAFF']
(fig, ax) = (plt.figure(figsize=(20, 3)), plt.axes())
ax.stackplot(
    lbyGaussDaily[0][0], *[-y[1] for y in lbyGaussDaily], 
    labels=gModes, baseline='zero',
    colors=gModesCols
)
ax.legend(loc='upper left').remove()
ax.set_xlim(0, lbyGaussDaily[0][0][-1])
ax.set_ylim(0, -1250)
xtickRan = np.arange(0, lbyGaussDaily[0][0][-1], 15)
ax.set_ylim(ax.get_ylim()[::-1])
ax.xaxis.tick_top()
ax.set_xticks(
    xtickRan, 
    ['{}/{}'.format(lbyDaily.index[i].month, lbyDaily.index[i].day) for i in xtickRan],
    ha='left', va='bottom', rotation=0, fontsize=12.5
)
ax.set_yticks([], [])
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
fName = 'Stacked - {}.png'.format(SEASON)
plt.savefig(
    path.join(DATA_PATH, 'statInk/'+fName),
    dpi=350, transparent=False, facecolor='#ffffff', bbox_inches='tight'
)
plt.close('all')