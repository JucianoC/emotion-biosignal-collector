from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String

from models.engine import Base


class Signals(Base):
    __tablename__ = 'signals'

    id = Column(Integer, primary_key=True)
    id_subject = Column(Integer, nullable=False)
    id_session = Column(Integer, nullable=False)
    id_collect = Column(Integer, nullable=False)
    date_time = Column(DateTime(timezone=True), nullable=False)
    ppg_signal = Column(Float, nullable=False)
    eda_signal = Column(Float, nullable=False)
    skt_signal = Column(Float, nullable=False)
    sam_arousal = Column(Float, nullable=False)
    sam_valence = Column(Float, nullable=False)
    id_iaps = Column(String(10), nullable=False)
