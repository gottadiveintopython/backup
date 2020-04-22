import trio
from kivy.app import App
from kivy.lang import Builder

KV_CODE = '''
Label:
    text: 'Kivy & Trio'
    font_size: sp(40)
'''

async def animate_label(label):
    import asks
    sleep = trio.sleep
    await sleep(1)

    session = asks.Session()
    while True:
        response = await session.get(r'http://httpbin.org/user-agent')
        label.text = response.text
        await sleep(3)
        response = await session.get(r'http://httpbin.org/headers')
        label.text = response.text
        await sleep(3)


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
