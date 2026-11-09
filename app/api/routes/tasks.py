
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse
from app.api.dependencies import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"]
)


def get_user_project(project_id: int, db: Session, user_id: int):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.user_id == user_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado."
        )

    return project


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_user_project(project_id, db, current_user.id)

    new_task = Task(
        project_id=project_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task



@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    project_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    status_filter: str | None = Query(
        default=None,
        alias="status",
        pattern="^(pending|in_progress|completed)$"
    ),
    search: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_user_project(project_id, db, current_user.id)

    query = db.query(Task).filter(
        Task.project_id == project_id
    )

    # Filtrar pelo status
    if status_filter:
        query = query.filter(Task.status == status_filter)

    # Pesquisar pelo título
    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    # Aplicar paginação
    tasks = (
        query
        .order_by(Task.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return tasks



@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_user_project(project_id, db, current_user.id)

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_user_project(project_id, db, current_user.id)

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )

    db.delete(task)
    db.commit()

    return None
