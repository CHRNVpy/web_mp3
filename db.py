from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('postgresql://postgres:postgres@db/mp3_web')


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    uuid = Column(String)
    token = Column(String)


class Music(Base):
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    filename = Column(String)
    filedata = Column(LargeBinary)


Base.metadata.create_all(engine)


def add_user(username: str, uuid: str, token: str):
    """
    Добавление пользователя в БД

    :param username:
    :param uuid:
    :param token:
    :return:
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = Users(
        username=username,
        uuid=uuid,
        token=token,
    )
    session.add(new_user)
    session.commit()

    # Close the session
    session.close()


def add_audiofile(uuid: str, filename: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    with open(f'audio/{filename}', 'rb') as file:
        file_data = file.read()

    mp3_file = Music(
        uuid=uuid,
        filename=filename,
        filedata=file_data)

    session.add(mp3_file)
    session.commit()


def find_audiofile(uuid: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    audio_file = session.query(Music).filter_by(uuid=uuid).first()
    session.close()
    if audio_file:
        return audio_file.filename
    else:
        return False


def get_audiofile(uuid):
    Session = sessionmaker(bind=engine)
    session = Session()
    mp3_file = session.query(Music).filter_by(uuid=uuid).first()
    file_name = mp3_file.filename
    file_data = mp3_file.filedata
    return {'filename': file_name, 'filedata': file_data}
