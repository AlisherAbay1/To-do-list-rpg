from todo_rpg.application.interfaces import (
    RedisRepositoryProtocol,
    ShopTransactionRepositoryProtocol,
)
from todo_rpg.application.dto import ShopTransactionDTO, ShopTransactionFiltersDTO
from todo_rpg.application.mappers import ShopTransactionMapper
from todo_rpg.application.exceptions import SessionNotFoundError


class GetShopTransactionsInteractor:
    def __init__(
        self,
        repo: ShopTransactionRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self,
        session_token: str,
        limit: int,
        offset: int,
        filters: ShopTransactionFiltersDTO,
    ) -> list[ShopTransactionDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_transactions = await self.repo.get_shop_transactions_by_user_id(
            user_id, limit, offset, filters
        )
        return ShopTransactionMapper.to_list_dto(shop_transactions)
