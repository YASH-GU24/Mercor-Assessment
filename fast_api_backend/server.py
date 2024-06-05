from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils import get_user_chat_history
from llm.get_candidates import get_response
from queries.query import fetch_results

app = FastAPI()
origins = [
    "*"
]  # Adjust this to specify the origins you want to allow (e.g., ["http://localhost:3000"])

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_candidates")
async def check_product(request: Request):
    data = await request.json()
    chat_history = data["chatHistory"]
    user_chat_history = get_user_chat_history(chat_history)
    resp = get_response(user_chat_history)
    results = fetch_results(resp, user_chat_history)
    if results == []:
        resp[
            "message"
        ] = "None of the candidates in the database match this information"
    return {"answer": resp["message"], "results": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
