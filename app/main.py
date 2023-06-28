import os
import sys

from kivy.config import Config
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.resources import resource_add_path
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition, WipeTransition, FadeTransition, FallOutTransition, \
    NoTransition

from app.tools import resource_path

from app.screens.mainmenu import MainMenu
from app.screens.todo import ToDo
from app.screens.notebook import Notebook
from app.screens.wikipedia import Wikipedia
from app.screens.youtube import Youtube
from app.screens.books import Books
from app.screens.settings import Settings

# Screen configuration
Config.set('graphics', 'window_state', 'hidden')
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 720)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', '0')

Window.minimum_width, Window.minimum_height = (720, 480)


class ProductifApp(MDApp):
    title = "Productif"

    # IMPORTANT CONFIG:
    color_theme = 'dark'
    bg_color = ListProperty([29 / 255, 29 / 255, 29 / 255, 1])
    tile_color = ListProperty([40 / 255, 40 / 255, 40 / 255, 1])
    raised_button_color = ListProperty([52 / 255, 52 / 255, 52 / 255, 1])
    text_color = ListProperty([1, 1, 1, 1])
    title_text_color = ListProperty([1, 1, 1, 1])
    accent_color = ListProperty([0.5, 0.7, 0.5, 1])
    app_font = StringProperty(
        resource_path(
            os.path.join(
                'app',
                'data',
                'fonts',
                'Poppins-Regular.ttf')))
    cursor_width = NumericProperty(3)
    home_icon = StringProperty('home')
    home_icon_tooltip = StringProperty('Back')
    add_icon = StringProperty('plus-circle-outline')
    add_icon_tooltip = StringProperty('Create new')
    search_icon = StringProperty('magnify')
    search_icon_tooltip = StringProperty('Search')

    def build(self):
        self.load_all_kv_files()

        # Dictionary of themes
        self.themes = {
            'dark': self.color_theme_dark,
            'light': self.color_theme_light,
        }

        # Dictionary of transitions
        self.transitions = {
            'slide': SlideTransition,
            'wipe': WipeTransition,
            'fade': FadeTransition,
            'fall out': FallOutTransition,
            'none': NoTransition
        }
        # All the screens
        self.root = ScreenManager()
        self.mainmenu = MainMenu()
        self.todo = ToDo()
        self.notebook = Notebook()
        self.wikipedia = Wikipedia()
        self.youtube = Youtube()
        self.books = Books()
        self.settings = Settings()

        # Storage of screen in dictionary
        self.screens = {
            'mainmenu': self.mainmenu,
            'todo': self.todo,
            'notebook': self.notebook,
            'wikipedia': self.wikipedia,
            'youtube': self.youtube,
            'books': self.books,
            'settings': self.settings,
        }

        # Calling switch screen function
        self.root.switch_to(self.mainmenu)
        return self.root

    # Screen switch configuration
    def switch_screen(self, screen_name, direction='left'):
        self.root.transition.direction = direction
        self.root.switch_to(self.screens.get(screen_name))

    # Dark theme configuration
    def color_theme_dark(self):
        self.color_theme = 'dark'
        try:
            Animation.cancel_all(self)
        except BaseException:
            pass
        self.bg_color = [29 / 255, 29 / 255, 29 / 255, 1]
        self.tile_color = [40 / 255, 40 / 255, 40 / 255, 1]
        self.raised_button_color = [52 / 255, 52 / 255, 52 / 255, 1]
        self.text_color = [1, 1, 1, 1]
        self.title_text_color = [1, 1, 1, 1]
        self.accent_color = [0.5, 0.7, 0.5, 1]

    # Light theme configuration
    def color_theme_light(self):
        self.color_theme = 'light'
        try:
            Animation.cancel_all(self)
        except BaseException:
            pass
        self.bg_color = [0.989, 0.989, 0.989, 1.0]
        self.tile_color = [0.94, 0.94, 0.94, 1.0]
        self.raised_button_color = [0.823, 0.823, 0.823, 1.0]
        self.text_color = [0.0, 0.0, 0.0, 1.0]
        self.title_text_color = [0.0, 0.0, 0.0, 1.0]
        self.accent_color = [0.212, 0.099, 1.0, 1.0]

    # Change transitions
    def transition_changed(self, user_settings):
        try:
            self.root.transition = self.transitions.get(
                user_settings.get('page_transition'))()
        except BaseException:
            self.root.transition = SlideTransition()

    # Load other screen UI
    def load_all_kv_files(self):
        Builder.load_file(os.path.join('screens', 'mainmenu.kv'))
        Builder.load_file(os.path.join('screens', 'todo.kv'))
        Builder.load_file(os.path.join('screens', 'notebook.kv'))
        Builder.load_file(os.path.join('screens', 'wikipedia.kv'))
        Builder.load_file(os.path.join('screens', 'youtube.kv'))
        Builder.load_file(os.path.join('screens', 'books.kv'))
        Builder.load_file(os.path.join('screens', 'settings.kv'))


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = ProductifApp()
        app.run()
    except Exception as e:
        print(e)
