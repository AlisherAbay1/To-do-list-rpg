from todo_rpg.application.dto.common.items import ItemCreateDTO
from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
    SessionRepositoryProtocol,
    UoWProtocol,
)
from todo_rpg.domain import Item
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.mappers.common import ItemMapper
from todo_rpg.application.dto import ItemDTO


class CreateCurrentUserItemInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, session_token: str, dto: ItemCreateDTO) -> ItemDTO:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = Item(user_id=user_id, title=dto.title, description=dto.description)
        output_dto = ItemMapper.to_dto(item)
        self.uow.add(item)
        await self.uow.commit()
        return output_dto
