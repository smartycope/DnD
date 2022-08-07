# This Python file uses the following encoding: utf-8
import json
import os
import random
import re
import sys
from pathlib import Path

from Cope import debug, todo, unreachableState, FunctionCall
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QFile, QSize, Qt, QPoint
from PyQt5.QtGui import QBrush, QColor, QIcon, QImage, QPalette, QPixmap
from PyQt5.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication,
                             QCommonStyle, QDialogButtonBox, QFileDialog,
                             QListView, QListWidget, QMainWindow, QMdiArea,
                             QMdiSubWindow, QMessageBox, QProxyStyle, QSlider,
                             QStyle, QStyleFactory, QWidget, QCheckBox, QAbstractItemView)

# from os.path import dirname, join, basename; DIR = dirname(__file__)

DIR = Path(__file__).resolve().parent

todo('figure out how passive stats work')
todo('add death counters')
todo('fix counters spawning')
todo('add better spell stuffs')
todo('add a better inventory system')
todo('add leveling up mechanics better')
todo('add a damage/heal bar?')
todo('add a rage state')
todo('research and add more states')
todo('save states')
tood('save counters')
todo('disable closing MDI windows')
todo('limit exhaustion levels')
todo('have the exhaustion levels automatically disadvantage the appropriate rolls')

__DEBUG__ = True

BACKGROUND_IMAGE_PATH = '/home/leonard/hello/python/DnD/background.png'
# FRAME_PATH = '/home/leonard/hello/python/DnD/thinCelticBorder.png'
# FRAME_PATH = '/home/leonard/hello/python/DnD/celticFrame.png'
# FRAME_PATH = '/home/leonard/hello/python/DnD/gothicFrame.png'
FRAME_PATH = '/home/leonard/hello/python/DnD/BrownBoarder.png'
PAPER_BACKGROUND_2 = '/home/leonard/hello/python/DnD/paperBackground2.png'

