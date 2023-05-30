from sqlalchemy import (Column, DateTime, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


engine = create_engine(
    f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@127.0.0.1:5432/{os.getenv('PG_DB')}")
Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)


class Announcements(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user = Column(String, nullable=False)
    create_date = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)
