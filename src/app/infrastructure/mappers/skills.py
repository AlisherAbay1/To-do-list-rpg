from src.app.infrastructure.database.models import Skill
from src.app.domain import SkillDomain
from typing import Sequence

class SkillMapper:
    @staticmethod
    def to_domain(orm: Skill) -> SkillDomain:
        skill = SkillDomain(
            id=orm.id,
            user_id=orm.user_id,
            title=orm.title,
            description=orm.description,
            ico=orm.ico,
            lvl=orm.lvl,
            xp=orm.xp,
            deleted=orm.deleted,
            deleted_at=orm.deleted_at
        )
        return skill
    
    @staticmethod
    def to_domain_list(orms: Sequence[Skill]) -> list[SkillDomain]:
        return [SkillMapper.to_domain(orm) for orm in orms]
    
    @staticmethod
    def update_orm(domain: SkillDomain, orm: Skill) -> None:
        orm.id = domain.id
        orm.user_id = domain.user_id
        orm.title = domain.title
        orm.description = domain.description
        orm.ico = domain.ico
        orm.lvl = domain.lvl
        orm.xp = domain.xp
        orm.deleted = domain.deleted
        orm.deleted_at = domain.deleted_at