from fastapi import APIRouter, status, HTTPException, Query, Depends
from typing import List, Literal
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.core.exceptions import TaskNotFoundError
from app.models.task import Task, TaskCreate, UpdateTaskStatus
from app.services.task_services import TaskService

router = APIRouter()

@router.post(
    "/tasks/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу"
)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    try:
        return TaskService.create(db, task_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/tasks/",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
    summary="Получить все задачи"
)
def list_tasks(
    completed: bool | None = Query(None),
    db: Session = Depends(get_db)
):
    try:
        if completed == None:
            return TaskService.get_all(db)
        elif completed:
            return TaskService.get_completed_tasks(db)
        else:
            return TaskService.get_active_tasks(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Получить задачу по ID"
)
def get_task(task_id: str, db: Session = Depends(get_db)):
    try:
        return TaskService.get_task(db, task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Изменить статус задачи"
)
def update_task_status(task_id: str, update_data: UpdateTaskStatus, db: Session = Depends(get_db)):
    try:
        if update_data.completed:
            return TaskService.complete_task(db, task_id)
        else:
            return TaskService.uncomplete_task(db, task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу"
)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    try:
        TaskService.delete_task(db, task_id)
        return None
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )