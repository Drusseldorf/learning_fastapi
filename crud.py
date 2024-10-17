import asyncio

from sqlalchemy import select, text
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.testing.suite.test_reflection import users

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none() scalar_one_or_none - если не найдется в бд то будет None, а если просто scalar то выдаст исключение
    user = await session.scalar(stmt)  # None вернет если нету в бд
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    await session.close()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[(User, Profile)]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # joinedload используется так как мы не можем просто вызвать user.profile ниже в коде,
    # так как находимся в асинхронном контексте. Ибо профиль бы подгружался отдельно, а в асинкайо нужно сразу вместе одной операцией. тут под капотом в joinload используется join. Почему так? на след строке
    # Ленивая загрузка — это подход, при котором связанные данные (например, связанные таблицы) загружаются только тогда, когда к ним обращаются
    # Пример: Если у вас есть модель User, которая связана с моделью Post (например, один пользователь может иметь несколько постов),
    # при запросе пользователя данные о постах не будут загружены сразу.
    # Они загружаются только тогда, когда вы обращаетесь к атрибуту posts объекта User..
    # Неленивая загрузка (Eager Loading)
    # Что это такое: Неленивая загрузка — это подход, при котором связанные данные загружаются сразу же при выполнении основного запроса, одним объединённым запросом (JOIN).
    # Как это работает: SQLAlchemy сразу же загружает все необходимые данные и связанные записи, используя соединения (JOIN), чтобы минимизировать количество запросов к базе данных.
    # Проблема N+1
    # Что это такое: Проблема N+1 возникает, когда для каждого объекта из основного запроса выполняется дополнительный запрос для получения связанных данных. В результате получается N+1 запрос, где N — количество объектов из основного запроса.
    # Пример:
    # Вы делаете запрос, чтобы получить 10 профилей (SELECT * FROM profile — 1 запрос).
    # Для каждого профиля вы запрашиваете пользователя (SELECT * FROM user WHERE user_id = ...), что добавляет 10 запросов.
    # Итог: 1 основной запрос + 10 дополнительных запросов = 11 запросов.
    # Почему это плохо: Это неэффективно, особенно если данных много. Каждый дополнительный запрос требует сетевых ресурсов и времени на выполнение.
    # Как решать проблему N+1
    # Использование неленивой загрузки, таких как joinedload или selectinload, помогает избежать этой проблемы, загружая все данные сразу одним запросом:
    #
    # joinedload: Выполняет соединение (JOIN), чтобы получить все данные одним запросом. Подходит, если вы знаете, что данные не будут слишком большими.
    # selectinload: Делает один дополнительный запрос для получения всех связанных данных (без использования JOIN). Подходит, если вы ожидаете, что количество связанных данных будет большим.

    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    return list(users)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # варинат 1
    # stmt = select(User).options(joinedload(User.post)).order_by(User.id)
    # users = await session.scalars(stmt)
    #
    # # Тут left join и могут вернуться пользователи которые повторяются, поэтому к users можно применить uniqe()
    # for user in users.unique():  # type: User
    #     print("**" * 10)
    #     print(user)
    #     for post in user.post:
    #         print("-", post)

    # вариант 2
    # joinedload - можно использовать для связей и 1 ко многим и многие к 1 и 1 к 1
    # stmt = select(User).options(joinedload(User.post)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = (
    #     result.unique().scalars()
    # )  # а вот в таком варианте уже будут уникальные значения, когда через scalars
    #
    # for user in users:  # type: User
    #     print("**" * 10)
    #     print(user)
    #     for post in user.post:
    #         print("-", post)

    # вариант 3
    # Для связи 1 ко многим можно использовать selectinload, в таком вариаенте выполняется два селекта (2 отдельных запроса) без джоинов

    stmt = select(User).options(selectinload(User.post)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars()

    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for post in user.post:
            print("-", post)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(joinedload(User.profile), joinedload(User.post))
        .order_by(User.id)
    )

    users = await session.scalars(stmt)

    for user in users.unique():  # type: User
        print("**" * 10)
        print(
            user, user.profile and user.profile.first_name
        )  # интересный синтаксис, когда проверяется если А тру, то выводим Б. Если А фолс то выводим А
        for post in user.post:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(
    session: AsyncSession, user_id: int
):
    # stmt = (
    #     select(Profile)
    #     # .join(Profile.user)
    #     .options(
    #         joinedload(Profile.user).selectinload(User.post),
    #     )
    #     # .where(User.username == "john") # для алхимии чтобы сделать фильтрацию нужно добавлять join
    #     .order_by(Profile.id)
    # )
    #
    # profiles = await session.scalars(stmt)
    #
    # for profile in profiles:
    #     print(profile.first_name, profile.user)
    #     print(profile.user.post)

    # можно и параметризированным сырым запросом, но на выходе мы не получим объекты.
    # Тут уже нужно самому создавать их на основе моделек и парится о наличии None и тд
    query = text(
        """
        SELECT *
        FROM public.profile p
        LEFT JOIN public.user u ON p.user_id = u.id
        LEFT JOIN public.post po ON u.id = po.user_id
        WHERE (u.id = :user_id)
        ORDER BY p.id
    """
    )

    result: Result = await session.execute(query, {"user_id": user_id})
    rows = result.fetchall()
    print(rows)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="John")
        await create_user(session=session, username="Man")
        # user_sam = await get_user_by_username(session=session, username="Sam")
        # await create_user_profile(
        #     session=session,
        #     user_id=user_sam.id,
        #     first_name="Sam",
        #     last_name="White",
        # )
        # users_with_profiles = await show_users_with_profiles(session=session)
        # for user in users_with_profiles:
        #     print(user, user.profile)  # None if there is no profile
        # await create_posts(session, 2, "Some Post 1", "Some Post 2")
        # await get_users_with_posts(session=session)
        # await get_users_with_posts_and_profiles(session=session)
        # await get_profiles_with_users_and_users_with_posts(session=session, user_id=2)


if __name__ == "__main__":
    asyncio.run(main())
