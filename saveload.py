#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 21.09.2019
# saveload

import yaml

def loadGame(filename="savegame"):
    """
    loads a YAML formatted "savegame" file,
    and returns a fully fledged gameStatus object.
    """
    try:
        savefile = open(filename, "r")
    except FileNotFoundError:
        print("Could not find %s" % filename)
        return None
    save = yaml.load(savefile, Loader=yaml.FullLoader)
    savefile.close()

    return save

def saveGame(game_status, filename="savegame"):
    """
    Packs the game status in to a yaml and saves
    """
    savefile = open(filename, "w")
    yaml.dump(game_status, savefile)
    savefile.close()

    return True

