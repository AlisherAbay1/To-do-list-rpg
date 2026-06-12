from dishka import Provider, provide, Scope
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRankRepositoryProtocol,
)
from todo_rpg.infrastructure.database.repositories import UserRankRepository
from todo_rpg.application.interactors import (
    GetCurrentUserRanksInteractor,
    GetCurrentUserRankInteractor,
    CreateCurrentUserRankInteractor,
    UpdateCurrentUserRankInteractor,
    DeleteCurrentUserRankInteractor,
)


class UserRankProvider(Provider):
    scope = Scope.REQUEST
    user_rank_repository = provide(
        UserRankRepository, provides=UserRankRepositoryProtocol
    )
    get_current_user_ranks = provide(GetCurrentUserRanksInteractor)
    get_current_user_rank = provide(GetCurrentUserRankInteractor)
    create_current_user_rank = provide(CreateCurrentUserRankInteractor)
    update_current_user_rank = provide(UpdateCurrentUserRankInteractor)
    delete_current_user_rank = provide(DeleteCurrentUserRankInteractor)
