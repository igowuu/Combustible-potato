import wpilib
import wpimath.filter

from components.drivetrain import DriveTrain

class TeleopDrive:
    def __init__(self, drivetrain: DriveTrain):
        self.drivetrain = drivetrain
        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        self.xspeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yspeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.omegaLimiter = wpimath.filter.SlewRateLimiter(3)

    def execute(self) -> None:
        if self.lstick.getRawButtonPressed(1):
            self.drivetrain.reset_odometry()

        self.ySpeed = (
            -self.yspeedLimiter.calculate(
                wpimath.applyDeadband(self.lstick.getY(), 0.15)
            )
        )

        self.omega = (
            -self.omegaLimiter.calculate(
                wpimath.applyDeadband(self.rstick.getX(), 0.15)
            )
        )

        self.drivetrain.drive(self.ySpeed, self.omega)
