from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial

KV_CODE = '''
Label:
    text: 'Kivy & Trio'
    font_size: sp(80)
'''


def animate_label(label, __):
    from kivy.url
    schedule_once = Clock.schedule_once

    def phase1(__):
        label.text = 'Kivy + Trio'
        label.color = get_random_color()
        schedule_once(phase2, .5)

    def phase2(__):
        label.text = '=='
        label.color = get_random_color()
        schedule_once(phase3, .5)

    def phase3(__):
        label.text = 'Awesome!'
        label.color = get_random_color()
        schedule_once(phase1, 2)

    schedule_once(phase1, 2)

    
class TestApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        Clock.schedule_once(partial(animate_label, self.root))


if __name__ == '__main__':
    TestApp().run()
