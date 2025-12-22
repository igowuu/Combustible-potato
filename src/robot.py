import logging

import wpilib
import wpimath

from components.drivetrain import DriveTrain
from components.arm import Arm
from components.intake import Intake
from controls.arm_control import ArmControl
from controls.intake_control import IntakeControl
from utils.dashboard import Dashboard
from constants.hardware import DEADBAND

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PotatoBot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = DriveTrain()

        self.arm = Arm(self.drivetrain)
        self.arm_control = ArmControl(self.arm)

        self.intake = Intake()
        self.intake_control = IntakeControl(self.intake)

        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        self.vertical_volts = 0.0
        self.rotation_volts = 0.0

        self.dashboard = Dashboard(self.drivetrain, self.arm, self)

    def robotPeriodic(self) -> None:
        self.dashboard.execute()
        
    def teleopPeriodic(self) -> None:
        if self.lstick.getRawButton(1):
            self.arm_control.set_arm_up()
        elif self.lstick.getRawButton(2):
            self.arm_control.set_arm_down()
        else:
            self.arm_control.set_arm_idle()
        
        if self.lstick.getRawButton(3):
            self.intake_control.set_intake_grab()
        elif self.lstick.getRawButton(4):
            self.intake_control.set_intake_release()
        else:
            self.intake_control.set_intake_idle()

        self.vertical_volts = -wpimath.applyDeadband(self.lstick.getY(), DEADBAND)
        self.rotation_volts = wpimath.applyDeadband(self.rstick.getX(), DEADBAND)
        
        self.arm_control.update()
        self.intake_control.update()
        self.drivetrain.drive(self.vertical_volts, self.rotation_volts)