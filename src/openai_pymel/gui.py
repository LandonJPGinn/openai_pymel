# check if maya
import pymel.core as pm


class OpenAIPymelGUI:
    """pymel gui class for OpenAIPymelGUI"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(OpenAIPymelGUI, cls).__new__(cls)
        cls.instance.redraw()
        return cls.instance

    def __init__(self, controller):
        self.controller = controller
