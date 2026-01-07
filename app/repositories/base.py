from typing import TypeVar, Generic, Type, Optional, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый репозиторий для CRUD операций"""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, obj_id: int) -> Optional[ModelType]:
        """Получить объект по ID"""
        result = await self.db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: Optional[int] = None) -> List[ModelType]:
        """Получить список объектов с пагинацией"""
        query = select(self.model).offset(skip)
        if limit:
            query = query.limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Создать новый объект"""
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        return db_obj

    async def update(self, obj_id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """Обновить объект"""
        db_obj = await self.get(obj_id)
        if not db_obj:
            return None

        # Подготавливаем данные для обновления
        update_data = obj_in.dict(exclude_unset=True)

        # Обновляем поля
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        return db_obj

    async def delete(self, obj_id: int) -> bool:
        """Удалить объект"""
        db_obj = await self.get(obj_id)
        if not db_obj:
            return False

        await self.db.delete(db_obj)
        return True
