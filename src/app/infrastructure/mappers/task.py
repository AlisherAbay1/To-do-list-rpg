from src.app.infrastructure.database.repositories.tasks import Task
from src.app.domain import TaskDomain, SkillDomain, UserDomain

class TaskMapper:
    @staticmethod
    def to_domain(orm: Task):
        task = TaskDomain(
            id=orm.id,
            user_id=orm.user_id,
            title=orm.title,
            description=orm.description,
            category_id=orm.category_id,
            repeat_limit=orm.repeat_limit,
            repeat_frequency=orm.repeat_frequency,
            deadline=orm.deadline,
            last_completed_at=orm.last_completed_at,
            created_at=orm.created_at,
            type=orm.type,
            difficulty=orm.difficulty,
            priority=orm.priority,
            custom_xp_reward=orm.custom_xp_reward,
            custom_gold_reward=orm.custom_gold_reward,
            user=UserDomain(
                id=orm.user.id,
                username=orm.user.username,
                email=orm.user.email,
                password=orm.user.password,
                lvl=orm.user.lvl,
                xp=orm.user.xp,
                is_admin=orm.user.is_admin,
                current_rank_id=orm.user.current_rank_id,
                profile_picture=orm.user.profile_picture,
                gold=orm.user.gold
            ),
            skills=[SkillDomain(
                id=skill.id,
                user_id=skill.user_id,
                title=skill.title,
                description=skill.description,
                ico=skill.ico,
                lvl=skill.lvl,
                xp=skill.xp,
                deleted=skill.deleted,
                deleted_at=skill.deleted_at,
            ) for skill in orm.skills]
        )
        return task