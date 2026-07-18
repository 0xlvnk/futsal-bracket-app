from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    round_name = Column(String(50), nullable=False)
    match_code = Column(String(20), nullable=False)

    team1_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    team2_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])

    match_date = Column(Date, nullable=True)
    time_start = Column(String(10), nullable=True)
    time_end = Column(String(10), nullable=True)

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)

    is_penalty = Column(Boolean, default=False)
    penalty_home_score = Column(Integer, nullable=True)
    penalty_away_score = Column(Integer, nullable=True)

    winner_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    winner = relationship("Team", foreign_keys=[winner_id])

    def calculate_result(self):
        if self.home_score is None or self.away_score is None:
            return None

        if self.home_score > self.away_score:
            self.winner_id = self.team1_id
            self.is_penalty = False
        elif self.away_score > self.home_score:
            self.winner_id = self.team2_id
            self.is_penalty = False
        else:
            if self.penalty_home_score is not None and self.penalty_away_score is not None:
                self.is_penalty = True
                if self.penalty_home_score > self.penalty_away_score:
                    self.winner_id = self.team1_id
                else:
                    self.winner_id = self.team2_id

        return self.winner_id


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    name = Column(String(150), nullable=True)
    