# !/usr/bin/env python3

import os    
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
from os import path
from sys import argv
from glob import glob
from random import shuffle
import pandas as pd
from math import radians, sin, cos
from matplotlib.colors import LogNorm, PowerNorm, SymLogNorm
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors
from matplotlib.transforms import Bbox
from collections import Counter, OrderedDict
import SplatStats as splat


if splat.isNotebook():
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = (
        'All', 'All Modes', 'False', 'True', '500'
    )
else:
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = argv[1:]
dpi = int(DPI)
overwrite = (True if OVERWRITE=="True"  else False)
titles = (True if TITLES=="True"  else False)
prepFnme = ('' if titles else 'Untitled_')
###############################################################################
# Constants
###############################################################################
GMODES = {'Clam Blitz', 'Splat Zones', 'Tower Control', 'Turf War', 'Rainmaker'}
if GMODE in GMODES:
    POLAR = {
        'fontSizes': (12, 10), 'ticksStep': 1,
        'yRange': (0, 75e3), 'rRange': (0, 90)
    }
    PART_SCALER = ['k', 1e3]
    TITLES = True
else:
    POLAR = {
        'fontSizes': (12, 3.75), 'ticksStep': 4,
        'yRange': (0, 300e3), 'rRange': (0, 180),
        'topRank': None
    }
    PART_SCALER = ['M', 1e6]
    TITLES = True
###############################################################################
# Get files and set font
###############################################################################
if splat.isNotebook():
    DATA_PATH = '/Users/chipdelmal/Documents/BattlesDocker/'
    splat.setSplatoonFont(DATA_PATH, fontName="Splatfont 2")
else:
    DATA_PATH = '/data/'
    splat.setSplatoonFont('/other/', fontName="Splatfont 2")
FPATHS = glob(path.join(DATA_PATH, 'battle-results-csv', '*-*-*.csv'))
COLORS = splat.ALL_COLORS
shuffle(COLORS)
###############################################################################
# Parse and Filter Data Object
###############################################################################
statInk = splat.StatInk(path.join(DATA_PATH, 'battle-results-csv'))
btls = statInk.battlesResults
try:
    six = list(set(btls['season'])).index(SEASON)
    FREQ_SCALER = 1
except:
    six = -1
    SEASON = 'All Seasons'
    FREQ_SCALER = 4
POLAR['yRange'] = (POLAR['yRange'][0], POLAR['yRange'][1]*FREQ_SCALER)
FNSTR = '{} ({}) - '.format(SEASON, GMODE)
if SEASON!='All Seasons':
    if GMODE in GMODES:
        fltrs = (btls['season']==SEASON, btls['mode']==GMODE)
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsFiltered = btls[fltrBool]
    else:
        GMODE = 'All'
        fltrs = (btls['season']==SEASON, )
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsFiltered = btls[fltrBool]
else:
    if GMODE in GMODES:
        fltrs = (btls['mode']==GMODE, )
        fltrBool = [all(i) for i in zip(*fltrs)]
        btlsFiltered = btls[fltrBool]
    else:
        btlsFiltered = btls
# Add 'day' to dataset for filtering ------------------------------------------
dfBtls = btlsFiltered.copy()
dfBtls['day'] = dfBtls['period'].dt.floor('d')
UNIQUE_DAYS = sorted(dfBtls['day'].unique())
###############################################################################
# Aggregate
###############################################################################       
LABELS = ('kill', 'kill-assist', 'assist', 'death', 'inked')
PLAYERS = ('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')
IDS = [f'{p}-weapon' for p in PLAYERS]
# Count weapons everyday ------------------------------------------------------
(ctsDict, fullCtr, wpnsSet) = (OrderedDict(), Counter(), set())
for day in UNIQUE_DAYS:
    dayBtls = dfBtls[dfBtls['day']==day]
    dayCtrs = [Counter(dayBtls[p]) for p in IDS]
    dayWpns = sum(dayCtrs, Counter())
    fullCtr = sum([fullCtr, dayWpns], Counter())
    ctsDict[day] = dayWpns
    wpnsSet.update(set(dayWpns.keys()))
