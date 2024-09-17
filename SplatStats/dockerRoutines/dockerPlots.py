#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os    
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
from os import path
from sys import argv
import SplatStats as splat
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


if splat.isNotebook():
    (plyrName, weapon, mode, overwrite) = ('čħîþ ウナギ', 'All', 'All', 'False')
    (iPath, bPath, oPath) = (
        path.expanduser('/Users/chipdelmal/Documents/BattlesDocker/jsons'),
        path.expanduser('/Users/chipdelmal/Documents/BattlesDocker/battles'),
        path.expanduser('/Users/chipdelmal/Documents/BattlesDocker/out')
    )
    fontPath = '/Users/chipdelmal/Documents/GitHub/SplatStats/other/'
else:
    (plyrName, weapon, mode, overwrite) = argv[1:]
    (iPath, bPath, oPath) = (
        '/data/jsons', 
        '/data/battles', 
        '/data/out'
    )
    fontPath = '/other/'
overwrite = (True if overwrite=="True"  else False)
LEN_LIMIT = 400
###############################################################################
# Auxiliary 
###############################################################################
title = '(Kills+0.5*Assists)/Deaths'
fNameID = f'{plyrName}-{weapon}'
splat.setSplatoonFont(fontPath, fontName="Splatfont 2")
###############################################################################
# Process JSON files into battle objects
###############################################################################
hFilepaths = splat.getDataFilepaths(iPath, filePat='results.json')
bPaths = splat.dumpBattlesFromJSONS(hFilepaths, bPath, overwrite=overwrite)
bFilepaths = splat.getBattleFilepaths(bPath)
###############################################################################
# Create Player Object
###############################################################################
plyr = splat.Player(plyrName, bFilepaths, timezone='America/Los_Angeles')
playerHistory = plyr.battlesHistory
playerHistory = playerHistory[playerHistory['match mode']!='PRIVATE']
# Weapon filter ---------------------------------------------------------------
if weapon!='All':
    playerHistory = playerHistory[playerHistory['main weapon']==weapon]
else:
    playerHistory = playerHistory
