# SplatStats

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SplatStats)](https://pypi.org/project/SplatStats)
[![PyPI version](https://badge.fury.io/py/SplatStats.svg)](https://badge.fury.io/py/SplatStats)
[![Conda](https://github.com/chipdelmal/MGSurvE/actions/workflows/Anaconda.yml/badge.svg)](https://github.com/Chipdelmal/MGSurvE/blob/main/.github/workflows/Anaconda.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Chipdelmal/MGSurvE)

**UNDER DEVELOPMENT** 

This codebase works in tandem with the [s3s package](https://github.com/frozenpandaman/s3s) to refactor and analayze [Splatoon 3](https://en.wikipedia.org/wiki/Splatoon_3)'s data. When finished, it will be able to load [s3s package](https://github.com/frozenpandaman/s3s) `json` files, re-shape them, and visualize the data from battles history.


![](./docs/img/playerDF.png)

Have a look at our [documentation](https://chipdelmal.github.io/SplatStats/) for more information on how to install and use this package!

<hr>

## [Matches History Panel](https://chipdelmal.github.io/SplatStats/build/html/plots.html#matches-history-panel)

![](./docs/img/bHistory.png)

This panel is constructed as a panel composed of two different figures. The top one is a detailed breakdown of the statistics of each battle. Each column on the x axis represents a single battle; where the left y axis shows the number of kills, deaths, assists and specials; and the right y axis the turf painted over the match (bars on the plot).

## [Kills VS Deaths Distributions](https://chipdelmal.github.io/SplatStats/build/html/plots.html#matches-history-panel)

![](./docs/img/kdHistogram.png)

These paired histograms show the frequency distributions of the number of kills or kassists (top, blue), and the number of deaths (bottom, magenta) across matches.

## [Stage Stats Treemaps](https://chipdelmal.github.io/SplatStats/build/html/plots.html#stats-treemaps)

<img src="./docs/img/treemapA.png" width="50%" align="middle"><img src="./docs/img/treemapB.png" width="50%" align="middle">

These plots are designed to show which stages are the ones in which the player performs best on any given stage with respect to a selected metric. Auxiliary provided functions generate the statistics dataframe required for these plots, which includes: kills, deaths, win ratio, paint, total matches; amongst many others. These statistics can be also generated for a specific match type (Rainmaker, Turf War, Tower Control, etc), or for a combination of them.

<hr>

# Author

<img src="./docs/img/chip.jpg" height="250px" align="middle">

[Héctor M. Sánchez C.](chipdelmal.github.io)