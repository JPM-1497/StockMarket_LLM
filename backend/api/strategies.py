# backend/api/strategies.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from db.session import get_db
from models.strategy import Strategy
from auth.dependencies import get_current_user
from models.user import User
from uuid import UUID  
from services.ai import generate_stock_insights  # We'll create this next

router = APIRouter(
    prefix="/api/strategies",
    tags=["strategies"]
)

# Pydantic schemas
class StrategyCreate(BaseModel):
    name: str
    description: str
    stocks: str
    entry_criteria: str
    exit_criteria: str
    notes: str

class StrategyOut(BaseModel):
    id: str
    name: str
    description: str
    stocks: str
    entry_criteria: str
    exit_criteria: str
    notes: str

    class Config:
        orm_mode = True

@router.post("/", response_model=StrategyOut)
def create_strategy(
    strategy: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_strategy = Strategy(
        name=strategy.name,
        description=strategy.description,
        stocks=strategy.stocks,
        entry_criteria=strategy.entry_criteria,
        exit_criteria=strategy.exit_criteria,
        notes=strategy.notes,
        user_id=current_user.id
    )
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)
    return new_strategy

@router.get("/", response_model=List[StrategyOut])
def list_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Strategy).filter(Strategy.user_id == current_user.id).all()


@router.get("/{strategy_id}", response_model=StrategyOut)
def get_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id, Strategy.user_id == current_user.id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.put("/{strategy_id}", response_model=StrategyOut)
def update_strategy(
    strategy_id: UUID,
    updated_strategy: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id, Strategy.user_id == current_user.id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    strategy.name = updated_strategy.name
    strategy.description = updated_strategy.description
    strategy.stocks = updated_strategy.stocks
    strategy.entry_criteria = updated_strategy.entry_criteria
    strategy.exit_criteria = updated_strategy.exit_criteria
    strategy.notes = updated_strategy.notes

    db.commit()
    db.refresh(strategy)
    return strategy

@router.delete("/{strategy_id}")
def delete_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id, Strategy.user_id == current_user.id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    db.delete(strategy)
    db.commit()
    return {"detail": "Strategy deleted successfully"}


class StrategyAIOut(BaseModel):
    analysis: str

    class Config:
        orm_mode = True

@router.post("/{strategy_id}/analyze", response_model=StrategyAIOut)
def analyze_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id, Strategy.user_id == current_user.id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    analysis = generate_stock_insights(strategy)
    return {"analysis": analysis}
