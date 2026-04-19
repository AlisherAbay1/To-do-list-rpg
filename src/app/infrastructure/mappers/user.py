from src.app.infrastructure.database.models import User
from src.app.domain import UserDomain

class UserMapper:
    @staticmethod
    def to_domain(orm: User) -> UserDomain:
        user = UserDomain(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            password=orm.password,
            lvl=orm.lvl,
            xp=orm.xp,
            is_admin=orm.is_admin,
            current_rank_id=orm.current_rank_id,
            profile_picture=orm.profile_picture,
            gold=orm.gold
        )
        return user
    
    @staticmethod
    def update_orm(domain: UserDomain, orm: User) -> None:
        orm.id = domain.id
        orm.username = domain.username
        orm.email = domain.email
        orm.password = domain.password
        orm.lvl = domain.lvl
        orm.xp = domain.xp
        orm.is_admin = domain.is_admin
        orm.current_rank_id = domain.current_rank_id
        orm.profile_picture = domain.profile_picture
        orm.gold = domain.gold