(WPNS_FREQ, WPNS_TOTAL, WPNS_LIST) = (ctsDict, fullCtr, sorted(list(wpnsSet)))
###############################################################################
# Assemble dataframe
###############################################################################  
WPNS_FREQ_DF = pd.DataFrame.from_records(
    list(WPNS_FREQ.values()), columns=WPNS_LIST, index=UNIQUE_DAYS
).fillna(0).astype(int)
###############################################################################
# Get Splatfest
###############################################################################  
(seasons, versions) = (
    list(dfBtls['season'].unique()),
    sorted(list(dfBtls['game-ver'].unique()))
)
(SEASONS_START, VERSIONS_START) = (
    {s: min(dfBtls[dfBtls['season']==s]['day']) for s in seasons},
    {s: min(dfBtls[dfBtls['game-ver']==s]['day']) for s in versions}
)
SPLATFEST_DAYS = sorted(list(
    dfBtls[
        (dfBtls['lobby']=='Splatfest (Open)') |
        (dfBtls['lobby']=='Splatfest (Pro)')
    ]['day'].unique()
))
###############################################################################
# Get Splatfest
############################################################################### 
(xStep, xDelta) = (1, 0)
(yStep, yDelta) = (1, 0.5)
SAT_CATS = [
    '#8338ec', '#ff006e', '#3a86ff', '#f15bb5', '#6BFF00',
]
NORM = colors.SymLogNorm(linthresh=.50e3, vmin=0, vmax=17.5e3)
MAPS = [
    splat.colorPaletteFromHexList(['#000000', c, '#ffffff']) 
    for c in SAT_CATS
]
# Get weapons sorting ---------------------------------------------------------
wpns = [i[0] for i in WPNS_TOTAL.most_common()][::-1]
# wpns = WPNS_FREQ_DF.columns[::-1]
days = list(WPNS_FREQ_DF.index.values)
# Map dates to columns --------------------------------------------------------
seasons_column = [
    (days.index(SEASONS_START[k].to_numpy()), k) 
    for k in SEASONS_START.keys()
]
version_column = [
    (days.index(VERSIONS_START[k].to_numpy()), k) 
    for k in VERSIONS_START.keys()
]
fest_column = [
    days.index(d.to_numpy())
    for d in SPLATFEST_DAYS
]
# Plot frequency --------------------------------------------------------------
(fig, ax) = plt.subplots(figsize=(30, 30))
ax1 = ax.twinx()
for (row, wpn) in enumerate(wpns):
    wpnName = wpns[row]
    wpnCount = WPNS_FREQ_DF[wpnName].values
    # with mpl.rc_context({'path.sketch': (2, 0.1, 100)}):
    for day in range(0, len(days)):
        ax.plot(
            (day*xStep, day*xStep+xDelta), 
            (row*yStep, row*yStep+yDelta), 
            color=MAPS[row%len(MAPS)](NORM(wpnCount[day]))
        )
ax.vlines(
    [i[0] for i in version_column], 
    0-.5, len(wpns)-.5, 
    color='#ffffff44', ls=':', lw=0.5,
    zorder=2,
    # transform=ax.get_xaxis_transform()
)
ax.vlines(
    [i[0] for i in seasons_column], 
    0-.5, len(wpns)+1, 
    color='#ffffff44', ls=':', lw=0.5,
    zorder=2,
    # transform=ax.get_xaxis_transform()
)
ax.vlines(
    [i[0] for i in seasons_column], 
    len(wpns), len(wpns)+10, 
    color='#ffffffCC', ls='-', lw=5,
    zorder=4,
    # transform=ax.get_xaxis_transform()
)
# ax.vlines(
#     fest_column, 0-.25, -1, 
#     color='#ffffff66', ls='-', lw=2,
#     zorder=5,
#     # transform=ax.get_xaxis_transform()
# )
ax.vlines(
    fest_column, len(wpns), len(wpns)+1, 
    color='#ffffff66', ls='-', lw=2,
    zorder=5,
    # transform=ax.get_xaxis_transform()
)
sSeasons = sorted(seasons_column)
for (ix, (i, t)) in enumerate(sSeasons):
    if ix<(len(seasons_column)-1):
        ax.text(
            (i+sSeasons[ix+1][0])/2, len(wpns)+2, 
            t.replace("Season", ""), 
            rotation=0, ha='center', va='bottom',
            fontsize=25, color='#ffffff', 
            zorder=5
        )
# Axes ------------------------------------------------------------------------
ax.set_xlim(-1, len(days)+1)
ax.set_ylim(-1, len(wpns)+2)
ax.set_yticks([i+yDelta/2 for i in range(0, len(wpns))])
ax.set_yticklabels(wpns, fontsize=10, color='#ffffff')
ax1.set_ylim(ax.get_ylim())
ax1.set_yticks([i+yDelta/2 for i in range(0, len(wpns))])
ax1.set_yticklabels(wpns, fontsize=10, color='#ffffff')
ax.set_facecolor('#000000')
plt.figure(facecolor="#000000")
fig.patch.set_facecolor("#000000")
[s.set_visible(False) for s in ax.spines.values()]
[t.set_visible(False) for t in ax.get_xticklines()]
[t.set_visible(False) for t in ax.get_yticklines()]

# Export ----------------------------------------------------------------------
fName = f'WeaponUsage.png'
fig.savefig(
    path.join(DATA_PATH, 'inkstats/'+fName), 
    dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor()
)