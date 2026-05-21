from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_store = [
    {"id":1,"title":"基本設計書の作成","bpo":"建築BPO","status":"未着手","assignee":"田中 一郎","due":"2026-06-10","note":""},
    {"id":2,"title":"施工図レビュー依頼","bpo":"土木BPO","status":"未着手","assignee":"鈴木 花子","due":"2026-06-05","note":""},
    {"id":3,"title":"業務フロー整備","bpo":"LinkBPO","status":"未着手","assignee":"中村 誠","due":"2026-06-15","note":""},
    {"id":4,"title":"竣工図デジタル化","bpo":"建築BPO","status":"進行中","assignee":"田中 一郎","due":"2026-05-28","note":""},
    {"id":5,"title":"CADデータ整理","bpo":"土木BPO","status":"進行中","assignee":"伊藤 さき","due":"2026-05-30","note":""},
    {"id":6,"title":"ナーミング規則策定","bpo":"LinkBPO","status":"進行中","assignee":"中村 誠","due":"2026-06-01","note":""},
    {"id":7,"title":"積算チェック対応","bpo":"土木BPO","status":"進行中","assignee":"鈴木 花子","due":"2026-05-25","note":""},
    {"id":8,"title":"組織図ドラフト","bpo":"LinkBPO","status":"レビュー待ち","assignee":"中村 誠","due":"2026-05-22","note":""},
    {"id":9,"title":"断面図修正版","bpo":"建築BPO","status":"レビュー待ち","assignee":"伊藤 さき","due":"2026-05-23","note":""},
    {"id":10,"title":"ヒアリングシート作成","bpo":"建築BPO","status":"完了","assignee":"鈴木 花子","due":"2026-05-15","note":""},
    {"id":11,"title":"クライアント報告資料","bpo":"建築BPO","status":"完了","assignee":"田中 一郎","due":"2026-05-18","note":""},
    {"id":12,"title":"マニュアル初版","bpo":"LinkBPO","status":"完了","assignee":"中村 誠","due":"2026-05-20","note":""},
]
_next_id = 13

class TaskIn(BaseModel):
    title: str
    bpo: str = "建築BPO"
    status: str = "未着手"
    assignee: str = ""
    due: Optional[str] = ""
    note: Optional[str] = ""

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/tasks")
def list_tasks(bpo: Optional[str] = None, status: Optional[str] = None):
    result = _store
    if bpo:
        result = [t for t in result if t["bpo"] == bpo]
    if status:
        result = [t for t in result if t["status"] == status]
    return result

@app.post("/api/tasks", status_code=201)
def create_task(task: TaskIn):
    global _next_id
    new = {"id": _next_id, **task.dict()}
    _store.append(new)
    _next_id += 1
    return new

@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    t = next((t for t in _store if t["id"] == task_id), None)
    if not t:
        raise HTTPException(404, "Not found")
    return t

@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: TaskIn):
    for i, t in enumerate(_store):
        if t["id"] == task_id:
            _store[i] = {"id": task_id, **task.dict()}
            return _store[i]
    raise HTTPException(404, "Not found")

@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global _store
    orig = len(_store)
    _store = [t for t in _store if t["id"] != task_id]
    if len(_store) == orig:
        raise HTTPException(404, "Not found")

@app.get("/api/stats")
def stats():
    by_status = {}
    by_bpo = {}
    for t in _store:
        by_status[t["status"]] = by_status.get(t["status"], 0) + 1
        by_bpo[t["bpo"]] = by_bpo.get(t["bpo"], 0) + 1
    return {"by_status": by_status, "by_bpo": by_bpo}
