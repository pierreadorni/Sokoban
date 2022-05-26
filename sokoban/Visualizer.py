""" Classe de visualisation de Sokoban """
import pygame
from .Sokoban import Sokoban
from .State import State
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources  # python <3.7

from .assets import sprites

SCREEN_SIZE = (700, 700)
FPS = 24

with pkg_resources.path(sprites, "hero.png") as path:
    HERO_SPRITE = pygame.image.load(path)
with pkg_resources.path(sprites, "crate.png") as path:
    CRATE_SPRITE = pygame.image.load(path)
with pkg_resources.path(sprites, "goal.png") as path:
    GOAL_SPRITE = pygame.image.load(path)
with pkg_resources.path(sprites, "wall.png") as path:
    WALL_SPRITE = pygame.image.load(path)
with pkg_resources.path(sprites, "floor.png") as path:
    FLOOR_SPRITE = pygame.image.load(path)
with pkg_resources.path(sprites, "crate_goal.png") as path:
    CRATE_GOAL_SPRITE = pygame.image.load(path)


class Visualizer:
    """
    Classe de visualisation d'un jeu Sokoban
    """
    def __init__(self, sokoban: Sokoban) -> None:
        pygame.init()
        self.Sokoban = sokoban
        self.map_size = sokoban.current_state.map_size
        self.case_size = (SCREEN_SIZE[0] // self.map_size[0], SCREEN_SIZE[1] // self.map_size[1])
        # resize the sprites to fit in a case
        self.hero_sprite = pygame.transform.scale(HERO_SPRITE, self.case_size)
        self.crate_sprite = pygame.transform.scale(CRATE_SPRITE, self.case_size)
        self.goal_sprite = pygame.transform.scale(GOAL_SPRITE, self.case_size)
        self.wall_sprite = pygame.transform.scale(WALL_SPRITE, self.case_size)
        self.crate_goal_sprite = pygame.transform.scale(CRATE_GOAL_SPRITE, self.case_size)
        self.floor_sprite = pygame.transform.scale(FLOOR_SPRITE, self.case_size)

        # initialize font
        self.font = pygame.font.SysFont("monospace", 20)

    def show_history(self) -> None:
        """
        Affiche l'historique de l'état du Sokoban
        """
        on = True
        screen = pygame.display.set_mode(SCREEN_SIZE)
        clock = pygame.time.Clock()
        shown_state = 0
        while on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and shown_state < len(self.Sokoban.states) - 1:
                        shown_state += 1
                    elif event.key == pygame.K_LEFT and shown_state > 0:
                        shown_state -= 1
                    elif event.key == pygame.K_ESCAPE:
                        on = False

            screen.fill((195, 210, 210))
            # draw state
            for x in range(0, self.map_size[0]):
                for y in range(0, self.map_size[1]):
                    state: State = self.Sokoban.states[shown_state]
                    if state.but(x, y) and state.caisse(x, y):
                        screen.blit(self.crate_goal_sprite, (x * self.case_size[0], y * self.case_size[1]))
                    elif state.but(x, y):
                        screen.blit(self.goal_sprite, (x * self.case_size[0], y * self.case_size[1]))
                    elif state.caisse(x, y):
                        screen.blit(self.crate_sprite, (x * self.case_size[0], y * self.case_size[1]))
                    elif state.mur(x, y):
                        screen.blit(self.wall_sprite, (x * self.case_size[0], y * self.case_size[1]))
                    else:
                        screen.blit(self.floor_sprite, (x * self.case_size[0], y * self.case_size[1]))
                    if state.personnage(x, y):
                        screen.blit(self.hero_sprite, (x * self.case_size[0], y * self.case_size[1]))

            # if state is win, display a message
            if self.Sokoban.states[shown_state].is_valid():
                s = pygame.Surface(SCREEN_SIZE)
                s.set_alpha(100)
                s.fill((0, 255, 0))
                screen.blit(s, (0, 0))
                # message in the middle of the screen
                text = self.font.render("Win !", True, (0, 0, 0))
                screen.blit(text, (SCREEN_SIZE[0] // 2 - text.get_width()/2, SCREEN_SIZE[1] // 2 - text.get_height()/2))

            # draw text
            text = self.font.render(f"{shown_state+1}/{len(self.Sokoban.states)}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            pygame.display.flip()

            clock.tick(FPS)
