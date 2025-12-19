# This probably doesn't work - created entirely without pylance or python installed (complete API guessing) D:
from phoenix5 import TalonSRX

class Arm:
    def __init__(self):
        self.left_arm_motor = TalonSRX(21)
        self.right_arm_motor = TalonSRX(22)

        self.right_arm_motor.follow(self.left_arm_motor)

        self.arm_left_encoder = self.left_arm_motor.getAbsoluteEncoder()
        self.arm_right_encoder = self.right_arm_motor.getAbsoluteEncoder()

    def request_arm_movement(self, desired_voltage: float) -> None:
        if abs(desired_voltage) > MAX_VOLTAGE:
            print("ERROR: Tried to set voltage above MAX_VOLTAGE!")
            self.stop()
            return

        if self.get_angle() <= MIN_ANGLE:
            self.stop()
            return

        self.left_arm_motor.setVoltage(desired_voltage)

    def stop(self) -> None:
        self.left_arm_motor.setVoltage(0)

    def get_angle(self) -> float:
        return self.arm_left_encoder.get_angle()
