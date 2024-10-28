# coding: utf-8
from PyQt5.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.text = self.tr('Help')
        self.view = self.tr('View')
        self.menus = self.tr('Menus & toolbars')
        self.icons = self.tr('Symbol')
        self.layout = self.tr('Layout')
        self.dialogs = self.tr('Dialogs & flyouts')
        self.scroll = self.tr('Tuto')
        self.material = self.tr('Material')
        self.dateTime = self.tr(' time Management')
        self.navigation = self.tr('Navigation')
        self.basicInput = self.tr('Basic input')
        self.statusInfo = self.tr('Status & info')
        self.price = self.tr("Price")