from sqlalchemy import select

from fast_zero.models import Todo, User


def test_create_user(session):
    user = User(username='slash', email='snakepit@gnr.com', password='secret')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'snakepit@gnr.com')
    )

    assert result.username == 'slash'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
