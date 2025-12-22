from phoenix5 import TalonSRX, ControlMode

from constants.hardware import MAX_VOLTAGE, MAX_ANGLE, MIN_ANGLE
from components.drivetrain import DriveTrain
from utils.conversions import rotations_to_degrees

class Arm:
    def __init__(self, drivetrain: DriveTrain) -> None:
        self.drivetrain = drivetrain

        self.left_arm_motor = TalonSRX(21)
        self.right_arm_motor = TalonSRX(22)

        self.right_arm_motor.setInverted(True)

        self.right_arm_motor.follow(self.left_arm_motor)

        self.left_arm_motor.enableVoltageCompensation(True)
        self.left_arm_motor.configVoltageCompSaturation(MAX_VOLTAGE)

        self.right_arm_motor.enableVoltageCompensation(True)
        self.right_arm_motor.configVoltageCompSaturation(MAX_VOLTAGE)

        # Getting absolute encoder output from drivetrain motors is intentional here and is a
        # major design flaw of our bot. Please do NOT replicate this and change it for all use.
        self.arm_left_encoder = self.drivetrain.back_right_motor.getAbsoluteEncoder()
        self.arm_right_encoder = self.drivetrain.back_left_motor.getAbsoluteEncoder()

    def _clamp_voltage(self, voltage: float) -> float:
        return max(-MAX_VOLTAGE, min(voltage, MAX_VOLTAGE))
    
    def stop(self) -> None:
        self.left_arm_motor.set(ControlMode.PercentOutput, 0.0)

    def get_angle(self) -> float:
        left_pos = self.arm_left_encoder.getPosition()
        right_pos = self.arm_right_encoder.getPosition()
        avg_rotations = (left_pos + right_pos) / 2
        return rotations_to_degrees(avg_rotations)
    
    def conduct_arm_movement(self, desired_voltage: float) -> None:
        desired_voltage = self._clamp_voltage(desired_voltage)

        angle = self.get_angle()

        if angle <= MIN_ANGLE and desired_voltage < 0:
            self.stop()
            return
        if angle >= MAX_ANGLE and desired_voltage > 0:
            self.stop()
            return
        
        self.left_arm_motor.set(ControlMode.PercentOutput, desired_voltage)