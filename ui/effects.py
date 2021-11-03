from kivy.effects.dampedscroll import DampedScrollEffect

from core.structures.structures import CallController


class ImageOverscroll(DampedScrollEffect):
    func = None

    def on_overscroll(self, *args):
        super().on_overscroll(*args)

        self.spring_constant = 0.4

        if self.overscroll > 1:
            self.do_something()

    @CallController(max_call_interval=5)
    def do_something(self):
        print("Overscrolled")
        self.func()
