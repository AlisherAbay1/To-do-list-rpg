from dishka import Provider, provide, Scope
from app.repositories.interfaces import SkillRepositoryProtocol
from app.repositories.skills import SkillRepository
from app.services.interactors import GetAllSkillsInteractor, GetCurrentUserSkillsInteractor, CreateCurrentUserSkillInteractor, \
                                    GetSkillInteractor, DeleteSkillInteractor

class SkillProvider(Provider):
    scope=Scope.REQUEST
    skill_repository = provide(SkillRepository, provides=SkillRepositoryProtocol)
    get_all_skills = provide(GetAllSkillsInteractor)
    get_current_user_skills = provide(GetCurrentUserSkillsInteractor)
    get_skill = provide(GetSkillInteractor)
    create_skill = provide(CreateCurrentUserSkillInteractor)
    delete_skill = provide(DeleteSkillInteractor)