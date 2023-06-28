import random

from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty
from ..widgets.hovericonbutton import HoverIconButton
from ..widgets.hoverflatbutton import HoverFlatButton
from ..widgets.custom_scroll import CustomScroll
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.toast import toast
import pyrebase


class ToDo(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = ToDoBackend()
        self.initialize_tasks()

    def initialize_tasks(self):
        self.ids.scroll_box.clear_widgets()
        tasks = self.database.show_item()
        for task in tasks:
            task_widget = Task()
            task_widget.ids.title.text = task.get('item')
            task_widget.unique_id = task.get('id')
            task_widget.status = task.get('status')
            self.ids.scroll_box.add_widget(task_widget)
            self.ids.scroller.scroll_y = 1

    def delete_task(self, task_widget):
        self.database.delete_item(task_widget.unique_id)
        self.initialize_tasks()
        toast('Task deleted.', duration=0.3)

    def add_task(self):
        added = self.database.add_item('', 0)

        if added:
            self.initialize_tasks()
            toast('Task Created.', duration=0.3)
        else:
            toast('Cannot add task.', duration=1)

    def update_status(self, task_widget):
        if task_widget.status:
            task_widget.status = 0
            self.database.update_item_status(task_widget.unique_id, 0)
        elif not task_widget.status:
            task_widget.status = 1
            self.database.update_item_status(task_widget.unique_id, 1)

    def edit_task(self, task_widget):
        if task_widget.ids.edit_button.text == "EDIT TASK":
            task_widget.ids.title.readonly = False
            task_widget.ids.delete_button.disabled = True
            task_widget.ids.title.cursor_blink = True
            task_widget.ids.edit_button.text = "SAVE"
        else:
            task_widget.ids.title.readonly = True
            task_widget.ids.delete_button.disabled = False
            task_widget.ids.title.cursor_blink = False
            task_widget.ids.title.text = task_widget.ids.title.text.strip()
            self.database.update_item_content(
                task_widget.unique_id, task_widget.ids.title.text)
            task_widget.ids.edit_button.text = "EDIT TASK"
            toast('Note data saved.', duration=0.3)

    def cleanup(self):
        for task_widget in self.ids.scroll_box.children:
            if task_widget.ids.edit_button.text == "SAVE":
                task_widget.ids.title.readonly = True
                task_widget.ids.delete_button.disabled = False
                task_widget.ids.title.cursor_blink = False
                task_widget.ids.edit_button.text = "EDIT"
        self.initialize_tasks()


class Task(MDGridLayout):
    status = NumericProperty()


class ToDoBackend():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        firebase_config = {
          "apiKey": "AIzaSyCrqWiprtSTZhYoDnbWxWoMkU7TBODE88Q",
          "authDomain": "kivy-todo-list.firebaseapp.com",
          "databaseURL": "https://kivy-todo-list-default-rtdb.firebaseio.com",
          "projectId": "kivy-todo-list",
          "storageBucket": "kivy-todo-list.appspot.com",
          "messagingSenderId": "230828293284",
          "appId": "1:230828293284:web:17dc34003c807bd3f8ba31",
          "measurementId": "G-MVMXP956DB"
        }

        firebase = pyrebase.initialize_app(firebase_config)

        self.db = firebase.database()

    def add_item(self, item, status):
        try:
            unique_id = random.randint(1, 10000)
            data = {"id": unique_id, "completed": status, "item": item}

            self.db.child(unique_id).set(data)
            return True
        except BaseException:
            return False

    def delete_item(self, unique_id):
        try:
            dd = self.db.get()

            for sd in dd.each():
                dict = sd.val()

                if int(dict["id"]) == unique_id:
                    self.db.child(unique_id).remove()
        except BaseException:
            return False

    def show_item(self):
        dd = self.db.get()

        output_data = []

        for sd in dd.each():
            dict = sd.val()

            tmp_data = {
                "id": dict["id"],
                "item": dict["item"],
                "status": dict["completed"]
            }

            output_data.append(tmp_data)

        return output_data

    def update_item_content(self, unique_id, item):
        dd = self.db.get()

        for sd in dd.each():
            dict = sd.val()

            data = {"item": item}

            if dict["id"] == unique_id:
                self.db.child(unique_id).update(data)

    def update_item_status(self, unique_id, status):
        dd = self.db.get()

        for sd in dd.each():
            dict = sd.val()

            data = {"completed": status}

            if dict["id"] == unique_id:
                self.db.child(unique_id).update(data)

