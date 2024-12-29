from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import uuid
from models import User, Embeddings
import numpy as np
from datetime import datetime

from utils import get_brazil_time

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create_user")
async def create_user(db: AsyncSession = Depends(get_db)):
    unique_email = f"johndoe_{uuid.uuid4()}@example.com"
    new_user = User(
        uuid=uuid.uuid4(),
        name="John Doe",
        nickname="johnd",
        email=unique_email,
        hashed_password="hashedpassword",
        created_at=get_brazil_time(),
        updated_at=get_brazil_time(),
        activated_at=get_brazil_time(),
        is_active=True,
        roles={}
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


    # Gerar um embedding fictício com um vetor de tamanho 100
    embedding_vector = np.random.rand(100).tolist()
    new_embedding = Embeddings(
        user_uuid=new_user.uuid,
        embedding=embedding_vector,
        created_at=get_brazil_time(),
    )
    db.add(new_embedding)
    await db.commit()
    await db.refresh(new_embedding)

    return f'Usuário criado com sucesso às {get_brazil_time()}'