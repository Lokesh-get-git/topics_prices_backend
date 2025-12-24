
from fastapi import FastAPI
from routers import topics, experience, pricing, adjustments, calculate

app = FastAPI(title="Topics And Pricing API")

app.include_router(topics.router, prefix="/api")
app.include_router(experience.router, prefix="/api")
app.include_router(adjustments.router, prefix="/api")
app.include_router(pricing.router, prefix="/api")
app.include_router(calculate.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Interview Pricing API running"}
