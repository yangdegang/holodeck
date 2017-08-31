from gym import spaces
import json
import threading
from collections import defaultdict
import time
from HolodeckClient import HolodeckClient
import numpy as np


class HolodeckAgent(object):
    class TimeoutError(Exception):
        pass

    def __init__(self, client, name="DefaultAgent"):
        self.name = name
        self._client = client
        self._action_buffer = self._client.subscribe_command(name, self.__action_space_shape__())

    def act(self, action):
        self.__act__(action)

    @property
    def action_space(self):
        raise NotImplementedError()

    def __action_space_shape__(self):
        raise NotImplementedError()

    def __act__(self, action):
        # The default act function is to copy the data,
        # but if needed it can be overridden
        np.copyto(self._action_buffer, action)


class UAVAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Box(-1, 3.5, shape=[4])

    def __action_space_shape__(self):
        return [4]


class ContinuousSphereAgent(HolodeckAgent):
    @property
    def action_space(self):
        # return spaces.Box(-1, 1, shape=[2])
        return spaces.Box(np.array([-1, -.25]), np.array([1, .25]))

    def __action_space_shape__(self):
        return [2]


class DiscreteSphereAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Discrete(4)

    def __action_space_shape__(self):
        return [2]

    def __act__(self, action):
        actions = [(10, 0), (-10, 0), (0, 90), (0, -90)]
        # to_act = None
        # for i, j in enumerate(action):
        #     if j == 1:
        #         to_act = actions[i]
        to_act = np.array(actions[action])

        if to_act is None:
            raise RuntimeError("Action must be one-hot")

        np.copyto(self._action_buffer, to_act)


class AndroidAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Box(-1000, 1000, shape=[127])

    def __action_space_shape__(self):
        return [127]
