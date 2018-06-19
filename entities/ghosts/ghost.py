# coding=utf-8
"""
Ghost Class. The monster class that handles pretty much all ghost interactions.
"""
import random
import sys
from collections import deque

import constants
from utility import Tile, PVector
from constants import DEFAULT_SPEED, SCARED_TICKS
from entities.ghosts import GhostInit, GhostState
from entities import Pacman, Entity


class Ghost(Entity):
    """
    Ghost class
    """
    # Class variables
    surfs = ()  # The default frames are a class variable and are modified
    blue_surfs = []
    white_surfs = []
    grey_surfs = []
    cycle_states = (
        GhostState.SCATTER, GhostState.CHASE, GhostState.SCATTER, GhostState.CHASE, GhostState.SCATTER,
        GhostState.CHASE)  # Ghosts alternate between chasing and scattering.
    cycle_timers = (5 * 60, 20 * 60, 5 * 60, 20 * 60, 5 * 60, sys.maxsize)  # 60 ticks per second

    def __init__(self, level, init_ghost: GhostInit, pacman: Pacman):
        super().__init__(init_ghost.get_start(), level)
        # Surfaces
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
        """
        Modify default colours to ghost colour
        :param target_clr:
        :return:
        """
        for surf in Ghost.surfs:
            new_surf = surf.copy()
            new_surf.load_surface(ghost_colour=target_clr, gif_location=constants.SPRITE_FOLDER)
            self.surf_list.append(new_surf)

    @classmethod
    def load_surfs(cls):
        """
        Class method to load surfaces
        :return:
        """
        for frame_num in range(1, 7):
            cls.surfs += (Tile(frame_num, f'ghost {frame_num}', f'Frame {frame_num} of ghost'),)
        # make scared surfs
        for surf in cls.surfs:
            blue_surf = surf.copy()  # Scared
            blue_surf.load_surface(ghost_colour=(50, 50, 255, 255), gif_location=constants.SPRITE_FOLDER)
            white_surf = surf.copy()  # Flashing
            white_surf.load_surface(ghost_colour=(255, 255, 255, 255), gif_location=constants.SPRITE_FOLDER)
            grey_surf = surf.copy()  # Dead
            grey_surf.load_surface(ghost_colour=(0, 0, 0, 255), gif_location=constants.SPRITE_FOLDER)
            cls.blue_surfs.append(blue_surf)
            cls.white_surfs.append(white_surf)
            cls.grey_surfs.append(grey_surf)

    def update(self):
        """
        Method called by Game to update ghost
        :return:
        """
        self.check_node()
        self.move()
        if self.dead():
            return

        self.check_pacman_eat()
        if self.scared():
            self.reduce_scared_timer()
        else:  # Normal Game State
            self.increment_cycle()

    def increment_cycle(self):
        """
        Increment cycle timer
        :return:
        """
        self.cycle_timer += 1
        if self.cycle_timer >= Ghost.cycle_timers[self.cycle_pos]:
            self.cycle_timer = 0
            self.cycle_pos += 1
            self.reverse()
        self.cycle_state = Ghost.cycle_states[self.cycle_pos]
        # To make sure that revived Ghost snaps back to original state

    def check_node(self):
        """
        Checks if Ghost is on node and processes location if it is
        :return:
        """
        if self.is_on_node():  # If we need to check our direction
            self.check_teleport()  # Check if we need to teleport
            if self.dead():  # If we're dead
                self.adjust_speed()  # Try to speed up
                self.enter_box()  # Try to get into the box
            elif self.scared():  # If we're scared
                self.speed = 0.5  # Immediately slow down
                self.choose_random_direc()  # Move randomly
                # print(self.scared_timer)
            else:  # Normal state
                self.speed = DEFAULT_SPEED
                # Will always be able to go back to normal speed instantly because of even timer value from scared
                # and dead requires to be on tile
                if self.start in self.level.ghost_box and self.nearest_node in self.level.ghost_box:
                    # If we're in the box and we're not blinky
                    self.exit_box()
                elif self.cycle_state == GhostState.SCATTER:
                    # Scatter to corners
                    self.scatter()
                else:
                    # Use specialized targeting method
                    self.update_direc()

    def scatter(self):
        """
        Alternates between the two different corners.
        :return:
        """
        if self.nearest_node == self.corner_1:
            self.next_corner = self.corner_2
        elif self.nearest_node == self.corner_2:
            self.next_corner = self.corner_1
        self.direc = self.closest_direction(self.next_corner)

    def reduce_scared_timer(self):
        """
        Reduces scared timer
        :return:
        """
        if self.scared_timer:
            self.scared_timer -= 1

    def check_pacman_eat(self):
        """
        Check if they should be scared and start slowly running away
        :return:
        """
        if self.pacman.ate_big_dot:
            self.scared_timer = SCARED_TICKS  # ticks. Current default is 300 aka 5 seconds.
            if not self.scared():
                self.reverse()

    def reverse(self):
        """
        Ghosts always reverse direction when they change states.
        :return:
        """
        self.direc *= -1

    def adjust_speed(self):
        """
        Try to speed up if we are on the correct increment to ensure that we land on the node perfectly.
        :return:
        """
        if self.pos % 4 == PVector(0, 0):
            # Quadruple Speed
            self.speed = 4
        elif self.pos % 2 == PVector(0, 0):
            # Double Speed
            self.speed = 2
        elif self.pos % 1 == PVector(0, 0):
            # Normal Speed
            self.speed = 1
        else:  # Half speed, continue
            pass

    def choose_random_direc(self):
        """
        Chooses a random direction to go in
        :return:
        """
        choices = self.level.edges[self.nearest_node].copy()  # So that we don't modify the original dictionary
        choices -= {self.nearest_node + round(self.direc) * -1}  # Take out backwards direction, if it is in set
        chosen_direc = self.direc_to(random.choice(tuple(choices)))  # Choose random direction
        self.direc = chosen_direc

    def update_surf(self):
        """
        Update surface.
        :return:
        """
        self.increment_frame_num()  # Change frames to simulate ghost_moving
        if self.dead():
            self.surf = Ghost.grey_surfs[self.anim_num].surface.copy()  # Dead
        elif self.scared():
            if self.flash_white():
                self.surf = Ghost.white_surfs[self.anim_num].surface.copy()  # White
            else:
                self.surf = Ghost.blue_surfs[self.anim_num].surface.copy()  # Blue
        else:
            self.surf = self.surf_list[self.anim_num].surface.copy()  # Standard

        self.look_at_pacman()  # Change eye location

    def flash_white(self):
        """

        :return:
        """
        if self.scared_timer < 120:  # Less than 2 seconds
            flash_num = self.scared_timer // 12  # Every 1/5 of a second they change colours
            if flash_num % 2 == 0:
                return True
            else:
                return False
        return False

    def closest_direction(self, target):
        """
        Uses euclidean distance to determine the node that will get the ghost closest to the target location.
        May not be the best, but it's what the original used.
        :param target:
        :return:
        """
        dist = {}
        for node in self.level.edges[self.nearest_node]:
            if self.direc_to(node) is None:  # for Teleport catching
                continue
            if self.direc_to(node) == self.direc * -1:  # Cannot go backwards
                continue
            dist[self.direc_to(node)] = node.dist_from(target)
        sorted_dist = sorted(dist.keys(), key=dist.get)
        return sorted_dist[0]

    def bfs(self, target):
        """

        :param target:
        :return:
        """
        # Another method that can be used, however has not been updated for the new Ghost class.
        queue = deque([(self.nearest_node, [self.nearest_node])])
        closest_distance = sys.maxsize
        closest_path = None
        visited = set()

        # Every element is a tuple of the current node and the path that it took INCLUDING START
        while queue:  # Standard BFS
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

    @staticmethod
    def build_direc(node_path):
        """

        :param node_path:
        :return:
        """
        # OUTDATED
        direc_path = []
        if len(node_path) == 1:
            raise ValueError('Ghost is already on Pacman, but has not won yet. ')
        for idx, node in enumerate(node_path):
            if idx == len(node_path) - 1:
                break
            direc_path.append(node.direc_to(node_path[idx + 1]))
        return direc_path

    def collided_with_pacman(self):
        """

        :return:
        """
        # sprite_dist = abs(self.pos - self.pacman.pos)
        # if sprite_dist.x < 15 and sprite_dist.y < 15:
        #     return True
        return self.nearest_node == self.pacman.nearest_node
        # Simple check, sometimes results in pacman phasing through ghost, but that it is in original game too.

    def in_ghost_box(self):
        """
        Utility Function
        :return:
        """
        return self.nearest_node in self.level.ghost_box

    def exit_box(self):
        """
        If the ghost is in the box, this function will be called to force the ghost out of the box
        since ghost door is a wall.
        :return:
        """
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
        """
        Just like exit_box, but is the opposite.
        :return:
        """
        if self.nearest_node == self.start:  # We can now switch states.
            self.direc = PVector(0, 0)
            self.increment_cycle()
        elif self.nearest_node == self.level.ghost_door:  # We're on the door, now to get in
            exit_node, = tuple(self.level.edges[self.level.ghost_door])
            opposite_direc = self.direc_to(exit_node) * -1  # Move in the opposite direction as the exit
            self.direc = opposite_direc
        elif self.in_ghost_box():  # Move to start location
            self.direc = self.direc_to(self.start)
        elif self.nearest_node in self.level.edges[self.level.ghost_door]:  # We're right outside the ghost door
            self.direc = self.direc_to(self.level.ghost_door)
        else:  # Make our way to the ghost door
            self.direc = self.closest_direction(self.level.ghost_door)

    def look_at_pacman(self):
        """

        :return:
        """
        pupil_set = (4, 6)
        for y in range(4, 8, 1):
            for x in range(3, 7, 1):
                self.surf.set_at((x, y), (255, 255, 255, 255))
                self.surf.set_at((x + 6, y), (255, 255, 255, 255))

                if self.pacman.pos.x > self.pos.x and self.pacman.pos.y > self.pos.y:
                    # player is to lower-right
                    pupil_set = (5, 6)
                elif self.pacman.pos.x < self.pos.x and self.pacman.pos.y > self.pos.y:
                    # player is to lower-left
                    pupil_set = (3, 6)
                elif self.pacman.pos.x > self.pos.x and self.pacman.pos.y < self.pos.y:
                    # player is to upper-right
                    pupil_set = (5, 4)
                elif self.pacman.pos.x < self.pos.x and self.pacman.pos.y < self.pos.y:
                    # player is to upper-left
                    pupil_set = (3, 4)
                else:
                    pupil_set = (4, 6)

        for y in range(pupil_set[1], pupil_set[1] + 2, 1):
            for x in range(pupil_set[0], pupil_set[0] + 2, 1):
                self.surf.set_at((x, y), (0, 0, 255, 255))
                self.surf.set_at((x + 6, y), (0, 0, 255, 255))

    def path_to(self, target: PVector):
        """
        Used to switch between bfs and closest when testing
        :param target:
        :return:
        """
        return self.closest_direction(target)

    def dead(self):
        """
        Utility
        :return:
        """
        return self.cycle_state == GhostState.DEAD

    def die(self):
        """
        Utility
        :return:
        """
        self.cycle_state = GhostState.DEAD
        self.scared_timer = 0

    def scared(self):
        """
        Utility
        :return:
        """
        return self.scared_timer

    def update_direc(self):
        """
        To suppress warning for pycharm
        :return:
        """
        raise NotImplementedError('Do not create raw Ghost objects.')
