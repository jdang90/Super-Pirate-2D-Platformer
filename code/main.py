from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import * 
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld
import os

# Normalize the working directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Working directory set to:", os.getcwd())

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Super Pirate World')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {
            0: load_pygame(join('data', 'levels', 'omni.tmx')),
            1: load_pygame(join('data', 'levels', '1.tmx')),
            2: load_pygame(join('data', 'levels', '2.tmx')),
            3: load_pygame(join('data', 'levels', '3.tmx')),
            4: load_pygame(join('data', 'levels', '4.tmx')),
            5: load_pygame(join('data', 'levels', '5.tmx')),
        }
        self.tmx_overworld = load_pygame(join('data', 'overworld', 'overworld.tmx'))
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        self.bg_music.play(-1)

    def switch_stage(self, target, unlock=0):
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        else:  # overworld
            if unlock > 0:
                self.data.unlocked_level = 6
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('graphics', 'enemies','level', 'flag'),
            'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('graphics', 'enemies','level', 'palms'),
            'candle': import_folder('graphics','enemies', 'level', 'candle'),
            'window': import_folder('graphics', 'enemies','level', 'window'),
            'big_chain': import_folder('graphics', 'enemies','level', 'big_chains'),
            'small_chain': import_folder('graphics', 'enemies','level', 'small_chains'),
            'candle_light': import_folder('graphics', 'enemies','level', 'candle light'),
            'player': import_sub_folders('graphics', 'player'),
            'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('saw', 'saw_chain'),
            'helicopter': import_folder('graphics', 'enemies','level', 'helicopter'),
            'boat': import_folder('graphics', 'objects', 'boat'),
            'spike': import_image('spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('spike_ball', 'spiked_chain'),
            'tooth': import_folder('graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('graphics', 'enemies', 'shell'),
            'pearl': import_image('bullets', 'pearl'),
            'items': import_sub_folders('graphics', 'items'),
            'particle': import_folder('graphics', 'effects', 'particle'),
            'water_top': import_folder('graphics', 'enemies','level', 'water', 'top'),
            'water_body': import_image('level', 'water', 'body'),
            'bg_tiles': import_folder_dict('graphics', 'enemies','level', 'bg', 'tiles'),
            'cloud_small': import_folder('graphics', 'enemies','level', 'clouds', 'small'),
            'cloud_large': import_image('level', 'clouds', 'large_cloud'),
        }
        self.font = pygame.font.Font(join('graphics', 'enemies', 'ui', 'runescape_uf.ttf'), 40)
        
        self.ui_frames = {
            'heart': import_folder('graphics', 'enemies', 'ui', 'heart'),
            'coin': import_image('ui', 'coin')
        }
        self.overworld_frames = {
            'palms': import_folder('graphics', 'overworld', 'palm'),
            'water': import_folder('graphics', 'overworld', 'water'),
            'path': import_folder_dict('graphics', 'overworld', 'path'),
            'icon': import_sub_folders('graphics', 'overworld', 'icon'),
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('audio', 'jump.wav')),
            'damage': pygame.mixer.Sound(join('audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('audio', 'pearl.wav')),
        }
        self.bg_music = pygame.mixer.Sound(join('audio', 'starlight_city.mp3'))
        self.bg_music.set_volume(0.5)

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.check_game_over()
            self.current_stage.run(dt)
            self.ui.update(dt)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()