from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.exceptions import TaskNotFoundError
from src.app.application.dto.tasks import TaskWithSkillsAndItemsDTO
from src.app.application.dto.skills import SkillDTO
from src.app.application.dto.items import ItemDTO
from uuid import UUID

class GetTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, task_id: UUID, get_related_skills: bool, get_related_items: bool):
        task = await self.repo.get_task_by_id(task_id, get_related_skills, get_related_items)
        if task is None:
            raise TaskNotFoundError()
        return TaskWithSkillsAndItemsDTO(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                category_id=task.category_id,
                repeat_limit=task.repeat_limit,
                repeat_frequency=task.repeat_frequency, 
                deadline=task.deadline, 
                created_at=task.created_at,
                type=task.type,
                difficulty=task.difficulty, 
                priority=task.priority,
                custom_xp_reward=task.custom_xp_reward,
                custom_gold_reward=task.custom_gold_reward,
                skills=[SkillDTO(
                        id=skill.id,
                        user_id=skill.user_id, 
                        title=skill.title, 
                        description=skill.description, 
                        ico=skill.ico, 
                        lvl=skill.lvl, 
                        xp=skill.xp, 
                        deleted=skill.deleted, 
                        deleted_at=skill.deleted_at)
                            for skill in task.skills],  
                items=[ItemDTO(
                        id=item.id,
                        user_id=item.user_id, 
                        title=item.title, 
                        description=item.description, 
                        deleted=item.deleted, 
                        deleted_at=item.deleted_at) 
                            for item in task.items]
            )
