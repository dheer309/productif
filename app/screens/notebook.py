import random

import pyrebase

from datetime import datetime
from ..widgets.hovericonbutton import HoverIconButton
from ..widgets.hoverflatbutton import HoverFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import BooleanProperty
from kivymd.toast import toast
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from ..widgets.custom_scroll import CustomScroll


class Notebook(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = NotebookBackend()
        self.initialize_notes()

    def edit_note(self, note_widget):
        if note_widget.ids.edit_button.text == "SAVE":
            note_widget.ids.title.readonly = True
            note_widget.ids.body.readonly = True
            note_widget.ids.delete_button.disabled = False
            note_widget.ids.updatedate_button.disabled = False
            note_widget.ids.title.cursor_blink = False
            note_widget.ids.body.cursor_blink = False
            note_widget.ids.title.text = note_widget.ids.title.text.strip()
            note_widget.ids.body.text = note_widget.ids.body.text.strip()
            note_widget.ids.title.background_normal = 'atlas://data/images/defaulttheme/textinput_active'
            note_widget.ids.body.background_normal = 'atlas://data/images/defaulttheme/textinput_active'
            note_widget.ids.title.background_active = 'atlas://data/images/defaulttheme/textinput_active'
            note_widget.ids.body.background_active = 'atlas://data/images/defaulttheme/textinput_active'
            self.database.edit_notes(
                {
                    'unique_id': note_widget.unique_id,
                    'title': note_widget.ids.title.text,
                    'body': note_widget.ids.body.text})
            toast('Note data saved.', duration=0.3)
            note_widget.ids.edit_button.text = "EDIT"
        elif note_widget.ids.edit_button.text == "EDIT":
            note_widget.ids.title.readonly = False
            note_widget.ids.body.readonly = False
            note_widget.ids.delete_button.disabled = True
            note_widget.ids.updatedate_button.disabled = True
            note_widget.ids.title.cursor_blink = True
            note_widget.ids.body.cursor_blink = True
            note_widget.ids.title.background_normal = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.body.background_normal = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.title.background_active = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.body.background_active = 'atlas://data/images/defaulttheme/textinput'
            note_widget.ids.edit_button.text = "SAVE"
        else:
            print("[  ERROR  ] Huh? How is this even possible? Smh.")

    def delete_note(self, note_widget):
        self.database.delete_note({'unique_id': note_widget.unique_id})
        self.initialize_notes()
        toast('Note deleted.', duration=0.3)

    def add_note(self):
        added = self.database.add_new_note({'title': '', 'body': ''})
        if added:
            self.initialize_notes()
            toast('Note Created.', duration=0.3)
        else:
            toast('Cannot create more notes.', duration=1)

    def update_date(self, note_widget):
        self.database.update_date({'unique_id': note_widget.unique_id})
        self.initialize_notes()
        toast('Date updated.', duration=0.3)

    def initialize_notes(self):
        self.ids.scroll_box.clear_widgets()
        notes = self.database.show_notes()
        for note in notes:
            note_widget = Note()
            note_widget.ids.title.text = note.get('title')
            note_widget.ids.body.text = note.get('body')
            note_widget.ids.date.text = note.get('create_date')
            note_widget.unique_id = note.get('unique_id')
            self.ids.scroll_box.add_widget(note_widget)
            self.ids.scroller.scroll_y = 1

    def cleanup(self):
        for note_widget in self.ids.scroll_box.children:
            if note_widget.ids.edit_button.text == "SAVE":
                note_widget.ids.title.readonly = True
                note_widget.ids.body.readonly = True
                note_widget.ids.delete_button.disabled = False
                note_widget.ids.updatedate_button.disabled = False
                note_widget.ids.title.cursor_blink = False
                note_widget.ids.body.cursor_blink = False
                note_widget.ids.title.background_normal = 'atlas://data/images/defaulttheme/textinput_active'
                note_widget.ids.body.background_normal = 'atlas://data/images/defaulttheme/textinput_active'
                note_widget.ids.title.background_active = 'atlas://data/images/defaulttheme/textinput_active'
                note_widget.ids.body.background_active = 'atlas://data/images/defaulttheme/textinput_active'
                note_widget.ids.edit_button.text = "EDIT"
        self.initialize_notes()


class Note(MDGridLayout):
    pass


class TitleInput(TextInput):
    max_characters = 26

    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class NotebookBackend():
    def __init__(self):

        firebase_config = {
            "apiKey": "AIzaSyBgtD_gEJ7ML25GskLMmSBd0xSOuN_RTPU",
            "authDomain": "kivy-notebook.firebaseapp.com",
            "databaseURL": "https://kivy-notebook-default-rtdb.firebaseio.com",
            "projectId": "kivy-notebook",
            "storageBucket": "kivy-notebook.appspot.com",
            "messagingSenderId": "445896059647",
            "appId": "1:445896059647:web:e16feae24290b9476f7aca",
            "measurementId": "G-X3EW5JGT9R"
        }

        firebase = pyrebase.initialize_app(firebase_config)
        self.db = firebase.database()

    def add_new_note(self, data):
        title = data.get('title')
        body = data.get('body')
        creation_time = datetime.now().strftime("%x")

        try:
            unique_id = random.randint(1, 10000)
            data = {"id": unique_id, "title": title, "body": body, "created_at": creation_time}

            self.db.child(unique_id).set(data)
            return True

        except BaseException:
            return False

    def delete_note(self, data):
        unique_id = data["unique_id"]
        try:
            dd = self.db.get()

            for sd in dd.each():
                dict = sd.val()

                if int(dict["id"]) == unique_id:
                    self.db.child(unique_id).remove()
        except BaseException:
            return False

    def show_notes(self):
        dd = self.db.get()

        output_list = []

        for sd in dd.each():
            dict = sd.val()
            tmp_dict = {
                "unique_id": dict["id"],
                "title": dict["title"],
                "body": dict["body"],
                "create_date": dict["created_at"]
            }

            output_list.append(tmp_dict)

        return output_list[::-1]

    def edit_notes(self, data):
        unique_id = data.get("unique_id")
        title = data.get("title")
        body = data.get("body")

        dd = self.db.get()

        for sd in dd.each():
            dict = sd.val()

            data = {"title": title, "body": body}

            if dict["id"] == unique_id:
                self.db.child(unique_id).update(data)

    def update_date(self, data):
        unique_id = data.get("unique_id")
        creation_time = datetime.now().strftime("%x")

        dd = self.db.get()

        for sd in dd.each():
            dict = sd.val()

            data = {"created_at": creation_time}

            if dict["id"] == unique_id:
                self.db.child(unique_id).update(data)

