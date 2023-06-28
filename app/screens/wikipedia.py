from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
import requests
from datetime import datetime
import threading
from kivy.clock import mainthread


class Wikipedia(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query):
        if query.strip() != '':
            self.ids.results.text = 'Searching...'
            self.thread = threading.Thread(
                target=self.search_thread, args=(query,))
            self.thread.daemon = True
            self.thread.start()
        else:
            toast("There's nothing to search...", duration=1)

    def search_thread(self, query):
        wikipedia = WikipediaBackend(query)
        summary = wikipedia.summary()
        self.show_result(summary)

    @mainthread
    def show_result(self, summary):
        self.ids.results.text = summary
        self.ids.search_button.disabled = False
        self.ids.search_button.canvas.get_group(
            'hidden')[0].rgba = (0, 0, 0, 0)


class WikipediaBackend():
    def __init__(self, keyword):
        self.keyword = keyword

        self.DATE = datetime.now().strftime('%c')
        self.S = requests.Session()

        self.URL = "https://en.wikipedia.org/w/api.php"

        self.PARAMS = {
            "action": "query",
            "titles": self.keyword,
            "prop": "extracts|info",
            "inprop": "url",
            "redirects": 1,
            "format": "json",
            "exintro": 1,
            "explaintext": True
        }


        try:
            self.R = self.S.get(url=self.URL, params=self.PARAMS)
            self.DATA = self.R.json()["query"]["pages"]
            self.DATA = self.DATA[[i for i in self.DATA][0]]

        except Exception as e:
            self.DATA = None

    def summary(self):
        if self.DATA is not None:
            try:
                title = self.DATA["title"]
                summary = self.DATA["extract"]
                references = []

                if "may refer to" in summary[-16:]:
                    params = {
                        'action': 'query',
                        'list': 'search',
                        'srsearch': self.keyword.title(),
                        'format': 'json'
                    }

                    data = requests.get(self.URL, params=params).json()
                    data = data['query']['search']

                    for search in data:
                        references.append(search['title'])

                summary += '\n\n' + '\n'.join(references)

                return f"{' '*(56-round(len(title)/2))}{title}\n\n" + \
                    summary[:2000] + ('...' if len(summary) > 2000 else '')

            except Exception as e:
                return "Sorry, couldn't fetch any search result for that."

        else:
            toast('Could not connect to the internet/slow connection', duration=1)
            return ''

