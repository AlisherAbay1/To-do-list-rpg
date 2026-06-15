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
    DeleteCurrentUserSkillInteractor,
    GetCurrentUserSkillInteractor,
    UpdateCurrentUserSkillInteractor,
)


class SkillProvider(Provider):
    scope = Scope.REQUEST
    skill_repository = provide(SkillRepository, provides=SkillRepositoryProtocol)
    get_all_skills = provide(GetAllSkillsInteractor)
    get_skill = provide(GetSkillInteractor)
    delete_skill = provide(DeleteSkillInteractor)
    get_current_user_skills = provide(GetCurrentUserSkillsInteractor)
    create_current_user_skill = provide(CreateCurrentUserSkillInteractor)
    clear_expired_skills = provide(ClearExpiredSkillsInteractor)
    delete_current_user_skill_by_id = provide(DeleteCurrentUserSkillInteractor)
    get_current_user_skill = provide(GetCurrentUserSkillInteractor)
    update_current_user_skill = provide(UpdateCurrentUserSkillInteractor)
