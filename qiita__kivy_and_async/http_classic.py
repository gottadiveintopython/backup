from kivy.app import App
from kivy.lang import Builder
import threading

KV_CODE = '''
Label:
    text: 'Kivy & Trio'
'''


def animate_label(label, exit_flag):
    import time
    import requests
    from kivy.clock import mainthread

    @mainthread
    def update_label(*, text):
        label.text = text

    session = requests.Session()
    while not exit_flag.is_set():
        response = session.get(r'http://httpbin.org/user-agent', timeout=2)
        update_label(text=response.text)
        time.sleep(3)
        response = session.get(r'http://httpbin.org/headers', timeout=2)
        update_label(text=response.text)
        time.sleep(3)


class TestApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        self.exit_flag = threading.Event()
        threading.Thread(
            target=animate_label,
            args=(self.root, self.exit_flag)).start()

    def on_stop(self):
        self.exit_flag.set()


if __name__ == '__main__':
    TestApp().run()
