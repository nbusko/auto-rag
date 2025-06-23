from fastapi import FastAPI

app = FastAPI()


@app.get("/get_answer_by_message_id/{message_id}")
async def get_answer_by_message_id(message_id: str):
    return {"answer": "hihello!"}