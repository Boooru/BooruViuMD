import enum

from kivy import Logger


class FlowModuleState(enum.Enum):
    UNAVAILABLE = -1,
    AVAILABLE = 0,
    PROCESSING = 1
    IN_USE = 2


class FlowPhase(enum.Enum):
    PREPROCESSING = 0
    SORTING = 1
    MARKING = 2
    DECENSORING = 3


class FlowModule:
    def __init__(self, name="Generic Flow Module", setup=None, activation_condition=None):
        self.name = name # Name for the module
        self.state: FlowModuleState = FlowModuleState.UNAVAILABLE  # The state the module is in
        self.phase: FlowPhase = None  # The phase for execution of the flow
        self.prerequisites: list[str] = []
        self.space_requirements: int = 0  # Pre-computed space requirements for the module, in MB
        self.__setup = setup

    def is_activated(self):
        print("Running default is_active()!")
        return False

    def interface(self, **kwargs):
        pass

    # Perform all tasks necessary to set the module up and get it ready for use
    def attempt_to_activate(self) -> bool:
        Logger.info("Attempting to activate " + self.name + "...")
        if not self.is_activated():  # if the activation condition is not met
            print("Running setup!")
            self.__setup()
            Logger.info("Successfully activated " + self.name + "!")
            return True
        else:
            Logger.warn(self.name + " is already active!")
            return True
