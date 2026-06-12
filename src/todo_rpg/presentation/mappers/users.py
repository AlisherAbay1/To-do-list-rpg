from todo_rpg.presentation.schemas import (
    UserSchemaCreateAuth,
    UserSignInSchema,
    UserSchemaPatchEmail,
)
from todo_rpg.application.dto import CreateUserDTO, SignInDTO, UserEmailDTO


class UserSchemaMapper:
    @staticmethod
    def to_create_dto(schema: UserSchemaCreateAuth) -> CreateUserDTO:
        dto = CreateUserDTO(
            username=schema.username, email=schema.email, password=schema.password
        )
        return dto

    @staticmethod
    def to_sign_in_dto(schema: UserSignInSchema) -> SignInDTO:
        dto = SignInDTO(
            username_or_email=schema.username_or_email, password=schema.password
        )
        return dto

    @staticmethod
    def to_email_dto(schema: UserSchemaPatchEmail) -> UserEmailDTO:
        dto = UserEmailDTO(new_email=schema.new_email, password=schema.password)
        return dto
