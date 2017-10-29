import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from os import listdir
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


class ObjectButton(GridLayout):
    pass


class TitleLabel(Label):
    pass


class ObjectLabel(Label):
    pass


class Container(GridLayout):
    pass


class Direction(GridLayout):
    pass


class MobileApp(App):

    def build(self):
        self.icon = 'icon.png'
        return Container()


if __name__ == '__main__':
    MobileApp().run()