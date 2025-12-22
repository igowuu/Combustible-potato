from rev import SparkMax, SparkMaxConfig
from wpilib.drive import DifferentialDrive

from constants.hardware import MAX_VOLTAGE

class DriveTrain:
    def __init__(self) -> None:
        BRUSHLESS = SparkMax.MotorType.kBrushless

        self.front_left_motor = SparkMax(11, BRUSHLESS)
        self.front_right_motor = SparkMax(12, BRUSHLESS)
        self.back_left_motor = SparkMax(13, BRUSHLESS)
        self.back_right_motor = SparkMax(14, BRUSHLESS)

        self.back_right_motor.configure(
            SparkMaxConfig().follow(self.front_right_motor.getDeviceId(), True),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )
        self.back_left_motor.configure(
            SparkMaxConfig().follow(self.front_left_motor.getDeviceId(), True),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )
        self.front_left_motor.configure(
            SparkMaxConfig().setIdleMode(SparkMaxConfig.IdleMode.kCoast).inverted(True),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )
        self.front_right_motor.configure(
            SparkMaxConfig().setIdleMode(SparkMaxConfig.IdleMode.kCoast).inverted(True),
            SparkMax.ResetMode.kResetSafeParameters,
            SparkMax.PersistMode.kPersistParameters,
        )

        self.diff_drive = DifferentialDrive(
            self.front_left_motor,
            self.front_right_motor
        )

    def _clamp_voltage(self, voltage: float) -> float:
        return max(-MAX_VOLTAGE, min(voltage, MAX_VOLTAGE))
    
    def drive(self, vertical_volts: float, rotation_volts: float) -> None:
        self.diff_drive.arcadeDrive(vertical_volts, rotation_volts, squareInputs=True)