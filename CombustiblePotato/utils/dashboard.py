from typing import TYPE_CHECKING

from wpilib import SmartDashboard, RobotController

from components.drivetrain import DriveTrain
from components.arm import Arm
from constants.hardware import MIN_ANGLE

if TYPE_CHECKING:
    from robot import PotatoBot

class Dashboard:
    def __init__(self, drivetrain: DriveTrain, arm: Arm, robot: "PotatoBot") -> None:
        self.drivetrain = drivetrain
        self.arm = arm
        self.robot = robot

    def _get_pose_as_string(self) -> str:
        pose = self.drivetrain.get_pose()
        x = pose.X()
        y = pose.Y()
        rotation_deg = pose.rotation().degrees()
        return f"x: {x:.2f} m, y: {y:.2f} m, heading: {rotation_deg:.1f}"
    
    def execute(self) -> None:
        SmartDashboard.putNumber("General/Battery Voltage", RobotController.getBatteryVoltage())
        SmartDashboard.putNumber("Arm/Angle", self.arm.get_angle())
        SmartDashboard.putBoolean("Arm/MinLimit", self.arm.get_angle() <= MIN_ANGLE)
        SmartDashboard.putNumber("Drive/VerticalSpeed", self.robot.vertical_speed_pct)
        SmartDashboard.putNumber("Drive/RotationSpeed", self.robot.rotation_speed_pct)
        SmartDashboard.putString("Drive/Pose", self._get_pose_as_string())