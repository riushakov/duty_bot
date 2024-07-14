from connection import Base, session, engine
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, func, asc, distinct
from datetime import datetime as dt


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    date = Column(String)
    pos = Column(Integer)
    status = Column(String)
    username = Column(String)
    text = Column(String)
    dt_start = Column(DateTime)
    dt_finish = Column(DateTime)
    url = Column(String)
    env = Column(String)
    is_active = Column(Boolean)

    def update_event(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    @classmethod
    def get_event(cls, chat_id, date, pos):
        return session.query(cls).filter_by(chat_id=chat_id, date=date, pos=pos, is_active=1).first()

    @classmethod
    def get_all_events(cls, **filters):
        query = session.query(cls)
        for field, values in filters.items():
            if isinstance(values, list):
                query = query.filter(getattr(cls, field).in_(values))
            else:
                query = query.filter(getattr(cls, field) == values)
        return query.order_by(asc(cls.pos)).all()

    @classmethod
    def add_event(cls, **kwargs):
        new_event = cls(**kwargs)
        session.add(new_event)
        session.commit()

    @classmethod
    def new_pos(cls, chat_id, date):
        pos = (session.query(func.max(cls.pos)).
               filter(cls.chat_id == chat_id, cls.date == date, cls.is_active == 1).scalar())
        if pos:
            return pos + 1
        else:
            return 1

    @classmethod
    def get_distinct_chats_id(cls):
        chat_ids = session.query(distinct(Event.chat_id)).all()
        return [i[0] for i in chat_ids]


Base.metadata.create_all(engine)