# playerHistory = playerHistory.iloc[:5000]
###############################################################################
# Timecard
###############################################################################
if weapon=='All':
    TCARD_STAT = 'duration'
    try:
        tCard = splat.getTimecard(playerHistory)[TCARD_STAT]
    except:
        pass
    wpnSorting = tCard.sum(axis=1).sort_values(ascending=False)
    wpnsNumber = len(wpnSorting)
    fontSize = np.interp(wpnsNumber, [1, 10, 30, 50], [30, 20, 14, 5])
    (fig, ax) = splat.plotTimecard(
        tCard, wpnSorting, 
        fontSize=fontSize, 
        fmtStr='  {} ({:.0f})', statScaler=60,
        highColors=['#DE0B64AA', '#311AA8AA', '#6BFF00AA', '#9030FFAA', '#B62EA7AA']
    )
    fig.savefig(
        path.join(oPath, f'{fNameID}_Timecard-Duration.png'), 
        dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
###############################################################################
#  Circle Barchart Kills
###############################################################################
if weapon=='All':
    killsTotal = playerHistory['kassist'].sum()
    wColors = [
        '#C70864', '#6BFF00', '#4F55ED', '#B14A8D', 
        '#D645C8', '#830B9C', '#C6D314', '#0D37C3', 
        '#F52E71', '#571DB1', '#14BBE7', '#38377A',
    ][::]
    wColors = [i+'BB' for i in wColors]
    wColors = wColors*50
    (fig, ax) = splat.plotCircularBarchartStat(
        playerHistory, cat='main weapon', stat='kassist', aggFun=np.sum,
        colors=wColors, # yRange=(0, 10e3), 
        logScale=True, ticksStep=10,
        ticksFmt={
            'lw': 1, 'range': (-0.5, -0.25), 
            'color': '#000000DD', 'fontsize': 6, 'fmt': '{:.0f}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 4, 
            'ha': 'left', 'fmt': '{:.1f}'
        }
    )
    ax.set_title(f'(Kills+0.5*Assists) = {killsTotal}\n', fontsize=18)
    fig.savefig(
        path.join(oPath, f'{fNameID}_Polar-Kill.png'), 
        dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
###############################################################################
#  Circle Barchart Wins
###############################################################################
if weapon=='All':
    winsTotal = playerHistory['winBool'].sum()
    (fig, ax) = splat.plotCircularBarchartStat(
        playerHistory, cat='main weapon', stat='winBool', aggFun=np.sum,
        colors=wColors, # yRange=(0, 10e3), 
        logScale=True, ticksStep=10,
        ticksFmt={
            'lw': 1, 'range': (-0.5, -0.25), 
            'color': '#000000DD', 'fontsize': 6, 'fmt': '{:.0f}'
        },
        labelFmt={
            'color': '#000000EE', 'fontsize': 4, 
            'ha': 'left', 'fmt': '{:.1f}'
        }
    )
    ax.set_title(f'Wins = {winsTotal}\n', fontsize=18)
    fig.savefig(
        path.join(oPath, f'{fNameID}_Polar-Win.png'), 
        dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
###############################################################################
# Win Ratio
###############################################################################
winsTotal = playerHistory['winBool'].sum()
matchesTotal = playerHistory.shape[0]
winRatio = winsTotal/matchesTotal*100
(metric, aggMetrics) = ('win ratio', ('win', 'total matches'))
df = splat.calcStagesStatsByType(playerHistory)
dfFlat = splat.ammendStagesStatsByType(df, matchModes=list(df.keys()))
dfFlat.sort_values('match type', inplace=True)
g = splat.plotMatchTypeBars(
    dfFlat, metric, aggMetrics, digs=4,
    yRange=(0, 1), countsLegend={'color': '#00000077', 'fontsize': 4},
    textOffset=0.005, alpha=.98, fontsize=5
)
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle(f'Wins = {winRatio:.0f}% ({winsTotal}/{matchesTotal})\n', fontsize=18)
g.savefig(
    path.join(oPath, f'{fNameID}_Bars-Win.png'), 
    dpi=250, bbox_inches='tight'
)
plt.close(g.fig)
###############################################################################
# Kill Ratio
###############################################################################
kassistTotal = np.sum(playerHistory['kassist'])/np.sum(playerHistory['death'])
(metric, aggMetrics) = ('kassists ratio', ('kassists', 'deaths'))
g = splat.plotMatchTypeBars(
    dfFlat, metric, aggMetrics, yRange=(0, 4), digs=4,
    countsLegend={'color': '#00000077', 'fontsize': 4},
    percentage=False, textOffset=0.005, alpha=0.98, fontsize=5
)
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle(f'{title} = {kassistTotal:.4f}\n', fontsize=18)
g.savefig(
    path.join(oPath, f'{fNameID}_Bars-Kill.png'), 
    dpi=250, bbox_inches='tight'
)
plt.close(g.fig)
###############################################################################
# Waffle
###############################################################################
if weapon=='All':
    (fig, ax) = plt.subplots(figsize=(10, 10))
    (fig, ax) = splat.plotWaffleStat(
        (fig, ax), playerHistory,
        function=sum, grouping='main weapon', stat='kassist',
        rows=75, columns=75, vertical=True,
        colors=splat.ALL_COLORS,
        alpha=0.65
    )
    ax.set_title(f'(Kills+0.5*Assists) = {killsTotal}\n', fontsize=18)
    fig.savefig(
        path.join(oPath, f'{fNameID}_Waffle-Kill.png'), 
        dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
    )
    plt.close()
###############################################################################
# Histogram
###############################################################################
(fig, ax) = plt.subplots(figsize=(10, 3))
(fig, ax) = splat.plotKillsAndDeathsHistogram(
    (fig, ax), playerHistory, (0, 35), 
    yRange=(-.5, .5), edgecolor='k',
    alpha=0.85,
    normalized=True
)
ax.relim()
ax.autoscale()
(ymin, ymax) = ax.get_ylim()
mxLim = max([abs(ymin), ymax])
ax.set_ylim(-mxLim, mxLim)
ax.set_xlim(0, 35)
ax.set_aspect(.25/ax.get_data_ratio())
plt.savefig(
    path.join(oPath, f'{fNameID}_Histogram-Kill.png'),  
    dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Awards
###############################################################################
if weapon=='All':
    try:
        wColors = [
            '#C70864', '#6BFF00', '#4F55ED', '#B14A8D', 
            '#D645C8', '#830B9C', '#C6D314', '#0D37C3', 
            '#F52E71', '#571DB1', '#14BBE7', '#38377A',
        ][::]
        wColors = [i+'BB' for i in wColors]
        wColors = wColors*50
        awds = plyr.getAwardFrequencies()
        (fig, ax) = splat.polarBarChart(
            [i[0] for i in awds[::-1]], 
            [i[1] for i in awds[::-1]],
            labelFmt={
                'color': '#000000EE', 'fontsize': 6, 
                'ha': 'left', 'fmt': '{:.1f}'
            },
            colors=wColors
        )
        ax.set_title(f'Awards\n', fontsize=18)
        fig.savefig(
            path.join(oPath, f'{fNameID}_Awards.png'), 
            dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
        )
        plt.close()
    except:
        pass
###############################################################################
# Battle History
###############################################################################
phLen = playerHistory.shape[0]
if phLen > LEN_LIMIT:
    ilocRange = (-LEN_LIMIT, phLen)
else:
    ilocRange = (0, -1)
yRange = ((0, 40), (0, 2000))
fig = plt.figure(figsize=(30, 5))
gs = fig.add_gridspec(
    2, 1,  
    width_ratios=(1, ), height_ratios=(.75, .05),
    left=0.1, right=0.9, bottom=0.1, top=0.9,
    wspace=0.05, hspace=0
)
ax_top    = fig.add_subplot(gs[0])
ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)
(_, ax_top) = splat.plotMatchHistory(
    (fig, ax_top), playerHistory, 
    yRange=yRange, sizeMultiplier=.8, ilocRange=ilocRange
)
(_, ax_bottom) = splat.plotMatchTypeHistory(
    (fig, ax_bottom), playerHistory, 
    sizeMultiplier=.5, labelsize=4, ilocRange=ilocRange
)
ax_top.tick_params(labelbottom=False)
ax_bottom.set_yticks([])
plt.setp(ax_bottom.get_xticklabels(), rotation=90, ha='right')
plt.savefig(
    path.join(oPath, f'{fNameID}_History.png'), 
    dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Ranks
###############################################################################
cats = ['kill', 'death', 'assist', 'paint']
ranksNum = 4
dfRank = plyr.getPlayerAlliedRanking(cats=cats)
(fig, ax) = splat.polarBarRanks(dfRank, ranksNum)
for x in ax:
    x.set_ylim(-ranksNum/ranksNum, ranksNum)
fig.suptitle(f'Team Ranking Frequency\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_RanksAllied.png'), 
    dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
# Full Rank ---------------------------------------------------------------
ranksNum = 8
dfRank = plyr.getPlayerFullRanking(cats=cats)
(fig, ax) = splat.polarBarRanks(
    dfRank, ranksNum, yRange=(0, .5), ticksStep=5
)
for x in ax:
    x.set_ylim(-ranksNum/ranksNum, ranksNum)
fig.suptitle(f'Overall Ranking Frequency\n', fontsize=18)
fig.savefig(
    path.join(oPath, f'{fNameID}_RanksFull.png'), 
    dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Player History Iris
###############################################################################
(kaZero, kZero, dZero) = (
    playerHistory[(playerHistory['kill']+playerHistory['assist'])==0].shape[0],
    playerHistory[(playerHistory['kill'])==0].shape[0],
    playerHistory[(playerHistory['death'])==0].shape[0],
)
(kaMax, kMax, daMax, dMax) = (
    max((playerHistory['kill']+playerHistory['assist'])-(playerHistory['death'])),
    max((playerHistory['kill'])-(playerHistory['death'])),
    abs(min((playerHistory['kill']+playerHistory['assist'])-(playerHistory['death']))),
    abs(min((playerHistory['kill'])-(playerHistory['death'])))
)
tMatches = playerHistory.shape[0]
AMODES = {'Clam Blitz', 'Rainmaker', 'Splat Zones', 'Tower Control'}
koSS = [list(playerHistory['match type'].isin(AMODES)), ]
koST = np.sum([all(i) for i in zip(*koSS)])
(koWS, koLS) = (
    [list(playerHistory['ko']), list(playerHistory['match type'].isin(AMODES)), list(playerHistory['win']=='W')],
    [list(playerHistory['ko']), list(playerHistory['match type'].isin(AMODES)), list(playerHistory['win']=='L')],
)
(koWT, koLT) = [np.sum([all(i) for i in zip(*j)]) for j in (koWS, koLS)]
# Plot ------------------------------------------------------------------------
(fontSize, fontColor) = (8, "#000000CC")
lw = np.interp(
    playerHistory.shape[0], 
    [0, 50,  100,  250,  500, 1000, 3000,   5000], 
    [10, 3,    3,    2,  1.5,  0.8, 0.25,  0.125]
)
(fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
((fig, ax), kdRatio) = splat.plotIrisKDP(playerHistory, (fig, ax), lw=lw)
(fig, ax) = splat.plotIrisMatch(playerHistory, (fig, ax), typeLineLength=10, lw=lw)
((fig, ax), statQNT, statMNS) = splat.plotIrisStats(playerHistory, (fig, ax))
(fig, ax) = splat.plotIrisAxes((fig, ax), yRange=(0, 65))
# Add inner text ----------------------------------------------------------
(kill, death, assist, paint, special, win) = [
    splat.statSummaries(playerHistory, stat, summaryFuns=(np.sum, np.mean)) 
    for stat in ('kill', 'death', 'assist', 'paint', 'special', 'winBool')
]
(sw, sl) = (splat.longestRun(playerHistory['win'], elem='W'), splat.longestRun(playerHistory['win'], elem='L'))
strLng = 'Matches: {}\nWin: {} ({:.0f}%)\n(K+0.5A)/D: {:.2f}\n\n\n\n\n\n\nKill: {} ({:.1f})\nDeath: {} ({:.1f})\nAssist: {} ({:.1f})\nSpecial: {} ({:.1f})\nPaint: {} ({:.0f})'
innerText = strLng.format(
    playerHistory.shape[0], win[0], win[1]*100, 
    kdRatio,
    kill[0], kill[1], 
    death[0], death[1],
    assist[0], assist[1], 
    special[0], special[1],
    paint[0], paint[1],
    
)
ax.text(
    x=0.5, y=0.5, 
    s=innerText, fontsize=fontSize,
    va="center", ha="center",  ma="center", 
    color=fontColor, transform=ax.transAxes
)
wpnStr = '{}'.format(weapon) if weapon!='All' else 'All Weapons'
ax.text(
    x=0.5, y=0.525,
    s='{}'.format(plyrName),
    fontsize=fontSize+7.5,
    va="center", ha="center",
    color=fontColor, transform=ax.transAxes
)
ax.text(
    x=0.5, y=0.4975,
    s=wpnStr,
    fontsize=fontSize+2,
    va="center", ha="center",
    color=fontColor, transform=ax.transAxes
)
extStats = 'KOs: W {} ({:.0f}%) | L {} ({:.0f}%)\nStreaks: W {} | L {}\nMax Spread: KA/D {:.0f} | D/KA {:.0f}\nZero: D {:0.2f}% ({:.0f}) | K {:0.2f}% ({:.0f}) | KA {:0.2f}% ({:.0f})'.format(
    koWT, koWT/koST*100, koLT, koLT/koST*100,
    sw, sl,
    kaMax, daMax,
    dZero/tMatches*100, dZero,
    kZero/tMatches*100, kZero,
    kaZero/tMatches*100, kaZero
)
ax.text(
    x=0, y=0.025,
    s=extStats,
    fontsize=fontSize-3,
    va="center", ha="left",
    color=fontColor, transform=ax.transAxes
)
# Save -------------------------------------------------------------------
fig.savefig(
    path.join(oPath, f'{fNameID}_HistoryIris.png'), 
    dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor()
)
plt.close()
###############################################################################
# Player History to Disk
###############################################################################
# time.sleep(2)
playerHistory.to_csv(path.join(oPath, f'{fNameID}.csv'))
