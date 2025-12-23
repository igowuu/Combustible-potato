import math

from constants.hardware import MAX_VOLTAGE, GEAR_RATIO, WHEEL_DIAMETER

def clamp_voltage(voltage: float) -> float:
    return max(-MAX_VOLTAGE, min(voltage, MAX_VOLTAGE))

def rotations_to_degrees(rotations: float) -> float:
    """Convert rotations (full turns) to degrees."""
    return rotations * 360.0

def encoder_rotations_to_meters(
    encoder_rotations: float
) -> float:
    """Convert motor encoder rotations to linear distance in meters."""
    wheel_rotations = encoder_rotations / GEAR_RATIO
    distance = wheel_rotations * math.pi * WHEEL_DIAMETER
    return distance