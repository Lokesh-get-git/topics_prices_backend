# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import topics, experience, pricing, adjustments, calculate

app = FastAPI(title="Interview Pricing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topics.router, prefix="/api")
# app.include_router(experience.router, prefix="/api")
# app.include_router(pricing.router, prefix="/api")
# app.include_router(adjustments.router, prefix="/api")
# app.include_router(calculate.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Interview Pricing API running"}
