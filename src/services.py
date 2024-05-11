from src.repositories import UsersRepo


class UsersService:
    def __init__(self) -> None:
        self.repo = UsersRepo()

    async def get_or_create(self, tg_user_id):
        user = await self.repo.filter_one(tg_user_id=tg_user_id)
        if not user:
            user = await self.repo.create({"tg_user_id": tg_user_id})
        return user

    async def create(self, data):
        user = await self.repo.create(data)
        return user

    async def update(self, user_id, data):
        return await self.repo.update(user_id, data)

    async def is_exists(self, tg_user_id):
        return await self.repo.is_exists(tg_user_id=tg_user_id)
