"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file FireHose.py
@author Brian Lach
@date November 15, 2015

"""

from panda3d.core import Point3, Vec3, NodePath

from direct.interval.IntervalGlobal import Sequence, Wait, Func, ActorInterval, LerpScaleInterval, Parallel

from src.coginvasion.toon import ParticleLoader
from src.coginvasion.phys import PhysicsUtils
from GagState import GagState
from SquirtGag import SquirtGag
import GagGlobals

class FireHose(SquirtGag):
    
    name = GagGlobals.FireHose
    model = "phase_5/models/props/firehose-mod.bam"
    anim = 'phase_5/models/props/firehose-chan.bam'
    hitSfxPath = GagGlobals.NULL_SFX
    scale = 1.0

    def __init__(self):
        SquirtGag.__init__(self)
        self.hydrant = None
        self.hydrantNode = None
        self.hydrantScale = None
        self.hoseJoint = None
        self.controlHoseTask = None
        self.timeout = 6

    def cleanupHydrantNode(self):
        if self.hydrantNode:
            self.hydrantNode.removeNode()
            self.hydrentNode = None

    def reset(self):
        SquirtGag.reset(self)
        self.deleteHoseStuff()

    def __doBob(self):
        self.setAnimTrack(self.getBobSequence('firehose', 30, 30, 1.0), startNow = True, looping = True)

    def __controlHoseTask(self, task):
        if not self.hoseJoint or self.hoseJoint.isEmpty():
            return task.done

        hand = self.avatar.find("**/def_joint_left_hold")
        self.hoseJoint.setHpr(self.avatar, hand.getHpr(self.avatar) + (-5, 5, 0))
        self.hoseJoint.setPos(self.avatar, hand.getPos(self.avatar) + (-0.1, 0.2, 0.1))

        return task.cont

    def equip(self):
        self.deleteHoseStuff()

        SquirtGag.equip(self)
        
        if self.isLocal():
            vm = self.getViewModel()
            fpsCam = self.getFPSCam()
            fpsCam.setVMGag(self.gag, pos = (-1.8, 1.06, -4.13), hpr = (0, 90, 0), hand = 1, animate = False)
            fpsCam.setVMAnimTrack(Sequence(ActorInterval(vm, "hose_draw"), Func(vm.loop, "hose_idle")))
            
        self.hydrant = loader.loadModel('phase_5/models/props/battle_hydrant.bam')
        self.gag.reparentTo(self.hydrant)
        self.gag.pose('chan', 2)
        self.hoseJoint = self.gag.controlJoint(None, "modelRoot", "joint_x")

        self.hydrantNode = self.avatar.attachNewNode('hydrantNode')
        self.hydrantNode.clearTransform(self.avatar.getGeomNode().getChild(0))
        self.hydrantNode.setHpr(0, 0, 0)
        self.hydrantScale = self.hydrantNode.attachNewNode('hydrantScale')
        self.hydrant.reparentTo(self.hydrantScale)
        self.avatar.pose('firehose', 30)
        self.avatar.update(0)
        torso = self.avatar.getPart('torso')
        if 'dgm' in self.avatar.getTorso():
            self.hydrant.setPos(torso, 0, 0, -1.85)
        else:
            self.hydrant.setPos(torso, 0, 0, -1.45)
        hbase = self.hydrant.find('**/base')
        hbase.setColor(1, 1, 1, 0.5)
        hbase.setPos(self.avatar, 0, 0, 0)

        if self.controlHoseTask:
            self.controlHoseTask.remove()
            self.controlHoseTask = None
        self.controlHoseTask = taskMgr.add(self.__controlHoseTask, self.avatar.taskName("controlHoseTask"))

        self.avatar.loop('neutral')

        tAppearDelay = 0.7
        dAnimHold = 5.1
        dHoseHold = 0.7
        tSprayDelay = 2.8
        track = Parallel()
        toonTrack = Sequence(Wait(tAppearDelay),
                             Func(self.avatar.setForcedTorsoAnim, 'firehose'),
                             self.getAnimationTrack('firehose', endFrame = 30),
                             Func(self.__doBob))
        propTrack = Sequence(Func(self.hydrantNode.reparentTo, self.avatar), LerpScaleInterval(self.hydrantScale, tAppearDelay * 0.5, Point3(1, 1, 1.4),
            startScale=Point3(1, 1, 0.01)), LerpScaleInterval(self.hydrantScale, tAppearDelay * 0.3, Point3(1, 1, 0.8), startScale=Point3(1, 1, 1.4)),
            LerpScaleInterval(self.hydrantScale, tAppearDelay * 0.1, Point3(1, 1, 1.2), startScale=Point3(1, 1, 0.8)),
            LerpScaleInterval(self.hydrantScale, tAppearDelay * 0.1, Point3(1, 1, 1), startScale=Point3(1, 1, 1.2)),
            ActorInterval(self.gag, 'chan', endFrame = 30))
        track.append(toonTrack)
        track.append(propTrack)
        self.setAnimTrack(track, startNow = True)

        if self.isLocal() and base.localAvatar.isFirstPerson():
            self.hydrantNode.hide()

    def deleteHoseStuff(self):
        if self.controlHoseTask:
            self.controlHoseTask.remove()
            self.controlHoseTask = None
        if self.hoseJoint:
            self.hoseJoint.detachNode()
            self.gag.releaseJoint("modelRoot", "joint_x")
            self.hoseJoint = None
        if self.hydrant:
            self.hydrant.removeNode()
            self.hydrant = None
        if self.hydrantNode:
            self.hydrantNode.removeNode()
            self.hydrantNode = None
        if self.hydrantScale:
            self.hydrantScale.removeNode()
            self.hydrantScale = None
        if self.gag:
            self.gag.cleanup()
            self.gag.removeNode()
            self.gag = None

    def delete(self):
        self.deleteHoseStuff()
        SquirtGag.delete(self)

    def start(self):
        SquirtGag.start(self)

        if self.isLocal():
            vm = self.getViewModel()
            fpsCam = self.getFPSCam()
            fpsCam.setVMAnimTrack(Sequence(ActorInterval(vm, "hose_shoot_begin"), Func(vm.loop, "hose_shoot_loop")))

    def throw(self):
        SquirtGag.throw(self)
            
        if self.isLocal():
            vm = self.getViewModel()
            fpsCam = self.getFPSCam()
            fpsCam.setVMAnimTrack(Sequence(ActorInterval(vm, "hose_shoot_end"), Func(vm.loop, "hose_idle")))
