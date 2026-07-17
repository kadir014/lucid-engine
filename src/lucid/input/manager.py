"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

import pygame

from lucid.input.mapping import (
    KEY_MAPPING,
    MOUSE_MAPPING,
    KEY_INVDICT,
    MOUSE_INVDICT
)


class InputManager:
    """
    Input manager class.

    Attributes
    ----------
    mouse
        Mouse position
    mouse_rel
        Relative mouse position to last frame
    min_drift_threshold
        Minimum amount of drift allowed to not register joystick movement
    """

    def __init__(self) -> None:
        #                          held pressed released
        self.__key_states = {k:   [0,   0,      0       ] for k in KEY_MAPPING}
        self.__mouse_states = {b: [0,   0,      0       ] for b in MOUSE_MAPPING}

        self.mouse = pygame.Vector2()
        self.mouse_rel = pygame.Vector2()

        self.fetch_joysticks()

        self.min_drift_threshold = 0.01

    def fetch_joysticks(self) -> None:
        """
        Get all current joystick devices.
        
        You might want to call this to update internal state if any device is
        plugged or unplugged during application runtime.
        """
        self.__joysticks = [pygame.Joystick(i) for i in range(pygame.joystick.get_count())]

    def update(self, events: list[pygame.Event]) -> None:
        """
        Update input states.
        
        Parameters
        ----------
        events
            List of pygame events
        """

        self.mouse = pygame.Vector2(*pygame.mouse.get_pos())
        self.mouse_rel = pygame.Vector2(*pygame.mouse.get_rel())

        # Reset pressed and released states
        for k in self.__key_states:
            self.__key_states[k][1] = 0
            self.__key_states[k][2] = 0

        for b in self.__mouse_states:
            self.__mouse_states[b][1] = 0
            self.__mouse_states[b][2] = 0

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.__key_states[KEY_INVDICT[event.key]][0] = 1
                self.__key_states[KEY_INVDICT[event.key]][1] = 1

            elif event.type == pygame.KEYUP:
                self.__key_states[KEY_INVDICT[event.key]][0] = 0
                self.__key_states[KEY_INVDICT[event.key]][1] = 0
                self.__key_states[KEY_INVDICT[event.key]][2] = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__mouse_states[MOUSE_INVDICT[event.button]][0] = 1
                self.__mouse_states[MOUSE_INVDICT[event.button]][1] = 1

            elif event.type == pygame.MOUSEBUTTONUP:
                self.__mouse_states[MOUSE_INVDICT[event.button]][0] = 0
                self.__mouse_states[MOUSE_INVDICT[event.button]][1] = 0
                self.__mouse_states[MOUSE_INVDICT[event.button]][2] = 1

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.__mouse_states["wheelup"][1] = True
                else:
                    self.__mouse_states["wheeldown"][1] = True

    def key_pressed(self, key: str) -> bool:
        """ Check if key is just pressed. """
        return self.__key_states[key.lower()][1]

    def key_released(self, key: str) -> bool:
        """ Check if key is just released. """
        return self.__key_states[key.lower()][2]

    def key_held(self, key: str) -> bool:
        """ Check if key is currently pressed. """
        return self.__key_states[key.lower()][0]

    def mouse_pressed(self, button: str) -> bool:
        """ Check if mouse button is just pressed. """
        return self.__mouse_states[button.lower()][1]

    def mouse_released(self, button: str) -> bool:
        """ Check if mouse button is just released. """
        return self.__mouse_states[button.lower()][2]

    def mouse_held(self, button: str) -> bool:
        """ Check if mouse button is currently pressed. """
        return self.__mouse_states[button.lower()][0]

    def mouse_wheel_up(self) -> bool:
        """ Check if mouse wheel rotated upwards. """
        return self.__mouse_states["wheelup"][1]

    def mouse_wheel_down(self) -> bool:
        """ Check if mouse wheel is rotated downwards. """
        return self.__mouse_states["wheeldown"][1]
    
    def get_stick(self, index: int = 0, device: int = 0) -> pygame.Vector2:
        """ Return the normalized stick axis at given index. """

        if len(self.__joysticks) == 0:
            return pygame.Vector2(0.0)

        axis = self.get_stick_raw(index, device)
        length = axis.length_squared()

        if length > 1.0:
            axis.normalize_ip()

        if length <= self.min_drift_threshold:
            axis = pygame.Vector2(0.0)

        return axis
        
    def get_stick_raw(self, index: int = 0, device: int = 0) -> pygame.Vector2:
        """ Return the raw stick axis at given index. """

        if len(self.__joysticks) == 0:
            return pygame.Vector2(0.0)

        return pygame.Vector2(
            self.__joysticks[device].get_axis(index * 2),
            self.__joysticks[device].get_axis(index * 2 + 1)
        )