from typing import List
from threading import Lock
from app.core.exceptions import TaskNotFoundError
from app.models.task import Task, TaskCreate

_tasks: dict[str, Task] = {}
_lock = Lock()


class TaskService:
    @staticmethod
    def create(task_data: TaskCreate) -> Task:
        new_task = Task.create(
            title=task_data.title,
            description=task_data.description
        )

        with _lock:
            _tasks[new_task.id] = new_task

        return new_task

    @staticmethod
    def get_all() -> List[Task]:
        with _lock:
            return list(_tasks.values())

    @staticmethod
    def get_active_tasks() -> List[Task]:
        with _lock:
            active = [task for task in _tasks.values() if task.status == "active"]
            return [task.model_copy(deep=True) for task in active]

    @staticmethod
    def get_completed_tasks() -> List[Task]:
        with _lock:
            active = [task for task in _tasks.values() if task.status == "completed"]
            return [task.model_copy(deep=True) for task in active]

    @staticmethod
    def get_task(task_id: str) -> Task:
        with _lock:
            task = _tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError()
        return task

    @staticmethod
    def complete_task(task_id: str) -> Task:
        task = TaskService.get_task(task_id)
        with _lock:
            task.complete()

        return task

    @staticmethod
    def uncomplete_task(task_id: str) -> Task:
        task = TaskService.get_task(task_id)
        with _lock:
            task.uncomplete()

        return task

    @staticmethod
    def delete_task(task_id: str) -> None:
        with _lock:
            if task_id not in _tasks:
                raise TaskNotFoundError()
            del _tasks[task_id]