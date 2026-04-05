from fastapi import APIRouter, Depends, HTTPException
from analysis_queue.analysis_worker import process_brain_analysis
from schema.analysis_schema import AnalysisRequest
from middleware.verify_token import verify_token

router = APIRouter(
    prefix="/v1/api/analysis",
    tags=["analysis"],
)

@router.post("/process")
async def process_brain_analysis_endpoint(req: AnalysisRequest, user=Depends(verify_token)):
    try:
        task = process_brain_analysis.delay(req.html, user.id)
        return {"status": "queued", "task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
