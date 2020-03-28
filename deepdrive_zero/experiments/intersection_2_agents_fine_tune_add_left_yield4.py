import os
import sys

from deepdrive_zero.experiments import utils
from spinup.utils.run_utils import ExperimentGrid
from spinup import ppo_pytorch
import torch

experiment_name = os.path.basename(__file__)[:-3]
notes = """Try boost_explore 0.6 to get back to normal start entropy of 0.9"""
results = 'Entropy decreased desired amount but did not improve performance. ' \
          'Perhaps too deep into wrong yield policy space.'

env_config = dict(
    env_name='deepdrive-2d-intersection-w-gs-allow-decel-v0',
    is_intersection_map=True,
    expect_normalized_action_deltas=False,
    jerk_penalty_coeff=0.20 / (60*100),
    gforce_penalty_coeff=0.06,
    collision_penalty_coeff=4,
    end_on_harmful_gs=False,
    incent_win=True,
    constrain_controls=False,
    incent_yield_to_oncoming_traffic=True,
)

net_config = dict(
    hidden_units=(256, 256),
    activation=torch.nn.Tanh
)

eg = ExperimentGrid(name=experiment_name)
eg.add('env_name', env_config['env_name'], '', False)
# eg.add('seed', 0)
eg.add('resume', '/home/c2/src/tmp/spinningup/data/intersection_2_agents_fine_tune_add_left_yield3/intersection_2_agents_fine_tune_add_left_yield3_s0_2020_03-24_12-04.34')
eg.add('reinitialize_optimizer_on_resume', True)
eg.add('num_inputs_to_add', 0)
eg.add('pi_lr', 3e-6)
eg.add('vf_lr', 1e-5)
eg.add('boost_explore', 0.6)  # We boosted this too much previously
eg.add('epochs', 8000)
eg.add('steps_per_epoch', 32000)
eg.add('ac_kwargs:hidden_sizes', net_config['hidden_units'], 'hid')
eg.add('ac_kwargs:activation', net_config['activation'], '')
eg.add('notes', notes, '')
eg.add('run_filename', os.path.realpath(__file__), '')
eg.add('env_config', env_config, '')

def train():
    eg.run(ppo_pytorch)


if __name__ == '__main__':
    utils.run(train_fn=train, env_config=env_config, net_config=net_config)