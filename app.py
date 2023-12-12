from concurrent.futures import ThreadPoolExecutor
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from configuration.constant import IS_S3_ACTIVATE, SAVE_FILE_TYPE
from configuration.constant import MODEL_DESCRIPTION
from makeMelody.melodyModel import MelodyModel

app = FastAPI()
model = MelodyModel(MODEL_DESCRIPTION)
executor = ThreadPoolExecutor(max_workers=4)

origins = [
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/getMelody')
async def makeMelody(user_id: Annotated[str, Form()],
                     texts: Annotated[str, Form()],
                     token_cnt: Annotated[int, Form()] = 256):
    texts = texts.split("|")
    try:
        if IS_S3_ACTIVATE:
            content = model.upload_to_s3(texts, token_cnt, user_id, SAVE_FILE_TYPE)
        else:
            raise Exception()
        # else:
        #     content = model.upload_to_backend(texts, token_cnt)
        # content = executor.submit(model.upload_to_backend(), texts, token_cnt)

        return {'status': 'OK', 'content': content}
    except Exception:
        return {'status': 'NOT_FOUND'}


if __name__ == "__main__":
    uvicorn.run(app)
