from src.app.domain import TaskDomain, SkillDomain, UserDomain
from src.app.application.dto.tasks import CompleteTaskDTO, TaskReward
from src.app.application.dto.users import UserDTO
from src.app.application.dto.skills import SkillDTO

class CompleteTaskDtoMapper:
    @staticmethod
    def to_dto(task_domain: TaskDomain, 
               user_domain: UserDomain,
               skill_domains: list[SkillDomain], 
               rewards: TaskReward):
        dto = CompleteTaskDTO(
            id=task_domain.id,
            title=task_domain.title,
            description=task_domain.description,
            category_id=task_domain.category_id,
            xp=rewards.xp,
            gold=rewards.gold,
            repeat_limit=task_domain.repeat_limit,
            repeat_frequency=task_domain.repeat_frequency,
            deadline=task_domain.deadline,
            user=UserDTO(
                id=user_domain.id,
                username=user_domain.username,
                email=user_domain.email,
                password=user_domain.password,
                lvl=user_domain.lvl,
                xp=user_domain.xp,
                gold=user_domain.gold,
                is_admin=user_domain.is_admin,
                current_rank_id=user_domain.current_rank_id,
                profile_picture=user_domain.profile_picture
            ),
            skills=[SkillDTO(
                id=skill_domain.id,
                user_id=skill_domain.user_id,
                title=skill_domain.title,
                description=skill_domain.description,
                ico=skill_domain.ico,
                lvl=skill_domain.lvl,
                xp=skill_domain.xp,
                deleted=skill_domain.deleted,
                deleted_at=skill_domain.deleted_at
            ) for skill_domain in skill_domains]
        )
        return dto