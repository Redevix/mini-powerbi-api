from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "FastAPI funcionando com sucesso na Railway!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents))
        else:
            return {"erro": "Formato de arquivo não suportado"}
        return {"colunas": df.columns.tolist(), "linhas": len(df)}
    except Exception as e:
        return {"erro": str(e)}

