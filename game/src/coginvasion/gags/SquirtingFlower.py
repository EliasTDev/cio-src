"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file SquirtingFlower.py
@author Maverick Liberty
@date Februrary 22, 2016

"""

from panda3d.core import Vec3, Point3

from src.coginvasion.gags.SquirtGag import SquirtGag
from src.coginvasion.gags import GagGlobals

from direct.interval.IntervalGlobal import Sequence, Func, Wait, Parallel
from direct.interval.IntervalGlobal import LerpScaleInterval, ActorInterval

class SquirtingFlower(SquirtGag):
    
    name = GagGlobals.SquirtFlower
    model = 'phase_3.5/models/props/button.bam'
    hitSfxPath = GagGlobals.FLOWER_HIT_SFX

    def __init__(self):
        SquirtGag.__init__(self)
        self.setImage('phase_3.5/maps/squirting-flower.png')
        self.flower = None
        self.flowerScale = 1.5
        self.track = Parallel()
        self.timeout = 4.0
        self.sprayRotation = Vec3(0, 20, 0)
        
    def setAvatar(self, avatar):
        SquirtGag.setAvatar(self, avatar)
        if 'dgs' in avatar.getTorso():
            # It's a fat toon, change the spray rotation.
            self.sprayRotation = Vec3(0, 10, 0)

    def start(self):
        SquirtGag.start(self)
        self.buildFlower()
        self.build()
        self.equip()

        if self.isLocal():
            self.startTimeout()
        self.origin = self.getSprayStartPos()

        def attachFlower():
            flowerJoint = self.avatar.find('**/def_joint_attachFlower')
            if flowerJoint.isEmpty():
                flowerJoint = self.avatar.find('**/joint_attachFlower')
            self.flower.reparentTo(flowerJoint)
            self.flower.setY(self.flower.getY())

        # The variables we'll need.
        totalAnimationTime = 2.5
        flowerAppear = 1.0
        flowerScaleTime = 0.5

        # Let's start building the track.
        animTrack = ActorInterval(self.avatar, 'push-button')
        self.track.append(animTrack)

        flowerTrack = Sequence(
            Func(attachFlower),
            Wait(flowerAppear),
            LerpScaleInterval(self.flower, flowerScaleTime,
                1.5, startScale = GagGlobals.PNT3NEAR0),
            Wait(totalAnimationTime - flowerScaleTime - flowerAppear)
        )
        flowerTrack.append(Func(self.release))
        flowerTrack.append(LerpScaleInterval(self.flower, flowerScaleTime, GagGlobals.PNT3NEAR0))
        flowerTrack.append(LerpScaleInterval(self.gag, flowerScaleTime, GagGlobals.PNT3NEAR0))
        flowerTrack.append(Func(self.unEquip))
        self.track.append(flowerTrack)
        self.track.start()

    def getSprayStartPos(self):
        if not self.avatar.isEmpty() and not self.flower.isEmpty():
            self.avatar.update(0)
            return self.flower.getPos(render)

    def release(self):
        SquirtGag.release(self)
        if not self.avatar.isEmpty() and self.gag:
            self.sprayJoint = self.flower.find('**/joint_attachSpray')
            self.sprayRange = self.avatar.getPos(render) + Point3(0, GagGlobals.SELTZER_RANGE, 0)
            self.doSpray(0.2, 0.2, 0.1, horizScale = 0.3, vertScale = 0.3)
            if self.isLocal():
                base.localAvatar.sendUpdate('usedGag', [self.id])

    def unEquip(self):
        SquirtGag.unEquip(self)
        self.cleanup()
        self.reset()

    def cleanup(self):
        if self.flower:
            self.flower.removeNode()
            self.flower = None
        if self.track:
            self.track.pause()
            self.track = Parallel()

    def setHandJoint(self):
        if self.avatar:
            self.handJoint = self.avatar.find('**/def_joint_left_hold')

    def buildFlower(self):
        if self.flower:
            self.flower.removeNode()
            self.flower = None
        self.flower = loader.loadModel(GagGlobals.getProp(3.5, 'squirting-flower'))
        self.flower.setScale(GagGlobals.PNT3NEAR0)
