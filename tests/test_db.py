from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='slash', email='snakepit@gnr.com', password='secret')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'snakepit@gnr.com')
    )

    assert result.username == 'slash'