class MainWindow(QMainWindow):
    # namedGroup('count', number()) + either('d', 'D') + namedGroup('sides', number()) + optional(whitespace()) + '+' + optional(whitespace()) + namedGroup('additional', number())
    diceRegex = re.compile(r'(?P<count>\d+)[dD](?P<sides>\d+)(\s?\+\s?(?P<additional>\d+))?')
    MAX_ROLLS_HISTORY = 4
    jsonAttrs = [
        'acrobatics_prof',
        'animal_handling_prof',
        'arcana_prof',
        'athletics_prof',
        'deception_prof',
        'history_prof',
        'insight_prof',
        'intimidation_prof',
        'investigation_prof',
        'medicine_prof',
        'nature_prof',
        'perception_prof',
        'performance_prof',
        'persuasion_prof',
        'religion_prof',
        'sleight_of_hand_prof',
        'stealth_prof',
        'survival_prof',
        'wis_prof',
        'cha_prof',
        'str_prof',
        'int_prof',
        'dex_prof',
        'con_prof',
        'wis_base',
        'cha_base',
        'str_base',
        'int_base',
        'dex_base',
        'con_base',
        'inspiration',
        'proficiency_bonus',
        'current_hp',
        'base_hp',
        'temp_hp',
        'prone',
        'exaustion',
        'platinum',
        'silver',
        'gold',
        'copper',
        'speed',
        'race',
        'player',
        'alignment',
        'level',
        'background',
        'name',
        'class_',
        'notes',
        'weapons',
        'spells',
        # TODO: Save Counters
        # 'counters_name',
        # 'counters_2_name',
        # 'counters_start',
        # 'counters_2_start',
        # 'counters_reset_long_rest',
        # 'counters_2_reset_long_rest',
        # 'counters_reset_short_rest',
        # 'counters_2_reset_short_rest',
        # 'counters_reset_none',
        # 'counters_2_reset_none',
        # 'counters_amount',
        # 'counters_2_amount',
    ]
    skillAssociations = {
        'acrobatics': 'dex',
        'animal_handling': 'wis',
        'arcana': 'int',
        'athletics': 'str',
        'deception': 'cha',
        'history': 'int',
        'insight': 'wis',
        'intimidation': 'cha',
        'investigation': 'int',
        'medicine': 'wis',
        'nature': 'int',
        'perception': 'wis',
        'performance': 'cha',
        'persuasion': 'cha',
        'religion': 'int',
        'sleight_of_hand': 'dex',
        'stealth': 'dex',
        'survival': 'wis'
    }

    def __init__(self):
        # Load the UI
        super(MainWindow, self).__init__()
        uic.loadUi(Path(__file__).resolve().parent / "form.ui", self)
        # self.centralWidget().setLayout(self.mainLayout)

        # Set the cental widget of all the windows in the MDIArea
        self.initMDIArea()

        self.skills = [
            self.acrobatics,
            self.animal_handling,
            self.arcana,
            self.athletics,
            self.deception,
            self.history,
            self.insight,
            self.intimidation,
            self.investigation,
            self.medicine,
            self.nature,
            self.perception,
            self.performance,
            self.persuasion,
            self.religion,
            self.sleight_of_hand,
            self.stealth,
            self.survival,
        ]
        self.skillsStr = [
            'acrobatics',
            'animal_handling',
            'arcana',
            'athletics',
            'deception',
            'history',
            'insight',
            'intimidation',
            'investigation',
            'medicine',
            'nature',
            'perception',
            'performance',
            'persuasion',
            'religion',
            'sleight_of_hand',
            'stealth',
            'survival',
        ]
        self.skillProfs = [
            self.acrobatics_prof,
            self.animal_handling_prof,
            self.arcana_prof,
            self.athletics_prof,
            self.deception_prof,
            self.history_prof,
            self.insight_prof,
            self.intimidation_prof,
            self.investigation_prof,
            self.medicine_prof,
            self.nature_prof,
            self.perception_prof,
            self.performance_prof,
            self.persuasion_prof,
            self.religion_prof,
            self.sleight_of_hand_prof,
            self.stealth_prof,
            self.survival_prof,
        ]
        self.skillButtons = [
            self.acrobatics_roll,
            self.animal_handling_roll,
            self.arcana_roll,
            self.athletics_roll,
            self.deception_roll,
            self.history_roll,
            self.insight_roll,
            self.intimidation_roll,
            self.investigation_roll,
            self.medicine_roll,
            self.nature_roll,
            self.perception_roll,
            self.performance_roll,
            self.persuasion_roll,
            self.religion_roll,
            self.sleight_of_hand_roll,
            self.stealth_roll,
            self.survival_roll,
        ]
        self.savingThrows = [
            self.wis_saving_throw,
            self.cha_saving_throw,
            self.str_saving_throw,
            self.int_saving_throw,
            self.dex_saving_throw,
            self.con_saving_throw,
        ]
        self.savingThrowsProfs = [
            self.wis_prof,
            self.cha_prof,
            self.str_prof,
            self.int_prof,
            self.dex_prof,
            self.con_prof,
        ]
        self.baseStats = [
            self.wis_base,
            self.cha_base,
            self.str_base,
            self.int_base,
            self.dex_base,
            self.con_base,
        ]
        self.basesStr = [
            'wis',
            'cha',
            'str',
            'int',
            'dex',
            'con',
        ]

        for i in self.skillsStr:
            getattr(self, i + '_roll').setToolTip(self.skillAssociations[i])

        self.setCustomPalettes()
        self.bindSignals()
        self.updateStats()

    def initMDIArea(self):
        # Yes, this is a very weird way of doing things, but the QMdiSubWindow class has a bug somewhere in the
        # Pythonized version, so these all have to be members of the main class so they don't dereference in the
        # C++ code and cause a RuntimeError.

        wins = ('rolls', 'states', 'counters', 'counters_2')
        self._subWindows = dict(zip(wins, [None] * 4))
        self._subWindowWidgets = dict(zip(wins, [None] * 4))
        for win in wins:
            # Re-use the counters layout, just make 2 of them
            self._subWindowWidgets[win] = uic.loadUi(DIR / (('counters' if win == 'counters_2' else win) + "_window.ui"))
            self._subWindows[win] = QMdiSubWindow()
            self._subWindows[win].setWidget(self._subWindowWidgets[win])
            self._subWindows[win].setWindowTitle(win.capitalize())
            # TODO: This doesn't work, find a new way to block closing
            # self._subWindows[win].closeEvent = lambda *args, **kwargs: None
            self.mdiArea.addSubWindow(self._subWindows[win])


        self.rolls = self._subWindowWidgets['rolls'].rolls
        self.rollButton = self._subWindowWidgets['rolls'].rollButton
        self.clearRollsButton = self._subWindowWidgets['rolls'].clearRollsButton
        self.diceBox = self._subWindowWidgets['rolls'].diceBox
        self.count = self._subWindowWidgets['rolls'].count
        self.sides = self._subWindowWidgets['rolls'].sides
        self.additional = self._subWindowWidgets['rolls'].additional
        # self.disadvantage = self._subWindowWidgets['rolls'].disadvantage
        self.advantageBox = self._subWindowWidgets['rolls'].advantageBox

        self.states = self._subWindowWidgets['states']
        self.counters = self._subWindowWidgets['counters']
        self.counters_2 = self._subWindowWidgets['counters_2']

        self.counters.x = 3
        self.counters_2.x = 3

        self.counters.y = 0
        self.counters_2.y = 0

        self.counters.prev = 10
        self.counters_2.prev = 10

        # self.mdiArea.tileSubWindows()
        self.mdiArea.cascadeSubWindows()

        # print([i.widget() for i in self.mdiArea.subWindowList()])

    def setCustomPalettes(self):
        # Set the specific palettes for the big text edit boxes
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Base, QBrush(QPixmap(PAPER_BACKGROUND_2)))
        palette.setBrush(QPalette.ColorRole.PlaceholderText, QColor(60, 60, 60))
        palette.setBrush(QPalette.ColorRole. Text, QColor(30, 30, 30))
        for i in (self.notes, self.rolls, self.inventory, self.spells):
            i.setPalette(palette)

        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
        palette.setBrush(QPalette.ColorRole.Button, QColor(194, 159, 116, 255))
        for i in self.skillButtons:
            i.setPalette(palette)

        palette = QPalette()

    def bindSignals(self):
        self.loadButton.pressed.connect(self.load)
        self.saveButton.pressed.connect(self.save)

        self.editMode.toggled.connect(self.setEditMode)

        self.longRestButton.pressed.connect(self.longRest)
        self.shortRestButton.pressed.connect(self.shortRest)

        # Connect the roll dice triggers
        def rollEntered():
            self.rollDice(self.diceBox.text())
        self.diceBox.returnPressed.connect(rollEntered)
        def rollSelected():
            # [1:] because they all start with a D
            self.rollDice(self.count.value(), int(self.sides.currentText()[1:]), self.additional.value())
        self.rollButton.pressed.connect(rollSelected)
        self.clearRollsButton.pressed.connect(self.rolls.clear)

        # Connect the hit dice line edit
        def rollHitDice():
            self.rollDice(self.hit_dice.text(), roll='Hit Dice')
        self.hit_dice.returnPressed.connect(rollHitDice)

        self.addMoney.pressed.connect(lambda: self.adjustMoney(True))
        self.subMoney.pressed.connect(lambda: self.adjustMoney(False))

        # for cnt in (self.counters, self.counters_2):
            # Bind the reset buttons
            # cnt.reset.pressed.connect(lambda: self.resetCounters(cnt))
            # cnt.amount.valueChanged.connect(lambda to: self.updateCounterAmt(cnt, to))
        self.counters.reset.pressed.connect(lambda: self.resetCounters(self.counters))
        self.counters_2.reset.pressed.connect(lambda: self.resetCounters(self.counters_2))
        self.counters.amount.valueChanged.connect(lambda to: self.updateCounterAmt(self.counters, to))
        self.counters_2.amount.valueChanged.connect(lambda to: self.updateCounterAmt(self.counters_2, to))

        def updateAdvantageName(state):
            if state == Qt.CheckState.Checked:
                self.advantageBox.setText('Roll with Advantage')
            elif state == Qt.CheckState.PartiallyChecked:
                self.advantageBox.setText('Roll with Disadvantage')
            elif state == Qt.CheckState.Unchecked:
                self.advantageBox.setText('Regular Roll')
            else:
                unreachableState()
        self.advantageBox.stateChanged.connect(updateAdvantageName)

        # Connect all the auto-roll buttons that look like labels
        for i in self.skillsStr:
            getattr(self, i + '_roll').pressed.connect(FunctionCall(lambda var: self.rollDice(1, 20, getattr(self, var).value(), roll=var.capitalize()+' Check'), (i,)))
            getattr(self, i + '_prof').clicked.connect(self.updateStats)

        # Connect the saving throw buttons
        for k in self.basesStr:
            getattr(self, k + '_save').pressed.connect(FunctionCall(lambda var: self.rollDice(1, 20, getattr(self, var + '_saving_throw').value(), roll=var.capitalize()+' Saving Throw'), (k,)))
            getattr(self, k + '_base').valueChanged.connect(self.updateStats)
            getattr(self, k + '_prof').clicked.connect(self.updateStats)

    def updateStats(self, _=None):
        for stat in self.basesStr:
            # Set all the stat bonuses
            base = getattr(self, stat + '_base').value()
            bonus = ((base - 10) // 2)
            getattr(self, stat + '_bonus').setValue(bonus)

            # Set the saving throws
            if getattr(self, stat + '_prof').isChecked():
                bonus += self.proficiency_bonus.value()
            getattr(self, stat + '_saving_throw').setValue(bonus)

        for skill in self.skillsStr:
            val = getattr(self, self.skillAssociations[skill] + '_bonus').value()
            if getattr(self, skill + '_prof').isChecked():
                val += self.proficiency_bonus.value()
            getattr(self, skill).setValue(val)

    def resetCounters(self, counterWidget):
        # Get all the attributes in counterWidget that start with "checkBox" and set them to whatever the start checkbox is set to
        to = counterWidget.start.isChecked()
        for attr in dir(counterWidget):
            if attr.startswith('checkBox'):
                getattr(counterWidget, attr).setChecked(to)

    def updateCounterAmt(self, counterWidget, newAmt):
        def nextStep(x, y, dir=1):
            newx = x
            newy = y

            if (x if dir > 0 else y) == 0:
                if dir > 0:
                    newx = y + 1
                    newy = 0
                else:
                    newx = 0
                    newy = x - 1
            else:
                if x > y:
                    newy += dir
                elif x < y:
                    newx -= dir
                else:
                    if dir > 0:
                        newy += dir
                    else:
                        newx += dir
            return newx, newy

        x, y = nextStep(counterWidget.x, counterWidget.y, newAmt - counterWidget.prev)
        debug(counterWidget.prev)
        debug(newAmt)
        debug((counterWidget.x, counterWidget.y), 'current pos')
        debug((x, y), 'new pos')

        if newAmt > counterWidget.prev:
            if (widget := counterWidget._checkBoxLayout.itemAtPosition(x, y)) is not None:
                widget.widget().show()
            else:
                box = QCheckBox()
                box.setObjectName(f'checkBox_{newAmt}')
                counterWidget._checkBoxLayout.addWidget(box, x, y)
        elif newAmt < counterWidget.prev:
            # Don't go less than 1 counter -- this shouldn't ever happen
            if newAmt <= 1:
                return
            if (widget := counterWidget._checkBoxLayout.itemAtPosition(x, y)) is not None:
                widget.widget().hide()
            else:
                debug('error')
            # widget = counterWidget._checkBoxLayout.itemAtPosition(x, y)
            # if widget is not None:
                # counterWidget._checkBoxLayout.removeWidget(widget.widget())
        else:
            debug('...thats not how that works...', clr=-1)

        counterWidget.prev = newAmt
        counterWidget.x = x
        counterWidget.y = y

    @staticmethod
    def setPrefix(widget:'QSpinBox'):
        val = widget.value()
        if val > 0:
            widget.setPrefix('+')
        elif val < 0:
            widget.setPrefix('-')
        else:
            widget.setPrefix('')

    def longRest(self):
        self.current_hp.setValue(self.base_hp.value())

    def shortRest(self):
        self.current_hp.setValue(min(self.rollDice(debug(self.hit_dice.text(), 'thing'), roll='Short Rest HP') + self.current_hp.value(), self.base_hp.value()))

    def _parseDiceCode(self, code:str):
        if code == '':
            return 1, 20, 0
        match = self.diceRegex.match(code)
        debug(match)
        if match is None:
            return None
        else:
            count = match.group('count')
            additional = match.group('additional')
            if count is None:
                count = 1
            if additional is None:
                additional = 0
            try:
                return int(count), int(match.group('sides')), int(additional)
            except Exception as err:
                debug(err)
                return None

    def rollDice(self, code_or_count:(str, int), sides:int=None, additional:int=0, advantage=None, disadvantage=None, roll=''):
        def checkCrit(r):
            if sides == 20:
                if r == 20:
                    QMessageBox(QMessageBox.Icon.NoIcon, 'Critical Roll!', f'You rolled a natural 20{f" on your {roll}" if roll != "" else ""}!', QMessageBox.StandardButton.Yes, self).show()
                elif r == 1:
                    QMessageBox(QMessageBox.Icon.NoIcon, 'Critical Fail!', f'You rolled a natural 1{f" on your {roll}" if roll != "" else ""}!', QMessageBox.StandardButton.Ok, self).show()
            return r

        # Parse the parameters
        if disadvantage and advantage:
            raise ParameterError
        if advantage is None:
            advantage = self.advantageBox.checkState() == Qt.CheckState.Checked
        if disadvantage is None:
            disadvantage = self.advantageBox.checkState() == Qt.CheckState.PartiallyChecked
        if sides is None:
            parsed = self._parseDiceCode(code_or_count)
            if parsed is None:
                self.rolls.addItem('Invalid Dice Code')
                if self.rolls.count() > self.MAX_ROLLS_HISTORY:
                    self.rolls.takeItem(0)
                return 0
            else:
                count, sides, additional = parsed
        else:
            count = code_or_count

        log = f'{roll}{": " if roll != "" else ""}{count}D{sides}{f"+{additional}" if additional else ""} '

        result = sum([random.randint(1, sides) for _ in range(count)])
        if advantage or disadvantage:
            result2 = sum([random.randint(1, sides) for _ in range(count)])
            result1 = result
            result = (max if advantage else min)(result1, result2)
            log += f'{"with Advantage" if advantage else "with Disadvantage"} -> {result1}, {result2} = {checkCrit(result) + additional}'
        else:
            log += f' -> {checkCrit(result) + additional}'



        self.rolls.addItem(log)
        if self.rolls.count() > self.MAX_ROLLS_HISTORY:
            self.rolls.takeItem(0)
        # self.rolls.scrollTo(self.rolls.indexAt(QPoint(0, -1)), QAbstractItemView.PositionAtBottom)

        return result

    def adjustMoney(self, add):
        def convert2coppers(amt, type):
            if type == 'Platinum':
                return amt * 1000
            elif type == 'Gold':
                return amt * 100
            elif type == 'Electrum':
                return amt * 50
            elif type == 'Silver':
                return amt * 10
            elif type == 'Copper':
                return amt

        amt = self.moneyAdjust.value()
        if not add:
            amt *= -1
        type = self.moneyType.currentText()
        copper = self.copper.value()
        copper += self.silver.value() * 10
        copper += self.gold.value() * 100
        copper += self.platinum.value() * 1000

        copper += convert2coppers(amt, type)

        if copper < 0:
            amt *= -1
            QMessageBox.warning(self, 'Out of Money', f'You don\'t have {amt} {type}', QMessageBox.StandardButton.Ok)
            copper += convert2coppers(amt, type)


        self.platinum.setValue(copper // 1000)
        copper %= 1000
        self.gold.setValue(copper // 100)
        copper %= 100
        self.silver.setValue(copper // 10)
        copper %= 10
        self.copper.setValue(copper)

    def load(self):
        with open(self.getFile(save=False), 'r') as f:
            j = json.load(f)
            self.setAvailableFromJson(j)

    def save(self):
        name = self.name.text()
        file = self.getFile(save=True) if name == '' else name + '.json'
        if file is not None and file != '':
            with open(file, 'w') as f:
                j = {}
                for i in self.jsonAttrs:
                    self.attr2json(i, j)
                json.dump(j, f, indent=4)

    def attr2json(self, attr, json):
        try:
            val = getattr(self, attr).value()
        except AttributeError:
            try:
                val = getattr(self, attr).isChecked()
            except AttributeError:
                val = getattr(self, attr).toPlainText()

        json.update({attr: val})

    def setAvailableFromJson(self, json):
        for key, val in json.items():
            var = getattr(self, key, None)
            if var is not None:
                try:
                    var.setValue(val)
                except:
                    try:
                        var.setChecked(val)
                    except:
                        try:
                            var.setText(val)
                        except:
                            print(f'unable to set {key}')

    def getFile(self, save=True):
        # Promts the user for a filepath
        if save:
            file = QFileDialog.getSaveFileName(self,
                    caption='Save Your Character',
                    filter="*.json, *.jsonc",
                    initialFilter="*.json, *.jsonc"
                )[0]
        else:
            file = QFileDialog.getOpenFileName(self,
                caption='Open a Character',
                filter="*.json *.jsonc",
                initialFilter="*.json *.jsonc"
            )[0]

        if file != '' and file is not None:
            if not file.endswith(('.json', '.jsonc')):
                file = file + '.json'

        return file

    def setEditMode(self, to):
        for i in self.savingThrowsProfs + self.skillProfs:
            i.setEnabled(to)

        # self.savingThrows
        # self.skills
        for i in self.baseStats + [self.proficiency_bonus, self.base_hp, self.speed]:
            i.setReadOnly(not to)
            i.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus if to else QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.hit_dice.setReadOnly(not to)
        self.level.setReadOnly(not to)

        self.updateStats()

    def closeEvent(self, a0):
        if not __DEBUG__:
            self.save()
        return super().closeEvent(a0)



class Style(QProxyStyle):
    def __init__(self, *args, **kwargs):
        self.framePixmap = QPixmap(FRAME_PATH)
        self.paperPixmap = QPixmap(PAPER_BACKGROUND_2)
        super().__init__(*args, **kwargs)

    def drawPrimitive(self, element:'PrimitiveElement', option:'QStyleOption', painter:'QPainter', widget:'QWidget'):
        if element == QStyle.PrimitiveElement.PE_FrameGroupBox and widget is not None:
            # debug('drawing frame!')
            # painter.fillRect(2, 2, 2, 2, QColor('red'))
            self.drawItemPixmap(painter, widget.rect(), 0, self.paperPixmap.scaled(widget.size(), Qt.AspectRatioMode.IgnoreAspectRatio))
            self.drawItemPixmap(painter, widget.rect(), 0, self.framePixmap.scaled(widget.size(), Qt.AspectRatioMode.IgnoreAspectRatio))

        # elif element == QStyle.PrimitiveElement.PE_Frame and widget is not None:
            # if element == QStyle.PrimitiveElement.PE_FrameMenu and widget is not None:
                # debug()
                # self.drawItemPixmap(painter, widget.rect(), 0, self.background.scaled(widget.size(), Qt.AspectRatioMode.IgnoreAspectRatio))
                # self.drawItemPixmap(painter, widget.rect(), 0, self.background)

        else:
            super().drawPrimitive(element, option, painter, widget)

    # drawItemText(), drawItemPixmap(), drawPrimitive(), drawControl(), drawComplexControl()
    def drawItemPixmap(self, painter, rect, alignment, pixmap):
        super().drawItemPixmap(painter, rect, alignment, pixmap)


def generateStyle():
    # print(QStyleFactory.keys())
    # style = QStyleFactory.create('Fusion')
    # style = QCommonStyle()

    return Style()

def generatePalette(size):
    dark = QColor(30, 30, 30)
    light = QColor(235, 235, 235)
    mid = QColor(115, 123, 131)
    red = QColor('red')
    # palette = QPalette(dark,  # windowText
    #                    dark,  # button
    #                    light, # light
    #                    dark,  # dark
    #                    mid,   # mid
    #                    dark,  # text
    #                    light, # bright_text
    #                    dark,  # base
    #                    QColor('red') # window
    # )
    palette = QPalette()

    # Set the main window background
    palette.setBrush(QPalette.ColorRole.Background, QBrush(QPixmap(BACKGROUND_IMAGE_PATH).scaled(size, Qt.AspectRatioMode.IgnoreAspectRatio)))

    # palette.setBrush(QPalette.ColorRole.Window, )
    palette.setBrush(QPalette.ColorRole.WindowText, dark)
    palette.setBrush(QPalette.ColorRole.Base, dark)
    # palette.setBrush(QPalette.ColorRole.AlternateBase, red)
    palette.setBrush(QPalette.ColorRole.PlaceholderText, mid)
    palette.setBrush(QPalette.ColorRole.Text, light)
    palette.setBrush(QPalette.ColorRole.Button, dark)
    palette.setBrush(QPalette.ColorRole.ButtonText, light)
    # palette.setBrush(QPalette.ColorRole.BrightText, QColor('red'))
    # palette.setBrush(QPalette.ColorRole., QColor('red'))

    return palette


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    QApplication.setStyle(generateStyle())
    QApplication.setPalette(generatePalette(widget.size()))
    widget.show()
    sys.exit(app.exec_())
