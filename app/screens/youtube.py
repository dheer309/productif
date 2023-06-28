from youtubesearchpython import SearchVideos
import json
from kivymd.uix.screen import MDScreen
import webbrowser
from ..widgets.searching_text import SearchingText
from datetime import datetime
from kivymd.uix.gridlayout import MDGridLayout
import threading
from kivy.clock import mainthread
from kivymd.toast import toast


class Youtube(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = None

    def search(self, query):
        self.query = query.strip().lower()
        if query.strip() != '':
            self.ids.scroll_box.clear_widgets()
            self.searching_text = SearchingText()
            self.ids.scroll_box.add_widget(self.searching_text)
            self.thread = threading.Thread(
                target=self.search_thread, args=(query,))
            self.thread.daemon = True
            self.thread.start()
        else:
            toast("There's nothing to search...", duration=1)

    @mainthread
    def add_video_widgets(self):
        if self.results:
            self.ids.scroll_box.remove_widget(self.searching_text)
            for result in self.results:
                result_widget = ResultCard()
                result_widget.ids.thumbnail.source = str(
                    result.get('thumbnails')[0])
                result_widget.ids.video_name.text = str(result.get('title'))
                result_widget.ids.channel_name.text = str(
                    result.get('channel'))
                result_widget.ids.video_duration.text = str(
                    result.get('duration'))
                result_widget.ids.video_views.text = str(
                    result.get('views')) + ' views'
                result_widget.link = str(result.get('link'))
                self.ids.scroll_box.add_widget(result_widget)
        else:
            self.searching_text.text = "No results"

        self.ids.scroller.scroll_y = 1
        self.ids.search_button.disabled = False
        self.ids.search_button.canvas.get_group(
            'hidden')[0].rgba = (0, 0, 0, 0)

    @mainthread
    def no_internet(self):
        self.ids.scroll_box.remove_widget(self.searching_text)

    def search_thread(self, query):
        self.DATE = datetime.now().strftime("%c")
        self.results = None
        try:
            self.results = json.loads(
                SearchVideos(
                    query.strip(),
                    offset=1,
                    mode="json",
                    max_results=10).result())["search_result"]
        except BaseException:
            toast('Could not connect to the internet.', 1)
            self.no_internet()
            return

        self.add_video_widgets()

    def open_in_browser(self, result_widget):
        try:
            webbrowser.open(result_widget.link)
        except:
            toast("Can't find any web browser.", duration=1)


class ResultCard(MDGridLayout):
    pass
