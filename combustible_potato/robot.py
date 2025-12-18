import wpilib
from phoenix6.hardware import TalonFX, CANcoder, Pigeon2
from components.drivetrain import DriveTrain
from controls.teleop_drive import TeleopDrive

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drivetrain = DriveTrain()

    def teleopInit(self) -> None:
        self.teleop_drive = TeleopDrive(self.drivetrain)

    def teleopPeriodic(self) -> None:
        self.teleop_drive.execute()
        self.drivetrain.update_odometry()
