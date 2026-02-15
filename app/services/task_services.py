from datetime import datetime
from typing import List
from app.core.exceptions import TaskNotFoundError
from app.models.task import Task, TaskCreate, TaskDB
from sqlalchemy.orm import Session
from sqlalchemy import update

class TaskService:
    @staticmethod
    def create(db: Session, task_data: TaskCreate) -> Task:
        new_task = TaskDB(title=task_data.title, description=task_data.description)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return Task.from_orm(new_task)

    @staticmethod
    def get_all(db: Session) -> List[Task]:
        return [Task.from_orm(t) for t in db.query(TaskDB).all()]

    @staticmethod
    def get_active_tasks(db: Session) -> List[Task]:
        return [Task.from_orm(t) for t in db.query(TaskDB).filter(TaskDB.completed == False).all()]

    @staticmethod
    def get_completed_tasks(db: Session) -> List[Task]:
        return [Task.from_orm(t) for t in db.query(TaskDB).filter(TaskDB.completed).all()]

    @staticmethod
    def get_task(db: Session, task_id: str) -> Task:
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if task is None:
            raise TaskNotFoundError()
        return Task.from_orm(task)

    @staticmethod
    def complete_task(db: Session, task_id: str) -> Task:
        task = TaskService.get_task(db, task_id)
        db.execute(update(TaskDB).where(TaskDB.id == task_id).values(completed=True, completed_at=datetime.now()))
        db.commit()
        return TaskService.get_task(db, task_id)

    @staticmethod
    def uncomplete_task(db: Session, task_id: str) -> Task:
        task = TaskService.get_task(db, task_id)
        db.execute(update(TaskDB).where(TaskDB.id == task_id).values(completed=False, completed_at=None))
        db.commit()
        return TaskService.get_task(db, task_id)

    @staticmethod
    def delete_task(db: Session, task_id: str) -> None:
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if task is None:
            raise TaskNotFoundError()
        db.delete(task)
        db.commit()