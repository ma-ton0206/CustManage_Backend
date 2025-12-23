# sessionはSQLを実行したり、データベースとの通信を行うための一時的な接続
from sqlalchemy.orm import Session
from api.models.task import Task as TaskModel
from api.schemas.task import PostTaskIn, PutTaskIn
from fastapi import HTTPException
from sqlalchemy import select
from api.models.users import Users


def create_task(db: Session, task_in: PostTaskIn, current_user: Users):
    # dumpは「型付きのもの」→「辞書」などに変換する動き。
    # 例user = User(name="たろう", age=30) → user.model_dump() → {"name":"たろう", "age":30}
    task = TaskModel(
        user_id=current_user.user_id,
        company_id=current_user.company_id,
        created_by_user_id=current_user.user_id,
        # is_completed=task_in.is_completed,
        **task_in.model_dump(),
    )
    # 作成したtaskインスタンスをセッションに追加（まだDBには反映されていない）
    try:
        db.add(task)
        db.commit()  # セッションをコミットしてDBに永続化
        db.refresh(task)  # コミットによって生成されたIDなどを含め、最新の状態でインスタンスを再取得
        return task  # 作成されたtask（DBに保存済み）を返却
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_tasks(db: Session, current_user: Users):
    print("get_tasks")
    try:
        query = (
            select(TaskModel).
            filter(TaskModel.company_id == current_user.company_id).
            filter(TaskModel.user_id == current_user.user_id)
        )
        result = db.execute(query)
        tasks = result.scalars().all()
        return tasks
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def update_task(db: Session, task_id: int, task_in: PutTaskIn, current_user: Users):
    query = (
        select(TaskModel).
        filter(TaskModel.company_id == current_user.company_id).
        filter(TaskModel.user_id == current_user.user_id).
        filter(TaskModel.task_id == task_id)
    )
    result = db.execute(query)
    task = result.scalar_one_or_none()  # i件だけ or noneを出す。2以上はエラーになる。
    if not task:
        db.rollback()
        raise HTTPException(status_code=404, detail="task not found")
    # db内のtaskを引数のtask_inに更新し、taskをreturnすることでdbの最新情報を取得する。
    task.is_completed = task_in.is_completed
    task.content = task_in.content
    task.due_date = task_in.due_date
    task.status = task_in.status
    try:
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def delete_task(db: Session, task_id: int, current_user: Users):
    query = (
        select(TaskModel).
        filter(TaskModel.company_id == current_user.company_id).
        filter(TaskModel.user_id == current_user.user_id).
        filter(TaskModel.task_id == task_id)
    )
    result = db.execute(query)
    task = result.scalar_one_or_none()
    if not task:
        db.rollback()
        raise HTTPException(status_code=404, detail="task not found")
    try:
        db.delete(task)
        db.commit()
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
