import traceback
from typing import List
from typing import Tuple
from datetime import datetime

from loguru import logger
from models.engine import Session
from models.signals import Signals


class Serializer:

    def __init__(self, id_subject: int, id_session: int) -> None:
        self.session = Session()
        self.id_subject = id_subject
        self.id_session = id_session

    def serialize(self, id_collect: int, id_iaps: str, valence: float,
                  arousal: float,
                  signals: List[Tuple[datetime, float, float, float]]) -> None:
        instances = [
            Signals(
                id_subject=self.id_subject,
                id_session=self.id_session,
                id_collect=id_collect,
                date_time=signal[0],
                ppg_signal=signal[1],
                eda_signal=signal[2],
                skt_signal=signal[3],
                sam_arousal=arousal,
                sam_valence=valence,
                id_iaps=id_iaps) for signal in signals
        ]

        try:
            self.session.add_all(instances)
            self.session.commit()
        except BaseException:
            self.session.rollback()
            logger.error(traceback.format_exc())
