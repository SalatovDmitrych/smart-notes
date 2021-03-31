from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QLabel, \
    QListWidget, QInputDialog, QMessageBox
import json
from datetime import datetime
a =0

class App(QApplication):
    def __init__(self):
        super().__init__(["Умные заметки"])
        self.win = QWidget()
        self.win.show()
        self.win.setContextMenuPolicy(Qt.CustomContextMenu)
        self.date = datetime.now()

        try:
            with open("notes.json", "r") as file:
                file.read()
        except:
            notes = {"Добро пожаловать": {"text": "Добро пожаловать!", "tags": ["приветствие"],
                                          "date_create": self.date.strftime("%d.%m.%Y"),
                                          "last_edit": self.date.strftime("%d.%m.%Y")}}
            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump(notes, file)

        # виджеты
        self.note_text = QTextEdit()
        self.note_list = QListWidget()
        self.tag_list = QListWidget()
        self.create_note_button = QPushButton("Создать заметку")
        self.delete_note_button = QPushButton("Удалить заметку")
        self.tag_line_edit = QLineEdit()
        self.tag_line_edit.setPlaceholderText("Введите тег")
        self.add_tag_button = QPushButton("Добавить к заметеке")
        self.delete_tag_button = QPushButton("удалить тег")
        self.search_tag = QPushButton("Искать заметки по тегу")
        self.note_label = QLabel("Список заметок")
        self.tag_label = QLabel("Список тегов")
        self.date_create_label = QLabel("создан: ")
        self.last_edit_label = QLabel("последние изменение: ")

        # направляющие
        self.date_layout = QHBoxLayout()
        self.root_layout = QHBoxLayout()
        self.text_edit_layout = QVBoxLayout()
        self.func_layout = QVBoxLayout()
        self.double_layout1 = QHBoxLayout()
        self.double_layout2 = QHBoxLayout()

        # размещение
        self.date_layout.addWidget(self.date_create_label)
        self.date_layout.addWidget(self.last_edit_label)
        self.text_edit_layout.addLayout(self.date_layout)
        self.text_edit_layout.addWidget(self.note_text)
        self.func_layout.addWidget(self.note_label)
        self.func_layout.addWidget(self.note_list)
        self.double_layout1.addWidget(self.create_note_button)
        self.double_layout1.addWidget(self.delete_note_button)
        self.func_layout.addLayout(self.double_layout1)
        self.func_layout.addWidget(self.tag_label)
        self.func_layout.addWidget(self.tag_list)
        self.func_layout.addWidget(self.tag_line_edit)
        self.double_layout2.addWidget(self.add_tag_button)
        self.double_layout2.addWidget(self.delete_tag_button)
        self.func_layout.addLayout(self.double_layout2)
        self.func_layout.addWidget(self.search_tag)
        self.root_layout.addLayout(self.text_edit_layout)
        self.root_layout.addLayout(self.func_layout)
        self.win.setLayout(self.root_layout)

        # коннекты
        self.note_list.itemClicked.connect(self.__show_note)
        self.create_note_button.clicked.connect(self.__create_note)
        self.delete_note_button.clicked.connect(self.__del_note)
        self.add_tag_button.clicked.connect(self.__add_tag)
        self.delete_tag_button.clicked.connect(self.__del_tag)
        self.note_text.textChanged.connect(self.__save_text)
        self.search_tag.clicked.connect(self.__search_by_tag)

        self.__load_from_json()

        super().exec_()

    def __load_from_json(self):
        with open("notes.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
            self.note_list.addItems(self.data)

    def __create_note(self):
        date_loc = self.date.strftime("%d.%m.%Y")
        name, result = QInputDialog.getText(self.win, "Добавить заметку", "Название заметки:")
        if result:
            if name in self.data:
                msg = QMessageBox.question(self.win, "предупреждение",
                                           "заметка с таким именем уже сущуствуетю Заменить?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
                if msg == QMessageBox.Ok:
                    self.data[name] = {"text": "", "tags": [], "date_create": date_loc, "last_edit": date_loc}
                    self.note_list.clear()
                    self.note_list.addItems(self.data)
                    self.__save_note(name=name)

            else:
                self.data[name] = {"text": "", "tags": [], "date_create": date_loc, "last_edit": date_loc}
                self.note_list.clear()
                self.note_list.addItems(self.data)
                self.__save_note(name=name)

    def __show_note(self):
        name = self.note_list.selectedItems()[0].text()
        self.note_text.setText(self.data[name]["text"])
        self.tag_list.clear()
        self.tag_list.addItems(self.data[name]["tags"])
        self.date_create_label.setText("создан: " + self.data[name]["date_create"])
        self.last_edit_label.setText("последние изменение: " + self.data[name]["last_edit"])

    def __save_note(self, name=None):
        with open("notes.json", "w", encoding="utf-8") as file:
            date = self.date.strftime("%d.%m.%Y")
            if name == None:
                name = self.note_list.selectedItems()[0].text()
                text = self.note_text.toPlainText()
                self.data[name]["text"] = text
                self.data[name]["last_edit"] = date
            else:
                self.data[name]["text"] = ""
                self.data[name]["last_edit"] = date
            json.dump(self.data, file, sort_keys=True)

    def __del_note(self):
        with open("notes.json", "w", encoding="utf-8") as file:
            name = self.note_list.selectedItems()[0].text()
            del self.data[name]
            json.dump(self.data, file, sort_keys=True)
        self.note_list.clear()
        self.note_text.clear()
        self.__load_from_json()

    def __add_tag(self):
        name = self.note_list.selectedItems()[0].text()
        text = self.tag_line_edit.text()
        if text == "":
            pass
        else:
            if text in self.data[name]["tags"]:
                pass
            else:
                self.data[name]["tags"].append(text)
                self.__show_note()

    def __del_tag(self):
        name_note = self.note_list.selectedItems()[0].text()
        name_tag = self.tag_list.selectedItems()[0].text()
        self.data[name_note]["tags"].remove(name_tag)
        self.__show_note()

    def __search_by_tag(self):
        tag = self.tag_line_edit.text()
        if self.search_tag.text() == "Искать заметки по тегу" and tag != "":
            notes_filtred = {}
            for note in self.data:
                if tag in self.data[note]["tags"]:
                    notes_filtred[note] = self.data[note]
            self.search_tag.setText("Сбросить поиск")
            self.note_list.clear()
            self.tag_list.clear()
            self.note_list.addItems(notes_filtred)
        elif self.search_tag.text() == "Сбросить поиск":
            self.tag_line_edit.clear()
            self.note_list.clear()
            self.tag_list.clear()
            self.note_list.addItems(self.data)
            self.search_tag.setText("Искать заметки по тегу")

    def __save_text(self):
        try:
            name = self.note_list.selectedItems()[0].text()
            text = self.note_text.toPlainText()
            self.data[name]["text"] = text
            self.__save_note()
        except:
            pass


if __name__ == "__main__":
    app = App()