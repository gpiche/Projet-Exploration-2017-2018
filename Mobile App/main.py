import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from os import listdir
from Connexion import Connexion
import json
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

client = Connexion()


class ObjectButton(GridLayout):

    def find_object(self, button):
        client.send(json.dumps({'object': button.text}))
        # sm.current = 'detail'


class TitleLabel(Label):
    pass


class ObjectLabel(Label):
    pass


class ObjectsScreen(GridLayout):
    pass


class Direction(GridLayout):

    @staticmethod
    def go_forward():
        client.send(json.dumps({'command': 'go_ahead'}))

    @staticmethod
    def go_back():
        client.send(json.dumps({'command': 'go_back'}))

    @staticmethod
    def go_left():
        client.send(json.dumps({'command': 'go_left'}))

    @staticmethod
    def go_right():
        client.send(json.dumps({'command': 'go_right'}))

    @staticmethod
    def stop():
        client.send(json.dumps({'command': 'stop'}))


class MenuScreen(Screen, GridLayout):
    pass


class ImageAnimation(GridLayout):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ImageAnimation, self).__init__(**kwargs)
        anim = Animation(angle=360, duration=2)
        anim += Animation(angle=360, duration=2)
        anim.repeat = True
        anim.start(self)

    @staticmethod
    def on_angle( item, angle):
        if angle == 360:
            item.angle = 0


class DetailScreen(Screen):

    @staticmethod
    def go_to_main_page():
        sm.current = 'menu'


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(DetailScreen(name='detail'))


class MobileApp(App):

    def build(self):
        self.icon = 'icon.png'
        return sm


if __name__ == '__main__':
    MobileApp().run()