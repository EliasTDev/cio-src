"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file OptionsCategory.py
@author Brian Lach
@date March 13, 2017

"""

from direct.showbase.DirectObject import DirectObject

from src.coginvasion.globals import CIGlobals
from src.coginvasion.gui.Dialog import GlobalDialog

class OptionsCategory(DirectObject):
    AppendOptions = True
    ApplyCancelButtons = True
    WantTitle = True

    def __init__(self, page):
        self.page = page
        self.page.header.setScale(0.1)
        if self.WantTitle:
            self.page.header.setText(self.Name + (" Options" if self.AppendOptions else ""))
        else:
            self.page.header.setText("")
        if self.ApplyCancelButtons:
            self.applyBtn = CIGlobals.makeOkayButton("Apply/Save", parent = self.page.book, command = self.applyChanges,
                                                     pos = (0.45, -0.62, -0.62))
            self.discardBtn = CIGlobals.makeCancelButton("Discard", parent = self.page.book, command = self.discardChanges,
                                                         pos = (0.65, -0.62, -0.62))

        self.applying = GlobalDialog("Saving settings...")
        self.applying.hide()
        
        self.settingsMgr = CIGlobals.getSettingsMgr()
        
        # This is a list of ChoiceWidgets under this options category.
        self.widgets = []

    def applyChanges(self):
        self._showApplying()
        if self.widgets:
            for widget in self.widgets:
                widget.saveSetting()
        self.settingsMgr.saveFile()
        self._hideApplying()

    def discardChanges(self):
        if self.widgets:
            for widget in self.widgets:
                widget.reset()

    def _showApplying(self):
        self.applying.show()
        base.cr.renderFrames()

    def _hideApplying(self):
        base.cr.renderFrames()
        self.applying.hide()

    def cleanup(self):
        self.page.header.setScale(0.12)
        if hasattr(self, 'title'):
            self.title.destroy()
            del self.title
        if hasattr(self, 'applyBtn'):
            self.applyBtn.destroy()
            del self.applyBtn
        if hasattr(self, 'discardBtn'):
            self.discardBtn.destroy()
            del self.discardBtn
        if hasattr(self, 'applying'):
            self.applying.cleanup()
            del self.applying
        self.widgets = None
        del self.widgets
