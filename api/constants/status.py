from enum import Enum
from enum import IntEnum

class TaskStatus(Enum):
    NOT_STARTED = 1 #未着手
    IN_PROGRESS = 2 #作業中
    DONE = 3 #完了


class SalesStatus(Enum):
    ORDER_CONFIRMED = 1   # 受注済み
    NOT_SOLD = 2          # 未売上
    SOLD = 3              # 売上済み
    
    
class UserRole(Enum):
    ADMIN = 1 #管理者
    USER = 2 #ユーザー