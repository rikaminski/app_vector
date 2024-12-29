import uuid

import numpy as np
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Embeddings, User
from app.routers import user
from app.utils import get_brazil_time

app = FastAPI()

app.include_router(user.router)


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.post('/create_user')
async def create_user(db: AsyncSession = Depends(get_db)):
    unique_email = f'johndoe_{uuid.uuid4()}@example.com'
    new_user = User(
        uuid=uuid.uuid4(),
        name='John Doe',
        nickname='johnd',
        email=unique_email,
        hashed_password='hashedpassword',
        created_at=get_brazil_time(),
        updated_at=get_brazil_time(),
        activated_at=get_brazil_time(),
        is_active=True,
        roles={},
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


if __name__ == '__main__':
    print('Running main')
