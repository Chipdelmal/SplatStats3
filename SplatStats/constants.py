
import SplatStats.colors as clr

###############################################################################
# Dataframe-related constants
###############################################################################
BATTLE_DTYPES = {
    'self': bool,       'ko': bool,
    'kill': int,        'death': int,
    'assist': int,      'special': int,
    'splatfest': bool
}
MATCH_TYPES = (
    'Turf War', 'Tower Control', 'Rainmaker', 'Splat Zones', 'Clam Blitz'
)

###############################################################################
# Colors and Markers for plots
###############################################################################
# Markers for basic stats
MKR_STATS = {
    'kill':     'o',
    'death':    'x',
    'assist':   '.',
    'special':  '_'
}
CLR_STATS = {
    'kill':  clr.LPINK_V_BLUE_S2[1],
    'death': clr.LPINK_V_BLUE_S2[0],
    'assist': clr.AUTOBOTS_V_DECEPTICONS[1],
    'special': clr.AUTOBOTS_V_DECEPTICONS[1]
}
# Markers/Colors for match types
MKR_MT = {
    'Turf War':             ',',
    'Rainmaker':            '1',
    'Splat Zones':          '2',
    'Clam Blitz':           '3',
    'Tower Control':        '4',
    'Tricolor Turf War':    '.'
}
CLR_MT = {
    'Turf War':             clr.LMODEL_V_PMODEL_S2[-1],
    'Rainmaker':            clr.WINNERW_V_WOUTERW_S2[2],
    'Splat Zones':          clr.BLUE_V_GREEN_S2[2],
    'Clam Blitz':           clr.RPURPLE_V_GAPPLE_S2[0],
    'Tower Control':        clr.PINK_V_GREEN_S1 [0],
    'Tricolor Turf War':    clr.PINK_V_GREEN_S1 [0]  
}
CLR_PAINT = clr.TURQUOISE_V_PUMPKIN_S2[-1]
# Colors for scatter elements
CLR_WL = {
    'W': clr.SKY_V_GOLD_S2[0],
    'L': clr.LBLUE_V_FUCHSIA_S2[1]
}
MKR_WL = {
    'W': '^',
    'L': 'v'
}
MKR_KO = {
    True: '.',
    False: ','    
}
CLR_KO = {
    True: clr.SKY_V_GOLD_S2[0],
    False: clr.LMODEL_V_PMODEL_S2[-1]
}
MKR_FEST = {
    True: '.',
    False: ','
}
CLR_FEST = {
    True: clr.PINK_V_GREEN_S1 [0],
    False: clr.LMODEL_V_PMODEL_S2[-1]
}
CLR_STAGE = {
    'Barnacle & Dime': clr.GHERKOUT_V_GHERKIN_S2[1],
    'Bluefin Depot': clr.SHIVER_FRYE_BIGMAN_S3[2],
    'Brinewater Springs': clr.GRAPE_V_TURQUOISE_S2[0], 
    'Crableg Capital': clr.SHIVER_FRYE_BIGMAN_S3[-1],
    'Eeltail Alley': clr.PINK_V_ORANGE_S1[1],
    'Flounder Heights': clr.SWEATER_V_SOCKS_S2[0],
    'Hagglefish Market': clr.LPINK_V_BLUE_S2[1],
    'Hammerhead Bridge': clr.MAYO_V_KETCHUP_S2[1],
    'Humpback Pump Track': clr.CALLIE_V_MARIE_S1[1],
    'Inkblot Art Academy': clr.LPINK_V_BLUE_S2[0],
    'Mahi-Mahi Resort': clr.CHAOS_V_ORDER_S2[1],
    'MakoMart': clr.PINK_V_GREEN_S1[2],
    'Marlin Airport': clr.LPINK_V_BLUE_S2[1],
    'Mincemeat Metalworks': clr.TSUBUAN_V_KOSHIAN_S2[1],
    "Museum d'Alfonsino": clr.SALTY_V_SWEET_S2[0],
    'Robo ROM-en': clr.SHIVER_FRYE_BIGMAN_S3[0],
    'Scorch Gorge': clr.UNICORN_V_NARWHAL_S2[0],
    'Shipshape Cargo Co.': clr.MONEY_FAME_LOVE[2],
    'Sturgeon Shipyard': clr.VAMPIRE_V_WEREWOLF_S2[2],
    'Undertow Spillway': clr.RASPBERRY_V_NYELLOW_S2[1],
    'Wahoo World': clr.PINK_V_ORANGE_S1[2],
    'Manta Maria': clr.DARK_MILK_WHITE_S3[-1],
    "Um'ami Ruins": clr.YELLOW_V_INDIGO_S3 [-1],
    'Lemuria Hub': clr.SALTY_V_SWEET_S2[0],
    'Grand Splatlands Bowl': clr.DBLUE_V_ORANGE_S1[-1]
}
CLR_WEAPON = {
    'Clash Blaster': '#0D37C3',
    'Hero Shot Replica': '#FDFF00',
    'Splattershot': '#4F55ED',
    'Tentatek Splattershot': '#C920B7',
}
CLR_CLS_LONG = [
    clr.TSUBUAN_V_KOSHIAN_S2[1],
    clr.FAM_V_FRIEND_S2[1],
    clr.DBLUE_V_YELLOW_S1[0],
    clr.YELLOW_V_DTEAL_LK_S3[0], clr.YELLOW_V_DTEAL_LK_S3[1], clr.YELLOW_V_DTEAL_LK_S3[2],
    clr.WINNERW_V_WOUTERW_S2[0], clr.WINNERW_V_WOUTERW_S2[1], clr.WINNERW_V_WOUTERW_S2[2],
    clr.LPINK_V_BLUE_S2[0], clr.LPINK_V_BLUE_S2[1],
    clr.NPINK_V_NGREEN_S2[1], 
    clr.RASPBERRY_V_NYELLOW_S2[1],
    clr.YELLOW_V_LBLU_V_DBLU_LK_S3[1], clr.BLUE_FRYE_S3[2],
    clr.GRAPE_V_TURQUOISE_S2[0], clr.GRAPE_V_TURQUOISE_S2[1],
    clr.PBODY_V_PBRAIN_S1[0], clr.PBODY_V_PBRAIN_S1[1],
    clr.SGREEN_V_GRAPE_S2[0], clr.SGREEN_V_GRAPE_S2[1], clr.SGREEN_V_GRAPE_S2[2],
    clr.TEAL_PURPLE_ORANGE_S3[0], clr.TEAL_PURPLE_ORANGE_S3[1], clr.TEAL_PURPLE_ORANGE_S3[2], clr.TEAL_PURPLE_ORANGE_S3[3],
    clr.YELLOW_V_LBLU_V_DBLU_LK_S3[0], clr.YELLOW_V_LBLU_V_DBLU_LK_S3[1], clr.YELLOW_V_LBLU_V_DBLU_LK_S3[2], clr.YELLOW_V_LBLU_V_DBLU_LK_S3[3]
]
CLR_BAR = clr.SMUSHROOM_V_SSTAR_S2[-1]
###############################################################################
# Weapons Classes
###############################################################################
WPN_CLASS = {
    'Blaster': {
        'Blaster', 'Clash Blaster', 'Luna Blaster', 'Luna Blaster Neo',
        'Range Blaster', 'Rapid Blaster', 'Rapid Blaster Pro'
    },
    'Brella': {
        'Splat Brella', 'Tenta Brella', 'Undercover Brella'
    },
    'Brush': {
        'Inkbrush', 'Inkbrush Nouveau', 'Octobrush'
    },
    'Charger': {
        'Bamboozler 14 Mk I', 'Classic Squiffer', 'E-liter 4K', 
        'E-liter 4K Scope', 'Goo Tuber', 'Snipewriter 5H', 'Splat Charger',
        'Splatterscope'
    },
    'Dualie': {
        'Dapple Dualies', 'Dapple Dualies Nouveau', 'Dark Tetra Dualies',
        'Dualie Squelchers', 'Glooga Dualies', 'Splat Dualies'
    },
    'Roller': {
        'Big Swig Roller', 'Carbon Roller', 'Carbon Roller Deco',
        'Dynamo Roller', 'Flingza Roller', 'Splat Roller'
    },
    'Shooter': {
        '.52 Gal', '.96 Gal', 'Aerospray MG', 'Aerospray RG', 
        'Custom Splattershot Jr.', 'Forge Splattershot Pro', 
        'H-3 Nozzlenose', 'Hero Shot Replica', 'Jet Squelcher',
        'L-3 Nozzlenose', "N-ZAP '85", 'Splash-o-matic', 'Splattershot',
        'Splattershot Jr.', 'Splattershot Nova', 'Splattershot Pro', 
        'Sploosh-o-matic', 'Squeezer', 'Tentatek Splattershot'
    },
    'Slosher': {
        'Bloblobber', 'Explosher', 'Slosher', 'Slosher Deco',
        'Sloshing Machine', 'Tri-Slosher'
    },
    'Splatana': {
        'Splatana Stamper', 'Splatana Wiper'
    },
    'Splatling': {
        'Ballpoint Splatling', 'Heavy Splatling', 'Hydra Splatling',
        'Mini Splatling', 'Nautilus 47', 'Zink Mini Splatling'
    },
    'Stringer': {
        'REEF-LUX 450', 'Tri-Stringer'
    }
}