

# TODO: Add emergency actions

COMFORTABLE_ACTIONS2 = {
    0: 'IDLE',
    1: 'DECAY_STEERING_MAINTAIN_SPEED',
    2: 'DECAY_STEERING_DECREASE_SPEED',
    3: 'DECAY_STEERING_INCREASE_SPEED',
    4: 'SMALL_STEER_LEFT_MAINTAIN_SPEED',
    5: 'SMALL_STEER_LEFT_DECREASE_SPEED',
    6: 'SMALL_STEER_LEFT_INCREASE_SPEED',
    7: 'SMALL_STEER_RIGHT_MAINTAIN_SPEED',
    8: 'SMALL_STEER_RIGHT_DECREASE_SPEED',
    9: 'SMALL_STEER_RIGHT_INCREASE_SPEED',
    10: 'MICRO_STEER_LEFT_MAINTAIN_SPEED',
    11: 'MICRO_STEER_LEFT_DECREASE_SPEED',
    12: 'MICRO_STEER_LEFT_INCREASE_SPEED',
    13: 'MICRO_STEER_RIGHT_MAINTAIN_SPEED',
    14: 'MICRO_STEER_RIGHT_DECREASE_SPEED',
    15: 'MICRO_STEER_RIGHT_INCREASE_SPEED',
    16: 'LARGE_STEER_LEFT_MAINTAIN_SPEED',
    17: 'LARGE_STEER_LEFT_DECREASE_SPEED',
    18: 'LARGE_STEER_LEFT_INCREASE_SPEED',
    19: 'LARGE_STEER_RIGHT_MAINTAIN_SPEED',
    20: 'LARGE_STEER_RIGHT_DECREASE_SPEED',
    21: 'LARGE_STEER_RIGHT_INCREASE_SPEED',

    # Total safe = 5 steer * 3 accel + idle = 16
    # TODO: Decrease speed, zero steer?
    # TODO: Increase speed (max without losing traction)
    # TODO: Brake emergency stop
}


COMFORTABLE_ACTIONS2_IDLE = 0
COMFORTABLE_ACTIONS2_MAINTAIN_SPEED = {1, 4, 7, 10, 13, 16, 19}
COMFORTABLE_ACTIONS2_DECREASE_SPEED = {2, 5, 8, 11, 14, 17, 20}
COMFORTABLE_ACTIONS2_INCREASE_SPEED = {3, 6, 9, 12, 15, 18, 21}
COMFORTABLE_ACTIONS2_DECAY_STEERING = {1, 2, 3}
COMFORTABLE_ACTIONS2_SMALL_STEER_LEFT = {4, 5, 6}
COMFORTABLE_ACTIONS2_SMALL_STEER_RIGHT = {7, 8, 9}
COMFORTABLE_ACTIONS2_MICRO_STEER_LEFT = {10, 11, 12}
COMFORTABLE_ACTIONS2_MICRO_STEER_RIGHT = {13, 14, 15}
COMFORTABLE_ACTIONS2_LARGE_STEER_LEFT = {16, 17, 18}
COMFORTABLE_ACTIONS2_LARGE_STEER_RIGHT = {19, 20, 21}
COMFORTABLE_ACTIONS2_LARGE_STEER = COMFORTABLE_ACTIONS2_LARGE_STEER_LEFT | COMFORTABLE_ACTIONS2_LARGE_STEER_RIGHT