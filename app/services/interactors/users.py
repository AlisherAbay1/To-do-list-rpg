from app.repositories.interfaces import UserRepositoryProtocol, RedisRepositoryProtocol, TransactionProtocol
from app.schemas.dto import UserEmailDTO, UserPasswordDTO, CreateUserDTO, \
                            CreateUserResultDTO, LoginIdentifierDTO
from app.core.security import hash_password, password_verify
from app.exceptions import UserNotFoundError, EmailAlreadyTakenError, IncorrectPasswordError, \
                        UsernameAlreadyTakenError, SessionNotFoundError
from app.models import User
from uuid import UUID

class GetUsersInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit, offset):
        users = await self.repo.get_all_users(limit, offset)
        return users

class GetCurrentUser:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        return user

class UpdateCurrentUserEmailInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: UserEmailDTO, session_id: str):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        if not user:
            raise UserNotFoundError()
        if not password_verify(dto.password, user.password):
            raise IncorrectPasswordError()
        if self.repo.get_user_by_email(dto.new_email):
            raise EmailAlreadyTakenError()
        user.email = dto.new_email
        await self.transaction.commit()
        return dto.new_email
    
class UpdateCurrentUserPasswordInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: UserPasswordDTO, session_id: str):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        if not user:
            raise UserNotFoundError()
        if not password_verify(dto.old_password, user.password): 
            raise IncorrectPasswordError()
        user.password = dto.new_password
        await self.transaction.commit()

class DeleteCurrentUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_id):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        if not user:
            raise UserNotFoundError()
        await self.repo.delete(user)
        await self.transaction.commit()

class CreateUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: CreateUserDTO) -> CreateUserResultDTO:
        if self.repo.does_username_exists(dto.username):
            raise UsernameAlreadyTakenError()
        if self.repo.does_email_exists(dto.email):
            raise EmailAlreadyTakenError()
        hashed_password = hash_password(dto.password)
        user = User(
            username=dto.username, 
            email=dto.email,
            password=hashed_password
        )
        self.repo.save(user)
        session_id = await self.cash_repo.create_session(str(user.id))
        user_result = CreateUserResultDTO(
            username=user.username, 
            email=user.email, 
            session_id=session_id
        )
        await self.transaction.commit()
        return user_result

class AuthenticateUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, dto: LoginIdentifierDTO):
        if "@" in dto.username_or_email:
            user = await self.repo.get_user_by_email(dto.username_or_email)
        else:
            user = await self.repo.get_user_by_username(dto.username_or_email)
        if user is None:
            raise UserNotFoundError()
        if not password_verify(dto.password, user.password):
            raise IncorrectPasswordError()
        session_id = await self.cash_repo.create_session(str(user.id))
        return CreateUserResultDTO(
            username=user.username, 
            email=user.email, 
            session_id=session_id
        )

class DeleteSessionInteractor:
    def __init__(self, cash_repo: RedisRepositoryProtocol) -> None:
        self.cash_repo = cash_repo

    async def __call__(self, session_id: str) -> None:
        await self.cash_repo.delete_session(session_id)

#admin 
class GetUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, user_id):
        pass

#admin 
class UpdateUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, user_id, data: dict):
        pass

#admin 
class DeleteUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, user_id):
        pass