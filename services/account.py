from datetime import datetime, time, date
from decimal import Decimal
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.account import AccountCreatePayload, AccountCreate, Account
from database import accounts_collection, transactions_collection
from schemas.transaction import DepositTransactionPayload, WithdrawTransactionPayload
from schemas.user import User
from serializers import account_serializer
from bson.objectid import ObjectId
from datetime import datetime, time, timedelta
import pytz 


class AccountService:

    @staticmethod
    def create_account(account_data: AccountCreatePayload, user: User) -> Account:
        account_data = account_data.model_dump()
        account_with_defaults = Account(
            **account_data,
            user_id=user.id,
            balance=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        account_id = accounts_collection.insert_one(jsonable_encoder(account_with_defaults)).inserted_id
        account = accounts_collection.find_one({"_id": account_id})
        return account_serializer(account)


    @staticmethod
    def get_account(user: User):
        account = accounts_collection.find_one({"user_id": user.id})
        return account_serializer(account)
    

    @staticmethod
    def get_account_by_id(account_id: str):
        account = accounts_collection.find_one({"_id": ObjectId(account_id)})
        return account_serializer(account)



    @staticmethod
    def deposit_fund(deposit_payload: DepositTransactionPayload, account_id):
        acc = AccountService.get_account_by_id(account_id)
        if not acc:
            return None
        
        old_balance = float(acc.balance)
        new_balance = old_balance + float(deposit_payload.amount)
        acc.balance = new_balance
        accounts_collection.find_one_and_update(
            {"_id": ObjectId(acc.id)},
            {"$set": {"balance": new_balance}}
        )
        return "success"
    
    
    
    
    @staticmethod
    def withdraw_fund(wihdraw_payload: WithdrawTransactionPayload, account_id):
        acc = AccountService.get_account_by_id(account_id)
        if not acc:
            return None
        
        old_balance = float(acc.balance)
        withdraw_balance = float(wihdraw_payload.amount)
        new_balance = old_balance - withdraw_balance
        accounts_collection.find_one_and_update(
            {"_id": ObjectId(acc.id)},
            {"$set": {"balance": new_balance}}
        )
        
        transactions_collection.insert_one({
            "account_id": account_id,
            "amount": float(wihdraw_payload.amount),
            "transaction_type": "debit", 
            "date": datetime.utcnow()
        })
       
        return "success"
    
    
    @staticmethod
    def get_withdrawal_count_today(account_id: str, day: date):
        
        timezone = pytz.timezone("UTC")  # or your local timezone
        day = timezone.localize(datetime.combine(day, time.min))  # Localize the start of the day to UTC

        # Set the end of the day to 23:59:59.999999
        end_of_day = timezone.localize(datetime.combine(day, time.max))  # Localize the end of the day

        # Debugging logs
        # print(f"Checking withdrawals for {account_id} on {day}")
        # print(f"Start of day: {day}, End of day: {end_of_day}")

        
        count = transactions_collection.count_documents({
            "account_id": account_id,
            "transaction_type": "debit",  
            "date": {
                "$gte": day,          
                "$lte": end_of_day   
            }
        })

        # print(f"Found {count} withdrawals for the day.")
        return count


account_service = AccountService()
