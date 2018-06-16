# coding=utf-8
import random
import sys
from collections import deque
from math import ceil

import constants
from PVector import PVector
from constants import GameMode, default_speed
from entity import Entity
from ghosts.ghost_init import GhostInit
from ghosts.ghost_state import GhostState
from level import Level
from pacman import Pacman
from tile import Tile


class Ghost(Entity):
    surfs = ()  # The default frames are a class variable and are modified
    blue_surfs = []
    white_surfs = []
    grey_surfs = []
    cycle_states = (
        GhostState.SCATTER, GhostState.CHASE, GhostState.SCATTER, GhostState.CHASE, GhostState.SCATTER,
        GhostState.CHASE)
    cycle_timers = (5 * 60, 20 * 60, 5 * 60, 20 * 60, 5 * 60, sys.maxsize)

    def __init__(self, level: Level, init_ghost: GhostInit, pacman: Pacman):
        super().__init__(init_ghost.get_start(), level)
        self.surf_list = []
        self.surf = None
        self.max_anim_num = 5
        self.pacman = pacman
        self.corner_1 = init_ghost.corner_1
        self.corner_2 = init_ghost.corner_2
        self.start = init_ghost.get_start()
        self.next_corner = self.corner_2

        self.scared_timer = 0
        self.dead_timer = 0

        self.cycle_pos = 0
        self.cycle_timer = 0
        self.cycle_state = Ghost.cycle_states[self.cycle_pos]

        if not Ghost.surfs:
            Ghost.load_surfs()

    def convert_surfaces(self, target_clr: tuple) -> None:
        for surf in Ghost.surfs:
            new_surf = surf.copy()
            new_surf.load_surface(ghost_colour=target_clr, gif_location=constants.sprite_folder)
            self.surf_list.append(new_surf)

    @classmethod
    def load_surfs(cls):
        for frame_num in range(1, 7):
            cls.surfs += (Tile(frame_num, f'ghost {frame_num}', f'Frame {frame_num} of ghost'),)
        # make scared surfs
        for surf in cls.surfs:
            blue_surf = surf.copy()
            blue_surf.load_surface(ghost_colour=(50, 50, 255, 255), gif_location=constants.sprite_folder)
            white_surf = surf.copy()
            white_surf.load_surface(ghost_colour=(255, 255, 255, 255), gif_location=constants.sprite_folder)
            grey_surf = surf.copy()
            grey_surf.load_surface(ghost_colour=(0, 0, 0, 255), gif_location=constants.sprite_folder)
            cls.blue_surfs.append(blue_surf)
            cls.white_surfs.append(white_surf)
            cls.grey_surfs.append(grey_surf)

    def update(self):
        self.check_node()
        self.move()
        if self.dead():
            pass
        elif self.scared():
            self.reduce_scared_timer()
        else:  # Normal Game State
            self.check_pacman_eat()
            self.increment_cycle()

    def increment_cycle(self):
        self.cycle_timer += 1
        if self.cycle_timer >= Ghost.cycle_timers[self.cycle_pos]:
            self.cycle_timer = 0
            self.cycle_pos += 1
            self.reverse()
        self.cycle_state = Ghost.cycle_states[self.cycle_pos]

    def check_node(self):
        if self.is_on_node():  # If we need to check our direction
            self.check_teleport()
            if self.dead():
                self.adjust_speed()
                self.enter_box()
            elif self.scared():
                self.speed = 0.5
                self.choose_random_direc()
                # print(self.scared_timer)
            else:
                self.speed = default_speed
                if self.start in self.level.ghost_box and self.nearest_node in self.level.ghost_box:
                    # TODO change to level ghost box
                    self.exit_box()
                elif self.cycle_state == GhostState.SCATTER:
                    self.scatter()
                else:
                    self.update_direc()

    def scatter(self):
        if self.nearest_node == self.corner_1:
            self.next_corner = self.corner_2
        elif self.nearest_node == self.corner_2:
            self.next_corner = self.corner_1
        self.direc = self.closest_direction(self.next_corner)

    def reduce_scared_timer(self):
        if self.scared_timer:
            self.scared_timer -= 1

    def check_pacman_eat(self):
        if self.pacman.ate_big_dot:
            self.scared_timer = 300  # ticks, TODO add this to level file
            self.reverse()

    def reverse(self):
        self.direc *= -1

    def adjust_speed(self):
        if self.pos % 4 == PVector(0, 0):
            # Quadruple Speed
            self.speed = 4
        elif self.pos % 2 == PVector(0, 0):
            # Double Speed
            self.speed = 2
        elif self.pos % 1 == PVector(0, 0):
            # Double Speed
            self.speed = 1
        else:
            pass

    def choose_random_direc(self):
        # print(self.nearest_node,self.direc)
        choices = self.level.edges[self.nearest_node].copy()
        # print(choices)
        choices -= {self.nearest_node + round(self.direc) * -1}
        # print(choices)
        chosen_direc = self.direc_to(random.choice(tuple(choices)))
        # print(self.direc,chosen_direc)
        # print()
        self.direc = chosen_direc

    def update_surf(self):
        self.increment_frame_num()
        if self.dead():
            self.surf = Ghost.grey_surfs[self.anim_num].surface
        elif self.scared():
            # TODO Add flashing
            if self.flash_white():
                self.surf = Ghost.white_surfs[self.anim_num].surface
            else:
                self.surf = Ghost.blue_surfs[self.anim_num].surface
        else:
            self.surf = self.surf_list[self.anim_num].surface

    def flash_white(self):
        if self.scared_timer < 120:
            flash_num = self.scared_timer // 12
            if flash_num % 2 == 0:
                return True
            else:
                return False
        return False

    def closest_direction(self, target):
        dist = {}
        for node in self.level.edges[self.nearest_node]:
            if self.direc_to(node) is None:  # for Teleport catching
                continue
            if self.direc_to(node) == self.direc * -1:  # Cannot go backwards
                continue
            dist[self.direc_to(node)] = node.dist_from(target)
        sorted_dist = sorted(dist.keys(), key=dist.get)
        return sorted_dist[0]

    def bfs(self, target):  # Has not been fixed since changes to speed
        queue = deque([(self.nearest_node, [self.nearest_node])])
        closest_distance = sys.maxsize
        closest_path = None
        visited = set()

        # Every element is a tuple of the current node and the path that it took INCLUDING START
        while queue:
            current, path = queue.popleft()
            visited.add(current)
            if current == target and len(path) > 1:
                return self.direc_to(path[1])
            for node in self.level.edges[current] - visited:
                if len(path) == 1 and self.direc_to(node) == self.direc * -1:  # Cannot go backwards
                    continue
                queue.append((node, path + [node]))
                if path[-1].dist_from(target) < closest_distance:
                    closest_path = path
        return self.direc_to(closest_path[1])
        # return None

    def build_direc(self, node_path):  # OUTDATED
        direc_path = []
        if len(node_path) == 1:
            raise ValueError('Ghost is already on Pacman, but has not won yet. ')
        for idx, node in enumerate(node_path):
            if idx == len(node_path) - 1:
                break
            direc_path.append(node.direc_to(node_path[idx + 1]))
        return direc_path

    def collided_with_pacman(self):
        # sprite_dist = abs(self.pos - self.pacman.pos)
        # if sprite_dist.x < 15 and sprite_dist.y < 15:
        #     return True
        return self.nearest_node == self.pacman.nearest_node

    def in_ghost_box(self):
        return self.nearest_node in self.level.ghost_box  # TODO modify to level ghost box

    def exit_box(self):
        if self.nearest_node == self.level.ghost_door:  # Let's get out of the ghost box. And never go back
            assert len(self.level.edges[
                           self.level.ghost_door]) == 1, "There is more than 1 exit for the ghost door. \
                           The ghosts don't know which way to go!"
            outside, = self.level.edges[self.level.ghost_door]
            self.direc = self.direc_to(outside)
        elif self.level.ghost_door in self.get_adj_nodes():  # We're almost out of the ghost box.
            self.direc = self.direc_to(self.level.ghost_door)
        else:  # Find node that is closest to the exit.
            self.direc = self.closest_direction(self.level.ghost_door)

    def enter_box(self):
        if self.nearest_node == self.start:
            self.direc = PVector(0, 0)
            self.increment_cycle()
        elif self.nearest_node == self.level.ghost_door:  # We're on the door, now to get in
            exit_node, = tuple(self.level.edges[self.level.ghost_door])
            opposite_direc = self.direc_to(exit_node) * -1
            self.direc = opposite_direc
        elif self.in_ghost_box():
            self.direc = self.direc_to(self.start)
        elif self.nearest_node in self.level.edges[self.level.ghost_door]:  # We're right outside it
            self.direc = self.direc_to(self.level.ghost_door)
        else:  # Make our way to the ghost door
            self.direc = self.closest_direction(self.level.ghost_door)

    def path_to(self, target: PVector):
        return self.closest_direction(target)

    def dead(self):
        return self.cycle_state == GhostState.DEAD

    def die(self):
        self.cycle_state = GhostState.DEAD
        self.scared_timer = 0

    def scared(self):
        return self.scared_timer
