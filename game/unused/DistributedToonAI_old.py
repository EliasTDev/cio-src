"""

Copyright (c) Cog Invasion Online. All rights reserved.

@file DistributedToonAI.py
@author Brian Lach
@date October 12, 2014

"""

from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.IntervalGlobal import Sequence, Wait, Func

from src.coginvasion.avatar.DistributedAvatarAI import DistributedAvatarAI
from src.coginvasion.quests.QuestManagerAI import QuestManagerAI
from src.coginvasion.gags.backpack.BackpackAI import BackpackAI
from src.coginvasion.gags import GagGlobals
from src.coginvasion.globals import CIGlobals
from src.coginvasion.distributed import AdminCommands
from src.coginvasion.tutorial.DistributedTutorialAI import DistributedTutorialAI
import ToonDNA
import types

class DistributedToonAI(DistributedAvatarAI, DistributedSmoothNodeAI, ToonDNA.ToonDNA):
    notify = directNotify.newCategory('DistributedToonAI')

    def __init__(self, air):
        try:
            self.DistributedToonAI_initialized
            return
        except:
            self.DistributedToonAI_initialized = 1
        DistributedAvatarAI.__init__(self, air)
        DistributedSmoothNodeAI.__init__(self, air)
        ToonDNA.ToonDNA.__init__(self)
        self.questManager = QuestManagerAI(self)
        self.avatarType = CIGlobals.Toon
        self.money = 0
        self.anim = "neutral"
        self.chat = ""
        self.health = 50
        self.damage = 0
        self.height = 3
        self.gender = "boy"
        self.headtype = "dgm_skirt"
        self.head = "dog"
        self.legtype = "dgm"
        self.torsotype = "dgm_shorts"
        self.hr = 1
        self.hg = 1
        self.hb = 1
        self.tr = 1
        self.tg = 1
        self.tb = 1
        self.lr = 1
        self.lg = 1
        self.lb = 1
        self.shir = 1
        self.shig = 1
        self.shib = 1
        self.shor = 1
        self.shog = 1
        self.shob = 1
        self.shirt = "phase_3/maps/desat_shirt_1.jpg"
        self.short = "phase_3/maps/desat_shorts_1.jpg"
        self.sleeve = "phase_3/maps/desat_sleeve_1.jpg"
        self.isdying = False
        self.isdead = False
        self.toon_legs = None
        self.toon_torso = None
        self.toon_head = None
        self.portal = None
        self.book = None
        self.token = -1
        self.ghost = 0
        self.attackers = []
        self.puInventory = []
        self.equippedPU = -1
        self.backpack = BackpackAI(self)
        self.quests = ""
        self.questHistory = []
        self.tier = -1
        self.friends = []
        self.tutDone = 0
        self.hoodsDiscovered = []
        self.teleportAccess = []
        self.lastHood = 0
        self.defaultShard = 0
        self.numGagSlots = 0
        self.trackExperience = dict(GagGlobals.DefaultTrackExperiences)
        return

    def __requesterAuthorized(self, notDev = False):
        requester = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if requester:
            hasToken = requester.getAdminToken() > AdminCommands.NoToken
            if ((not notDev and hasToken) or
                (notDev and hasToken and self.getAdminToken() != AdminCommands.DevToken)):
                return True
        return False

    def reqUnlockAllGags(self):
        if self.__requesterAuthorized():
            self.b_setTrackExperience(GagGlobals.trackExperienceToNetString(GagGlobals.MaxedTrackExperiences))
            self.backpack.refillSupply()

    def reqAllGagSlots(self):
        if self.__requesterAuthorized():
            self.b_setNumGagSlots(GagGlobals.MaxGagSlots)
        
    def reqSetWorldAccess(self, andTP):
        if self.__requesterAuthorized():
            self.b_setHoodsDiscovered(CIGlobals.Hood2ZoneId.values())
            if andTP:
                self.b_setTeleportAccess(CIGlobals.Hood2ZoneId.values())
        
    def d_setDNAStrand(self, strand):
        self.sendUpdate('setDNAStrand', [strand])
        
    def reqSetTSAUni(self, flag):
        if self.__requesterAuthorized():
            if flag:
                # Apply the TSA uniform to this toon.
                if self.getAdminToken() != AdminCommands.DevToken:
                    if self.gender == 'girl':
                        self.shirt = ToonDNA.ToonDNA.femaleTopDNA2femaleTop['135'][0]
                        self.shorts = ToonDNA.ToonDNA.femaleBottomDNA2femaleBottom['43'][0]
                        self.sleeve = ToonDNA.ToonDNA.Sleeves[ToonDNA.ToonDNA.femaleTopDNA2femaleTop['135'][1]]
                    else:
                        self.shirt = ToonDNA.ToonDNA.maleTopDNA2maleTop['135'][0]
                        self.shorts = ToonDNA.ToonDNA.maleBottomDNA2maleBottom['57'][0]
                        self.sleeve = ToonDNA.ToonDNA.Sleeves[ToonDNA.ToonDNA.maleTopDNA2maleTop['135'][1]]
                else:
                    # Blue suit signifies developer.
                    if self.gender == 'girl':
                        self.shirt = ToonDNA.ToonDNA.femaleTopDNA2femaleTop['136'][0]
                        self.shorts = ToonDNA.ToonDNA.femaleBottomDNA2femaleBottom['44'][0]
                        self.sleeve = ToonDNA.ToonDNA.Sleeves[ToonDNA.ToonDNA.femaleTopDNA2femaleTop['136'][1]]
                    else:
                        self.shirt = ToonDNA.ToonDNA.maleTopDNA2maleTop['136'][0]
                        self.shorts = ToonDNA.ToonDNA.maleBottomDNA2maleBottom['58'][0]
                        self.sleeve = ToonDNA.ToonDNA.Sleeves[ToonDNA.ToonDNA.maleTopDNA2maleTop['136'][1]]
            else:
                # Apply the default white clothes.
                if self.gender == 'girl':
                    self.shirt = ToonDNA.ToonDNA.femaleTopDNA2femaleTop['00'][0]
                    self.shorts = ToonDNA.ToonDNA.femaleBottomDNA2femaleBottom['00'][0]
                    self.sleeve = ToonDNA.ToonDNA.Sleeves[ToonDNA.ToonDNA.femaleTopDNA2femaleTop['00'][1]]
                else:
                    self.shirt = ToonDNA.ToonDNA.maleTopDNA2maleTop['00'][0]
                    self.shorts = ToonDNA.ToonDNA.maleBottomDNA2maleBottom['00'][0]
                    self.sleeve = ToonDNA.ToonDNA.Sleeves[ToonDNA.ToonDNA.maleTopDNA2maleTop['00'][1]]
                                   
            self.shirtColor = self.sleeveColor = self.shortColor = ToonDNA.ToonDNA.clothesColorDNA2clothesColor['27']
                    
            self.generateDNAStrandWithCurrentStyle()
            self.d_setDNAStrand(self.getDNAStrand())
        
    def reqSetAdminToken(self, token):
        if self.__requesterAuthorized(True):
            self.b_setAdminToken(token)

    def setNumGagSlots(self, num):
        self.numGagSlots = num

    def b_setNumGagSlots(self, num):
        self.sendUpdate('setNumGagSlots', [num])
        self.setNumGagSlots(num)

    def getNumGagSlots(self):
        return self.numGagSlots

    def setDefaultShard(self, shardId):
        self.defaultShard = shardId

    def d_setDefaultShard(self, shardId):
        self.sendUpdate('setDefaultShard', [shardId])

    def b_setDefaultShard(self, shardId):
        self.d_setDefaultShard(shardId)
        self.setDefaultShard(shardId)

    def getDefaultShard(self):
        return self.defaultShard

    def setLastHood(self, zoneId):
        self.lastHood = zoneId

    def getLastHood(self):
        return self.lastHood

    def setHoodsDiscovered(self, array):
        self.hoodsDiscovered = array

    def b_setHoodsDiscovered(self, array):
        self.sendUpdate('setHoodsDiscovered', [array])
        self.setHoodsDiscovered(array)

    def getHoodsDiscovered(self):
        return self.hoodsDiscovered

    def setTeleportAccess(self, array):
        self.teleportAccess = array

    def b_setTeleportAccess(self, array):
        self.sendUpdate('setTeleportAccess', [array])
        self.setTeleportAccess(array)

    def getTeleportAccess(self):
        return self.teleportAccess

    def createTutorial(self):
        zone = self.air.allocateZone()
        tut = DistributedTutorialAI(self.air, self.doId)
        tut.generateWithRequired(zone)
        self.sendUpdate('tutorialCreated', [zone])

    def setTutorialCompleted(self, value):
        self.tutDone = value

    def d_setTutorialCompleted(self, value):
        self.sendUpdate('setTutorialCompleted', [value])

    def b_setTutorialCompleted(self, value):
        self.d_setTutorialCompleted(value)
        self.setTutorialCompleted(value)

    def getTutorialCompleted(self):
        return self.tutDone

    def requestSetLoadout(self, gagIds):
        for gagId in gagIds:
            if not gagId in self.getInventory():
                self.ejectSelf(reason = "Tried to add a gag to the loadout that isn't in the backpack.")
                return
        self.b_setLoadout(gagIds)

    def requestAddFriend(self, avId):
        av = self.air.doId2do.get(avId)
        if av:
            if av.zoneId == self.zoneId and not avId in self.friends:
                fl = list(self.friends)
                fl.append(avId)
                self.b_setFriendsList(fl)

    def setFriendsList(self, friends):
        self.friends = friends

    def d_setFriendsList(self, friends):
        self.sendUpdate('setFriendsList', [friends])

    def b_setFriendsList(self, friends):
        self.d_setFriendsList(friends)
        self.setFriendsList(friends)

    def getFriendsList(self):
        return self.friends

    ################################################
    ##       Functions to send Quest updates      ##
    ################################################

    def setTier(self, tier):
        self.tier = tier

    def d_setTier(self, tier):
        self.sendUpdate('setTier', [tier])

    def b_setTier(self, tier):
        self.d_setTier(tier)
        self.setTier(tier)

    def getTier(self):
        return self.tier

    def setQuestHistory(self, history):
        self.questHistory = history

    def d_setQuestHistory(self, history):
        self.sendUpdate('setQuestHistory', [history])

    def b_setQuestHistory(self, history):
        self.d_setQuestHistory(history)
        self.setQuestHistory(history)

    def getQuestHistory(self):
        return self.questHistory

    def d_setChat(self, chat):
        self.sendUpdate('setChat', [chat])

    def setQuests(self, dataStr):
        self.quests = dataStr
        self.questManager.makeQuestsFromData()

    def d_setQuests(self, dataStr):
        self.sendUpdate('setQuests', [dataStr])

    def b_setQuests(self, questData):
        self.d_setQuests(questData)
        self.setQuests(questData)

    def getQuests(self):
        return self.quests

    ################################################


    def usedPU(self, index):
        self.puInventory[index] = 0
        self.puInventory[1] = 0
        self.b_setPUInventory(self.puInventory)

    def requestEquipPU(self, index):
        if len(self.puInventory) > index and self.puInventory[index] > 0:
            self.b_setEquippedPU(index)

    def setEquippedPU(self, index):
        self.equippedPU = index

    def d_setEquippedPU(self, index):
        self.sendUpdate('setEquippedPU', [index])

    def b_setEquippedPU(self, index):
        self.d_setEquippedPU(index)
        self.setEquippedPU(index)

    def getEquippedPU(self):
        return self.equippedPU

    def setPUInventory(self, array):
        self.puInventory = array

    def d_setPUInventory(self, array):
        self.sendUpdate("setPUInventory", [array])

    def b_setPUInventory(self, array):
        self.d_setPUInventory(array)
        self.setPUInventory(array)

    def getPUInventory(self):
        return self.puInventory

    def addNewAttacker(self, suitId, length = 5):
        if not suitId in self.attackers:
            self.attackers.append(suitId)
            Sequence(Wait(length), Func(self.removeAttacker, suitId)).start()

    def removeAttacker(self, suitId):
        if self.attackers:
            self.attackers.remove(suitId)
        else:
            self.attackers = []

    def getNumAttackers(self):
        return len(self.attackers)

    def getAttackers(self):
        return self.attackers

    def ejectSelf(self, reason = ""):
        self.air.eject(self.doId, 0, reason)

    def requestEject(self, avId, andBan = 0):
        clientChannel = self.GetPuppetConnectionChannel(avId)

        def getToonDone(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonAI']:
                return
            accId = fields['ACCOUNT']
            self.air.dbInterface.updateObject(
                self.air.dbId,
                accId,
                self.air.dclassesByName['AccountAI'],
                {"BANNED": 1}
            )

        if self.getAdminToken() > AdminCommands.NoToken:
            if andBan:
                self.air.dbInterface.queryObject(
                    self.air.dbId,
                    avId,
                    getToonDone
                )
            self.air.eject(clientChannel, 0, "Ejected by an administrator.")
        else:
            # Oh ok, a non-admin is trying to eject someone.
            # Let's eject them instead.
            self.ejectSelf("This player did not have administrator rights, but was trying to eject someone.")

    def setGhost(self, value):
        if not self.getAdminToken() > AdminCommands.NoToken and value > 0:
            self.ejectSelf("This player did not have administrator rights, but was trying to set ghost.")
            return
        self.ghost = value

    def getGhost(self):
        return self.ghost

    def toonUp(self, hp, announce = 1, sound = 1):
        amt = hp
        originalHealth = self.getHealth()
        hp = self.getHealth() + hp
        if hp > self.getMaxHealth():
            amt = self.getMaxHealth() - originalHealth
            hp = self.getMaxHealth()
        self.b_setHealth(hp)
        if announce and sound:
            self.d_announceHealthAndPlaySound(1, amt)
        elif announce and not sound:
            self.d_announceHealth(1, amt)

    def d_announceHealthAndPlaySound(self, level, hp):
        self.sendUpdate("announceHealthAndPlaySound", [level, hp])

    def setMoney(self, money):
        self.money = money

    def d_setMoney(self, money):
        self.sendUpdate('setMoney', [money])

    def b_setMoney(self, money):
        self.d_setMoney(money)
        self.setMoney(money)

    def getMoney(self):
        return self.money

    def setAnimState(self, anim, timestamp = 0):
        self.anim = anim

    def getAnimState(self):
        return self.anim

    def setAdminToken(self, token):
        self.token = token
        
    def b_setAdminToken(self, token):
        self.sendUpdate('setAdminToken', [token])
        self.setAdminToken(token)

    def getAdminToken(self):
        return self.token

    def usedGag(self, gagId):
        supply = self.backpack.getSupply(gagId)
        amt = supply - 1
        if amt < 0:
            self.ejectSelf()
            return
        self.b_setGagAmmo(gagId, amt)

    def setLoadout(self, gagIds):
        if self.backpack:
            for i in range(len(gagIds)):
                gagId = gagIds[i]
                if not self.backpack.hasGag(gagId):
                    gagIds.remove(gagId)
            self.backpack.setLoadout(gagIds)

    def b_setLoadout(self, gagIds):
        self.sendUpdate('setLoadout', [gagIds])
        self.setLoadout(gagIds)

    def d_addGag(self, gagId, curSupply, maxSupply):
        self.sendUpdate('addGag', [gagId, curSupply, maxSupply])

    def b_setGagAmmo(self, gagId, ammo):
        self.setGagAmmo(gagId, ammo)
        self.sendUpdate('setGagAmmo', [gagId, ammo])

    def setGagAmmo(self, gagId, ammo):
        self.backpack.setSupply(gagId, ammo)
    
    def setBackpackAmmo(self, netString):
        data = self.backpack.fromNetString(netString)
        
        for gagId in data.keys():
            supply = data[gagId]
            if not self.backpack.hasGag(gagId):
                self.backpack.addGag(gagId, curSupply=supply)
            else:
                self.backpack.setSupply(gagId, supply, updateEnabled=False)
    
    def b_setBackpackAmmo(self, netString):
        self.setBackpackAmmo(netString)
        self.d_setBackpackAmmo(netString)
        
    def d_setBackpackAmmo(self, netString):
        self.sendUpdate('setBackpackAmmo', [netString])
        
    def getBackpackAmmo(self):
        if self.backpack:
            netString = self.backpack.toNetString()
            return netString
        else:
            defaultBackpack = GagGlobals.getDefaultBackpack(isAI = True)
            return defaultBackpack.toNetString()
        
    def setTrackExperience(self, netString):
        self.trackExperience = GagGlobals.getTrackExperienceFromNetString(netString)
        GagGlobals.processTrackData(self.trackExperience, self.backpack)
        
    def d_setTrackExperience(self, netString):
        self.sendUpdate('setTrackExperience', [netString])
        
    def b_setTrackExperience(self, netString):
        self.setTrackExperience(netString)
        self.d_setTrackExperience(netString)
        
    def getTrackExperience(self):
        return GagGlobals.trackExperienceToNetString(self.trackExperience)

    def getInventory(self):
        return self.backpack.gags.keys()

    def died(self):
        self.b_setHealth(self.getMaxHealth())

    def suitKilled(self, avId):
        pass

    def toonHitByPie(self, avId, gagId):
        obj = self.air.doId2do.get(avId, None)
        hp = GagGlobals.getGagData(gagId).get('health', 0)
        if obj:
            if obj.getHealth() < obj.getMaxHealth() and not obj.isDead():
                if obj.__class__.__name__ == 'DistributedToonAI':
                    obj.toonUp(hp)
                else:
                    if obj.getHealth() + hp > obj.getMaxHealth():
                        hp = obj.getMaxHealth() - obj.getHealth()
                    obj.b_setHealth(obj.getHealth() + hp)
                    obj.d_announceHealth(1, hp)

    def gagStart(self, gagId):
        for suit in self.air.doFindAll("DistributedSuitAI"):
            if suit.zoneId == self.zoneId:
                # Let this Suit know that we've started using a gag.
                suit.handleToonThreat(self, False)

    def announceGenerate(self):
        DistributedAvatarAI.announceGenerate(self)
        DistributedSmoothNodeAI.announceGenerate(self)
        if self.parentId != self.getDefaultShard():
            self.b_setDefaultShard(self.parentId)

    def delete(self):
        try:
            self.DistributedToonAI_deleted
        except:
            if type(self.backpack) != types.IntType and self.backpack is not None:
                self.backpack.cleanup()
                self.backpack = None
            self.DistributedToonAI_deleted = 1
            DistributedAvatarAI.delete(self)
            DistributedSmoothNodeAI.delete(self)
            self.questManager.cleanup()
            self.questManager = None
            self.tutDone = None
            self.token = None
            self.anim = None
            self.chat = None
            self.health = None
            self.damage = None
            self.height = None
            self.gender = None
            self.headtype = None
            self.head = None
            self.legtype = None
            self.torsotype = None
            self.hr = None
            self.hg = None
            self.hb = None
            self.tr = None
            self.tg = None
            self.tb = None
            self.lr = None
            self.lg = None
            self.lb = None
            self.shir = None
            self.shig = None
            self.shib = None
            self.shor = None
            self.shog = None
            self.shob = None
            self.shirt = None
            self.short = None
            self.sleeve = None
            self.isdying = None
            self.isdead = None
            self.toon_legs = None
            self.toon_torso = None
            self.toon_head = None
            self.portal = None
            self.book = None
            self.place = None
            self.attackers = None
            self.numGagSlots = None
        return
