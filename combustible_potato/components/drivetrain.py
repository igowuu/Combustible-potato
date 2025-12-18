from phoenix6.hardware import Pigeon2, TalonFX
from wpimath.kinematics import DifferentialDriveOdometry
from wpimath.geometry import Pose2d, Rotation2d
from wpilib.drive import DifferentialDrive

from constants.hardware import GEAR_RATIO, WHEEL_CIRCUMFERENCE, MAX_VOLTAGE

class DriveTrain:
    def __init__(self) -> None:
        self.left_motor = TalonFX(0, canbus="can0")
        self.right_motor = TalonFX(1, canbus="can0")

        self.gyro = Pigeon2(2, canbus="can0")
        self.gyro.reset()

        self.odometry = DifferentialDriveOdometry(
            self.gyro.getRotation2d(),
            self.getLeftDistanceMeters(),
            self.getRightDistanceMeters(),
            Pose2d()
        )

    def getLeftDistanceMeters(self):
        rotations = self.left_motor.get_position().value
        return (rotations / GEAR_RATIO) * WHEEL_CIRCUMFERENCE

    def getRightDistanceMeters(self):
        rotations = self.right_motor.get_position().value
        return (rotations / GEAR_RATIO) * WHEEL_CIRCUMFERENCE

    def update_odometry(self):
        self.odometry.update(
            self.gyro.getRotation2d(),
            self.getLeftDistanceMeters(),
            self.getRightDistanceMeters()
        )

    def reset_odometry(self):
        self.odometry.resetPose(Pose2d(0, 0, 0))

    def drive(self, ySpeed: float, omega: float) -> None:
        left = ySpeed + omega
        right = ySpeed - omega

        self.left_motor.setVoltage(left * MAX_VOLTAGE)
        self.right_motor.setVoltage(right * MAX_VOLTAGE)
