from typing import Tuple
import unittest

from jkinpylib.robot import Robot
from jkinpylib.robots import PandaArm
from jkinpylib.conversions import geodesic_distance_between_quaternions_np
from jkinpylib.utils import set_seed

import torch
import numpy as np

# Set seed to ensure reproducibility
set_seed()

# suppress=True: print with decimal notation, not scientific
np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True)


class TestSolutionRerfinement(unittest.TestCase):
    @classmethod
    def setUpClass(clc):
        clc.panda_arm = PandaArm()

    def test_inverse_kinematics_single_step_batch_np(self):
        """Test that ik steps made with inverse_kinematics_single_step_batch_np() are making progress"""
        robot = self.panda_arm
        alpha = 0.1

        # Get the current poses (these will be the seeds)
        x_current = 0.0 * np.ones((4, 7))
        x_current[0, 0] = 0.0
        x_current[1, 0] = 0.1
        x_current[2, 0] = 0.2
        x_current[3, 0] = 0.3
        current_poses = robot.forward_kinematics(x_current)

        # Get the target poses
        _target_pose_xs = np.zeros((4, 7))
        _target_pose_xs[:, 0] = 0.5
        target_poses = robot.forward_kinematics(_target_pose_xs)
        l2_errs_original = np.linalg.norm(target_poses[:, 0:3] - current_poses[:, 0:3], axis=1)

        x_updated, _ = robot.inverse_kinematics_single_step_batch_np(target_poses, x_current, alpha)
        updated_poses = robot.forward_kinematics(x_updated)
        l2_errs_final = np.linalg.norm(target_poses[:, 0:3] - updated_poses[:, 0:3], axis=1)

        print("x_current:\n", x_current)
        print("x_updated:\n", x_updated)

        print("\n-----")
        print("target poses: \n", target_poses)
        print("current poses:\n", current_poses)
        print("updated_poses:\n", updated_poses)
        print("\n-----")
        print("l2 errors initial:", l2_errs_original)
        print("l2 errors final:  ", l2_errs_final)


if __name__ == "__main__":
    unittest.main()


"""
xs_current, _ = self.forward_kinematics_batch(xs_current, device=config.device)
        xs_current_np = xs_current.detach().cpu().numpy()
        xs_current_np_R = xs_current_np[:, 0:3, 0:3]
        current_pose_quat = matrix_to_quaternion(xs_current_np_R)

"""