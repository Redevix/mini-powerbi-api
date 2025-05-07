from fastapi import APIRouter, UploadFile, Form
import pandas as pd
import json
from models import TreatedModel
from database import SessionLocal
from sqlalchemy.orm import Session
import io

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/tratar-e-salvar")
async def tratar_e_salvar_excel(file: UploadFile, project_id: str = Form(...), db: Session = next(get_db())):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        # Remover colunas vazias
        df.dropna(how='all', axis=1, inplace=True)

        # Detectar se a primeira linha é cabeçalho
        if df.columns.str.contains("Unnamed").any():
            df.columns = df.iloc[0]
            df = df[1:]

        df = df.reset_index(drop=True)

        # Salva o JSON do dataframe tratado
        model = TreatedModel(project_id=project_id, data_json=df.to_json(orient="records"))
        db.add(model)
        db.commit()

        return {"message": "Modelo tratado salvo com sucesso!", "rows": len(df)}

    except Exception as e:
        return {"error": str(e)}

