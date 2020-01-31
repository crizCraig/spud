import math
import sys
import timeit
from random import randint
from typing import Type, Union, List, Tuple

import numpy as np
from numba import njit
pi = np.pi


# TODO: Implement broad phase sweep and prune when you have more than 2 objects


@njit(cache=True, nogil=True)
def lines_intersect(a1, a2, b1, b2):
    p = get_intersect(a1, a2, b1, b2)
    if p is not None:
        if is_between(a1, p, a2) and is_between(b1, p, b2):
            return True
    return False


@njit(cache=True, nogil=True)
def distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


@njit(cache=True, nogil=True)
def is_between(start, mid, end):
    diff = abs(distance(start, mid) + distance(mid, end) - distance(start, end))
    return diff < 1e-4


@njit(cache=True, nogil=True)
def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: np.array [x, y] a point on the first line
    a2: np.array [x, y] another point on the first line
    b1: np.array [x, y] a point on the second line
    b2: np.array [x, y] another point on the second line

    Explanation: http://robotics.stanford.edu/~birch/projective/node4.html
    """
    s = np.vstack((a1, a2, b1, b2))            # s for stacked
    h = np.hstack((s, np.ones((4, 1))))        # h for homogeneous
    l1 = np.cross(h[0], h[1])                  # get first line
    l2 = np.cross(h[2], h[3])                  # get second line
    x, y, z = np.cross(l1, l2)                 # point of intersection
    if z == 0:                                 # lines are parallel
        return None
    return np.array([x / z, y / z])


@njit(cache=True, nogil=True)
def get_lines_from_rect_points(rect_points: tuple):
    p = rect_points
    ret = ((p[0], p[1]),
           (p[1], p[2]),
           (p[2], p[3]),
           (p[3], p[0]))
    return ret


@njit(cache=True, nogil=True)
def check_collision_agents(agents: list):
    """
    :param agents: List of agents with ego_lines property containing 4 points
        representing corners of hit box
    """
    pairs = get_pairs(agents)
    collisions = []
    for pair in pairs:
        if check_collision(pair[0].ego_lines, pair[1].ego_lines):
            pair[0].collided_with.append(pair[1])
            pair[1].collided_with.append(pair[0])
            collisions.append(pair)
    return collisions


@njit(cache=True, nogil=True)
def check_collision_ego_obj(ego_rect: tuple, obj2: tuple):
    """

    :param ego_rect: Points representing 4 corners of ego
    :param obj2: n x 2 x 2 tuple of start & end points for n lines
    :return: (bool) True if collision
    """
    return check_collision(get_lines_from_rect_points(ego_rect), obj2)


@njit(cache=True, nogil=True)
def check_collision(obj1: tuple, ob2: tuple):
    """

    :param obj1: n x 2 x 2 tuple of start & end points for n lines
    :param ob2: n x 2 x 2 tuple of start & end points for n lines
    :return:
    """

    for line1_start, line1_end in obj1:
        for line2_start, line2_end in ob2:
            if lines_intersect(np.array(line1_start), np.array(line1_end),
                               np.array(line2_start), np.array(line2_end)):
                return True
    return False



def get_rect(center_x, center_y, angle, width, height):
    """
    :param angle: angle in radians
    :return: 4 points of the rectangle
    """
    ego_rect = _get_rect(center_x, center_y, angle, width, height)

    # Numba likes tuples
    ego_rect_tuple = tuple(map(tuple, ego_rect.tolist()))

    return ego_rect, ego_rect_tuple


@njit(cache=True, nogil=True)
def _get_rect(center_x, center_y, angle, width, height):
    """
    :param angle: angle in radians
    :return: 4 points of the rectangle
    """
    w = width
    h = height
    rot = np.array([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle),  np.cos(angle)]])
    p = np.array([[-w/2, h/2], [w/2, h/2], [w/2, -h/2], [-w/2, -h/2]])

    # Rotate
    ret = rot @ p.T

    # Zip up to proper shape
    ret = np.dstack((ret[0], ret[1]))[0]

    # Shift
    ret += np.array([center_x, center_y])

    return ret


@njit(cache=True, nogil=True)
def get_pairs(items: Union[List, Tuple]) -> List:
    pairs = []
    for i, aid1 in enumerate(items):
        for aid2 in items[i+1:]:
            pairs.append((aid1, aid2))
    return pairs


def test_check_collision():
    ego_rect, ego_rect_tuple = get_rect(1, 1, pi / 4, 2, 1)
    ert = tuple(map(tuple, ego_rect.tolist()))  # ego rect tuple
    max_x = max(ego_rect.T[0])
    min_x = min(ego_rect.T[0])
    max_y = max(ego_rect.T[1])
    min_y = min(ego_rect.T[1])
    y_at_max_x = ego_rect[np.where(ego_rect.T[0] == max_x)][0][1]
    mid_x = (max_x - min_x) / 2 + min_x
    mid_y = (max_y - min_y) / 2 + min_y

    # Top boundary should collide
    assert check_collision_ego_obj(ert, (((1e-10, max_y), (1e10, max_y)),))

    # Bottom boundary should collide
    assert check_collision_ego_obj(ert, (((1e-10, min_y), (1e10, min_y)),))

    # Right boundary should collide
    assert check_collision_ego_obj(ert, (((max_x, -1e10), (max_x, 1e10)),))

    # Left boundary should collide
    assert check_collision_ego_obj(ert, (((min_x, -1e10), (min_x, 1e10)),))

    # Small line should collide
    assert check_collision_ego_obj(ert, (((max_x, y_at_max_x),
                                          (max_x, y_at_max_x + 1e-4)),))

    # Zero length line should not collide
    assert not check_collision_ego_obj(ert, (((max_x, y_at_max_x),
                                              (max_x, y_at_max_x)),))

    # Mid x should collide
    assert check_collision_ego_obj(ert, (((mid_x, max_y), (mid_x, min_y)),))

    # Mid x outside y should not collide
    assert not check_collision_ego_obj(ert, (((mid_x, 1e10), (mid_x, 1e10 + 1)),))

    # Mid y should collide
    assert check_collision_ego_obj(ert, (((min_x, mid_y), (max_x, mid_y)),))

    # Mid x outside y should not collide
    assert not check_collision_ego_obj(ert, (((1e20, mid_y), (mid_x, 1e20 - 1)),))


def test_get_rect():
    r, _ = get_rect(0, 0, pi / 2, 2, 1)
    assert all(np.isclose(r[0], [-0.5, -1]))

    r, _ = get_rect(1, 1, pi / 2, 2, 1)
    assert all(np.isclose(r, [[0.5, 0],
                              [0.5, 2],
                              [1.5, 2],
                              [1.5, 0]]).flatten())


def test_lines_intersect():
    assert not lines_intersect(np.array([0, 1], dtype=np.float),
                               np.array([0, 2], dtype=np.float),
                               np.array([1, 10], dtype=np.float),
                               np.array([2, 10], dtype=np.float))
    assert lines_intersect(np.array([0, 1], dtype=np.float),
                           np.array([0, 2], dtype=np.float),
                           np.array([-1, 1], dtype=np.float),
                           np.array([1, 2], dtype=np.float))
    assert lines_intersect(np.array([0, 1], dtype=np.float),
                           np.array([0, 2], dtype=np.float),
                           np.array([0, 2], dtype=np.float),
                           np.array([2, 0], dtype=np.float))
    assert not lines_intersect(np.array([0, 0], dtype=np.float),
                               np.array([0, 1], dtype=np.float),
                               np.array([0, 2], dtype=np.float),
                               np.array([2, 0], dtype=np.float))

    lines_intersect(np.array([randint(0, 10), randint(0, 10)], dtype=np.float),
                    np.array([randint(0, 10), randint(0, 10)], dtype=np.float),
                    np.array([randint(0, 10), randint(0, 10)], dtype=np.float),
                    np.array([randint(0, 10), randint(0, 10)], dtype=np.float))


def test_lines_intersect_x2():
    test_lines_intersect()
    test_lines_intersect()


def test_get_pairs():
    assert get_pairs([1,2,3]) == [(1, 2), (1, 3), (2, 3)]


def main():
    if '--test_check_collision' in sys.argv:
        # get_lines_from_rect_points(
        #     ((1, 0), (1, 0), (1, 0), (1, 0))
        # )
        test_check_collision()
    elif '--test_get_pairs' in sys.argv:
        test_get_pairs()
    else:
        print(timeit.timeit(test_lines_intersect_x2, number=1000))




if __name__ == "__main__":
    main()
