import trio
from kivy.app import App
from kivy.lang import Builder

KV_CODE = '''
Label:
    text: 'Kivy & Trio'
    font_size: sp(80)
'''


async def animate_label(label):
    from kivy.utils import get_random_color
    sleep = trio.sleep
    await sleep(2)
    while True:
        label.text = 'Kivy + Trio'
        label.color = get_random_color()
        await sleep(.5)
        label.text = '=='
        label.color = get_random_color()
        await sleep(.5)
        label.text = 'Awesome!'
        label.color = get_random_color()
        await sleep(2)
    

class TestApp(App):
    nursery = None

    def build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        self.nursery.start_soon(animate_label, self.root)

    async def root_task(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def app_task():
                await self.async_run(async_lib='trio')
                nursery.cancel_scope.cancel()

            nursery.start_soon(app_task)


if __name__ == '__main__':
    trio.run(TestApp().root_task)
