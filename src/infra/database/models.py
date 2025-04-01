from sqlalchemy import Column, BigInteger, String, Text, Enum,Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.models.user import UserSexEnum


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False, server_default=Identity(start=1, increment=1))
    phone_number: Mapped[str] = mapped_column(String(21), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    sex: Mapped[UserSexEnum] = mapped_column(Enum(UserSexEnum), nullable=False)
    full_name: Mapped[str] = mapped_column(String(64), nullable=True)
    is_ban: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


# async def add_user(**data):
#     async with async_session() as session:
#         async with session.begin():  # Начинаем транзакцию
#             user = await session.get(User, data["user_id"])
#             if user:
#                 await session.execute(update(User).where(User.user_id == data['user_id']).values(**data))
#             else:
#                 session.add(User(**data))  # Добавляем нового пользователя
#
#
# async def add_user(**data):
#     try:
#         async with async_session() as session:
#             session.add(User(**data))
#             await session.commit()
#     except:
#         await session.execute(update(User).where(User.user_id == data['user_id']).values(**data))
#         await session.commit()


