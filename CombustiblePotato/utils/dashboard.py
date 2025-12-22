from wpilib import SmartDashboard, RobotController
from typing import TYPE_CHECKING

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

    def execute(self) -> None:
        SmartDashboard.putNumber("Battery Voltage", RobotController.getBatteryVoltage())
        SmartDashboard.putNumber("Arm/Angle", self.arm.get_angle())
        SmartDashboard.putBoolean("Arm/MinLimit", self.arm.get_angle() <= MIN_ANGLE)
        SmartDashboard.putNumber("Drive/VerticalVoltage", self.robot.vertical_volts)
        SmartDashboard.putNumber("Drive/RotationVoltage", self.robot.rotation_volts)