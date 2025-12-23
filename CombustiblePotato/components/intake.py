from phoenix6.hardware import TalonFX

from utils.conversions import clamp_voltage

class Intake:
    def __init__(self) -> None:
        self.intake_motor = TalonFX(23)
    
    def stop(self) -> None:
        self.intake_motor.setVoltage(0)
    
    def conduct_intake_movement(self, desired_voltage: float) -> None:
        desired_voltage = clamp_voltage(desired_voltage)

        self.intake_motor.setVoltage(desired_voltage)