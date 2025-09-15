"""
Я нихуя не понимаю в питоне.
Пожалуйста, не бейте.
Я не умею программировать
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from pypresence import Presence
import time
import os

# Game :3
from game.settings import DiscordRPC
from game.settings import toggle_fullscreen

from game.player import Player

from game.voxel import Voxel
from game.voxel import blocks

from game.world import World

discord_rpc = DiscordRPC()

app = Ursina()

# Отключаем все стандартные overlay-элементы
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False

window.color = color.hex("#87CEEB")
window.title = 'Quadix'
window.icon = 'resources/icon.ico'

# Создаем текстовый объект для дебаг-информации
debug_text = Text(
    position=window.top_left,
    origin=(-0.5, 0.5),
    scale=(1, 1),
    color=color.white,
    background=False,
    visible=False
)

def update_debug_info():
    debug_text.text = (
        f"FPS: {round(1/time.dt)}\n"
        f"Координаты: {round(player.get_position().x, 1), round(player.get_position().y, 1), round(player.get_position().z, 1)}\n"
        f"Объектов: {len(scene.entities)}\n"
        f"Скорость: {round(player.get_speed(), 1)}\n"
        f"Режим полета: {'ВКЛ' if player.get_fly_status() else 'ВЫКЛ'}\n"
        f"Высота камеры: {round(player.get_y_pivot(), 2)}\n"
    )

player = Player()

Texture.default_path = './resources/'
Audio.default_path = './resources/'

current_world = World(player=player)

for box in current_world.get_boxes():
    box.world = current_world
    box.player = player

def update():
    if debug_text.visible:
        update_debug_info()

    player.update()
    player.control()

    if time.time() % 15 < time.dt:
        discord_rpc.update_status()

def input(key):
    if key == 'f3':
        debug_text.visible = not debug_text.visible
    
    if key == 'f11':
        toggle_fullscreen()
    
    if key == 'escape':
        if not player.get_inventory().visible:
            application.quit()

    player.ursina_control(key)

# Предзагрузка инвентаря
player.get_inventory().enabled = True
player.get_inventory().visible = False

# Завершение работы
def on_exit():
    try:
        discord_rpc.close()
    except:
        pass

app.on_exit = on_exit
player.respawn()
app.run()
