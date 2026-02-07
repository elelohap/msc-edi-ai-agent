from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rag.retriever import retrieve_context
from rag.llm import ask_llm
import traceback

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask(payload: AskRequest):
    try:
        question = payload.question.strip()
        if not question:
            return JSONResponse(
                {"error": "No question provided"},
                status_code=400
            )

        context_chunks = retrieve_context(question, top_k=10)
        answer = ask_llm(question, context_chunks)

        return JSONResponse({"answer": answer})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )
