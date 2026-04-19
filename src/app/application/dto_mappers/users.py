from src.app.domain import UserDomain 
from src.app.application.dto.users import UserDTO

class UserMapper:
    @staticmethod
    def to_dto(domain: UserDomain):
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
            profile_picture=domain.profile_picture
        )
        return dto