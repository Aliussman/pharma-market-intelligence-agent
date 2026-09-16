"""FastAPI application for the Pharma Market Intelligence API."""

import logging

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import API_HOST, API_PORT, API_TITLE, API_VERSION, CORS_ORIGINS
from src.schemas.models import MarketBriefOutput, PharmaInput, PharmaOutput
from src.services.analyzer import AnalysisService
from src.services.market_brief import MarketBriefAgent
from src.services.pdf_export import PDFExportService

logger = logging.getLogger(__name__)

app = FastAPI(title=API_TITLE, version=API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = AnalysisService()
market_brief_agent = MarketBriefAgent()


@app.get("/")
def root():
    return {"status": "Pharma Market Intelligence API is running"}


@app.post("/analyze", response_model=PharmaOutput)
def analyze(data: PharmaInput):
    try:
        analysis = service.analyze(company=data.company, raw_text=data.raw_text)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.exception("Analysis failed")
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return PharmaOutput(company=data.company, analysis=analysis)


@app.get("/market-brief", response_model=MarketBriefOutput)
def market_brief(
    topic: str = Query(
        default="pharmaceutical industry", max_length=120, description="Topic to research"
    )
):
    try:
        return market_brief_agent.generate_brief(topic=topic.strip() or "pharmaceutical industry")
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.exception("Market brief generation failed")
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/export/pdf")
def export_pdf(data: PharmaOutput):
    """Convert an analysis result into a downloadable PDF report."""
    text = PDFExportService.format_analysis_for_export(
        company=data.company, analysis=data.analysis.model_dump()
    )
    pdf = PDFExportService.create_pdf(text, title="Pharma Market Intelligence Report")
    filename = f"{data.company}_pharma_intelligence.pdf".replace(" ", "_")
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
