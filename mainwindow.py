# This Python file uses the following encoding: utf-8
import collections
import copy
import multiprocessing
import os
import random
import re
import sys
import tkinter as tk
from collections import deque
from threading import Thread
from time import sleep

from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QBrush, QCloseEvent, QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)

from HOF import HOF_Hanover as HOF_KMBHan
from HOF import ericcode
from stop_name_encoder import (
    decode_stop_name,
    encode_stop_name,
    get_ui_values_from_name,
    update_stop_name_from_ui,
)
from ui_AddBusStop import Ui_MainWindow as AddBusStop_UI
from ui_AddDDU import Ui_MainWindow as AddDDU_UI
from ui_AddRouteEntry import Ui_MainWindow as AddRouteEntry_UI
from ui_AddTermini import Ui_MainWindow as AddTermini_UI
from ui_dialog import Ui_Dialog as EricGuesser_UI
from ui_EditEnMasse import Ui_MainWindow as EditEnMasse_UI

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from ui_HOFView import Ui_MainWindow as HOFView_Ui_MainWindow
from ui_PrefWin import Ui_MainWindow as PrefWin_UI
from ui_Welc import Ui_MainWindow as Entrypoint_Ui_MainWindow

global build_with_genLED
build_with_genLED = False


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def search_in_slice(sliceee, name):
    for index, stop in enumerate(sliceee):
        if stop.name == name:
            return stop, index
    return None, -1


