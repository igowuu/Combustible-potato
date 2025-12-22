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

        self.command: ArmCommand = ArmCommand.IDLE

        self._setup_states()

    def _setup_states(self) -> None:
        self.fsm.set_default_state(
            name="idle",
            on_update=self._idle_update,
            on_enable=self._on_idle_enable,
            on_disable=self._on_idle_disable,
        )

        self.fsm.add_state(
            name="move_up",
            conditional=self._should_move_up,
            on_update=self._move_up_update,
            on_enable=lambda: logger.info("[ARM] Moving up"),
            on_disable=lambda: logger.debug("[ARM] Stopped moving up")
        )

        self.fsm.add_state(
            name="move_down",
            conditional=self._should_move_down,
            on_update=self._move_down_update,
            on_enable=lambda: logger.info("[ARM] Moving down"),
            on_disable=lambda: logger.debug("[ARM] Stopped moving down")
        )

    def _apply_voltage(self, voltage: float) -> None:
        self.arm.conduct_arm_movement(voltage)
        
    def set_arm_up(self) -> None:
        self.command = ArmCommand.UP

    def set_arm_down(self) -> None:
        self.command = ArmCommand.DOWN

    def set_arm_idle(self) -> None:
        self.command = ArmCommand.IDLE

    def _should_move_up(self) -> bool:
        return self.command == ArmCommand.UP

    def _should_move_down(self) -> bool:
        return self.command == ArmCommand.DOWN

    def _idle_update(self) -> None:
        pass
        
    def _move_up_update(self) -> None:
        self._apply_voltage(ARM_VOLTAGE)

    def _move_down_update(self) -> None:
        self._apply_voltage(-ARM_VOLTAGE)

    def _on_idle_enable(self) -> None:
        logger.info("[ARM] Idle")
        self.arm.stop()

    def _on_idle_disable(self) -> None:
        logger.debug("[ARM] Leaving idle")

    def update(self) -> None:
        self.fsm.execute()