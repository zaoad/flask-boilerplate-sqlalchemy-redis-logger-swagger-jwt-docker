import enum


class StatusType(enum.Enum):
    ACTIVE = 1
    DELETED = 2
    BLOCKED = 3


class RoleType(enum.Enum):
    SUPER_ADMIN = 1
    ADMIN = 2
    MANAGER = 3
    AGENT = 4
