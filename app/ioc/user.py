from dishka import Provider, provide, Scope
from app.repositories.interfaces import UserRepositoryProtocol
from app.repositories.users import UserRepository
from app.services.interactors import GetUsersInteractor, UpdateCurrentUserEmailInteractor, DeleteCurrentUserInteractor, \
                                    GetUserInteractor, GetSessionTimeInteractor, UpdateCurrentUserPasswordInteractor, \
                                    CreateUserInteractor, GetCurrentUser, AuthenticateUserInteractor, \
                                    DeleteSessionInteractor, RefreshSessionTokenInteractor


class UserProvider(Provider):
    scope = Scope.REQUEST
    user_repository = provide(UserRepository, provides=UserRepositoryProtocol)
    get_users_interactor = provide(GetUsersInteractor)
    update_current_user_email_interactor = provide(UpdateCurrentUserEmailInteractor)
    delete_current_user_interactor = provide(DeleteCurrentUserInteractor)
    get_user_interactor = provide(GetUserInteractor)
    get_session_time_interactor = provide(GetSessionTimeInteractor)
    update_current_user_password_interactor = provide(UpdateCurrentUserPasswordInteractor)
    create_user_interactor = provide(CreateUserInteractor)
    get_current_user = provide(GetCurrentUser)
    authenticate_user_interactor = provide(AuthenticateUserInteractor)
    delete_session_interactor = provide(DeleteSessionInteractor)
    refresh_session_token_interactor = provide(RefreshSessionTokenInteractor)