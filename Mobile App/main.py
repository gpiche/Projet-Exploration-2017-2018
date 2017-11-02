import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


class ObjectButton(GridLayout):

    def find_object(self, button):
        sm.current = 'detail'


class TitleLabel(Label):
    pass


class ObjectLabel(Label):
    pass


class ObjectsScreen(GridLayout):
    pass


class Direction(GridLayout):

    def go_forward(self):
        pass

    def go_back(self):
        pass

    def go_left(self):
        pass

    def go_right(self):
        pass


class MenuScreen(Screen, GridLayout):
    pass


class DetailScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(DetailScreen(name='detail'))


class MobileApp(App):

    def build(self):
        self.icon = 'icon.png'
        return sm


if __name__ == '__main__':
    MobileApp().run()