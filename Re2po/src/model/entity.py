from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, text, update ,Double
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    'RE2PO_DATABASE_URL',
    'mysql+pymysql://root:mysql_pwd@localhost:3306/minio?charset=utf8mb4',
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ModelInfo(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    layer_hash = Column(String(255), nullable=False)
    model_name = Column(String(255), nullable=False)
    minio_id = Column(String(255), nullable=False)
    layer_number = Column(Integer, nullable=False)
    layer_name = Column(String(255), nullable=False)
    layer_location = Column(String(255), nullable=False)
    layer_size = Column(Double, nullable=False)

class StorageInfo(Base):
    __tablename__ = 'storage'

    minio_id = Column(String(255), primary_key=True, index=True)
    minio_location = Column(String(255), nullable=False)
    used_space = Column(String(255), nullable=False)
    free_space = Column(String(255), nullable=False)
    total_space = Column(String(255), nullable=False)

class DataInfo(Base):
    __tablename__ = 'storage_data'

    model_name = Column(String(255), primary_key=True, index=True)
    file_number = Column(Integer, nullable=False) 
    layer_number = Column(Integer, nullable=False) 
    minio_count = Column(Integer, nullable=False)
    complete = Column(Integer, nullable=False) 

class ModelInfo_2(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), nullable=False)
    layer_num = Column(Integer, nullable=False)
    layer_hash = Column(String(255), nullable=False)
    layer_name = Column(String(255), nullable=False)

class LocationInfo(Base):
    __tablename__ = 'location'

    layer_hash = Column(String(255), primary_key=True, nullable=False)
    layer_location = Column(String(255), nullable=False)
    minio_id = Column(String(255), nullable=False)
