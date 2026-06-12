from dishka import Provider, provide, Scope
from todo_rpg.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
)
from todo_rpg.infrastructure.database.repositories import SkillRepository
from todo_rpg.application.interactors import (
    GetAllSkillsInteractor,
    GetCurrentUserSkillsInteractor,
    CreateCurrentUserSkillInteractor,
    GetSkillInteractor,
    DeleteSkillInteractor,
    ClearExpiredSkillsInteractor,
    DeleteCurrentUserSkillByIdInteractor,
    GetCurrentUserSkillByIdInteractor,
    UpdateCurrentUserSkillById,
)


class SkillProvider(Provider):
    scope = Scope.REQUEST
    skill_repository = provide(SkillRepository, provides=SkillRepositoryProtocol)
    get_all_skills = provide(GetAllSkillsInteractor)
    get_current_user_skills = provide(GetCurrentUserSkillsInteractor)
    get_skill = provide(GetSkillInteractor)
    create_skill = provide(CreateCurrentUserSkillInteractor)
    delete_skill = provide(DeleteSkillInteractor)
    clear_expired_skills = provide(ClearExpiredSkillsInteractor)
    delete_current_user_skill_by_id = provide(DeleteCurrentUserSkillByIdInteractor)
    get_current_user_skill_by_id = provide(GetCurrentUserSkillByIdInteractor)
    update_current_user_skill_by_id = provide(UpdateCurrentUserSkillById)
