from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Game, User
from app.schemas import GameRequest, GameResponse
from app.security import get_current_user

# Every route requires a token and only touches the games of that user
router = APIRouter(prefix="/games", tags=["games"])


def find_owned_game(game_id: int, user: User, session: Session) -> Game:
    game = session.get(Game, game_id)
    # Games of other users are reported as not found
    if game is None or game.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Game not found")
    return game


@router.get("", response_model=list[GameResponse])
def list_games(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[Game]:
    query = select(Game).where(Game.user_id == user.id).order_by(Game.id)
    return list(session.exec(query).all())


@router.get("/{game_id}", response_model=GameResponse)
def get_game(
    game_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Game:
    return find_owned_game(game_id, user, session)


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(
    body: GameRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Game:
    game = Game(**body.model_dump(), user_id=user.id)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@router.put("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: int,
    body: GameRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Game:
    game = find_owned_game(game_id, user, session)
    for field, value in body.model_dump().items():
        setattr(game, field, value)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(
    game_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    game = find_owned_game(game_id, user, session)
    session.delete(game)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
