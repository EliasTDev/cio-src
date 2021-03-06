"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file BookPage.py
@author Maverick Liberty
@date June 17, 2016

@desc HAPPY BIRTHDAY COG INVASION ONLINE!!!
             2 YEAR ANNIVERSARY

"""

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.StateData import StateData
from direct.gui.DirectGui import OnscreenText

class BookPage(StateData):

    def __init__(self, book, title, doneEvent = '%s-done', wantHeader = True):
        StateData.__init__(self, doneEvent % title)
        self.notify = directNotify.newCategory(title)
        self.book = book
        self.title = title
        self.icon = None
        self.iconScale = 1
        self.iconColor = (1, 1, 1, 1)
        self.tabButton = None

        # The actual header that displays the title.
        self.header = None
        self.wantHeader = wantHeader

        # The required access level(s) to view this page.
        self.restriction = []

    def load(self):
        StateData.load(self)

    def unload(self):
        StateData.unload(self)
        if self.header:
            self.header.destroy()
            self.header = None
        self.book = None
        self.tabButton = None
        if self.icon:
            self.icon.removeNode()
            self.icon = None
        if hasattr(self, 'notify'):
            del self.notify
            del self.icon
            del self.iconScale
            del self.iconColor
            del self.book
            del self.title
            del self.header
            del self.wantHeader
            del self.restriction

    def enter(self):
        if not self.isEntered:
            if self.wantHeader:
                # Create the header at the top of the page.
                self.header = OnscreenText(text = self.title, pos=(0, 0.62, 0), scale = 0.12)
        StateData.enter(self)

    def exit(self):
        if self.isEntered:

            if self.header:
                # Hide the header at the top of the page.
                self.header.hide()
        StateData.exit(self)

    # Sets the required access levels to view this page.
    def setRestriction(self, levels):
        self.restriction = levels

    # Returns the required access levels to view this page.
    def getRestriction(self):
        return self.restriction

    def getName(self):
        return self.title

    # Returns the header at the top of the page.
    def getHeader(self):
        return self.header

    def getIcon(self):
        return self.icon

    def getIconScale(self):
        return self.iconScale

    def getIconColor(self):
        return self.iconColor
