from dishka import Provider, provide, Scope
from src.app.application.interfaces.repositories_interfaces import SkillRepositoryProtocol
from src.app.infrastructure.database.repositories import SkillRepository
from src.app.application.interactors import GetAllSkillsInteractor, GetCurrentUserSkillsInteractor, CreateCurrentUserSkillInteractor, \
                                        GetSkillInteractor, DeleteSkillInteractor, ClearExpiredSkillsInteractor

class SkillProvider(Provider):
    scope=Scope.REQUEST
    skill_repository = provide(SkillRepository, provides=SkillRepositoryProtocol)
    get_all_skills = provide(GetAllSkillsInteractor)
    get_current_user_skills = provide(GetCurrentUserSkillsInteractor)
    get_skill = provide(GetSkillInteractor)
    create_skill = provide(CreateCurrentUserSkillInteractor)
    delete_skill = provide(DeleteSkillInteractor)
    clear_expired_skills = provide(ClearExpiredSkillsInteractor)