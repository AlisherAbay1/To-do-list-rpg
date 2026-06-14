from todo_rpg.presentation.schemas import ShopTransactionFilters
from todo_rpg.application.dto import ShopTransactionFiltersDTO


class ShopTransactionSchemaMapper:
    @staticmethod
    def to_filters_dto(filters: ShopTransactionFilters) -> ShopTransactionFiltersDTO:
        dto = ShopTransactionFiltersDTO(
            date_from=filters.date_from,
            date_to=filters.date_to,
            sum_from=filters.sum_from,
            sum_to=filters.sum_to,
        )
        return dto
