from rev import SparkMax, SparkMaxConfig
from wpilib.drive import DifferentialDrive
from wpimath.kinematics import DifferentialDriveOdometry
from wpimath.geometry import Rotation2d, Pose2d
from navx import AHRS

from utils.conversions import encoder_rotations_to_meters

class DriveTrain:
    def __init__(self) -> None:
        BRUSHLESS = SparkMax.MotorType.kBrushless

        self.front_right_motor = SparkMax(12, BRUSHLESS)
        self.front_left_motor = SparkMax(11, BRUSHLESS)
        self.back_left_motor = SparkMax(13, BRUSHLESS)
        self.back_right_motor = SparkMax(14, BRUSHLESS)

        self.front_right_motor.configure(
            SparkMaxConfig().setIdleMode(SparkMaxConfig.IdleMode.kBrake).inverted(True),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )
        self.front_left_motor.configure(
            SparkMaxConfig().setIdleMode(SparkMaxConfig.IdleMode.kBrake),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )
        self.back_left_motor.configure(
            SparkMaxConfig()
                .setIdleMode(SparkMaxConfig.IdleMode.kBrake)
                .follow(self.front_left_motor.getDeviceId(), False),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )
        self.back_right_motor.configure(
            SparkMaxConfig()
                .setIdleMode(SparkMaxConfig.IdleMode.kBrake)
                .follow(self.front_right_motor.getDeviceId(), True),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )

        self.front_right_encoder = self.front_right_motor.getEncoder()
        self.front_left_encoder = self.front_left_motor.getEncoder()

        self.front_right_encoder.setPosition(0)
        self.front_left_encoder.setPosition(0)

        self.diff_drive = DifferentialDrive(
            self.front_left_motor,
            self.front_right_motor
        )

        self.diff_drive.setSafetyEnabled(False)

        self.gyro = AHRS.create_spi()
        self.gyro.reset()

        self.odometry = DifferentialDriveOdometry(
            self.get_heading(),
            self.get_left_distance_m(),
            self.get_right_distance_m()
        )
    
    def get_left_distance_m(self) -> float:
        return encoder_rotations_to_meters(self.front_left_encoder.getPosition())

    def get_right_distance_m(self) -> float:
        return encoder_rotations_to_meters(self.front_right_encoder.getPosition())
    
    def get_heading(self) -> Rotation2d:
        return Rotation2d.fromDegrees(-self.gyro.getAngle())
    
    def get_pose(self) -> Pose2d:
        return self.odometry.getPose()
    
    def reset_odometry(self, pose: Pose2d = Pose2d()) -> None:
        self.odometry.resetPosition(
            self.get_heading(),
            self.get_left_distance_m(),
            self.get_right_distance_m(),
            pose
        )

    def reset_heading(self) -> None:
        self.gyro.reset()

    def reset_sensors_and_pose(self) -> None:
        self.front_left_encoder.setPosition(0)
        self.front_right_encoder.setPosition(0)
        self.reset_heading()
        self.reset_odometry()

    def stop(self) -> None:
        self.diff_drive.stopMotor()

    def drive(self, vertical_speed_pct: float, rotation_speed_pct: float) -> None:
        self.diff_drive.arcadeDrive(vertical_speed_pct, rotation_speed_pct, squareInputs=True)

    def update(self) -> None:
        self.odometry.update(
            self.get_heading(),
            self.get_left_distance_m(),
            self.get_right_distance_m()
        )