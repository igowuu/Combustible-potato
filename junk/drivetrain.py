from phoenix6.hardware import Pigeon2, TalonFX
from wpimath.kinematics import DifferentialDriveOdometry
from wpimath.geometry import Pose2d, Rotation2d
from wpilib.drive import DifferentialDrive

from constants.hardware import GEAR_RATIO, WHEEL_CIRCUMFERENCE, MAX_VOLTAGE

class DriveTrain:
    def __init__(self) -> None:
        BRUSHLESS = SparkMax.MotorType.kBrushless

        self.front_left_motor = SparkMax(11, BRUSHLESS)
        self.front_right_motor = SparkMax(12, BRUSHLESS)
        self.back_left_motor = SparkMax(13, BRUSHLESS)
        self.back_right_motor = SparkMax(14, BRUSHLESS)

        self.shooter_front_left_motor = TalonSRX(31)
        self.shooter_front_right_motor = TalonSRX(32)
        self.shooter_back_left_motor = TalonSRX(33)
        self.shooter_back_right_motor = TalonSRX(34)

        self.indexer_motor = TalonSRX(41)

        # FRONT LEFT
        fl_cfg = SparkMaxConfig()
        fl_cfg.setIdleMode(SparkMaxConfig.IdleMode.kCoast)
        self.front_left_motor.configure(fl_cfg)

        # BACK LEFT
        bl_cfg = SparkMaxConfig()
        bl_cfg.follow(self.front_left_motor.getDeviceId(), True)
        bl_cfg.setIdleMode(SparkMaxConfig.IdleMode.kCoast)
        self.back_left_motor.configure(bl_cfg)

        # FRONT RIGHT
        fr_cfg = SparkMaxConfig()
        fr_cfg.setIdleMode(SparkMaxConfig.IdleMode.kCoast)
        fr_cfg.inverted(True)
        self.front_right_motor.configure(fr_cfg)

        # BACK RIGHT
        br_cfg = SparkMaxConfig()
        br_cfg.follow(self.front_right_motor.getDeviceId(), True)
        br_cfg.setIdleMode(SparkMaxConfig.IdleMode.kCoast)
        br_cfg.inverted(True)
        self.back_right_motor.configure(br_cfg)

    def drive(self, ySpeed: float, omega: float) -> None:
        left = ySpeed + omega
        right = ySpeed - omega

        self.front_left_motor.setVoltage(left * MAX_VOLTAGE)
        self.front_right_motor.setVoltage(right * MAX_VOLTAGE)
