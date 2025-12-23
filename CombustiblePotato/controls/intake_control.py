from enum import Enum, auto
import logging

from components.intake import Intake
from utils.fsm import FiniteStateMachine
from constants.hardware import INTAKE_VOLTAGE

logger = logging.getLogger(__name__)

class IntakeCommand(Enum):
    IDLE = auto()
    GRAB = auto()
    RELEASE = auto()

class IntakeControl:
    def __init__(self, intake: Intake) -> None:
        self.intake = intake
        self.fsm = FiniteStateMachine()

        self.command = IntakeCommand.IDLE
        
        self._setup_states()

    def _setup_states(self) -> None:
        self.fsm.set_default_state(
            name="idle",
            on_update=self._on_idle_update,
            on_enable=self._on_idle_enable,
            on_disable=self._on_idle_disable,
        )

        self.fsm.add_state(
            name="grab",
            conditional=self._should_grab,
            on_update=self._on_grab_update,
            on_enable=self._on_grab_enable,
            on_disable=self._on_grab_disable
        )

        self.fsm.add_state(
            name="release",
            conditional=self._should_release,
            on_update=self._on_release_update,
            on_enable=self._on_release_enable,
            on_disable=self._on_release_disable
        )
    
    # General helpers
    def _apply_voltage(self, voltage: float) -> None:
        self.intake.conduct_intake_movement(voltage)

    # Conditions
    def _should_grab(self) -> bool:
        return self.command == IntakeCommand.GRAB

    def _should_release(self) -> bool:
        return self.command == IntakeCommand.RELEASE

    # On_update methods
    def _on_idle_update(self) -> None:
        self.intake.stop()
        
    def _on_grab_update(self) -> None:
        self._apply_voltage(INTAKE_VOLTAGE)

    def _on_release_update(self) -> None:
        self._apply_voltage(-INTAKE_VOLTAGE)

    # On_enable methods
    def _on_idle_enable(self) -> None:
        logger.info("[INTAKE] Idle")
        self.intake.stop()

    def _on_grab_enable(self) -> None:
        logger.info("[INTAKE] Grabbing")

    def _on_release_enable(self) -> None:
        logger.info("[INTAKE] Releasing")

    # On_disable methods
    def _on_idle_disable(self) -> None:
        logger.debug("[INTAKE] Leaving idle")

    def _on_grab_disable(self) -> None:
        logger.debug("[INTAKE] Stopped grabbing")

    def _on_release_disable(self) -> None:
        logger.debug("[INTAKE] Stopped releasing")

    # Setters
    def set_intake_grab(self) -> None:
        self.command = IntakeCommand.GRAB

    def set_intake_release(self) -> None:
        self.command = IntakeCommand.RELEASE

    def set_intake_idle(self) -> None:
        self.command = IntakeCommand.IDLE

    # Main executable
    def update(self) -> None:
        self.fsm.execute()