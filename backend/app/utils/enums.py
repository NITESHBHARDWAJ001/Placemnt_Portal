import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    COMPANY = "COMPANY"
    STUDENT = "STUDENT"


class CompanyApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class DriveStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"


class JobType(str, enum.Enum):
    FULL_TIME = "FULL_TIME"
    INTERNSHIP = "INTERNSHIP"
    PPO = "PPO"


class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class InterviewMode(str, enum.Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class InterviewStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class InterviewResult(str, enum.Enum):
    PENDING = "PENDING"
    PASS_ = "PASS"
    FAIL = "FAIL"


class NotificationType(str, enum.Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class PlacementStatus(str, enum.Enum):
    NOT_PLACED = "NOT_PLACED"
    PLACED = "PLACED"
