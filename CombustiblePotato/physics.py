from typing import TYPE_CHECKING

from pyfrc.physics.core import PhysicsInterface
from rev import SparkMaxSim
from wpimath.system.plant import DCMotor
from wpilib.simulation import DifferentialDrivetrainSim

from constants.hardware import GEAR_RATIO, MOMENT_OF_INTERTIA, ROBOT_MASS, WHEEL_RADIUS, TRACK_WIDTH

if TYPE_CHECKING:
    from robot import PotatoBot

class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface, robot: "PotatoBot"):
        self.physics_controller = physics_controller
        self.drivetrain = robot.drivetrain

        self.right_gearbox_sim = SparkMaxSim(self.drivetrain.front_right_motor, DCMotor.NEO(2))
        self.left_gearbox_sim = SparkMaxSim(self.drivetrain.front_left_motor, DCMotor.NEO(2))

        self.right_gearbox_encoder_sim = self.right_gearbox_sim.getRelativeEncoderSim()
        self.left_gearbox_encoder_sim = self.left_gearbox_sim.getRelativeEncoderSim()

        self.diff_drive_sim = DifferentialDrivetrainSim(
            driveMotor=DCMotor.NEO(2),
            gearing=GEAR_RATIO,
            J=MOMENT_OF_INTERTIA,
            mass=ROBOT_MASS,
            wheelRadius=WHEEL_RADIUS,
            trackWidth=TRACK_WIDTH
        )

    def update_sim(self, now: float, tm_diff: float) -> None:
        self.diff_drive_sim.setInputs(
            self.left_gearbox_sim.getSetpoint() * 12.0,
            self.right_gearbox_sim.getSetpoint() * 12.0,
        )

        self.right_gearbox_encoder_sim.setPosition(self.diff_drive_sim.getRightPosition())
        self.right_gearbox_encoder_sim.setVelocity(self.diff_drive_sim.getRightVelocity())

        self.left_gearbox_encoder_sim.setPosition(self.diff_drive_sim.getLeftPosition())
        self.left_gearbox_encoder_sim.setVelocity(self.diff_drive_sim.getLeftVelocity())

        if self.physics_controller.field is not None:
            self.physics_controller.field.setRobotPose(self.diff_drive_sim.getPose())

        self.diff_drive_sim.update(tm_diff)