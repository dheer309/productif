from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.properties import NumericProperty
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from ..widgets.custom_scroll import CustomScroll
from ..widgets.hoverflatbutton import HoverFlatButton
from ..widgets.hovericonbutton import HoverIconButton
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import pyrebase


class Settings(MDScreen):
    def __init__(self, **kwargs):
        super(MDScreen, self).__init__(**kwargs)

        self.backend = SettingsBackend()

        app_current_theme = self.backend.show_settings().get('theme')
        # app_current_transition = self.backend.show_settings().get('page_transition')
        current_user_settings = self.backend.show_settings()

        MDApp.get_running_app().themes.get(app_current_theme.lower())()
        MDApp.get_running_app().transition_changed(current_user_settings)

        self.theme = DropDown(
            bar_width=10,
            scroll_type=[
                'bars',
                'content'],
            effect_cls='ScrollEffect',
            smooth_scroll_end=10)
        self.theme.bar_inactive_color = self.theme.bar_color
        self.theme.bind(on_select=lambda instance, x: self.theme_changed(x))

        self.mainbutton_theme = HoverFlatButton(
            text=f"{self.backend.show_settings().get('theme').title()}",
            size_hint=(
                0.6,
                1))
        self.mainbutton_theme.bind(on_release=self.theme.open)
        self.ids.theme.add_widget(self.mainbutton_theme)

        for theme in list(MDApp.get_running_app().themes):
            btn = HoverFlatButton(
                text=theme.title(),
                size_hint_y=None,
                height=self.mainbutton_theme.height)
            btn.bind(on_release=lambda btn: self.theme.select(btn.text))
            self.theme.add_widget(btn)

        self.transition = DropDown(
            bar_width=10,
            scroll_type=[
                'bars',
                'content'],
            effect_cls='ScrollEffect',
            smooth_scroll_end=10)
        self.transition.bar_inactive_color = self.transition.bar_color
        self.transition.bind(
            on_select=lambda instance,
            x: self.transition_changed(x))

        self.mainbutton_transition = HoverFlatButton(
            text=f"{self.backend.show_settings().get('page_transition').title()}",
            size_hint=(
                0.6,
                1))
        self.ids.transition.add_widget(self.mainbutton_transition)
        self.mainbutton_transition.bind(on_release=self.transition.open)

        for transition in list(MDApp.get_running_app().transitions):
            btn = HoverFlatButton(
                text=transition.title(),
                size_hint_y=None,
                height=self.mainbutton_transition.height)
            btn.bind(on_release=lambda btn: self.transition.select(btn.text))
            self.transition.add_widget(btn)

        self.choose_color = ChooseColors()

    def theme_changed(self, theme):
        try:
            self.ids.appearance_settings.remove_widget(self.choose_color)
            self.ids.scroller.scroll_y = 1
        except BaseException:
            pass
        setattr(self.mainbutton_theme, 'text', theme.title())
        self.backend.edit_settings('theme', theme.lower())
        MDApp.get_running_app().themes.get(theme.lower())()

    def transition_changed(self, transition):
        setattr(self.mainbutton_transition, 'text', transition.title())
        self.backend.edit_settings('page_transition', transition.lower())
        user_settings = self.backend.show_settings()
        MDApp.get_running_app().transition_changed(user_settings)


class ChooseColors(GridLayout):
    pass


class ColorField():
    pass


class SettingsBackend:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        firebase_config = {
            "apiKey": "AIzaSyBea6bseF08qPyY9VDhDVrDv0_nmEY6ayA",
            "authDomain": "kivy-pp-se.firebaseapp.com",
            "databaseURL": "https://kivy-pp-se-default-rtdb.firebaseio.com",
            "projectId": "kivy-pp-se",
            "storageBucket": "kivy-pp-se.appspot.com",
            "messagingSenderId": "107431491811",
            "appId": "1:107431491811:web:cbfbd94bb03c431a4e2dd6",
            "measurementId": "G-6ZTW1FJSRJ"
        }

        firebase = pyrebase.initialize_app(firebase_config)
        self.db = firebase.database()

    def show_settings(self):
        dd = self.db.get()

        for sd in dd.each():
            dict = sd.val()

            output_data = {
                "theme": dict["theme"],
                "page_transition": dict["page_transition"]
            }

            if output_data.get('theme') in MDApp.get_running_app().themes:
                pass
            else:
                self.edit_settings('theme', 'dark')
                self.show_settings()

            if output_data.get('page_transition') in MDApp.get_running_app().transitions:
                pass
            else:
                self.edit_settings('page_transition', 'slide')
                self.show_settings()

            return output_data

    def edit_settings(self, key, value):
        data = {f"{key}": value}
        self.db.child("settings").update(data)
