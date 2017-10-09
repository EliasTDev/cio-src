"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file Lighting.py
@author Brian Lach
@date September 25, 2017

"""

from panda3d.core import Point3

from src.coginvasion.globals import CIGlobals
from src.coginvasion.hood.SkyUtil import SkyUtil
from src.coginvasion.hood.SnowEffect import SnowEffect

class LightingConfig:

    def __init__(self, ambient):
        self.ambient = ambient
        self.ambientNP = None

    @staticmethod
    def makeDefault():
        return LightingConfig(DEFAULT_AMBIENT)
        
    def setupAndApply(self):
        self.setup()
        self.apply()
        
    def unapplyAndRemove(self):
        self.unapply()
        self.remove()

    def setup(self):
        self.ambientNP = CIGlobals.makeAmbientLight('config', self.ambient)

    def apply(self):
        render.setLight(self.ambientNP)

    def unapply(self):
        render.clearLight(self.ambientNP)

    def remove(self):
        if self.ambientNP:
            self.ambientNP.removeNode()
            self.ambientNP = None

    def cleanup(self):
        self.unapply()
        self.remove()
        self.ambient = None

class OutdoorLightingConfig(LightingConfig):

    # Sky types:
    STNone    = 0
    STMidday  = 1
    STCloudy  = 2
    STEvening = 3
    STNight   = 4
    STCog     = 5

    SkyData = {STMidday:    ["phase_3.5/models/props/TT_sky.bam",   True],
               STCloudy:    ["phase_3.5/models/props/BR_sky.bam",   False],
               STEvening:   ["phase_6/models/props/MM_sky.bam",     False],
               STNight:     ["phase_8/models/props/DL_sky.bam",     False],
               STCog:       ["phase_9/models/cogHQ/cog_sky.bam",    False]}

    def __init__(self, ambient, sun, sunPos, fog, fogDensity, skyType, snow):
        LightingConfig.__init__(self, ambient)
        self.sun = sun
        self.sunPos = sunPos
        self.fog = fog
        self.fogDensity = fogDensity
        self.setSkyType(skyType)
        self.fogNode = None
        self.sunNP = None
        self.skyNP = None

        self.skyEffect = None
        self.snowEffect = None

        self.snow = snow if not base.cr.isChristmas() else True

        # During winter, we will need to override the fog created here with the fog from snow effect.
        # This flag specifies whether or not we are going to be overriding the fog created here.
        # If it's true, we won't even create or apply any fog to the scene in this class.
        self.winterOverride = base.cr.isChristmas()

    def setSkyType(self, skyType):
        self.skyType = skyType
        if base.cr.isChristmas() and skyType != OutdoorLightingConfig.STNone:
            self.skyType = OutdoorLightingConfig.STCloudy
        if skyType != OutdoorLightingConfig.STNone:
            self.skyData = OutdoorLightingConfig.SkyData[self.skyType]

    @staticmethod
    def makeDefault():
        envConfig = base.loader.envConfig

        return OutdoorLightingConfig(envConfig.defaultOutdoorAmbientColor,
            envConfig.defaultSunColor,
            envConfig.defaultSunPosition,
            envConfig.defaultFogColor,
            envConfig.defaultFogDensity,
            envConfig.defaultSkyType,
        False)

    def setup(self):
        LightingConfig.setup(self)
        self.sunNP = CIGlobals.makeDirectionalLight('config', self.sun, self.sunPos)
        if not self.winterOverride:
            self.fogNode = CIGlobals.makeFog('config', self.fog, self.fogDensity)

        if self.skyType != OutdoorLightingConfig.STNone:
            self.skyEffect = SkyUtil()
            self.skyNP = loader.loadModel(self.skyData[0])

        if self.snow:
            self.snowEffect = SnowEffect()
            self.snowEffect.load()

    def apply(self):
        LightingConfig.apply(self)
        render.setLight(self.sunNP)
        if not self.winterOverride:
            render.setFog(self.fogNode)

        if self.skyType != OutdoorLightingConfig.STNone:
            self.skyNP.reparentTo(camera)
            self.skyNP.setZ(0.0)
            self.skyNP.setHpr(0.0, 0.0, 0.0)
            self.skyNP.setLightOff()
            self.skyNP.setFogOff()
            self.skyNP.setShaderOff()
            self.skyNP.setMaterialOff()
            self.skyNP.setCompass()
            self.skyNP.hide(CIGlobals.ShadowCameraBitmask)

            if self.skyData[1]:
                self.skyEffect.startSky(self.skyNP)
        
        if self.snow and self.snowEffect:
            self.snowEffect.start()

    def unapply(self):
        LightingConfig.unapply(self)
        render.clearLight(self.sunNP)
        if not self.winterOverride:
            render.clearFog()

        if self.skyType != OutdoorLightingConfig.STNone:
            self.skyNP.reparentTo(hidden)

            if self.skyData[1]:
                self.skyEffect.stopSky()
            
        if self.snow and self.snowEffect:
            self.snowEffect.stop()

    def remove(self):
        LightingConfig.remove(self)
        if self.skyNP:
            self.skyNP.removeNode()
            self.skyNP = None
        if self.sunNP:
            self.sunNP.removeNode()
            self.sunNP = None
        if self.snowEffect:
            self.snowEffect.unload()
            self.snowEffect = None
        if self.skyEffect:
            self.skyEffect.stopSky()
            self.skyEffect.cleanup()
            self.skyEffect = None

    def cleanup(self):
        LightingConfig.cleanup(self)
        self.sun = None
        self.sunPos = None
        self.fog = None
        self.fogDensity = None
        self.fogNode = None
        self.winterOverride = None
        self.skyType = None
        self.skyData = None
        self.snow = None

class IndoorLightingConfig(LightingConfig):

    def __init__(self, ambient, light, lights):
        LightingConfig.__init__(self, ambient)
        self.light = light
        self.lights = lights
        self.lightNPs = []

    @staticmethod
    def makeDefault():
        envConfig = base.loader.envConfig
        
        return IndoorLightingConfig(envConfig.defaultIndoorAmbientColor,
            envConfig.defaultInteriorLightColor,
        [Point3(0, 10, 11.5)])

    def setup(self):
        LightingConfig.setup(self)
        for lightPos in self.lights:
            light = CIGlobals.makePointLight('config', self.light, lightPos)
            self.lightNPs.append(light)

    def apply(self):
        LightingConfig.apply(self)
        for light in self.lightNPs:
            render.setLight(light)

    def unapply(self):
        LightingConfig.unapply(self)
        for light in self.lightNPs:
            render.clearLight(light)

    def remove(self):
        LightingConfig.remove(self)

        for light in self.lightNPs:
            if not light.isEmpty():
                light.removeNode()

        self.lightNPs = []

    def cleanup(self):
        LightingConfig.cleanup(self)
        self.lights = None
        self.light = None