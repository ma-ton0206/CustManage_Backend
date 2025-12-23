from datetime import date  # yyyy-mm-dd
from api.schemas.base import AuditTimestamps
from api.constants.status import TaskStatus

from pydantic import BaseModel, Field, ConfigDict

# GET


class GetTaskOut(BaseModel):
    task_id: int = Field(..., description="タスクID")
    content: str = Field(..., description="内容")
    status: TaskStatus = Field(..., description="ステータス")
    due_date: date = Field(..., description="期限")
    is_completed: bool = Field(..., description="完了フラグ")

    model_config = ConfigDict(from_attributes=True)


# POST
class PostTaskIn(BaseModel):
    content: str = Field(..., description="内容")
    due_date: date = Field(..., description="期限")
    status: TaskStatus = Field(TaskStatus.NOT_STARTED, description="初期ステータス")
    is_completed: bool = Field(False, description="完了フラグ")


class PostTaskOut(AuditTimestamps):
    task_id: int = Field(..., description="タスクID")


# PUT
class PutTaskIn(BaseModel):
    is_completed: bool = Field(..., description="完了フラグ")
    content: str = Field(..., description="内容")
    due_date: date = Field(..., description="期限")
    status: TaskStatus = Field(..., description="ステータス")

class PutTaskOut(AuditTimestamps):
    task_id: int = Field(..., description="タスクID")


# DELETE
class DeleteTaskOut(AuditTimestamps):
    task_id: int = Field(..., description="タスクID")
