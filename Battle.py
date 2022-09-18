#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import parsers as par
import auxiliary as aux

class Battle:
    """
    Attributes
    ----------
    alliedTeam : dataframe
        breakdown of my team
    enemyTeams : list of dataframes
        breakdown of the enemy teams

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, battleDetail):
        #######################################################################
        # Get allied team details
        #######################################################################
        myTeam = battleDetail['myTeam']
        # Get players details -------------------------------------------------
        players = myTeam['players']
        playersInfo = par.getPlayersBattleInfo(players)
        # Add W/L column ------------------------------------------------------
        win = aux.boolWinLose(myTeam['judgement'])
        # Assign dataframe ----------------------------------------------------
        alliedDF = pd.DataFrame.from_dict(playersInfo)
        alliedDF['Win'] = win
        self.alliedTeam = alliedDF
        #######################################################################
        # Get enemy teams details
        #######################################################################
        enemyTeams = []
        for i in range(len(battleDetail['otherTeams'])):
            eTeam = battleDetail['otherTeams'][i]
            ePlayers = eTeam['players']
            enemiesInfo = par.getPlayersBattleInfo(ePlayers)
            enemyTeams.append(pd.DataFrame.from_dict(enemiesInfo))
        self.enemyTeams = enemyTeams