from sqlalchemy import Column, Integer, String, Enum
from database import Base

class Users(Base):
   __tablename__ = 'users'
   id = Column(Integer, primary_key=True)
   username = Column(String(10), nullable=False)
   hashed_password = Column(String(100), nullable=False)
class DataProdi(Base):
   __tablename__ = 'data_prodi'
   id = Column(Integer, primary_key=True)
   kode_prodi = Column(String(10), nullable=True)
   nama_prodi = Column(String(100), nullable=True)
class DataDosen(Base):
   __tablename__ = 'data_dosen'
   nip = Column(String(10), primary_key=True)
   nama_lengkap = Column(String(100), nullable=True)
   prodi_id = Column(Integer, nullable=True)
class DataDokumen(Base):
   __tablename__ = 'data_dokumen'
   id = Column(Integer, primary_key=True)
   nip = Column(String(10), nullable=True)
   type_dokumen = Column(Enum("file", "url"), nullable=True)
   nama_dokumen = Column(String(100), nullable=True)
   nama_file = Column(String(100), nullable=True)