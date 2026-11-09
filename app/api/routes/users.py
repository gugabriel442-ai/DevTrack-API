
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import gerar_hash

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    dados: UserCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(User).filter(
        User.email == dados.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado."
        )

    novo_usuario = User(
        name=dados.name,
        email=dados.email,
        password_hash=gerar_hash(dados.password)
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível cadastrar este e-mail."
        )

    return novo_usuario
