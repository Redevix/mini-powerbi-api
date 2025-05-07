from sqlalchemy import Column, Integer, String, Text
from database import Base

class TreatedModel(Base):
    __tablename__ = "treated_models"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    data_json = Column(Text)  # Armazena dados tratados como JSON

