from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from pypresence import Presence
import time

class DiscordRPC:
    def __init__(self):
        try:
            self.RPC = Presence("112233445566778899")
            self.RPC.connect()
            self.RPC.update(
                details="Играет в Quadix",
                state="Строит мир",
                large_image="quadix_logo",
                large_text="Quadix Game",
                start=time.time()
            )
        except:
            pass

    def update_status(self):
        try:
            self.RPC.update(
                details=f"Hehe.... heh...",
                state="Meow",
                large_image="quadix_logo",
                large_text="silly",
                start=time.time()
            )
        except:
            pass

    def close(self):
        self.RPC.close();

def toggle_fullscreen():
    if window.fullscreen:
        window.fullscreen = False
        window.borderless = False
        window.size = (1280, 720)
        window.position = (0, 0)
    else:
        window.fullscreen = True
        window.borderless = True