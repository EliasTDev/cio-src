"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file JugglingBalls.py
@author Maverick Liberty
@date July 18, 2015

"""

from src.coginvasion.gags.ToonUpGag import ToonUpGag
from src.coginvasion.gags import GagGlobals
from src.coginvasion.globals import BSPUtility
from direct.interval.IntervalGlobal import Sequence, Func, Parallel, ActorInterval

class JugglingBalls(ToonUpGag):
        
    name = GagGlobals.JugglingBalls
    model = 'phase_5/models/props/cubes-mod.bam'
    minHeal = 90
    maxHeal = 120
    efficiency = 100
    hitSfxPath = GagGlobals.JUGGLE_SFX
    anim = 'phase_5/models/props/cubes-chan.bam'

    def __init__(self):
        ToonUpGag.__init__(self)
        self.setImage('phase_3.5/maps/juggling-cubes.png')
        self.track = None
        self.soundInterval = None
        self.timeout = 8.0

    def start(self):
        super(JugglingBalls, self).start()
        self.setupHips()
        self.build()
        self.placeProp(self.hips, self.gag)
        self.soundInterval = self.getSoundTrack(0.7, self.gag, 7.7)
        
        BSPUtility.applyUnlitOverride(self.gag)
        
        propInterval = Sequence()
        propInterval.append(ActorInterval(self.gag, 'chan'))
        if self.avatar == base.localAvatar:
            propInterval.append(Func(self.setHealAmount))
            propInterval.append(Func(self.healNearbyAvatars, 25))
        propInterval.append(Func(self.cleanupGag))
        propInterval.append(Func(self.reset))
        self.track = Parallel(ActorInterval(self.avatar, 'juggle'), propInterval, Func(self.soundInterval.start))
        self.track.start()

    def equip(self):
        # self.gag returns the juggling balls.
        super(JugglingBalls, self).equip()

    def unEquip(self):
        if self.track:
            self.soundInterval.finish()
            self.track.finish()
            self.track = None
        self.reset()
