from src.app.domain import User
from src.app.application.dto.common.users import UserDTO, UserAuthDTO
from typing import Sequence


class UserMapper:
    @staticmethod
    def to_dto(domain: User) -> UserDTO:
        dto = UserDTO(
            id=domain.id,
            username=domain.username,
            email=domain.email,
            password=domain.password,
            lvl=domain.lvl,
            xp=domain.xp,
            gold=domain.gold,
            language=domain.language,
            timezone=domain.timezone,
            is_admin=domain.is_admin,
            current_rank_id=domain.current_rank_id,
            profile_picture=domain.profile_picture,
        )
        return dto

    @staticmethod
    def to_list_dto(domains: Sequence[User]) -> list[UserDTO]:
        return [UserMapper.to_dto(domain) for domain in domains]

    @staticmethod
    def to_auth_dto(domain: User, session_token: str) -> UserAuthDTO:
        dto = UserAuthDTO(
            username=domain.username, email=domain.email, session_token=session_token
        )
        return dto
