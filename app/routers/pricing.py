from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
import models
from schemas.pricing import (
    BasePricingTableOut,
    BasePricingCellUpdate,
)

router = APIRouter(prefix="/pricing", tags=["pricing"])