class ObservableList(list):
    def __init__(self, *args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def _notify(self):
        if self.callback:
            self.callback()

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self._notify()

    def append(self, value):
        super().append(value)
        self._notify()

    def extend(self, iterable):
        super().extend(iterable)
        self._notify()

    def insert(self, index, value):
        super().insert(index, value)
        self._notify()

    def remove(self, value):
        super().remove(value)
        self._notify()

    def pop(self, index=-1):
        value = super().pop(index)
        self._notify()
        return value

    def clear(self):
        super().clear()
        self._notify()

    def __delitem__(self, index):
        super().__delitem__(index)
        self._notify()

    def __iadd__(self, other):
        result = super().__iadd__(other)
        self._notify()
        return result

    def __imul__(self, other):
        result = super().__imul__(other)
        self._notify()
        return result


# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.ui = HOFView_Ui_MainWindow()
#         self.ui.setupUi(self)
class Main(QMainWindow):
    hof_class = HOF_KMBHan()
    opened_windows = []
    export_path = ""
    hofname = ""
    # bus_rt_direction = 1
    # cross_method_dataqueue = ObservableList([None for _ in range(50)], callback=None)
    # head_index = 0
    # tail_index = 0
    cur_instance = None
    cross_method_datum = deque([Signal(int) for _ in range(1)], maxlen=50)
    stopreporter_genlist = []
    # def __init__(self, parent=None):
    #     super().__init__(parent)
    #     self.cross_method_dataqueue = ObservableList([None for _ in range(50)], callback=self.indexIncrement)
    #     self.head_index = 0
    #     self.tail_index = 0
    # def indexIncrement(self):
    #     # self.current_data_queue_index += 1
    #     # self.current_data_queue_index %= 50
    #     # self.next_queue_index +=1
    #     # self.next_queue_index %= 50

    @staticmethod
    def test_error_codes(a):
        case = {
            989: "Failed to load HOF file. Your HOF is not in UTF-8 and has ASCII non-complient charcters. Convert to UTF-8 and try again.",
            990: "Telargo entries are not supported. Please remove or convert them and try again.",
        }
        if a in case:
            QMessageBox.warning(None, "Error", case[a], QMessageBox.Ok)  # type: ignore

    @staticmethod
    def exhaust_guesses(code):
        """Exhausts all guesses of the eric code, returns a list of all guesses with reasonableness scores"""
        mapping = {
            "a": 11,
            "b": 12,
            "c": 13,
            "d": 21,
            "e": 22,
            "f": 23,
            "g": 31,
            "h": 32,
            "i": 33,
            "j": 41,
            "k": 42,
            "l": 43,
            "m": 51,
            "n": 52,
            "o": 53,
            "p": 61,
            "q": 62,
            "r": 63,
            "s": 71,
            "t": 72,
            "u": 73,
            "v": 81,
            "w": 82,
            "x": 83,
            "y": 91,
            "z": 92,
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
        }

        # Create reverse mapping for decoding
        reverse_mapping = {v: k for k, v in mapping.items()}

        def decode_recursive(remaining_code):
            if not remaining_code:
                return [""]

            results = []

            # Try interpreting first character as single digit
            if remaining_code[0].isdigit():
                digit = int(remaining_code[0])
                if digit in reverse_mapping:
                    char = reverse_mapping[digit]
                    for suffix in decode_recursive(remaining_code[1:]):
                        results.append(char + suffix)

            # Try interpreting first two characters as letter code
            if len(remaining_code) >= 2 and remaining_code[:2].isdigit():
                two_digit = int(remaining_code[:2])
                if (
                    two_digit in reverse_mapping
                    and reverse_mapping[two_digit].isalpha()
                ):
                    char = reverse_mapping[two_digit].upper()
                    for suffix in decode_recursive(remaining_code[2:]):
                        results.append(char + suffix)

            return results

        def calculate_reasonableness(result):
            """Calculate reasonableness percentage based on letter/digit patterns"""
            if not result:
                return 50

            # Analyze segments of consecutive letters/digits
            segments = []
            current_type = None
            current_length = 0

            for char in result:
                char_type = "letter" if char.isalpha() else "digit"
                if char_type == current_type:
                    current_length += 1
                else:
                    if current_type is not None:
                        segments.append((current_type, current_length))
                    current_type = char_type
                    current_length = 1

            if current_type is not None:
                segments.append((current_type, current_length))

            # Calculate score
            score = 100

            # Penalize transitions between letters and digits
            num_transitions = len(segments) - 1
            score -= num_transitions * 12

            # Bonus for common patterns
            if len(segments) == 1:
                if segments[0][0] == "letter":
                    score += 25  # All letters (like "CTB")
                else:
                    score += 15  # All digits
            elif len(segments) == 2:
                if segments[0][0] == "digit" and segments[1][0] == "letter":
                    score += 10  # Digits then letters (like "289YZ")

            # Heavy penalty for letters in middle of digit sequences
            for i in range(1, len(segments) - 1):
                if (
                    segments[i][0] == "letter"
                    and segments[i][1] == 1
                    and segments[i - 1][0] == "digit"
                    and segments[i + 1][0] == "digit"
                ):
                    score -= 50  # Letter surrounded by digits (bad pattern)

            return max(0, min(100, score))

        # Get all possible decodings
        all_guesses = decode_recursive(code)
        unique_guesses = list(set(all_guesses))

        # Add reasonableness scores
        scored_guesses = []
        for guess in unique_guesses:
            score = calculate_reasonableness(guess)
            scored_guesses.append((guess, score))

        # Sort by reasonableness (highest first)
        scored_guesses.sort(key=lambda x: x[1], reverse=True)

        return scored_guesses

    @staticmethod
    def maybeSave(lst: list) -> bool:
        if any(lst):
            ret = QMessageBox.warning(
                None,
                "Application",
                "The document has been modified.\nDo you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )  # type: ignore
            if ret == QMessageBox.Save:  # type: ignore
                return True
            elif ret == QMessageBox.Cancel:  # type: ignore
                return False
        return True

    @staticmethod
    def fileexplorer() -> str:

        path_Selected = QFileDialog.getExistingDirectory(
            None, "Select Directory", "C:\\"
        )

        return path_Selected

    @staticmethod
    def raise_unimplemented() -> None:
        message = QMessageBox()
        message.setMinimumSize(200, 100)
        message.setWindowTitle("Error")
        message.setText("This feature is not yet implemented.")
        message.setIcon(QMessageBox.Critical)  # type: ignore
        message.setStandardButtons(QMessageBox.Ok)  # type: ignore
        message.exec()

    class PrefWin(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = PrefWin_UI()
            self.ui.setupUi(self)
            self.ui.lineEdit.setText(Main.export_path)
            self.ui.lineEdit.textChanged.connect(self.set_path)
            self.ui.lineEdit_2.setText(Main.hofname)
            self.ui.lineEdit_2.textChanged.connect(
                lambda: setattr(Main, "hofname", self.ui.lineEdit_2.text())
            )
            self.ui.toolButton.clicked.connect(self.fileexplorer)
            # Read actual handrail flag from HOF class and sync with checkbox
            self.ui.checkBox.setChecked(not Main.hof_class.handrail_flag)
            self.ui.checkBox.stateChanged.connect(self.update_handrail_flag)

        def update_handrail_flag(self):
            Main.hof_class.handrail_flag = not self.ui.checkBox.isChecked()

        def closewindow(self):
            self.close()

        def fileexplorer(self):
            Main.export_path = QFileDialog.getExistingDirectory(
                self, "Select Directory", "C:\\"
            )
            self.ui.lineEdit.setText(Main.export_path)

        def set_path(self):
            Main.export_path = self.ui.lineEdit.text()

    class Entrypoint(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = Entrypoint_Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.actionOpen_Project_Folder.triggered.connect(self.open_db)
            self.ui.actionOpen_HOF.triggered.connect(self.open_hof)
            self.ui.pushButton.clicked.connect(self.open_hof)
            self.ui.pushButton_2.clicked.connect(self.open_db)
            # self.ui.pushButton_3.clicked.connect(self.open_globalcfg) Goodbye Map Import
            self.ui.pushButton_4.clicked.connect(self.create_blank_hof)

        def open_db(self):
            Main.hof_class = HOF_KMBHan()
            file = QFileDialog.getOpenFileName(
                self, "Open Database", "C:\\", "Database Files (*.db)"
            )
            if file[0]:
                Main.hof_class.load_from_db(file[0])
                Main.opened_windows.append(Main.HOFView())
                Main.opened_windows[-1].show()
                Main.hofname = file[0].split("/")[-1].removesuffix(".db")
                Main.export_path = file[0].removesuffix(Main.hofname + ".db")
                self.close()

        def open_hof(self):
            Main.hof_class = HOF_KMBHan()
            file = QFileDialog.getOpenFileName(
                self, "Open HOF", "C:\\", "HOF Files (*.hof)"
            )
            if file[0]:
                a = Main.hof_class.load_from_hof(file[0])
                Main.test_error_codes(a)
                # considering that the load_from_hof function can fail due to encoding issues, we should check its return value before proceeding
                Main.opened_windows.append(Main.HOFView())
                Main.opened_windows[-1].show()
                Main.hofname = file[0].split("/")[-1].removesuffix(".hof")
                self.close()

        def open_globalcfg(self):
            Main.raise_unimplemented()

        def create_blank_hof(self):
            Main.hof_class = HOF_KMBHan()
            # Main.hof_class.create_blank_hof()
            Main.opened_windows.append(Main.HOFView())
            Main.opened_windows[-1].show()
            Main.hofname = "New HOF"
            self.close()

        def closewindow(self):
            self.close()

    class HOFView(QMainWindow):
        bus_rt_direction = 1
        closed = Signal()

        def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = HOFView_Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowTitle(f"HOF Viewer - {Main.hofname}")
            self.stop_name_to_id_map = {
                stop.name: stop.busstopID for stop in Main.hof_class.stopreporter
            }
            # for i in Main.hof_class.stopreporter:
            #     self.ui.listWidget_3.addItem(i.name) #stopreporter
            # for i in Main.hof_class.ddu:
            #     self.ui.listWidget_4.addItem(i.RTNO) #ddu
            # for i in Main.hof_class.termini:
            #     self.ui.listWidget_5.addItem(ericcode(i.eric).retstr()) #termini
            # for i in Main.hof_class.infosystem:
            #     self.ui.listWidget_2.addItem(i.route) #infosystem
            # self.ui.listWidget_3.addItems([i.name for i in Main.hof_class.stopreporter])
            # for each in Main.hof_class.stopreporter:
            # item = QListWidgetItem(each.name)
            # print(f"Adding item: {each.name} with ID: {each.busstopID}")
            # self.ui.listWidget_3.addItem(item)
            # print(f"Stopreporter: {[i.name for i in Main.hof_class.stopreporter]}")

            self.busstop_id_to_index = {}
            self.add_bs_to_dict()
            Main.stopreporter_genlist = [
                "" for _ in range(len(Main.hof_class.stopreporter))
            ]
            self.ui.listWidget_4.addItems([i.RTNO for i in Main.hof_class.ddu])
            self.ui.listWidget_5.addItems(
                [i.destination for i in Main.hof_class.termini]
            )
            self.ui.listWidget_2.addItems([i.route for i in Main.hof_class.infosystem])
            self.ui.actionExport_HOF.triggered.connect(self.export_hof)
            self.ui.actionSave_to_DB.triggered.connect(self.save)
            self.ui.actionPreferences.triggered.connect(self.open_pref)
            self.ui.actionGenerate_8w_6w_LCD.triggered.connect(self.generate_8w_6w_LCD)
            self.ui.actionGenerate_DPIPv2.triggered.connect(self.generate_8w_6w_LCD)
            self.ui.actionOpen_global_cfg.triggered.connect(
                lambda: Main.raise_unimplemented()
            )
            self.ui.actionOpen_HOF.triggered.connect(self.reopen_hof)
            self.ui.actionOpen_Project_Folder.triggered.connect(self.open_db)
            self.ui.actionOpen_TTL_for_Route.triggered.connect(
                lambda: Main.raise_unimplemented()
            )
            self.ui.actionEric_Guesser.triggered.connect(self.open_eric_guesser)
            self.ui.actionExport_HOF_v2.triggered.connect(self.export_hof_v2)
            self.ui.actionReset_Busstop_List_IDs.triggered.connect(self.reset_bsl_ids)
            self.ui.actionEdit_En_Masse.triggered.connect(self.open_edit_en_masse)
            # self.ui.act
            # ----                               ----#
            # thread = Thread(target=self.update_listviews_every_3_minutes)
            # thread.start()
            # self.update_listviews_every_3_minutes() # Probably not needed anymore
            # ----Termini, DDU, Stopreporter Part----#
            self.ui.listWidget_3.doubleClicked.connect(self.open_bs_lw3)
            self.ui.listWidget_4.doubleClicked.connect(self.open_ddu)
            self.ui.listWidget_5.doubleClicked.connect(self.open_termini)

            self.ui.pushButton_3.clicked.connect(lambda: self.add_stuff(1))
            self.ui.pushButton_7.clicked.connect(lambda: self.add_stuff(2))
            self.ui.pushButton_14.clicked.connect(lambda: self.add_stuff(3))

            self.ui.pushButton_5.clicked.connect(lambda: self.delete_stuff(1))
            self.ui.pushButton_8.clicked.connect(lambda: self.delete_stuff(2))
            self.ui.pushButton_15.clicked.connect(lambda: self.delete_stuff(3))

            self.ui.pushButton_11.clicked.connect(lambda: self.duplicate_stuff(1))
            self.ui.pushButton_13.clicked.connect(lambda: self.duplicate_stuff(2))
            self.ui.pushButton_16.clicked.connect(lambda: self.duplicate_stuff(3))

            self.ui.pushButton_23.clicked.connect(lambda: self.sort_stuff(1))
            self.ui.pushButton_22.clicked.connect(lambda: self.sort_stuff(2))
            self.ui.pushButton_21.clicked.connect(lambda: self.sort_stuff(3))

            # ----Infosystem Part----#
            # self.ui.listWidget_2.itemSelectionChanged.connect(self.change_rt_info)
            self.ui.listWidget_2.itemSelectionChanged.connect(self.get_bsl)

            # self.ui.listWidget_2.itemSelectionChanged.connect(self.dirchange_Y) # shit change
            self.ui.pushButton.clicked.connect(self.dirchange_Y)
            self.ui.pushButton_2.clicked.connect(self.dirchange_Z)
            self.ui.listWidget.doubleClicked.connect(self.open_bs)
            self.ui.listWidget_2.doubleClicked.connect(self.open_rt)
            self.ui.pushButton_9.clicked.connect(lambda: self.add_stuff(4))
            self.ui.pushButton_10.clicked.connect(lambda: self.delete_stuff(4))
            self.ui.pushButton_12.clicked.connect(lambda: self.duplicate_stuff(4))
            self.ui.pushButton_4.clicked.connect(self.add_bs_from_sel)
            self.ui.pushButton_6.clicked.connect(self.del_bs_from_sel)
            self.ui.pushButton_20.clicked.connect(self.change_bs_FromSel)
            self.ui.toolButton_4.clicked.connect(self.bsl_goup)
            self.ui.toolButton_3.clicked.connect(self.bsl_godown)
            self.ui.toolButton_5.clicked.connect(self.termini_goup)
            self.ui.toolButton_6.clicked.connect(self.termini_godown)
            self.ui.toolButton_7.clicked.connect(self.ddu_goup)
            self.ui.toolButton_8.clicked.connect(self.ddu_godown)
            self.ui.toolButton_15.clicked.connect(self.routes_goup)
            self.ui.toolButton_16.clicked.connect(self.routes_godown)
            self.ui.pushButton_18.clicked.connect(self.check_bsl_validity)
            self.ui.pushButton_24.clicked.connect(self.check_all_bsl_validity)
            # self.ui.pushButton_5
            # ----Ctrl+S Shortcut----#
            self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
            self.shortcut.activated.connect(self.save)
            self.ui.Search.textChanged.connect(self.filter_bus_stops)

        def add_stuff(self, stuff: int):
            dct = {
                1: (Main.hof_class.stopreporter, self.ui.listWidget_3),
                2: (Main.hof_class.ddu, self.ui.listWidget_4),
                3: (Main.hof_class.termini, self.ui.listWidget_5),
                4: (Main.hof_class.infosystem, self.ui.listWidget_2),
            }
            if stuff == 1:
                lenth = len(Main.hof_class.stopreporter)
                Main.hof_class.add_stopreporter(
                    f"NS{lenth}", "New Stop", 0, 0, 0, -1.0, -1.0
                )
                Main.opened_windows.append(
                    Main.AddBusStop(
                        None,
                        f"NS{lenth}",
                        "New Stop",
                        0,
                        0,
                        0,
                        -1.0,
                        -1.0,
                        curindex=lenth,
                    )
                )
                Main.opened_windows[-1].show()
                new_item = QListWidgetItem(f"NS{lenth}")
                query = self.ui.Search.toPlainText().strip()
                if query:
                    new_item.setHidden(not self._fuzzy_match(query, f"NS{lenth}"))
                dct[stuff][1].addItem(new_item)
                self.reload_bslist_id()
            elif stuff == 2:
                lenth = len(Main.hof_class.ddu)
                Main.hof_class.add_ddu(
                    f"RT{lenth}", "Outbound", "Inbound", -1.0, -1.0, 0, 0
                )
                Main.opened_windows.append(
                    Main.AddDDU(
                        None,
                        f"RT{lenth}",
                        "Outbound",
                        "Inbound",
                        -1.0,
                        -1.0,
                        0,
                        0,
                        curindex=lenth,
                    )
                )
                Main.opened_windows[-1].show()
                dct[stuff][1].addItem(f"RT{lenth}")
            elif stuff == 3:
                lenth = len(Main.hof_class.termini)
                Main.hof_class.add_terminus(False, f"{lenth}A", "", "", [], f"{lenth}B")
                Main.opened_windows.append(
                    Main.AddTermini(None, f"{lenth}A", "", "", [], curindex=lenth)
                )
                Main.opened_windows[-1].show()
                dct[stuff][1].addItem(f"{lenth}A")
            elif stuff == 4:
                lenth = len(Main.hof_class.infosystem)
                Main.hof_class.add_infosystem(
                    False, False, f"R{lenth}", "Outbound", "Inbound", [], []
                )
                Main.opened_windows.append(
                    Main.AddRouteEntry(
                        None, False, f"R{lenth}", "Outbound", "Inbound", curindex=lenth
                    )
                )
                dct[stuff][1].addItem(f"R{lenth}")

        def duplicate_stuff(self, stuff: int):
            # dct = {
            #     1: (Main.hof_class.stopreporter, self.ui.listWidget_3),
            #     2: (Main.hof_class.ddu, self.ui.listWidget_4),
            #     3: (Main.hof_class.termini, self.ui.listWidget_5),
            #     4: (Main.hof_class.infosystem, self.ui.listWidget_2)
            # }
            if stuff == 1:
                ite = self.ui.listWidget_3.currentIndex()
                index = ite.row()
                if index < 0 or index >= len(Main.hof_class.stopreporter):
                    return
                original = Main.hof_class.stopreporter[index]
                new_item = copy.deepcopy(original)
                new_item.busstopID = "".join(
                    [chr((ord(i) + random.randint(0, 9))) for i in new_item.busstopID]
                )
                new_item.name = f"{new_item.name}_"
                Main.hof_class.stopreporter.insert(index, new_item)
                lw_item = QListWidgetItem(new_item.name)
                query = self.ui.Search.toPlainText().strip()
                if query:
                    lw_item.setHidden(not self._fuzzy_match(query, new_item.name))
                self.ui.listWidget_3.insertItem(index, lw_item)

                # Keep reverse lookups in sync without a full reload/get_bsl refresh.
                for key, value in list(self.busstop_id_to_index.items()):
                    if value >= index:
                        self.busstop_id_to_index[key] = value + 1
                self.busstop_id_to_index[new_item.busstopID] = index
                self.stop_name_to_id_map[new_item.name] = new_item.busstopID
            elif stuff == 2:
                ite = self.ui.listWidget_4.currentIndex()
                index = ite.row()
                original = Main.hof_class.ddu[index]
                new_item = copy.deepcopy(original)
                Main.hof_class.ddu.insert(index, new_item)
                self.ui.listWidget_4.insertItem(index, new_item.RTNO)
            elif stuff == 3:
                ite = self.ui.listWidget_5.currentIndex()
                index = ite.row()
                original = Main.hof_class.termini[index]
                new_item = copy.deepcopy(original)
                Main.hof_class.termini.insert(index, new_item)
                self.ui.listWidget_5.insertItem(index, new_item.eric)
            elif stuff == 4:
                ite = self.ui.listWidget_2.currentIndex()
                index = ite.row()
                original = Main.hof_class.infosystem[index]
                new_item = copy.deepcopy(original)
                Main.hof_class.infosystem.insert(index, new_item)
                self.ui.listWidget_2.insertItem(index, new_item.route)

            # elif stuff == 2:
            #     ite = self.ui.listWidget_4.currentIndex()
            #     index = ite.row()
            #     original = Main.hof_class.ddu[index]
            #     new_item = type(original)(**original.__dict__)  # Create a new instance with the same attributes
            #     Main.hof_class.ddu.insert(index, new_item)
            #     self.ui.listWidget_4.insertItem(index, new_item.RTNO)
            # elif stuff == 3:
            #     ite = self.ui.listWidget_5.currentIndex()
            #     index = ite.row()
            #     original = Main.hof_class.termini[index]
            #     new_item = type(original)(**original.__dict__)  # Create a new instance with the same attributes
            #     Main.hof_class.termini.insert(index, new_item)
            #     self.ui.listWidget_5.insertItem(index, new_item.eric)
            # elif stuff == 4:
            #     ite = self.ui.listWidget_2.currentIndex()
            #     index = ite.row()
            #     original = Main.hof_class.infosystem[index]
            #     new_item = type(original)(**original.__dict__)  # Create a new instance with the same attributes
            #     Main.hof_class.infosystem.insert(index, new_item)
            #     self.ui.listWidget_2.insertItem(index, new_item.route)

        def add_bs_to_dict(self) -> None:
            query = (
                self.ui.Search.toPlainText().strip()
                if hasattr(self.ui, "Search")
                else ""
            )
            for i, stop in enumerate(Main.hof_class.stopreporter):
                item = QListWidgetItem(stop.name)
                item.setData(
                    Qt.ItemDataRole.UserRole, stop.busstopID
                )  # Store the busstopID
                if query:
                    item.setHidden(not self._fuzzy_match(query, stop.name))
                self.ui.listWidget_3.addItem(item)
                # Create reverse lookup
                self.busstop_id_to_index[stop.busstopID] = i

        @staticmethod
        def _fuzzy_match(query: str, text: str) -> bool:
            """Return True if query matches text via substring or subsequence."""
            q = query.lower()
            t = text.lower()
            if q in t:
                return True
            # subsequence match
            it = iter(t)
            return all(c in it for c in q)

        def filter_bus_stops(self):
            query = self.ui.Search.toPlainText().strip()
            for i in range(self.ui.listWidget_3.count()):
                item = self.ui.listWidget_3.item(i)
                if item is None:
                    continue
                if query:
                    item.setHidden(not self._fuzzy_match(query, item.text()))
                else:
                    item.setHidden(False)

        def generate_8w_6w_LCD(self):
            if not build_with_genLED:
                QMessageBox.warning(
                    self,
                    "Error",
                    "This version of the program does not have the LED generator.",
                    QMessageBox.Ok,
                )  # type: ignore
            else:
                Main.raise_unimplemented()

        def reopen_hof(self):
            # Close all opened windows except self
            for win in Main.opened_windows[:]:
                if win is not self:
                    win.close()

            file = QFileDialog.getOpenFileName(
                self, "Open HOF", "C:\\", "HOF Files (*.hof)"
            )
            if file[0]:
                Main.opened_windows.clear()
                # Reset the HOF_KMBHan instance
                Main.hof_class = HOF_KMBHan()
                # Explicitly clear termini and other lists
                Main.hof_class.termini.clear()
                Main.hof_class.stopreporter.clear()
                Main.hof_class.ddu.clear()
                Main.hof_class.infosystem.clear()
                a = Main.hof_class.load_from_hof(file[0])
                Main.test_error_codes(a)
                self.close()
                Main.opened_windows.append(Main.HOFView())
                Main.opened_windows[-1].show()
                Main.hofname = file[0].split("/")[-1].removesuffix(".hof")

        def open_db(self):
            # Close all opened windows except self
            for win in Main.opened_windows[:]:
                if win is not self:
                    win.close()
            Main.opened_windows.clear()
            # Reset the HOF_KMBHan instance
            Main.hof_class = HOF_KMBHan()
            # Explicitly clear termini and other lists
            Main.hof_class.termini.clear()
            Main.hof_class.stopreporter.clear()
            Main.hof_class.ddu.clear()
            Main.hof_class.infosystem.clear()
            file = QFileDialog.getOpenFileName(
                self, "Open Database", "C:\\", "Database Files (*.db)"
            )
            if file[0]:
                Main.hof_class.load_from_db(file[0])
                self.close()
                Main.opened_windows.append(Main.HOFView())
                Main.opened_windows[-1].show()
                Main.hofname = file[0].split("/")[-1].removesuffix(".db")

        def open_pref(self):
            Main.opened_windows.append(Main.PrefWin())
            Main.opened_windows[-1].show()

        @Slot(None, bool)  # type: ignore
        def update_listviews_every_3_minutes(self, TF: bool = False) -> None:
            # self.shortcuta = QShortcut(QKeySequence("Ctrl+S"), self)

            # If TF is True, stop timer
            if TF and hasattr(self, "_updateTimer"):
                self._updateTimer.stop()
                return

            # Initialize timer if doesn't exist
            if not hasattr(self, "_updateTimer"):
                self._updateTimer = QTimer(self)
                self._updateTimer.timeout.connect(self._perform_listviews_update)

            # Start or restart timer for 3 minutes
            self._updateTimer.start(180000)  # 3 * 60 * 1000 ms
            self._perform_listviews_update()

        def _perform_listviews_update(self):
            lw3_curindex = self.ui.listWidget_3.currentIndex()
            lw4_curindex = self.ui.listWidget_4.currentIndex()
            lw5_curindex = self.ui.listWidget_5.currentIndex()

            self.ui.listWidget_3.clear()
            self.ui.listWidget_4.clear()
            self.ui.listWidget_5.clear()
            query = self.ui.Search.toPlainText().strip()
            for stop in Main.hof_class.stopreporter:
                item = QListWidgetItem(stop.name)
                if query:
                    item.setHidden(not self._fuzzy_match(query, stop.name))
                self.ui.listWidget_3.addItem(item)
            self.ui.listWidget_4.addItems([i.RTNO for i in Main.hof_class.ddu])
            self.ui.listWidget_5.addItems(
                [i.destination for i in Main.hof_class.termini]
            )
            self.ui.listWidget_3.setCurrentIndex(lw3_curindex)
            self.ui.listWidget_4.setCurrentIndex(lw4_curindex)
            self.ui.listWidget_5.setCurrentIndex(lw5_curindex)

        # def closeEvent(self, event):

        # ...existing code...

        def delete_stuff(self, stuff: int):
            dct = {
                1: (Main.hof_class.stopreporter, self.ui.listWidget_3),
                2: (Main.hof_class.ddu, self.ui.listWidget_4),
                3: (Main.hof_class.termini, self.ui.listWidget_5),
                4: (Main.hof_class.infosystem, self.ui.listWidget_2),
            }
            if stuff == 1:
                ite = self.ui.listWidget_3.currentIndex()
                index = ite.row()
                bs_obj = Main.hof_class.stopreporter[index]
                if bs_obj.busstopID in self.busstop_id_to_index:
                    cur_index = self.busstop_id_to_index[bs_obj.busstopID]
                    del self.busstop_id_to_index[bs_obj.busstopID]
                    for key, value in self.busstop_id_to_index.items():
                        if value > cur_index:
                            self.busstop_id_to_index[key] -= 1
                for i in Main.hof_class.infosystem:
                    if bs_obj.busstopID in i.busstop_list1_class.bustops_withid:
                        index_to_remove = i.busstop_list1_class.bustops_withid.index(
                            bs_obj.busstopID
                        )
                        i.busstop_list1_class._busstops.pop(index_to_remove)
                        i.busstop_list1_class.bustops_withid.pop(index_to_remove)
                        # i.busstop_list1_class._busstops.remove(bs_obj.name)
                        # i.busstop_list1_class.bustops_withid.remove(bs_obj.busstopID)
                    if bs_obj.busstopID in i.busstop_list2_class.bustops_withid:
                        index_to_remove = i.busstop_list2_class.bustops_withid.index(
                            bs_obj.busstopID
                        )
                        i.busstop_list2_class._busstops.pop(index_to_remove)
                        i.busstop_list2_class.bustops_withid.pop(index_to_remove)
                        # i.busstop_list2_class._busstops.remove(bs_obj.name)
                        # i.busstop_list2_class.bustops_withid.remove(bs_obj.busstopID)
                print()
                Main.hof_class.stopreporter.pop(index)
                self.ui.listWidget_3.takeItem(index)
            elif stuff == 2:
                ite = self.ui.listWidget_4.currentIndex()
                index = ite.row()
                Main.hof_class.ddu.pop(index)
                self.ui.listWidget_4.takeItem(index)
            elif stuff == 3:
                ite = self.ui.listWidget_5.currentIndex()
                index = ite.row()
                Main.hof_class.termini.pop(index)
                self.ui.listWidget_5.takeItem(index)
            elif stuff == 4:
                ite = self.ui.listWidget_2.currentIndex()
                index = ite.row()
                Main.hof_class.infosystem.pop(index)
                self.ui.listWidget_2.takeItem(index)

        def sort_stuff(self, stuff: int) -> None:
            dct = {
                1: (Main.hof_class.stopreporter, self.ui.listWidget_3),
                2: (Main.hof_class.ddu, self.ui.listWidget_4),
                3: (Main.hof_class.termini, self.ui.listWidget_5),
                4: (Main.hof_class.infosystem, self.ui.listWidget_2),
            }
            if stuff == 1:
                Main.hof_class.stopreporter = sorted(
                    Main.hof_class.stopreporter, key=lambda x: x.name
                )
                self.ui.listWidget_3.clear()
                query = self.ui.Search.toPlainText().strip()
                for stop in Main.hof_class.stopreporter:
                    item = QListWidgetItem(stop.name)
                    if query:
                        item.setHidden(not self._fuzzy_match(query, stop.name))
                    self.ui.listWidget_3.addItem(item)
            elif stuff == 2:
                Main.hof_class.ddu = sorted(Main.hof_class.ddu, key=lambda x: x.RTNO)
                self.ui.listWidget_4.clear()
                self.ui.listWidget_4.addItems([i.RTNO for i in Main.hof_class.ddu])
            elif stuff == 3:
                Main.hof_class.termini = sorted(
                    Main.hof_class.termini, key=lambda x: x.eric
                )
                self.ui.listWidget_5.clear()
                self.ui.listWidget_5.addItems(
                    [i.destination for i in Main.hof_class.termini]
                )
            elif stuff == 4:
                Main.hof_class.infosystem = sorted(
                    Main.hof_class.infosystem, key=lambda x: x.route
                )
                self.ui.listWidget_2.clear()
                self.ui.listWidget_2.addItems(
                    [i.route for i in Main.hof_class.infosystem]
                )

        @Slot(None, int, int)  # type: ignore
        def update_listviews(self, index: int, func_in: int) -> int:
            dct = {
                1: lambda: self.ui.listWidget_3.item(index).setText(
                    Main.hof_class.stopreporter[index].name
                ),  # Stopreporter
                2: lambda: self.ui.listWidget_4.item(index).setText(
                    Main.hof_class.ddu[index].RTNO
                ),  # DDU
                3: lambda: self.ui.listWidget_5.item(index).setText(
                    Main.hof_class.termini[index].destination
                ),  # Termini
                4: lambda: self.ui.listWidget_2.item(index).setText(
                    Main.hof_class.infosystem[index].route
                ),  # Infosystem
            }

            # Execute the functions
            dct[func_in]()
            return 1

        def check_bsl_validity(self):
            miss_bs = []
            bsl = [i.name for i in Main.hof_class.stopreporter]
            rt_sel = self.ui.listWidget_2.currentIndex()
            rt_index = rt_sel.row()
            if Main.hof_class.infosystem[rt_index].busstop_list1_class._busstops == []:
                QMessageBox.warning(
                    self, "Error", "Bus stop list 1 is empty.", QMessageBox.Ok
                )  # type: ignore
            elif (
                Main.hof_class.infosystem[rt_index].busstop_list2_class._busstops == []
            ):
                QMessageBox.warning(
                    self, "Error", "Bus stop list 2 is empty.", QMessageBox.Ok
                )  # type: ignore
            else:
                for i in Main.hof_class.infosystem[
                    rt_index
                ].busstop_list1_class._busstops:
                    if i not in bsl:
                        miss_bs.append(i)
                for i in Main.hof_class.infosystem[
                    rt_index
                ].busstop_list2_class._busstops:
                    if i not in bsl:
                        miss_bs.append(i)
                if miss_bs != []:
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"Bus stops {miss_bs} are not found in the bus stop list.",
                        QMessageBox.Ok,
                    )  # type: ignore
                else:
                    QMessageBox.information(
                        self, "Success", "Bus stop list is valid.", QMessageBox.Ok
                    )  # type: ignore

        def check_all_bsl_validity(self):
            miss_bs = set()
            bsl = [i.name for i in Main.hof_class.stopreporter]
            for rt in Main.hof_class.infosystem:
                for i in rt.busstop_list1_class._busstops:
                    if i not in bsl:
                        miss_bs.add(i)
                for i in rt.busstop_list2_class._busstops:
                    if i not in bsl:
                        miss_bs.add(i)
            if miss_bs != set():
                # message = QMessageBox()
                # message.setMinimumSize(200, 100)
                # message.setWindowTitle("Error")
                # message.setText(f"Bus stops {miss_bs if len(miss_bs)< 20 else list(miss_bs)[:20]} are not found in the bus stop list. Do you want to add them?")
                # message.setIcon(QMessageBox.Warning) # type: ignore
                # message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) # type: ignore
                # message.accepted.connect(lambda: self.add_bs_from_list(list(miss_bs)))
                a = QMessageBox.warning(
                    self,
                    "Error",
                    f"Bus stops {miss_bs if len(miss_bs) < 20 else list(miss_bs)[:20]} are not found in the bus stop list. Do you want to add them?",
                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                )  # type: ignore
                if (
                    a == QMessageBox.StandardButton.Ok
                ):  # Check directly against the returned button value
                    self.add_bs_from_list(list(miss_bs))
            else:
                QMessageBox.information(
                    self, "Success", "All bus stop lists are valid.", QMessageBox.Ok
                )  # type: ignore

            self.stop_name_to_id_map = {
                stop.name: stop.busstopID for stop in Main.hof_class.stopreporter
            }

        @Slot(None)  # type: ignore
        def reload_bslist_id(self) -> None:
            """Reload the bus stop name to ID mapping and update busstop_id_to_index"""
            self.stop_name_to_id_map = {
                stop.name: stop.busstopID for stop in Main.hof_class.stopreporter
            }

            # Rebuild the busstop_id_to_index mapping
            self.busstop_id_to_index.clear()
            for i, stop in enumerate(Main.hof_class.stopreporter):
                self.busstop_id_to_index[stop.busstopID] = i

            # Refresh the current bus stop list display only if there are routes
            if Main.hof_class.infosystem:
                self.get_bsl()

        def add_bs_from_list(self, bs: list[str]) -> None:
            for i in bs:
                Main.hof_class.add_stopreporter(f"{i}", f"{i}", 0, 0, 0, -1.0, -1.0)
                # Add to UI
                stop_index = len(Main.hof_class.stopreporter) - 1
                stop = Main.hof_class.stopreporter[stop_index]
                item = QListWidgetItem(stop.name)
                item.setData(Qt.ItemDataRole.UserRole, stop.busstopID)
                query = self.ui.Search.toPlainText().strip()
                if query:
                    item.setHidden(not self._fuzzy_match(query, stop.name))
                self.ui.listWidget_3.addItem(item)
                # Update the busstop_id_to_index dictionary
                self.busstop_id_to_index[stop.busstopID] = stop_index
            Main.hof_class.fill_busttoplist_with_id()

        def reset_bsl_ids(self) -> None:
            for rt in Main.hof_class.infosystem:
                bsl1 = rt.busstop_list1_class._busstops
                bsl2 = rt.busstop_list2_class._busstops
                rt.busstop_list1_class.bustops_withid = [""] * len(bsl1)
                rt.busstop_list2_class.bustops_withid = [""] * len(bsl2)
                print(rt.busstop_list2_class.bustops_withid)
                for index, i in enumerate(bsl1):
                    rt.busstop_list1_class.bustops_withid[index] = (
                        self.stop_name_to_id_map.get(i, "")
                    )
                for index, i in enumerate(bsl2):
                    rt.busstop_list2_class.bustops_withid[index] = (
                        self.stop_name_to_id_map.get(i, "")
                    )

        def del_bs_from_sel(self):
            item = self.ui.listWidget.currentIndex()
            index = item.row()
            routesel = self.ui.listWidget_2.currentIndex()
            routeindex = routesel.row()

            if self.bus_rt_direction == 1:
                # Remove from both name list and ID list
                Main.hof_class.infosystem[routeindex].busstop_list1_class._busstops.pop(
                    index
                )
                Main.hof_class.infosystem[
                    routeindex
                ].busstop_list1_class.bustops_withid.pop(index)
            else:
                Main.hof_class.infosystem[routeindex].busstop_list2_class._busstops.pop(
                    index
                )
                Main.hof_class.infosystem[
                    routeindex
                ].busstop_list2_class.bustops_withid.pop(index)

            self.ui.listWidget.takeItem(index)

        def add_bs_from_sel(self):
            item = self.ui.listWidget_3.currentIndex()
            index = item.row()
            routesel = self.ui.listWidget_2.currentIndex()
            routeindex = routesel.row()

            # Get the bus stop ID directly from the stopreporter
            selected_stop = Main.hof_class.stopreporter[index]
            stop_name = selected_stop.name
            stop_id = selected_stop.busstopID

            if self.ui.checkBox.isChecked():
                if self.bus_rt_direction == 1:
                    # Add to the busstop list and the ID list
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list1_class._busstops.append(stop_name)
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list1_class.bustops_withid.append(stop_id)
                    # Create the item with proper data
                    item = QListWidgetItem(stop_name)
                    item.setData(Qt.ItemDataRole.UserRole, stop_id)
                    self.ui.listWidget.addItem(item)
                else:
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list2_class._busstops.append(stop_name)
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list2_class.bustops_withid.append(stop_id)
                    item = QListWidgetItem(stop_name)
                    item.setData(Qt.ItemDataRole.UserRole, stop_id)
                    self.ui.listWidget.addItem(item)
            else:
                cur_bs = self.ui.listWidget.currentIndex()
                cur_index = cur_bs.row()

                if self.bus_rt_direction == 1:
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list1_class._busstops.insert(cur_index, stop_name)
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list1_class.bustops_withid.insert(cur_index, stop_id)
                    item = QListWidgetItem(stop_name)
                    item.setData(Qt.ItemDataRole.UserRole, stop_id)
                    self.ui.listWidget.insertItem(cur_index, item)
                else:
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list2_class._busstops.insert(cur_index, stop_name)
                    Main.hof_class.infosystem[
                        routeindex
                    ].busstop_list2_class.bustops_withid.insert(cur_index, stop_id)
                    item = QListWidgetItem(stop_name)
                    item.setData(Qt.ItemDataRole.UserRole, stop_id)
                    self.ui.listWidget.insertItem(cur_index, item)

        def bsl_goup(self):
            item = self.ui.listWidget.currentIndex()
            index = item.row()
            if index <= 0:
                return
            route_index = self.ui.listWidget_2.currentIndex().row()
            # Swap items in UI
            self._swap_listwidget_items(index - 1, index)
            # Swap items in data model
            self._swap_busstop_data(route_index, index - 1, index)
            # Update selection
            self.ui.listWidget.setCurrentRow(index - 1)

        def bsl_godown(self):
            item = self.ui.listWidget.currentIndex()
            index = item.row()

            if index >= self.ui.listWidget.count() - 1:
                return

            route_index = self.ui.listWidget_2.currentIndex().row()

            # Swap items in UI
            self._swap_listwidget_items(index, index + 1)

            # Swap items in data model
            self._swap_busstop_data(route_index, index, index + 1)

            # Update selection
            self.ui.listWidget.setCurrentRow(index + 1)

        def termini_goup(self):
            item = self.ui.listWidget_5.currentIndex()
            index = item.row()
            if index <= 0:
                return
            # Swap in data model
            Main.hof_class.termini[index - 1], Main.hof_class.termini[index] = (
                Main.hof_class.termini[index],
                Main.hof_class.termini[index - 1],
            )
            # Swap in UI
            item1 = self.ui.listWidget_5.takeItem(index - 1)
            item2 = self.ui.listWidget_5.takeItem(
                index - 1
            )  # index is now index-1 after takeItem
            self.ui.listWidget_5.insertItem(index - 1, item2)
            self.ui.listWidget_5.insertItem(index, item1)
            # Update selection
            self.ui.listWidget_5.setCurrentRow(index - 1)

        def termini_godown(self):
            item = self.ui.listWidget_5.currentIndex()
            index = item.row()
            if index >= self.ui.listWidget_5.count() - 1:
                return
            # Swap in data model
            Main.hof_class.termini[index], Main.hof_class.termini[index + 1] = (
                Main.hof_class.termini[index + 1],
                Main.hof_class.termini[index],
            )
            # Swap in UI
            item1 = self.ui.listWidget_5.takeItem(index)
            item2 = self.ui.listWidget_5.takeItem(
                index
            )  # index is now index after takeItem
            self.ui.listWidget_5.insertItem(index, item2)
            self.ui.listWidget_5.insertItem(index + 1, item1)
            # Update selection
            self.ui.listWidget_5.setCurrentRow(index + 1)

        def ddu_goup(self):
            item = self.ui.listWidget_4.currentIndex()
            index = item.row()
            if index <= 0:
                return
            # Swap in data model
            Main.hof_class.ddu[index - 1], Main.hof_class.ddu[index] = (
                Main.hof_class.ddu[index],
                Main.hof_class.ddu[index - 1],
            )
            # Swap in UI
            item1 = self.ui.listWidget_4.takeItem(index - 1)
            item2 = self.ui.listWidget_4.takeItem(
                index - 1
            )  # index is now index-1 after takeItem
            self.ui.listWidget_4.insertItem(index - 1, item2)
            self.ui.listWidget_4.insertItem(index, item1)
            # Update selection
            self.ui.listWidget_4.setCurrentRow(index - 1)

        def ddu_godown(self):
            item = self.ui.listWidget_4.currentIndex()
            index = item.row()
            if index >= self.ui.listWidget_4.count() - 1:
                return
            # Swap in data model
            Main.hof_class.ddu[index], Main.hof_class.ddu[index + 1] = (
                Main.hof_class.ddu[index + 1],
                Main.hof_class.ddu[index],
            )
            # Swap in UI
            item1 = self.ui.listWidget_4.takeItem(index)
            item2 = self.ui.listWidget_4.takeItem(
                index
            )  # index is now index after takeItem
            self.ui.listWidget_4.insertItem(index, item2)
            self.ui.listWidget_4.insertItem(index + 1, item1)
            # Update selection
            self.ui.listWidget_4.setCurrentRow(index + 1)

        def routes_goup(self):
            item = self.ui.listWidget_2.currentIndex()
            index = item.row()
            if index <= 0:
                return
            # Swap in data model
            Main.hof_class.infosystem[index - 1], Main.hof_class.infosystem[index] = (
                Main.hof_class.infosystem[index],
                Main.hof_class.infosystem[index - 1],
            )
            # Swap in UI
            item1 = self.ui.listWidget_2.takeItem(index - 1)
            item2 = self.ui.listWidget_2.takeItem(
                index - 1
            )  # index is now index-1 after takeItem
            self.ui.listWidget_2.insertItem(index - 1, item2)
            self.ui.listWidget_2.insertItem(index, item1)
            # Update selection
            self.ui.listWidget_2.setCurrentRow(index - 1)

        def routes_godown(self):
            item = self.ui.listWidget_2.currentIndex()
            index = item.row()
            if index >= self.ui.listWidget_2.count() - 1:
                return
            # Swap in data model
            Main.hof_class.infosystem[index], Main.hof_class.infosystem[index + 1] = (
                Main.hof_class.infosystem[index + 1],
                Main.hof_class.infosystem[index],
            )
            # Swap in UI
            item1 = self.ui.listWidget_2.takeItem(index)
            item2 = self.ui.listWidget_2.takeItem(
                index
            )  # index is now index after takeItem
            self.ui.listWidget_2.insertItem(index, item2)
            self.ui.listWidget_2.insertItem(index + 1, item1)
            # Update selection
            self.ui.listWidget_2.setCurrentRow(index + 1)

        def change_bs_FromSel(self):
            item = self.ui.listWidget.currentIndex()
            index = item.row()
            routesel = self.ui.listWidget_2.currentIndex()
            routeindex = routesel.row()

            # Get selected bus stop from the bus stop list
            cur_bs = self.ui.listWidget_3.currentIndex()
            cur_index = cur_bs.row()
            selected_stop = Main.hof_class.stopreporter[cur_index]
            stop_name = selected_stop.name
            stop_id = selected_stop.busstopID

            if self.bus_rt_direction == 1:
                # Update both name and ID
                Main.hof_class.infosystem[routeindex].busstop_list1_class._busstops[
                    index
                ] = stop_name
                Main.hof_class.infosystem[
                    routeindex
                ].busstop_list1_class.bustops_withid[index] = stop_id
            else:
                Main.hof_class.infosystem[routeindex].busstop_list2_class._busstops[
                    index
                ] = stop_name
                Main.hof_class.infosystem[
                    routeindex
                ].busstop_list2_class.bustops_withid[index] = stop_id

            # Update the item text and data
            list_item = self.ui.listWidget.item(index)
            list_item.setText(stop_name)
            list_item.setData(Qt.ItemDataRole.UserRole, stop_id)

        def _swap_listwidget_items(self, index1, index2):
            """Swap two QListWidgetItem objects by exchanging their text and stored data."""
            item1 = self.ui.listWidget.item(index1)
            item2 = self.ui.listWidget.item(index2)
            # Retrieve texts and data
            text1 = item1.text()
            data1 = item1.data(Qt.ItemDataRole.UserRole)
            text2 = item2.text()
            data2 = item2.data(Qt.ItemDataRole.UserRole)
            # Swap the properties
            item1.setText(text2)
            item1.setData(Qt.ItemDataRole.UserRole, data2)
            item2.setText(text1)
            item2.setData(Qt.ItemDataRole.UserRole, data1)

        def _swap_busstop_data(self, route_index, index1, index2):
            """Swap bus stop data in the appropriate direction list"""
            if self.bus_rt_direction == 1:
                busstop_list = Main.hof_class.infosystem[
                    route_index
                ].busstop_list1_class
            else:
                busstop_list = Main.hof_class.infosystem[
                    route_index
                ].busstop_list2_class

            # Swap bus stops
            busstop_list._busstops[index1], busstop_list._busstops[index2] = (
                busstop_list._busstops[index2],
                busstop_list._busstops[index1],
            )

            # Swap bus stop IDs
            busstop_list.bustops_withid[index1], busstop_list.bustops_withid[index2] = (
                busstop_list.bustops_withid[index2],
                busstop_list.bustops_withid[index1],
            )

        def open_rt(self):
            item = self.ui.listWidget_2.currentIndex()
            index = item.row()
            Main.opened_windows.append(
                Main.AddRouteEntry(
                    None,
                    False,
                    Main.hof_class.infosystem[index].route,
                    Main.hof_class.infosystem[index].direction1,
                    Main.hof_class.infosystem[index].direction2,
                    curindex=index,
                )
            )
            Main.opened_windows[-1].show()

        def open_bs(self):
            """Open bus stop directly using stored ID - no search needed!"""
            item = self.ui.listWidget.currentItem()
            if not item:
                return

            # Get the busstopID from the item data
            busstop_id = item.data(Qt.ItemDataRole.UserRole)
            if not busstop_id:
                QMessageBox.warning(
                    self, "Error", "No bus stop ID found for this item.", QMessageBox.Ok
                )  # type: ignore
                return

            # Direct lookup - O(1) operation!
            index = self.busstop_id_to_index.get(busstop_id)
            if index is not None:
                stop = Main.hof_class.stopreporter[index]
                Main.opened_windows.append(
                    Main.AddBusStop(
                        None,
                        stop.name,
                        stop.EngDisplay,
                        stop.ChiSeconds,
                        stop.EngSeconds,
                        stop.ManSeconds,
                        stop.Outbound_sectionfare
                        if isinstance(stop.Outbound_sectionfare, float)
                        else -1.0,
                        stop.Inbound_sectionfare
                        if isinstance(stop.Inbound_sectionfare, float)
                        else -1.0,
                        curindex=index,
                    )
                )
                Main.opened_windows[-1].show()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Bus stop with ID {busstop_id} not found.",
                    QMessageBox.Ok,
                )  # type: ignore

        def open_bs_lw3(self):
            item = self.ui.listWidget_3.currentIndex()
            index = item.row()
            Main.opened_windows.append(
                Main.AddBusStop(
                    None,
                    Main.hof_class.stopreporter[index].name,
                    Main.hof_class.stopreporter[index].EngDisplay,
                    Main.hof_class.stopreporter[index].ChiSeconds,
                    Main.hof_class.stopreporter[index].EngSeconds,
                    Main.hof_class.stopreporter[index].ManSeconds,
                    Main.hof_class.stopreporter[index].Outbound_sectionfare
                    if isinstance(
                        Main.hof_class.stopreporter[index].Outbound_sectionfare, float
                    )
                    else -1.0,  # type: ignore
                    Main.hof_class.stopreporter[index].Inbound_sectionfare
                    if isinstance(
                        Main.hof_class.stopreporter[index].Inbound_sectionfare, float
                    )
                    else -1.0,  # type: ignore
                    curindex=index,
                )
            )  # type: ignore
            Main.opened_windows[-1].show()

        def open_ddu(self):
            item = self.ui.listWidget_4.currentIndex()
            index = item.row()
            Main.opened_windows.append(
                Main.AddDDU(
                    None,
                    Main.hof_class.ddu[index].RTNO,
                    Main.hof_class.ddu[index].Outbound_dir,
                    Main.hof_class.ddu[index].Inbound_dir,
                    Main.hof_class.ddu[index].Outbound_price
                    if isinstance(Main.hof_class.ddu[index].Outbound_price, float)
                    else -1.0,  # type: ignore
                    Main.hof_class.ddu[index].Inbound_price
                    if isinstance(Main.hof_class.ddu[index].Inbound_price, float)
                    else -1.0,  # type: ignore
                    Main.hof_class.ddu[index].sectiontimes_Y,
                    Main.hof_class.ddu[index].sectiontimes_Z,
                    curindex=index,
                )
            )  # type: ignore
            Main.opened_windows[-1].show()

        def open_termini(self):
            item = self.ui.listWidget_5.currentIndex()
            index = item.row()
            Main.opened_windows.append(
                Main.AddTermini(
                    None,
                    Main.hof_class.termini[index].eric,
                    Main.hof_class.termini[index].destination,
                    Main.hof_class.termini[index].busfull,
                    Main.hof_class.termini[index].flip,
                    curindex=index,
                )
            )
            Main.opened_windows[-1].show()

        def open_edit_en_masse(self):
            Main.opened_windows.append(Main.EditEnMasse())
            Main.opened_windows[-1].show()

        def dirchange_Y(self):
            self.bus_rt_direction = 1
            # print(self.bus_rt_direction)
            self.get_bsl()

        def dirchange_Z(self):
            self.bus_rt_direction = 2
            # print(self.bus_rt_direction)
            self.get_bsl()

        def get_bsl(self, reset_rtbslLV: bool = True):
            # print("hi")
            item = self.ui.listWidget_2.currentIndex()
            index = item.row()
            index_2 = self.ui.listWidget.currentIndex().row()
            print(f"Current route index: {index_2}")
            self.ui.listWidget.clear()

            # Check if infosystem is empty or index is invalid
            if (
                not Main.hof_class.infosystem
                or index < 0
                or index >= len(Main.hof_class.infosystem)
            ):
                return

            info = Main.hof_class.infosystem[index]
            if self.bus_rt_direction == 1:
                bs_ids = info.busstop_list1_class.bustops_withid
                bs_names = info.busstop_list1_class._busstops
            else:
                bs_ids = info.busstop_list2_class.bustops_withid
                bs_names = info.busstop_list2_class._busstops

            if len(bs_ids) != len(bs_names):
                if len(bs_ids) < len(bs_names):
                    bs_ids.extend([""] * (len(bs_names) - len(bs_ids)))
                else:
                    del bs_ids[len(bs_names) :]

            missing_bus_stops = []

            for i, each in enumerate(bs_ids):
                busstop_obj = None

                # Only try lookup by bus stop ID - no fallback
                busstop_index = self.busstop_id_to_index.get(each)
                if busstop_index is None and i < len(bs_names):
                    stop_name = bs_names[i]
                    if stop_name:
                        fallback_id = self.stop_name_to_id_map.get(stop_name)
                        if fallback_id:
                            bs_ids[i] = fallback_id
                            busstop_index = self.busstop_id_to_index.get(fallback_id)

                if busstop_index is not None:
                    busstop_obj = Main.hof_class.stopreporter[busstop_index]
                    # Create list item with the bus stop name and store the ID as data
                    item = QListWidgetItem(busstop_obj.name)
                    item.setData(
                        Qt.ItemDataRole.UserRole, bs_ids[i]
                    )  # Store the busstopID directly
                    self.ui.listWidget.addItem(item)
                else:
                    if i < len(bs_names) and bs_names[i] == "":
                        continue
                    item_text = bs_names[i] if i < len(bs_names) else ""
                    if item_text:
                        item = QListWidgetItem(item_text)
                        item.setData(Qt.ItemDataRole.UserRole, "")
                        self.ui.listWidget.addItem(item)
                    missing_bus_stops.append(i)

            # Show error message if there are missing bus stops
            if missing_bus_stops:
                QMessageBox.warning(
                    self,
                    "Missing Bus Stops",
                    f"The following bus stop IDs could not be found:\n{', '.join([Main.hof_class.infosystem[index].db_export_bsl1[j] if self.bus_rt_direction == 1 else Main.hof_class.infosystem[index].db_export_bsl2[j] for j in missing_bus_stops])}\n\n"
                    f"This may indicate corrupted data or missing bus stops.",
                    QMessageBox.StandardButton.Ok,
                )

            self.ui.listWidget.setCurrentIndex(
                self.ui.listWidget.model().index(index_2, 0)
            ) if reset_rtbslLV else None

            # self.ui.tableWidget.setItem(0, 0, QTableWidgetItem(Main.hof_class.infosystem[index].route))
            # self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(Main.hof_class.infosystem[index].direction1))
            # self.ui.tableWidget.setItem(0, 2, QTableWidgetItem(Main.hof_class.infosystem[index].direction2))
            # return Main.hof_class.infosystem[index].busstoplist1 if Main.HOFView.bus_rt_direction == 1 else Main.hof_class.infosystem[index].busstoplist2

        def save(self):
            if Main.hofname == "":
                Main.hofname = "Untitled"
            if Main.export_path == "":
                Main.export_path = Main().fileexplorer()
            Main.hof_class.save_to_db(Main.export_path + "/" + Main.hofname + ".db")
            import sqlite3

            conn = sqlite3.connect(Main.export_path + "/" + Main.hofname + ".db")
            c = conn.cursor()
            c.execute("create table if not exists prefs (key text, value text)")
            c.execute("delete from prefs where key = 'export_path'")
            c.execute(
                "insert into prefs values ('export_path', ?)", (Main.export_path,)
            )
            c.execute("create table if not exists stopreporter_chi (chi text)")
            c.execute("delete from stopreporter_chi")
            c.executemany(
                "insert into stopreporter_chi values (?)",
                [(i,) for i in Main.stopreporter_genlist],
            )
            conn.commit()
            conn.close()
            QMessageBox.information(
                self,
                "Saved",
                "Saved to " + Main.export_path + "/" + Main.hofname + ".db",
            )

        def export_hof(self):
            """Export HOF file with proper bus stop handling and termination"""
            # Initialize basic settings
            if Main.hofname == "":
                Main.hof_class.name = "Untitled"
            if Main.export_path == "":
                Main.export_path = Main().fileexplorer()

            Main.hof_class.name = Main.hofname

            # Ensure blank stops exist if we have any routes
            if Main.hof_class.infosystem:
                self._ensure_blank_stops_exist()
                self.reload_bslist_id()

            # Process all infosystem entries
            for info in Main.hof_class.infosystem:
                # Update bus stop names from IDs
                self._update_busstop_names(info)

                # Process direction 1
                self._ensure_proper_terminator(
                    info.busstop_list1_class._busstops,
                    info.busstop_list1_class.bustops_withid,
                )

                # Process direction 2
                self._ensure_proper_terminator(
                    info.busstop_list2_class._busstops,
                    info.busstop_list2_class.bustops_withid,
                )

            # Final processing and export
            Main.hof_class.fill_busttoplist_with_id()
            Main.hof_class.export_hof(f"{Main.export_path}/{Main.hofname}.hof")
            QMessageBox.information(
                self, "Saved", f"Saved to {Main.export_path}/{Main.hofname}.hof"
            )

        def _ensure_blank_stops_exist(self):
            """Ensure blank and blank_2pages stops exist in the stopreporter"""
            lsa = [i.name.lower() for i in Main.hof_class.stopreporter]
            if "blank_2pages" not in lsa:
                Main.hof_class.add_stopreporter("blank_2pages", "", 0, 0, 0, -1.0, -1.0)
            if "blank" not in lsa:
                Main.hof_class.add_stopreporter("blank", "", 0, 0, 0, -1.0, -1.0)

        def _update_busstop_names(self, info):
            """Update bus stop names based on their IDs"""
            # Direction 1
            for index, stop_id in enumerate(info.busstop_list1_class.bustops_withid):
                bus_stop_index = self.busstop_id_to_index.get(stop_id)
                if isinstance(bus_stop_index, int):
                    info.busstop_list1_class._busstops[index] = (
                        Main.hof_class.stopreporter[bus_stop_index].name
                    )

            # Direction 2
            for index, stop_id in enumerate(info.busstop_list2_class.bustops_withid):
                bus_stop_index = self.busstop_id_to_index.get(stop_id)
                if isinstance(bus_stop_index, int):
                    info.busstop_list2_class._busstops[index] = (
                        Main.hof_class.stopreporter[bus_stop_index].name
                    )

        def _ensure_proper_terminator(self, busstop_names, busstop_ids):
            """Add appropriate blank terminator based on route length"""
            if not busstop_names:
                return

            # Remove empty strings from the end (check last 3 stops)
            for _ in range(3):  # Check up to 3 times
                if busstop_names and busstop_names[-1] == "":
                    busstop_names.pop()
                    busstop_ids.pop()
                else:
                    break

            if not busstop_names:
                return

            # Count effective stops (non-hidden)
            effective_stop = sum(
                1 for stop in busstop_names if not stop.startswith("_")
            )

            # Determine which terminator we need
            needed_terminator = "blank_2pages" if effective_stop >= 40 else "blank"
            wrong_terminator = "blank" if effective_stop >= 40 else "blank_2pages"

            # Get last 3 stops indices
            last_three_count = min(3, len(busstop_names))
            start_index = len(busstop_names) - last_three_count

            # Remove wrong terminators and track if we have the correct one
            has_correct = False
            for i in range(len(busstop_names) - 1, start_index - 1, -1):
                if i >= 0:
                    stop_lower = busstop_names[i].lower()
                    if stop_lower == needed_terminator:
                        has_correct = True
                    elif stop_lower == wrong_terminator:
                        busstop_names.pop(i)
                        busstop_ids.pop(i)

            # If we don't have the correct terminator, add it at the end
            if not has_correct:
                busstop_names.append(needed_terminator)
                blank_id = self._get_blank_id(needed_terminator)
                busstop_ids.append(blank_id)

        def export_hof_v2(self):
            """Export HOF file with proper bus stop handling and termination, version 2"""
            # Initialize basic settings
            if Main.hofname == "":
                Main.hof_class.name = "Untitled"
            if Main.export_path == "":
                Main.export_path = Main().fileexplorer()
            Main.hof_class.name = Main.hofname
            # Ensure blank stops exist if we have any routes
            if Main.hof_class.infosystem:
                self._ensure_blank_stops_exist()
                self.reload_bslist_id()
            # Process all infosystem entries
            for info in Main.hof_class.infosystem:
                # Update bus stop names from IDs
                self._update_busstop_names(info)

                # Process direction 1
                self._ensure_proper_terminator(
                    info.busstop_list1_class._busstops,
                    info.busstop_list1_class.bustops_withid,
                )

                # Process direction 2
                self._ensure_proper_terminator(
                    info.busstop_list2_class._busstops,
                    info.busstop_list2_class.bustops_withid,
                )
            # Final processing and export
            Main.hof_class.fill_busttoplist_with_id()
            Main.hof_class.export_hof_v2(f"{Main.export_path}/{Main.hofname}.hof")
            QMessageBox.information(
                self, "Saved", f"Saved to {Main.export_path}/{Main.hofname}.hof"
            )

        def open_eric_guesser(self):
            """Open the Eric Guesser window"""
            Main.opened_windows.append(Main.EricGuesser(None))
            Main.opened_windows[-1].show()

        def _get_blank_id(self, blank_name):
            """Get the ID for a blank terminator by name"""
            for stop in Main.hof_class.stopreporter:
                if stop.name.lower() == blank_name.lower():
                    return stop.busstopID
            return blank_name  # Fallback if somehow not found

        def closeEvent(self, event: QCloseEvent) -> None:
            Main.opened_windows = []
            if hasattr(self, "_updateTimer"):
                self._updateTimer.stop()
            event.accept()
            self.closed = True
            event.accept()

    class AddBusStop(QMainWindow):
        sig = Signal(int, int)
        sig2 = Signal(int)  # For AddBusStop_UI
        orig_autoskip = True

        def __init__(
            self,
            parent=None,
            name: str = "",
            engdisp: str = "",
            chisec: int = 0,
            engsec: int = 0,
            mansec: int = 0,
            osf: float = -1.0,
            isf: float = -1.0,
            curindex: int = 0,
        ):
            super().__init__(parent)
            self.curindex = curindex
            self.ui = AddBusStop_UI()
            self.ui.setupUi(self)

            # Parse the stop name to extract properties
            ui_values = get_ui_values_from_name(name, engdisp)

            # Set the base name (without prefix/suffix) in the lineEdit
            self.ui.lineEdit.setText(ui_values["base_name"])
            self.ui.lineEdit_2.setText(engdisp)
            self.ui.spinBox.setValue(chisec)
            self.ui.spinBox_2.setValue(engsec)
            self.ui.spinBox_3.setValue(mansec)
            self.ui.doubleSpinBox.setValue(osf)
            self.ui.doubleSpinBox_2.setValue(isf)

            # Set UI fields based on parsed properties
            self.ui.checkBox.setChecked(ui_values["autoskip"])
            self.ui.checkBox_8w6w.setChecked(ui_values["w8w6_different"])
            self.ui.spinBox_4.setValue(ui_values["chi_pages"])

            self.ui.pushButton.clicked.connect(self.get_routes_bs_in)
            orig_autoskip = ui_values["autoskip"]
            self.hofview = Main.opened_windows[0]

            # Connect UI changes to update stop name
            self.ui.checkBox.stateChanged.connect(self.update_stop_name_preview)
            self.ui.checkBox_8w6w.stateChanged.connect(self.update_stop_name_preview)
            self.ui.spinBox_4.valueChanged.connect(self.update_stop_name_preview)
            self.ui.lineEdit_2.textChanged.connect(self.update_stop_name_preview)

        def update_stop_name_preview(self):
            """Update the displayed stop name based on current UI field values."""
            base_name = self.ui.lineEdit.text().strip()
            if not base_name:
                return

            # Get current UI values
            autoskip = self.ui.checkBox.isChecked()
            w8w6_different = self.ui.checkBox_8w6w.isChecked()
            chi_pages = self.ui.spinBox_4.value()
            eng_display = self.ui.lineEdit_2.text()
            eng_at_count = eng_display.count("@")

            # Generate the encoded name
            encoded_name = encode_stop_name(
                base_name, autoskip, w8w6_different, chi_pages, eng_at_count
            )

            # Update the window title to show the encoded name
            self.setWindowTitle(f"Edit Bus Stop - Encoded: {encoded_name}")

        def get_bs(self):
            Main.raise_unimplemented()

        def get_routes_bs_in(self):
            """Get the routes that this bus stop is in."""
            idself = Main.hof_class.stopreporter[self.curindex].busstopID
            routes = []
            for i in Main.hof_class.infosystem:
                if idself in i.busstop_list1_class.bustops_withid:
                    routes.append(f"{i.route} (Y)")
                if idself in i.busstop_list2_class.bustops_withid:
                    routes.append(f"{i.route} (Z)")
            if routes:
                QMessageBox.information(
                    self,
                    "Routes",
                    f"This bus stop is in the following routes:\n" + "\n".join(routes),
                    QMessageBox.Ok,
                )
            else:
                QMessageBox.information(
                    self,
                    "Routes",
                    "This bus stop is not in any routes.",
                    QMessageBox.Ok,
                )

        def closeEvent(self, event):
            # Get values from UI
            base_name = self.ui.lineEdit.text().strip()
            eng_display = self.ui.lineEdit_2.text().strip()
            autoskip = self.ui.checkBox.isChecked()
            w8w6_different = self.ui.checkBox_8w6w.isChecked()
            chi_pages = self.ui.spinBox_4.value()
            eng_at_count = eng_display.count("@")

            # Encode the stop name with prefix/suffix
            encoded_name = encode_stop_name(
                base_name, autoskip, w8w6_different, chi_pages, eng_at_count
            )

            # Save to the HOF class
            Main.hof_class.stopreporter[self.curindex].name = encoded_name
            Main.hof_class.stopreporter[self.curindex].EngDisplay = eng_display
            Main.hof_class.stopreporter[
                self.curindex
            ].ChiSeconds = self.ui.spinBox.value()
            Main.hof_class.stopreporter[
                self.curindex
            ].EngSeconds = self.ui.spinBox_2.value()
            Main.hof_class.stopreporter[
                self.curindex
            ].ManSeconds = self.ui.spinBox_3.value()
            Main.hof_class.stopreporter[
                self.curindex
            ].Outbound_sectionfare = self.ui.doubleSpinBox.value()
            Main.hof_class.stopreporter[
                self.curindex
            ].Inbound_sectionfare = self.ui.doubleSpinBox_2.value()

            self.sig.connect(self.hofview.update_listviews)
            self.sig.emit(self.curindex, 1)
            self.sig2.connect(self.hofview.reload_bslist_id)
            self.sig2.emit(self.curindex)
            event.accept()  # let the window close

    class AddDDU(QMainWindow):
        sig = Signal(int, int)

        def __init__(
            self,
            parent=None,
            RTNO: str = "",
            OutDir: str = "",
            InDir: str = "",
            OutSecFare: float = -1.0,
            InSecFare: float = -1.0,
            Out_SectionCount: int = 0,
            In_SectionCount: int = 0,
            curindex: int = 0,
        ):
            super().__init__(parent)
            self.curindex = curindex
            # self.sig = Signal(int)
            self.hofview = Main.opened_windows[0]
            self.ui = AddDDU_UI()
            self.ui.setupUi(self)
            self.ui.lineEdit.setText(RTNO)
            self.ui.lineEdit_2.setText(OutDir)
            self.ui.lineEdit_3.setText(InDir)
            self.ui.doubleSpinBox.setValue(OutSecFare)
            self.ui.doubleSpinBox_2.setValue(InSecFare)
            self.ui.spinBox.setValue(Out_SectionCount)
            self.ui.spinBox_2.setValue(In_SectionCount)

        def closeEvent(self, event):
            # lst = [self.ui.plainTextEdit.document().isModified(), self.ui.plainTextEdit_2.document().isModified(), self.ui.plainTextEdit_3.document().isModified(), self.ui.doubleSpinBox.value() != 0.0, self.ui.doubleSpinBox_2.value() != 0.0, self.ui.spinBox.value() != 0, self.ui.spinBox_2.value() != 0]
            # if Main.maybeSave(lst):

            Main.hof_class.ddu[self.curindex].RTNO = self.ui.lineEdit.text()
            Main.hof_class.ddu[self.curindex].Outbound_dir = self.ui.lineEdit_2.text()
            Main.hof_class.ddu[self.curindex].Inbound_dir = self.ui.lineEdit_3.text()
            Main.hof_class.ddu[
                self.curindex
            ].Outbound_price = self.ui.doubleSpinBox.value()
            Main.hof_class.ddu[
                self.curindex
            ].Inbound_price = self.ui.doubleSpinBox_2.value()
            Main.hof_class.ddu[self.curindex].sectiontimes_Y = self.ui.spinBox.value()
            Main.hof_class.ddu[self.curindex].sectiontimes_Z = self.ui.spinBox_2.value()

            self.sig.connect(self.hofview.update_listviews)
            self.sig.emit(self.curindex, 2)
            event.accept()
            # else:
            #     event.ignore()
            # self.close()

    class AddRouteEntry(QMainWindow):
        sig = Signal(int, int)

        def __init__(
            self,
            parent=None,
            single_dual: bool = False,
            route: str = "",
            Outbound_dir: str = "",
            Inbound_dir: str = "",
            curindex: int = 0,
        ):
            super().__init__(parent)
            self.ui = AddRouteEntry_UI()
            self.ui.setupUi(self)
            self.curindex = curindex
            self.ui.lineEdit.setText(route)
            self.ui.lineEdit_2.setText(Outbound_dir)
            self.ui.lineEdit_3.setText(Inbound_dir)
            self.ui.checkBox.setChecked(single_dual)

        def closeEvent(self, event):
            Main.hof_class.infosystem[self.curindex].route = self.ui.lineEdit.text()
            Main.hof_class.infosystem[
                self.curindex
            ].direction1 = self.ui.lineEdit_2.text()
            Main.hof_class.infosystem[
                self.curindex
            ].direction2 = self.ui.lineEdit_3.text()
            self.sig.connect(Main.opened_windows[0].update_listviews)
            self.sig.emit(self.curindex, 4)
            event.accept()

    class AddTermini(QMainWindow):
        sig = Signal(int, int)

        def __init__(
            self,
            parent=None,
            eric: str = "",
            Destination: str = "",
            busfull: str = "",
            disps: list = [],
            curindex: int = 0,
        ):
            super().__init__(parent)
            self.ui = AddTermini_UI()
            self.ui.setupUi(self)
            self.ui.lineEdit.setText(eric)
            self.ui.lineEdit_2.setText(Destination)
            self.ui.lineEdit_3.setText(busfull)
            self.curindex = curindex
            self.ui.toolButton.clicked.connect(self.select_flip)
            # self.ui.tableWidget.setItem
            for i in range(len(disps)):
                self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(disps[i]))

        def select_flip(self):
            files = QFileDialog.getOpenFileNames(
                self,
                "Select Desti Display",
                "C:\\",
                "Destination Display Files (*.bmp)",
            )
            print(files)
            self.ui.tableWidget.clear()
            # for i in range(3,2-len(files),-1):
            #     print(i,3-len(files),files[0][4-i],len(files[0][4-i]))
            #     self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(re.sub(r'^(.*?hanover\\)', '', files[0][4-i])))
            count = 0
            lim = len(files[0]) - 1
            while count < 4:
                print(count, lim, files[0])
                # print(files[0][count],re.findall(r'^.*hanover/', files[0][count]))
                self.ui.tableWidget.setItem(
                    3 - count,
                    0,
                    (
                        QTableWidgetItem(
                            ""
                            if count > lim
                            else re.sub(r"(?i:^.*?hanover/)", "", files[0][count])
                        )
                    ),
                )  # QTableWidgetItem(re.sub(r'^.*?hanover/', '', files[0][count])) if count < lim else QTableWidgetItem("")))
                count += 1

        def closeEvent(self, event):
            Main.hof_class.termini[self.curindex].eric = self.ui.lineEdit.text()
            Main.hof_class.termini[
                self.curindex
            ].destination = self.ui.lineEdit_2.text()
            Main.hof_class.termini[self.curindex].busfull = self.ui.lineEdit_3.text()
            disps = []
            for i in range(3, -1, -1):
                item = self.ui.tableWidget.item(i, 0)
                if item is not None:
                    disps.append(item.text())
                else:
                    disps.append("")

            count_empty = disps.count("")
            if count_empty > 0 and (disps[3] != "" and disps[0] == ""):
                disps = disps[::-1]
            print(disps)
            Main.hof_class.termini[self.curindex].flip = disps
            self.sig.connect(Main.opened_windows[0].update_listviews)
            self.sig.emit(self.curindex, 3)
            event.accept()

    class EricGuesser(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = EricGuesser_UI()
            self.ui.setupUi(self)
            # self.ui.listWidget.addItems([i.eric for i in Main.hof_class.termini])
            print([i.eric for i in Main.hof_class.termini[:50]])
            self.ui.EricSEL.addItems([i.eric for i in Main.hof_class.termini])
            self.ui.EricSEL.currentItemChanged.connect(self.show_guesses)
            self.ui.pushButton.clicked.connect(self.choose_as_eric)
            # self.ui.pushButton.clicked.connect(self.guess)
            # self.ui.pushButton_2.clicked.connect(self.close)

        def show_guesses(self):
            self.ui.EricGuessur.clear()
            item = self.ui.EricSEL.currentIndex()
            index = item.row()
            code = Main.hof_class.termini[index]._eric.orig
            if not code:
                code = Main.hof_class.termini[index].eric
            guesses = Main.exhaust_guesses(code if code[-1] != "0" else code[:-1])

            for i in guesses:
                self.ui.EricGuessur.addItem(f"{i[0]} ({i[1]}%)")
                item = self.ui.EricGuessur.item(self.ui.EricGuessur.count() - 1)
                item.setData(
                    Qt.ItemDataRole.UserRole, i[0]
                )  # Store the guess as user data

            # self.ui.EricGuessur.addItems([f"{guess[0]} ({guess[1]}%)" for guess in guesses])
            # for i in range(self.ui.EricGuessur.count()):
            #     item = self.ui.EricGuessur.item(i)
            #     item.setData(Qt.ItemDataRole.UserRole, guess[0])  # Store the index as
            #     #         for i, each in enumerate(bs_ids):
            # busstop_obj = None

            # # Only try lookup by bus stop ID - no fallback
            # busstop_index = self.busstop_id_to_index.get(each)
            # if busstop_index is not None:
            #     busstop_obj = Main.hof_class.stopreporter[busstop_index]
            #     # Create list item with the bus stop name and store the ID as data
            #     item = QListWidgetItem(busstop_obj.name)
            #     item.setData(Qt.ItemDataRole.UserRole, each)  # Store the busstopID directly
            #     self.ui.listWidget.addItem(item)

        def choose_as_eric(self):
            """Choose the selected guess as the Eric code."""
            item = self.ui.EricGuessur.currentItem()
            if not item:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Please select a guess to set as Eric code.",
                    QMessageBox.Ok,
                )
                return

            eric_code = item.data(Qt.ItemDataRole.UserRole)
            itema = self.ui.EricSEL.currentIndex()
            index = itema.row()
            # index = Main.hof_class.termini[index].eric
            Main.hof_class.termini[index].eric = eric_code
            QMessageBox.information(
                self,
                "Success",
                f"Set Eric code to {eric_code} for {Main.hof_class.termini[index].destination}.",
                QMessageBox.Ok,
            )
            # self.ui.EricSEL.takeItem(itema.row())

        # def guess(self):
        #     code = self.ui.lineEdit.text().strip()
        #     if not code:
        #         QMessageBox.warning(self, "Error", "Please enter a code to guess.", QMessageBox.Ok)
        #         return
        #     results = exhaust_guesses(code)
        #     if not results:
        #         QMessageBox.information(self, "No Results", "No guesses found for the given code.", QMessageBox.Ok)
        #         return
        #     self.ui.textBrowser.clear()
        #     for text, score in results:
        #         self.ui.textBrowser.append(f"{text.upper()} ({score}%)")

    class EditEnMasse(QMainWindow):
        sig = Signal()  # Signal to notify parent of bulk changes

        def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = EditEnMasse_UI()
            self.ui.setupUi(self)

            # State management
            self.staged_changes = {}  # {stop_index: {'name': ..., 'EngDisplay': ..., etc.}}
            # Stop indices whose selection should survive filter passes.
            # Hidden items remain in this set so they re-appear selected once visible again.
            self._persisted_selection: set[int] = set()
            # Guard flag: True only while _restore_selection_if_possible is running so that
            # _load_current_selection does not overwrite the persisted set mid-restore.
            self._is_restoring_selection: bool = False
            self.hofview = Main.opened_windows[0] if Main.opened_windows else None

            # Load all stops into listWidget
            self._load_stops()

            # Connect search/filter
            self.ui.searchbar.textChanged.connect(self._filter_stops)

            # Connect selection change to load current values
            self.ui.listWidget.itemSelectionChanged.connect(
                self._load_current_selection
            )

            # Connect section fare spinboxes (apply-on-edit)
            self.ui.doubleSpinBox.valueChanged.connect(self._apply_outbound_fare)
            self.ui.doubleSpinBox_2.valueChanged.connect(self._apply_inbound_fare)

            # Connect English name textbox (apply-on-edit)
            self.ui.english_textbox.textEdited.connect(self._apply_english_name)

            # Connect autoskip checkbox (apply-on-edit)
            self.ui.checkBox.stateChanged.connect(self._apply_autoskip)

            # Connect page configuration buttons
            self.ui.pushButton_2.clicked.connect(
                lambda: self._apply_page_config(w8w6_different=True, chi_pages=3)
            )
            self.ui.pushButton.clicked.connect(
                lambda: self._apply_page_config(w8w6_different=False, chi_pages=3)
            )
            self.ui.pushButton_5.clicked.connect(
                lambda: self._apply_page_config(w8w6_different=True, chi_pages=2)
            )
            self.ui.pushButton_4.clicked.connect(
                lambda: self._apply_page_config(w8w6_different=False, chi_pages=2)
            )

            # Connect Revert and Confirm buttons
            self.ui.pushButton_6.clicked.connect(self._revert_changes)
            self.ui.pushButton_7.clicked.connect(self._confirm_changes)

            # Initialize spinboxes to neutral values
            self.ui.doubleSpinBox.setValue(-1.0)
            self.ui.doubleSpinBox_2.setValue(-1.0)

        def _load_stops(self):
            """Load all stops from Main.hof_class.stopreporter into listWidget."""
            self.ui.listWidget.clear()
            for i, stop in enumerate(Main.hof_class.stopreporter):
                item = QListWidgetItem(stop.name)
                item.setData(Qt.ItemDataRole.UserRole, i)  # Store original index
                self.ui.listWidget.addItem(item)

        def _filter_stops(self, search_text: str):
            """Filter listWidget items based on search text, preserving selection."""
            search_lower = search_text.lower()

            # Snapshot any currently selected stop indices into the persisted set
            # *before* visibility changes can cause Qt to silently drop them.
            for item in self.ui.listWidget.selectedItems():
                self._persisted_selection.add(item.data(Qt.ItemDataRole.UserRole))

            # Update visibility for every item.
            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                stop_index = item.data(Qt.ItemDataRole.UserRole)
                stop = Main.hof_class.stopreporter[stop_index]

                visible = (
                    search_lower in stop.name.lower()
                    or search_lower in stop.EngDisplay.lower()
                )
                item.setHidden(not visible)

            # Restore selection to all visible items that belong to the persisted
            # set, then refresh detail fields exactly once.
            self._restore_selection_if_possible()

        def _restore_selection_if_possible(self):
            """Re-select every visible item whose stop index is in _persisted_selection.

            listWidget signals are blocked for the duration so that each individual
            setSelected(True) call does not fire itemSelectionChanged and trigger a
            redundant cascade of field reloads.  _load_current_selection is called
            once manually at the end to refresh the detail fields.
            """
            lw = self.ui.listWidget
            self._is_restoring_selection = True
            lw.blockSignals(True)
            try:
                lw.clearSelection()
                for i in range(lw.count()):
                    item = lw.item(i)
                    if (
                        not item.isHidden()
                        and item.data(Qt.ItemDataRole.UserRole)
                        in self._persisted_selection
                    ):
                        item.setSelected(True)
            finally:
                lw.blockSignals(False)
                self._is_restoring_selection = False

            # Single refresh of detail fields for the restored selection state.
            self._load_current_selection()

        def _load_current_selection(self):
            """Load values from selected stop(s) into input fields."""
            # When the user drives a selection change (not an internal restore), keep
            # the persisted set in sync: add newly selected visible items and remove
            # visible items the user has explicitly deselected, while leaving
            # hidden items untouched so they re-appear selected when visible again.
            if not self._is_restoring_selection:
                lw = self.ui.listWidget
                visible_selected: set[int] = set()
                visible_deselected: set[int] = set()
                for i in range(lw.count()):
                    item = lw.item(i)
                    idx = item.data(Qt.ItemDataRole.UserRole)
                    if item.isSelected():
                        visible_selected.add(idx)
                    elif not item.isHidden():
                        visible_deselected.add(idx)
                self._persisted_selection = (
                    self._persisted_selection - visible_deselected
                ) | visible_selected

            selected_items = self.ui.listWidget.selectedItems()

            if len(selected_items) == 1:
                # Load values from single selected stop
                stop_index = selected_items[0].data(Qt.ItemDataRole.UserRole)
                stop = Main.hof_class.stopreporter[stop_index]

                # Get current or staged values
                if stop_index in self.staged_changes:
                    osf = self.staged_changes[stop_index].get(
                        "Outbound_sectionfare", stop._raw_Outbound_sectionfare
                    )
                    isf = self.staged_changes[stop_index].get(
                        "Inbound_sectionfare", stop._raw_Inbound_sectionfare
                    )
                    eng = self.staged_changes[stop_index].get(
                        "EngDisplay", stop.EngDisplay
                    )
                else:
                    # Access raw values directly to avoid string conversions
                    osf = stop._raw_Outbound_sectionfare
                    isf = stop._raw_Inbound_sectionfare
                    eng = stop.EngDisplay

                # Block signals while setting values to avoid triggering apply methods
                self.ui.doubleSpinBox.blockSignals(True)
                self.ui.doubleSpinBox_2.blockSignals(True)
                self.ui.english_textbox.blockSignals(True)

                # Handle both float and potential string values safely
                try:
                    osf_val = (
                        float(osf)
                        if (
                            isinstance(osf, (int, float))
                            or (
                                isinstance(osf, str)
                                and osf.replace(".", "").replace("-", "").isdigit()
                            )
                        )
                        else -1.0
                    )
                    isf_val = (
                        float(isf)
                        if (
                            isinstance(isf, (int, float))
                            or (
                                isinstance(isf, str)
                                and isf.replace(".", "").replace("-", "").isdigit()
                            )
                        )
                        else -1.0
                    )
                except (ValueError, AttributeError):
                    osf_val = -1.0
                    isf_val = -1.0

                self.ui.doubleSpinBox.setValue(osf_val)
                self.ui.doubleSpinBox_2.setValue(isf_val)
                self.ui.english_textbox.setText(eng)

                # Load autoskip state
                current_name = (
                    self.staged_changes[stop_index].get("name", stop.name)
                    if stop_index in self.staged_changes
                    else stop.name
                )
                props = decode_stop_name(current_name)
                self.ui.checkBox.setChecked(props.autoskip)

                self.ui.doubleSpinBox.blockSignals(False)
                self.ui.doubleSpinBox_2.blockSignals(False)
                self.ui.english_textbox.blockSignals(False)
            else:
                # Multiple or no selection - reset to neutral
                self.ui.doubleSpinBox.blockSignals(True)
                self.ui.doubleSpinBox_2.blockSignals(True)
                self.ui.english_textbox.blockSignals(True)
                self.ui.checkBox.blockSignals(True)

                self.ui.doubleSpinBox.setValue(-1.0)
                self.ui.doubleSpinBox_2.setValue(-1.0)
                self.ui.english_textbox.clear()
                self.ui.checkBox.setChecked(False)

                self.ui.doubleSpinBox.blockSignals(False)
                self.ui.doubleSpinBox_2.blockSignals(False)
                self.ui.english_textbox.blockSignals(False)
                self.ui.checkBox.blockSignals(False)

            # Update status bar with selection count
            count = len(selected_items)
            if count > 0:
                self.statusBar().showMessage(f"{count} stop(s) selected")
            else:
                self.statusBar().clearMessage()

        def _apply_outbound_fare(self, value: float):
            """Apply outbound section fare to all selected stops."""
            selected_items = self.ui.listWidget.selectedItems()
            if not selected_items:
                return

            for item in selected_items:
                stop_index = item.data(Qt.ItemDataRole.UserRole)

                # Initialize staged changes for this stop if not exists
                if stop_index not in self.staged_changes:
                    self.staged_changes[stop_index] = {}

                # Stage the change
                self.staged_changes[stop_index]["Outbound_sectionfare"] = value

                # Apply visual feedback
                self._mark_item_modified(item)

            self.statusBar().showMessage(
                f"Applied outbound fare ${value:.2f} to {len(selected_items)} stop(s)"
            )

        def _apply_inbound_fare(self, value: float):
            """Apply inbound section fare to all selected stops."""
            selected_items = self.ui.listWidget.selectedItems()
            if not selected_items:
                return

            for item in selected_items:
                stop_index = item.data(Qt.ItemDataRole.UserRole)

                # Initialize staged changes for this stop if not exists
                if stop_index not in self.staged_changes:
                    self.staged_changes[stop_index] = {}

                # Stage the change
                self.staged_changes[stop_index]["Inbound_sectionfare"] = value

                # Apply visual feedback
                self._mark_item_modified(item)

            self.statusBar().showMessage(
                f"Applied inbound fare ${value:.2f} to {len(selected_items)} stop(s)"
            )

        def _apply_english_name(self, text: str):
            """Apply English name to all selected stops."""
            selected_items = self.ui.listWidget.selectedItems()
            if not selected_items:
                return

            for item in selected_items:
                stop_index = item.data(Qt.ItemDataRole.UserRole)
                stop = Main.hof_class.stopreporter[stop_index]

                # Initialize staged changes for this stop if not exists
                if stop_index not in self.staged_changes:
                    self.staged_changes[stop_index] = {}

                # Stage the English display change
                self.staged_changes[stop_index]["EngDisplay"] = text

                # Also update the name suffix if @ count changed
                current_name = self.staged_changes[stop_index].get("name", stop.name)
                updated_name = self._recalculate_name_with_eng_display(
                    current_name, text
                )
                if updated_name != current_name:
                    self.staged_changes[stop_index]["name"] = updated_name
                    item.setText(updated_name)

                # Apply visual feedback
                self._mark_item_modified(item)

            self.statusBar().showMessage(
                f"Applied English name to {len(selected_items)} stop(s)"
            )

        def _apply_autoskip(self, state: int):
            """Apply autoskip setting to all selected stops."""
            selected_items = self.ui.listWidget.selectedItems()
            if not selected_items:
                return

            autoskip_enabled = state == Qt.CheckState.Checked.value

            for item in selected_items:
                stop_index = item.data(Qt.ItemDataRole.UserRole)
                stop = Main.hof_class.stopreporter[stop_index]

                # Get current or staged values
                if stop_index in self.staged_changes:
                    current_name = self.staged_changes[stop_index].get(
                        "name", stop.name
                    )
                    current_eng = self.staged_changes[stop_index].get(
                        "EngDisplay", stop.EngDisplay
                    )
                else:
                    current_name = stop.name
                    current_eng = stop.EngDisplay

                # Decode to get current properties
                props = decode_stop_name(current_name)
                base_name = props.base_name

                # Encode with new autoskip setting (preserve other settings)
                eng_at_count = current_eng.count("@")
                new_name = encode_stop_name(
                    base_name,
                    autoskip_enabled,
                    props.w8w6_different,
                    props.chi_pages,
                    eng_at_count,
                )

                # Stage the change
                if stop_index not in self.staged_changes:
                    self.staged_changes[stop_index] = {}
                self.staged_changes[stop_index]["name"] = new_name

                # Update listWidget display to show new name immediately
                item.setText(new_name)
                self._mark_item_modified(item)

            status = "enabled" if autoskip_enabled else "disabled"
            self.statusBar().showMessage(
                f"Autoskip {status} for {len(selected_items)} stop(s)"
            )

        def _mark_item_modified(self, item: QListWidgetItem):
            """Mark a list item as modified with visual feedback."""
            # Set background color to light yellow
            item.setBackground(QBrush(QColor(255, 255, 200)))

            # Add tooltip showing what's changed
            stop_index = item.data(Qt.ItemDataRole.UserRole)
            if stop_index in self.staged_changes:
                changes = self.staged_changes[stop_index]
                tooltip = "Modified: " + ", ".join(changes.keys())
                item.setToolTip(tooltip)

        def _apply_page_config(self, w8w6_different: bool, chi_pages: int):
            """Apply page configuration to all selected stops."""
            selected_items = self.ui.listWidget.selectedItems()
            if not selected_items:
                return

            for item in selected_items:
                stop_index = item.data(Qt.ItemDataRole.UserRole)
                stop = Main.hof_class.stopreporter[stop_index]

                # Get current or staged values
                if stop_index in self.staged_changes:
                    current_name = self.staged_changes[stop_index].get(
                        "name", stop.name
                    )
                    current_eng = self.staged_changes[stop_index].get(
                        "EngDisplay", stop.EngDisplay
                    )
                else:
                    current_name = stop.name
                    current_eng = stop.EngDisplay

                # Decode to get base name and current autoskip
                props = decode_stop_name(current_name)
                base_name = props.base_name
                autoskip = props.autoskip  # Preserve existing autoskip setting

                # Encode with new page configuration
                eng_at_count = current_eng.count("@")
                new_name = encode_stop_name(
                    base_name, autoskip, w8w6_different, chi_pages, eng_at_count
                )

                # Stage the change
                if stop_index not in self.staged_changes:
                    self.staged_changes[stop_index] = {}
                self.staged_changes[stop_index]["name"] = new_name

                # Update listWidget display to show new name immediately
                item.setText(new_name)
                self._mark_item_modified(item)

            # Create status message based on configuration
            if w8w6_different:
                if chi_pages == 3:
                    config_name = "6w 3 pages, 8w 2 pages (!~)"
                else:
                    config_name = "6w 2 pages, 8w 1 page (~)"
            else:
                config_name = (
                    f"{chi_pages} pages for 6w/8w {'!!' if chi_pages == 3 else '!'}"
                )

            self.statusBar().showMessage(
                f"Applied {config_name} to {len(selected_items)} stop(s)"
            )

        def _recalculate_name_with_eng_display(
            self, current_name: str, eng_display: str
        ) -> str:
            """Recalculate stop name based on new English display (for suffix update)."""
            # Decode current name to extract properties
            props = decode_stop_name(current_name)

            # Count @ in new English display
            eng_at_count = eng_display.count("@")

            # Re-encode with new @ count to update suffix if needed
            new_name = encode_stop_name(
                props.base_name,
                props.autoskip,
                props.w8w6_different,
                props.chi_pages,
                eng_at_count,
            )

            return new_name

        def _revert_changes(self):
            """Revert all staged changes and restore original state."""
            # Clear all staged changes and the persisted selection set so that no
            # stale selection state lingers after an intentional full revert.
            self.staged_changes.clear()
            self._persisted_selection.clear()

            # Reset all list items to original names and colors
            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                stop_index = item.data(Qt.ItemDataRole.UserRole)
                original_stop = Main.hof_class.stopreporter[stop_index]

                # Restore original name
                item.setText(original_stop.name)

                # Clear background color
                item.setBackground(QBrush())

                # Clear tooltip
                item.setToolTip("")

            # Reset input fields to neutral state
            self.ui.doubleSpinBox.blockSignals(True)
            self.ui.doubleSpinBox_2.blockSignals(True)
            self.ui.english_textbox.blockSignals(True)
            self.ui.checkBox.blockSignals(True)

            self.ui.doubleSpinBox.setValue(-1.0)
            self.ui.doubleSpinBox_2.setValue(-1.0)
            self.ui.english_textbox.clear()
            self.ui.checkBox.setChecked(False)

            self.ui.doubleSpinBox.blockSignals(False)
            self.ui.doubleSpinBox_2.blockSignals(False)
            self.ui.english_textbox.blockSignals(False)
            self.ui.checkBox.blockSignals(False)

            # Clear selection
            self.ui.listWidget.clearSelection()

            self.statusBar().showMessage("Reverted all changes")

        def _confirm_changes(self):
            """Commit all staged changes to Main.hof_class.stopreporter."""
            if not self.staged_changes:
                QMessageBox.information(self, "No Changes", "No changes to commit.")
                return

            # Ask for confirmation
            reply = QMessageBox.question(
                self,
                "Confirm Changes",
                f"Apply changes to {len(self.staged_changes)} stop(s)?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

            # Apply all staged changes to Main.hof_class.stopreporter
            for stop_index, changes in self.staged_changes.items():
                stop = Main.hof_class.stopreporter[stop_index]

                # Apply each modified property
                if "name" in changes:
                    stop.name = changes["name"]
                if "EngDisplay" in changes:
                    stop.EngDisplay = changes["EngDisplay"]
                if "Outbound_sectionfare" in changes:
                    stop.Outbound_sectionfare = changes["Outbound_sectionfare"]
                if "Inbound_sectionfare" in changes:
                    stop.Inbound_sectionfare = changes["Inbound_sectionfare"]

            # Notify parent HOFView to refresh all stopreporter displays
            if (
                self.hofview
                and hasattr(self.hofview, "ui")
                and hasattr(self.hofview.ui, "listWidget_3")
            ):
                # Refresh all items in HOFView's stopreporter listWidget
                for i in range(self.hofview.ui.listWidget_3.count()):
                    self.hofview.ui.listWidget_3.item(i).setText(
                        Main.hof_class.stopreporter[i].name
                    )

            # Show success message
            QMessageBox.information(
                self,
                "Success",
                f"Successfully applied changes to {len(self.staged_changes)} stop(s).",
            )

            # Clear staged changes after committing
            self.staged_changes.clear()

            # Close dialog
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Main.Entrypoint()
    widget.show()
    sys.exit(app.exec())
