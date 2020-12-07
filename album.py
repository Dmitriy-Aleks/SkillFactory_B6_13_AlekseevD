import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def find_album(album_data):
    """
    Поиск альбома в БД по введенным параметрам
    """
    session = connect_db()
    existing_album = session.query(Album).filter(
    Album.year == album_data["year"],
    Album.artist == album_data["artist"],
    Album.genre == album_data["genre"],
    Album.album == album_data["album"]
    ).first()

    return existing_album

def add_album(album_data):
    """
    Сохраняет в базу данных переданные пользователем данные об альбоме
    """
    session = connect_db()
    added_album = Album(
        year=int(album_data["year"]),
        artist=album_data["artist"],
        genre=album_data["genre"], 
        album=album_data["album"]
        )

    session.add(added_album)
    try:
        session.commit()
    except Exception as e:
        return False
    else:
        return True

def album_validation(key, value):

    """
    Проверяет введенные пользователем данные об альбоме. Год должен быть числом в определеном 
    диапазоне, остальные параметры не должны быть пустыми.
    """

    if value is None:
        return False, "В поле {} не введено значение".format(key)
    elif key == "year":
        try:
            value = int(value)
        except ValueError as e:
            return False, "Год должен быть числом, а не строкой"
        else:
            if value < 1900 or value > 2020:
                return False, "Год должен быть не меньше 1900 и не больше 2020"
            else:
                return True, ""
    else:
        return True, ""