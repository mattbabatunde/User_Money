from fastapi import APIRouter, Depends, HTTPException, status
from decimal import Decimal
from schemas.account import AccountCreatePayload
from schemas.transaction import DepositTransactionPayload, WithdrawTransactionPayload
from services.account import account_service
from deps import get_current_user
from datetime import date


account_router = APIRouter()


@account_router.post("")
def create_account(
    account_data: AccountCreatePayload,
    current_user=Depends(get_current_user)
):
    new_account = account_service.create_account(account_data, current_user)
    return new_account


@account_router.get("")
def get_account(current_user=Depends(get_current_user)):
    account = account_service.get_account(current_user)
    return account


@account_router.post("/deposit")
def deposit(transaction: DepositTransactionPayload, account=Depends(get_account), current_user=Depends(get_current_user)):
    return account_service.deposit_fund(transaction, account.id)


@account_router.post("/withdraw")
def withdraw(transaction: WithdrawTransactionPayload, account=Depends(get_account), current_user=Depends(get_current_user)):

    MIN_WITHDRAW_AMOUNT = 300
    MAX_DAILY_WITHDRAWALS = 6

    if transaction.amount > MIN_WITHDRAW_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Minimum withdrawal amount is ₦{MIN_WITHDRAW_AMOUNT}"
        )
        
        
    if transaction.amount > account.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
        

    withdrawals_today = account_service.get_withdrawal_count_today(account.id, date.today())

    if withdrawals_today >= MAX_DAILY_WITHDRAWALS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily withdrawal limit reached (3 per day)"
        )

    return account_service.withdraw_fund(transaction, account.id)
    
  