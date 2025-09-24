import enum

class TaskStatus(enum.Enum):
    TODO = "To do"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"