# !/usr/bin/env python3

import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
from os import path
from sys import argv
from glob import glob
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import SplatStats as splat

SSON = [
    'Drizzle Season 2022', 'Chill Season 2022', ' Fresh 2022', 'Sizzle Season 2022',
    'Drizzle Season 2023', 'Chill Season 2023', ' Fresh 2023', 'Sizzle Season 2023',
    'Drizzle Season 2024', 'Chill Season 2024', 'Fresh Season 2024', 'Sizzle Season 2024',
    'All Seasons'
]
GMOD = [
    'All Modes', 'Turf War', 
    'Clam Blitz', 'Splat Zones', 'Tower Control', 'Rainmaker'
]

if splat.isNotebook():
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = (
        'All Seasons', 'All Modes', 'True', 'True', '500'
    )
else:
    (SEASON, GMODE, TITLES, OVERWRITE, DPI) = argv[1:]

dpi = int(DPI)
overwrite = (True if OVERWRITE=="True"  else False)
titles = (True if TITLES=="True"  else False)
prepFnme = ('' if titles else 'Untitled_')
GMODES = {'Clam Blitz', 'Splat Zones', 'Tower Control', 'Turf War', 'Rainmaker'}
# (SEASON, GMOD) = ('All Seasons', 'All Modes') 
for SEASON in SSON[::-1]:
    for GMODE in GMOD:
        print(f'{SEASON}: {GMODE}')
        ###############################################################################
        # Constants
        ###############################################################################
        if GMODE in GMODES:
            POLAR = {
                'fontSizes': (12, 10), 'ticksStep': 1,
                'yRange': (0, 100e3), 'rRange': (0, 90)
            }
            PART_SCALER = ['k', 1e3]
            TITLES = True
        else:
            POLAR = {
                'fontSizes': (12, 5), 'ticksStep': 4,
                'yRange': (0, 400e3), 'rRange': (0, 90),
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
        # Parse Data Object
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
                GMODE = 'All Modes'
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
        (mNames, mMatrix) = splat.calculateDominanceMatrix(btlsFiltered)
        (sNames, sMatrix, sSort) = splat.normalizeDominanceMatrix(mNames, mMatrix)
        # Calculate auxiliary metrics -------------------------------------------------
        wpnRank = splat.rankWeaponsFrequency(wpnFreq, wpnWLT)
        (mWpnWins, mWpnLoss) = (
            np.sum(mMatrix, axis=1)/4, 
            np.sum(mMatrix, axis=0)/4
        )
        period = (min(btlsFiltered['period']), max(btlsFiltered['period']))
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
        # Get Frequencies for Strips
        ###############################################################################
        dfStats = splat.getWeaponsDataframe(btlsFiltered)
        weapons = sorted(list(dfStats['weapon'].unique()))
        dfStats['kassist'] = dfStats['kill']+dfStats['assist']/2
        dfStats['paint'] = dfStats['inked']/100
        wpnStats = ['kill', 'death', 'assist', 'special', 'paint']
        wpnHists = splat.getWeaponsStatsHistograms(
            dfStats, weapons, (0, 30), binSize=1, stats=wpnStats
        )
        wpnMeans = splat.getWeaponsStatsSummary(
            dfStats, weapons, summaryFunction=np.mean, stats=wpnStats
        )
        ###########################################################################
        # Weapon Matrix
        ###########################################################################
        fName = FNSTR+prepFnme+'Matrix.png'
        # COLS = splat.SEASON_COLORS
        # cPal = splat.colorPaletteFromHexList(
        #     [COLS[six][0]+'FF', '#ffffff00', COLS[six][1]+'FF']
        # )
        COLS = [
            '#4361ee', '#9030FF', '#B62EA7', 
            '#ff006e', '#fb8b24', '#80ed99'
        ]*100
        # cPal = splat.colorPaletteFromHexList(
        #     [COLS[six]+'FF', COLS[3]+'AA', '#000000', '#000000', '#000000']
        # )
        cPal = splat.colorPaletteFromHexList(
            [
                splat.SEASON_COLORS[six][0], # splat.SEASON_COLORS[six][0],
                '#00000000', 
                splat.SEASON_COLORS[six][1], # splat.SEASON_COLORS[six][1]
            ]
        )
        (fig, ax) = plt.subplots(figsize=(20, 20), facecolor='#ffffff')
        ax.set_facecolor('#ffffff')
        (fig, ax) = splat.plotDominanceMatrix(
            sNames, sMatrix, sSort, mMatrix,
            figAx=(fig, ax), vRange=(-.6, .6), # cmap=cPal,
            fontSize=8
        )
        plt.tick_params(
            axis='x', which='both',
            bottom=False, top=True, labelbottom=False
        )
        if titles:
            ax.set_title(
                '{}\n{} matches from {} to {}'.format(
                    f'{SEASON} ({GMODE})', btlsFiltered.shape[0],
                    period[0].strftime("%b %d %Y"), 
                    period[1].strftime("%b %d %Y")
                )
                , fontsize=35, y=-.085, color='#000000'
            )
            (transp, fc) = (False, '#ffffff')
        else:
            ax.set_title(
                'Matches: {}'.format(btlsFiltered.shape[0])
                , fontsize=35, y=-.045
            )
            (transp, fc) = (True, '#ffffff')
        ax.tick_params(axis='x', colors='#000000')
        ax.tick_params(axis='y', colors='#000000')
        plt.savefig(
            path.join(DATA_PATH, 'inkstats/'+fName),
            dpi=dpi, transparent=False, facecolor=fc, bbox_inches='tight'
        )
        plt.close('all')
        ###############################################################################
        # Plot Total Frequencies
        ###############################################################################
        fName = FNSTR+prepFnme+'Polar.png'
        if GMODE in GMODES:
            POLAR['topRank'] = (len(wpnRank)-50, len(wpnRank))
        if titles:
            POLAR['ticksStep'] = 4
        (fig, ax) = plt.subplots(
            figsize=(12, 12), subplot_kw={"projection": "polar"}, 
            facecolor='#000000'
        )
        ax.set_facecolor('#000000')
        ax.set_thetamin(POLAR['rRange'][0])
        ax.set_thetamax(POLAR['rRange'][1])
        (fig, ax) = splat.plotPolarFrequencies(
            wpnFreq, wpnRank, figAx=(fig, ax),
            fontSizes=POLAR['fontSizes'], 
            fontColors=('#ffffff', '#ffffff'),
            ticksStep=POLAR['ticksStep'],
            yRange=POLAR['yRange'], rRange=POLAR['rRange'],
            topRank=POLAR['topRank'],
            logScale=False
            # colors=[
            #     '#DE0B64', '#311AA8', '#9030FF', '#B62EA7', '#6BFF00'
            # ]*100
        )
        partp = np.sum(list(wpnFreq.values()))
        fstr = 'Participation: {:.2f}{}'.format(partp/PART_SCALER[1], PART_SCALER[0])
        if titles:
            ax.text(
                0.45, 0, f'{SEASON} ({GMODE})\n{fstr}', 
                fontsize=25, 
                horizontalalignment='center',
                verticalalignment='top',
                rotation=0,
                transform=ax.transAxes,
                color='#ffffff'
            )
        else:
            ax.text(
                0.45, 0, fstr,
                fontsize=20,
                horizontalalignment='center',
                verticalalignment='top',
                rotation=0,
                transform=ax.transAxes,
                color='#ffffff'
            )
        plt.savefig(
            path.join(DATA_PATH, 'inkstats/'+fName),
            dpi=dpi, transparent=False, facecolor='#000000', bbox_inches='tight'
        )
        plt.close('all')
        # ###############################################################################
        # # Gaussian Lobby
        # ###############################################################################
        # YLIM = (0, -1500)
        # if SEASON=='All Seasons':
        #     YLIM = (0, -7500)
        # if GMODE not in GMODES:
        #     fName = FNSTR+prepFnme+'Mode.png'
        #     (fig, ax) = (plt.figure(figsize=(20, 3)), plt.axes())
        #     (fig, ax) = splat.plotGaussianLobby(
        #         lbyDaily, lbyGaussDaily, figAx=(fig, ax), ylim=YLIM
        #     )
        #     ax.set_ylim(*YLIM)
        #     ax.set_ylim(ax.get_ylim()[::-1])
        #     if titles:
        #         ax.legend(loc='lower left', frameon=False, fancybox=False, fontsize=12)
        #     plt.savefig(
        #         path.join(DATA_PATH, 'inkstats/'+fName),
        #         dpi=dpi, transparent=False, facecolor='#ffffff', bbox_inches='tight'
        #     )
        #     plt.close('all')
        # ###############################################################################
        # # Lobby Type
        # ###############################################################################
        # if GMODE not in GMODES:
        #     fName = FNSTR+prepFnme+'Lobby.png'
        #     (fig, ax) = plt.subplots(figsize=(0.4, 20))
        #     (fig, ax) = splat.barChartLobby(lbyFreq)
        #     plt.savefig(
        #         path.join(DATA_PATH, 'inkstats/'+fName), dpi=dpi, 
        #         transparent=False, facecolor='#ffffff', bbox_inches='tight'
        #     )
        #     plt.close('all')
        ###############################################################################
        # Weapons Strips
        ###############################################################################
        INKSTATS_STYLE = {
            'kill': {
                'color': '#4361eeee', 'range': (0, 15),
                'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .625, 0.95]),
                'range': (0, 15)
            },
            'death': {
                'color': '#801AB3ee', 'range': (0, 15),
                'scaler': lambda x: np.interp(x, [0, 0.125, 0.25], [0, .625, 0.95]),
                'range': (0, 15)
            },
            'assist': {
                'color': '#C12D74ee', 'range': (0, 10),
                'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .625, 0.95]),
                
            },
            'special': {
                'color': '#4ad66dee', 'range': (0, 10),
                'scaler': lambda x: np.interp(x, [0, 0.25, 0.65], [0, .625, 0.95]),
            },
            'paint': {
                'color': '#b8c0ffee', 'range': (0, 20),
                'scaler': lambda x: np.interp(x, [0, 0.1, 0.2], [0, .625, 0.95]),
            }
        }
        # (fig, axs) = plt.subplots(1, 5, figsize=(5*5, 20), sharey=True)
        fName = FNSTR+prepFnme+'Strips.png'
        fig = plt.figure(figsize=(15, 20), facecolor='#000000')
        gs = fig.add_gridspec(1, 5, hspace=1, wspace=0.05)
        axs = gs.subplots()# sharex='col', sharey='row')
        for (ix, stat) in enumerate(wpnStats):
            axs[ix].set_facecolor('#000000')
            statPars = INKSTATS_STYLE[stat]
            (_, ax) = splat.plotWeaponsStrips(
                wpnHists, weapons, stat,
                figAx=(fig, axs[ix]),
                weaponsSummary=wpnMeans,
                color=statPars['color'], range=statPars['range'],
                cScaler=statPars['scaler'],
                edgecolor='#ffffff22',
                statcolor='#ffffff'
            )
            axs[ix].xaxis.set_tick_params(labelsize=10)
            axs[ix].yaxis.set_tick_params(labelsize=10)
            axs[ix].yaxis.set_ticks_position('both')
            for ax in axs:
                ax.tick_params(color='#ffffff', labelcolor='#ffffff')
                ax.set_title(ax.get_title(), color='#ffffff', fontsize=20)
                for spine in ax.spines.values():
                    spine.set_edgecolor('#ffffff')
            if (ix==0):
                lbs = [i.get_text() for i in axs[0].get_yticklabels()]
                axs[ix].set_yticklabels(lbs, color='#ffffff', fontsize=9)
                lbs = [int(i.get_text()) for i in axs[ix].get_xticklabels()]
                axs[ix].set_xticklabels(lbs, color='#ffffff')
            if (ix>0) and (ix<len(wpnStats)-1):
                axs[ix].set_yticklabels([])
                lbs = [int(i.get_text()) for i in axs[ix].get_xticklabels()]
                axs[ix].set_xticklabels(lbs, color='#ffffff')
            if ix == (len(wpnStats)-1):
                axs[ix].yaxis.tick_right()
                lbs = [i.get_text() for i in axs[0].get_yticklabels()]
                axs[ix].set_yticklabels(lbs, color='#ffffff', fontsize=9)
                lbs = [int(i.get_text())*100 for i in axs[ix].get_xticklabels()]
                axs[ix].set_xticklabels(lbs, color='#ffffff')
                axs[ix].yaxis.set_ticks_position('both')
        if titles:
            axs[2].text(
                0.5, 1.025, f'{SEASON} ({GMODE})',
                ha='center', va='bottom', 
                transform=axs[2].transAxes, fontsize=35,
                color='#ffffff'
            )
        plt.savefig(
            path.join(DATA_PATH, 'inkstats/'+fName), dpi=dpi, 
            transparent=False, facecolor='#000000', bbox_inches='tight'
        )
        plt.close('all')




# ###############################################################################
# # Bumpchart
# ###############################################################################
# ssn = 'Drizzle Season 2023'
# freqSSN = {}
# key = 'game-ver'
# for ssn in sorted(btls[key].unique()):
#     if GMODE in GMODES:
#         fltrs = (btls[key]==ssn, btls['mode']==GMODE)
#         fltrBool = [all(i) for i in zip(*fltrs)]
#         btlsFiltered = btls[fltrBool]
#     else:
#         fltrs = (btls[key]==ssn, )
#         fltrBool = [all(i) for i in zip(*fltrs)]
#         btlsFiltered = btls[fltrBool]
#     freq = splat.getWeaponsFrequencies(btlsFiltered)
#     freqSSN[ssn] = freq
# freqSSN

# btls[['game-ver', 'period']]