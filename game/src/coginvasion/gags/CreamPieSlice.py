"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file CreamPieSlice.py
@author Maverick Liberty
@date July 07, 2015

"""

from src.coginvasion.gags.ThrowGag import ThrowGag
from src.coginvasion.gags import GagGlobals

class CreamPieSlice(ThrowGag):

    name                = GagGlobals.CreamPieSlice
    model               = "phase_5/models/props/cream-pie-slice.bam"
    hitSfxPath          = GagGlobals.SLICE_SPLAT_SFX
    splatColor          = GagGlobals.CREAM_SPLAT_COLOR

    def __init__(self):
        ThrowGag.__init__(self)
        self.setHealth(GagGlobals.CREAM_PIE_SLICE_HEAL)
        self.setImage('phase_3.5/maps/cream_pie_slice.png')
