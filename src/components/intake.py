from phoenix6.hardware import TalonFX

from constants.hardware import MAX_VOLTAGE

class Intake:
    def __init__(self) -> None:
        self.intake_motor = TalonFX(23)

    def _clamp_voltage(self, voltage: float) -> float:
        return max(-MAX_VOLTAGE, min(voltage, MAX_VOLTAGE))
    
    def stop(self) -> None:
        self.intake_motor.setVoltage(0)
    
    def conduct_intake_movement(self, desired_voltage: float) -> None:
        desired_voltage = self._clamp_voltage(desired_voltage)

        self.intake_motor.setVoltage(desired_voltage)