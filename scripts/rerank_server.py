"""
BGE Reranker v2-m3 服务（兼容 SiliconFlow / Jina / Cohere rerank API）

端点: POST /rerank
请求体: {model, query, documents, top_n, return_documents, max_chunks_per_doc}
返回:  {results: [{index, relevance_score, document?}, ...]}

模型路径：D:\\AI agent\\tkk-library\\models\\bge-reranker-v2-m3
启动：python rerank_server.py
监听：0.0.0.0:8080
"""
import os
import sys
import time
from typing import List, Optional
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = r"D:\AI agent\tkk-library\models\bge-reranker-v2-m3"
HOST = "0.0.0.0"
PORT = 8080
MAX_LENGTH = 512
DTYPE = torch.float16  # F16 节省显存，精度损失 <0.5%

# 全局模型对象
_state = {"model": None, "tokenizer": None, "device": None}


def load_model():
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    print(f"[load] 加载模型: {MODEL_PATH}")
    print(f"[load] 设备: {'CUDA' if torch.cuda.is_available() else 'CPU'}, dtype: {DTYPE}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH, torch_dtype=DTYPE
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device).eval()

    _state["model"] = model
    _state["tokenizer"] = tokenizer
    _state["device"] = device
    print(f"[load] 模型加载完成 | device={device} | GPU mem={torch.cuda.memory_allocated()/1e9:.2f}GB")


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield
    # 清理
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


app = FastAPI(title="BGE Reranker v2-m3", lifespan=lifespan)


class RerankRequest(BaseModel):
    model: str = "BAAI/bge-reranker-v2-m3"
    query: str
    documents: List[str]
    top_n: Optional[int] = -1
    return_documents: Optional[bool] = True
    max_chunks_per_doc: Optional[int] = 1024


class RerankResultItem(BaseModel):
    index: int
    relevance_score: float
    document: Optional[str] = None


class RerankResponse(BaseModel):
    id: Optional[str] = None
    results: List[RerankResultItem]
    model: str
    usage: Optional[dict] = None


@app.get("/health")
async def health():
    if _state["model"] is None:
        raise HTTPException(503, "model not loaded")
    return {
        "status": "ok",
        "model": "BAAI/bge-reranker-v2-m3",
        "device": str(_state["device"]),
        "gpu_mem_gb": round(torch.cuda.memory_allocated() / 1e9, 2) if torch.cuda.is_available() else 0,
    }


@app.post("/rerank")
async def rerank(req: RerankRequest):
    if _state["model"] is None:
        raise HTTPException(503, "model not loaded yet")
    if not req.documents:
        return RerankResponse(results=[], model=req.model, usage={"total_tokens": 0})

    model = _state["model"]
    tokenizer = _state["tokenizer"]
    device = _state["device"]

    t0 = time.time()
    # BGE reranker 构造 (query, document) 对
    pairs = [[req.query, doc] for doc in req.documents]

    # 批量推理
    with torch.inference_mode():
        inputs = tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        ).to(device)
        scores = model(**inputs).logits.squeeze(-1).float().cpu().tolist()

    # 单个文档时 scores 是 float 不是 list
    if isinstance(scores, float):
        scores = [scores]

    # 按分数降序排序
    indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    if req.top_n is not None and req.top_n > 0:
        indexed = indexed[: req.top_n]

    results = []
    for idx, score in indexed:
        item = {"index": idx, "relevance_score": float(score)}
        if req.return_documents:
            item["document"] = req.documents[idx]
        results.append(item)

    elapsed_ms = int((time.time() - t0) * 1000)
    return RerankResponse(
        id=f"rerank-{int(time.time()*1000)}",
        results=results,
        model=req.model,
        usage={"total_tokens": 0, "latency_ms": elapsed_ms},
    )


if __name__ == "__main__":
    import uvicorn
    print(f"[start] BGE Reranker 服务 | 监听 {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", access_log=False)
