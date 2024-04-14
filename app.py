from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from database import engine, session
from sqlalchemy.orm import Session
import auth
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

class DataProdiBase(BaseModel):
    kode_prodi: str
    nama_prodi: str
class DataDosenBase(BaseModel):
    nama_lengkap : str
    prodi_id : int
class DataDokumenBase(BaseModel):
    nip : str
    type_dokumen : str
    nama_dokumen : str
    nama_file : str

class DataDosenBaseCreated(BaseModel):
    nip : str
    nama_lengkap : str
    prodi_id : int

def get_db():
   db = session()
   try:
      yield db
   finally:
       db.close

#PRODI
@app.post('/prodi', status_code=status.HTTP_201_CREATED)
async def add_prodi(prodi: DataProdiBase,current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
   try:
        db_prodi = models.DataProdi(**prodi.dict())
        db.add(db_prodi)
        db.commit()
        return {"message": "Prodi added successfully"}
   except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add Prodi: {str(e)}")
@app.get('/prodi/{prodi_id}', status_code=status.HTTP_200_OK)
async def get_prodi_by_id(prodi_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    prodi = db.query(models.DataProdi).filter(models.DataProdi.id == prodi_id).first()
    if prodi is None:
        raise HTTPException(status_code=404, detail="Prodi not found")
    return prodi
@app.put('/prodi/{prodi_id}', status_code=status.HTTP_201_CREATED)
async def update_prodi_by_id(prodi_id: int, prodi: DataProdiBase, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_prodi = db.query(models.DataProdi).filter(models.DataProdi.id == prodi_id).first()
    if db_prodi is None:
        raise HTTPException(status_code=404, detail="Prodi was not found")
    try :
        for attr, value in prodi.dict().items():
            setattr(db_prodi, attr, value)
        db.commit()
        return {"message": "Prodi updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update prodi: {str(e)}")
@app.delete('/prodi/{prodi_id}', status_code=status.HTTP_200_OK)
async def delete_prodi_by_id(prodi_id: int, current_user: dict = Depends(get_current_user), db : Session = Depends(get_db)):
    db_prodi = db.query(models.DataProdi).filter(models.DataProdi.id == prodi_id).first()
    if db_prodi is None:
        raise HTTPException(status_code=404, detail='Prodi was not found')
    db.delete(db_prodi)
    db.commit()
    return {"message": "Prodi deleted successfully"}
@app.get('/prodi', status_code=status.HTTP_200_OK)
async def get_all_prodi(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    prodi = db.query(models.DataProdi).all()
    if prodi is None:
        raise HTTPException(status_code=404, detail="Prodi is empty")
    return prodi

#DOSEN
@app.post('/dosen', status_code=status.HTTP_201_CREATED)
async def add_dosen(dosen: DataDosenBaseCreated, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    dosenIsExist = db.query(models.DataDosen).filter(models.DataDosen.nip == dosen.nip).first()
    prodiIsExist = db.query(models.DataProdi).filter(models.DataProdi.id == dosen.prodi_id).first()
    if dosenIsExist:
        raise HTTPException(status_code=400, detail=f"NIP '{dosen.nip}' already exists")
    if prodiIsExist is None:
        raise HTTPException(status_code=404, detail="Prodi was not found")
    try:
        db_dosen = models.DataDosen(**dosen.dict())
        db.add(db_dosen)
        db.commit()
        return {"message": "Dosen added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add Dosen: {str(e)}")
@app.get('/dosen/{dosen_nip}', status_code=status.HTTP_200_OK)
async def get_dosen_by_nip(dosen_nip: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    dosen = db.query(models.DataDosen).filter(models.DataDosen.nip == dosen_nip).first()
    if dosen is None:
        raise HTTPException(status_code=404, detail="Dosen not found")
    return dosen
@app.put('/dosen/{dosen_nip}', status_code=status.HTTP_201_CREATED)
async def update_dosen_by_nip(dosen_nip: str, dosen: DataDosenBase, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_dosen = db.query(models.DataDosen).filter(models.DataDosen.nip == dosen_nip).first()
    prodiIsExist = db.query(models.DataProdi).filter(models.DataProdi.id == dosen.prodi_id).first()
    if db_dosen is None:
        raise HTTPException(status_code=404, detail="Dosen was not found")
    if prodiIsExist is None:
        raise HTTPException(status_code=404, detail="Prodi was not found")
    try :
        for attr, value in dosen.dict().items():
            setattr(db_dosen, attr, value)
        db.commit()
        return {"message": "Dosen updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update dosen: {str(e)}")
@app.delete('/dosen/{dosen_nip}', status_code=status.HTTP_200_OK)
async def delete_dosen_by_nip(dosen_nip: str, current_user: dict = Depends(get_current_user), db : Session = Depends(get_db)):
    db_dosen = db.query(models.DataDosen).filter(models.DataDosen.nip == dosen_nip).first()
    if db_dosen is None:
        raise HTTPException(status_code=404, detail='Dosen was not found')
    db.delete(db_dosen)
    db.commit()
    return {"message": "Dosen deleted successfully"}
@app.get('/dosen', status_code=status.HTTP_200_OK)
async def get_all_dosen(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    dosen = db.query(models.DataDosen).all()
    if dosen is None:
        raise HTTPException(status_code=404, detail="Dosen is empty")
    return dosen

#DOKUMEN
@app.post('/document', status_code=status.HTTP_201_CREATED)
async def add_dokumen(dokumen: DataDokumenBase, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_dokumen = models.DataDokumen(**dokumen.dict())
        db.add(db_dokumen)
        db.commit()
        return {"message": "Document added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add Document: {str(e)}")
@app.get('/document/{document_id}', status_code=status.HTTP_200_OK)
async def get_document_by_id(document_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(models.DataDokumen).filter(models.DataDokumen.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
@app.put('/document/{document_id}', status_code=status.HTTP_201_CREATED)
async def update_document_by_id(document_id: int, document: DataDokumenBase, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_dokumen = db.query(models.DataDokumen).filter(models.DataDokumen.id == document_id).first()
    db_dosen = db.query(models.DataDosen).filter(models.DataDosen.nip == document.nip).first()
    if db_dokumen is None:
        raise HTTPException(status_code=404, detail="Document was not found")
    if db_dosen is None:
        raise HTTPException(status_code=404, detail="Dosen was not found")
    try :
        for attr, value in document.dict().items():
            setattr(db_dokumen, attr, value)
        db.commit()
        return {"message": "Document updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update document: {str(e)}")
@app.delete('/document/{document_id}', status_code=status.HTTP_200_OK)
async def delete_document_by_id(document_id: int, current_user: dict = Depends(get_current_user), db : Session = Depends(get_db)):
    db_document = db.query(models.DataDokumen).filter(models.DataDokumen.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail='Document was not found')
    db.delete(db_document)
    db.commit()
    return {"message": "Document deleted successfully"}
@app.get('/document', status_code=status.HTTP_200_OK)
async def get_all_document(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(models.DataDokumen).all()
    if document is None:
        raise HTTPException(status_code=404, detail="Dosen is empty")
    return document