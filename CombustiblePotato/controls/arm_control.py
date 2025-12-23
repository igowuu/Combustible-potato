import logging
from enum import Enum, auto

from components.arm import Arm
from utils.fsm import FiniteStateMachine
from constants.hardware import ARM_VOLTAGE

logger = logging.getLogger(__name__)

class ArmCommand(Enum):
    IDLE = auto()
    UP = auto()
    DOWN = auto()

class ArmControl:
    def __init__(self, arm: Arm) -> None:
        self.arm = arm
        self.fsm = FiniteStateMachine()

        self.command = ArmCommand.IDLE

        self._setup_states()

    def _setup_states(self) -> None:
        self.fsm.set_default_state(
            name="idle",
            on_update=self._on_idle_update,
            on_enable=self._on_idle_enable,
            on_disable=self._on_idle_disable,
        )

        self.fsm.add_state(
            name="move_up",
            conditional=self._should_move_up,
            on_update=self._on_up_update,
            on_enable=self._on_up_enable,
            on_disable=self._on_up_disable
        )

        self.fsm.add_state(
            name="move_down",
            conditional=self._should_move_down,
            on_update=self._on_down_update,
            on_enable=self._on_down_enable,
            on_disable=self._on_down_disable
        )
    
    # General helpers
    def _apply_voltage(self, voltage: float) -> None:
        self.arm.conduct_arm_movement(voltage)

    # Conditions
    def _should_move_up(self) -> bool:
        return self.command == ArmCommand.UP

    def _should_move_down(self) -> bool:
        return self.command == ArmCommand.DOWN

    # On_update methods
    def _on_idle_update(self) -> None:
        self.arm.stop()
        
    def _on_up_update(self) -> None:
        self._apply_voltage(ARM_VOLTAGE)

    def _on_down_update(self) -> None:
        self._apply_voltage(-ARM_VOLTAGE)

    # On_enable methods
    def _on_idle_enable(self) -> None:
        logger.info("[ARM] Idle")
        self.arm.stop()
    
    def _on_up_enable(self) -> None:
        logger.info("[ARM] Moving up")

    def _on_down_enable(self) -> None:
        logger.info("[ARM] Moving down")

    # On_disable methods
    def _on_idle_disable(self) -> None:
        logger.debug("[ARM] Leaving idle")

    def _on_up_disable(self) -> None:
        logger.debug("[ARM] Stopped moving up")

    def _on_down_disable(self) -> None:
        logger.debug("[ARM] Stopped moving down")

    # Setters
    def set_arm_up(self) -> None:
        self.command = ArmCommand.UP

    def set_arm_down(self) -> None:
        self.command = ArmCommand.DOWN

    def set_arm_idle(self) -> None:
        self.command = ArmCommand.IDLE

    # Main executable
    def update(self) -> None:
        self.fsm.execute()