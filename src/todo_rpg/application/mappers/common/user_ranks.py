from todo_rpg.domain import UserRank
from todo_rpg.application.dto import UserRankReadDTO
from typing import Sequence


class UserRankMapper:
    @staticmethod
    def to_dto(domain: UserRank) -> UserRankReadDTO:
        dto = UserRankReadDTO(id=domain.id, user_id=domain.user_id, title=domain.title)
        return dto

    @staticmethod
    def to_list_dto(domains: Sequence[UserRank]) -> list[UserRankReadDTO]:
        return [UserRankMapper.to_dto(domain) for domain in domains]
