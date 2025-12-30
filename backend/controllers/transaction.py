from fastapi import Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models import Transaction
from repositories import TransactionRepository, ItemRepository
from schemas import TransactionResponse, TransactionRequest

class TransactionController:

    @staticmethod
    def create(request: TransactionRequest, db: Session = Depends(get_db)):
        default_validators(request, db)
        transaction = TransactionRepository.save(db, Transaction(**request.model_dump()))
        return TransactionResponse.model_validate(transaction)

    @staticmethod
    def find_all(db: Session = Depends(get_db)):
        transactions = TransactionRepository.find_all(db)
        return [TransactionResponse.model_validate(transaction) for transaction in transactions]

    @staticmethod
    def find_by_id(id: int, db: Session = Depends(get_db)):
        transaction = TransactionRepository.find_by_id(db, id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
            )
        return TransactionResponse.model_validate(transaction)

    @staticmethod
    def find_by_item_id(item_id: int, db: Session = Depends(get_db)):
        transactions = TransactionRepository.find_by_item_id(db, item_id)
        return [TransactionResponse.model_validate(transaction) for transaction in transactions]

    @staticmethod
    def delete_by_id(id: int, db: Session = Depends(get_db)):
        if not TransactionRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
            )
        TransactionRepository.delete_by_id(db, id)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, 
            content={"message": "Transação removida com sucesso", "id": id}
        )

    @staticmethod
    def update(id: int, request: TransactionRequest, db: Session = Depends(get_db)):
        default_validators(request, db)
        if not TransactionRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
            )

        transaction = TransactionRepository.save(db, Transaction(id=id, **request.model_dump()))
        return TransactionResponse.model_validate(transaction)


def default_validators(request: TransactionRequest, db: Session):
    if request.price and request.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O preço não pode ser negativo")
    if request.order_type == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.description == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A quantidade deve ser maior que zero")
    if not ItemRepository.exists_by_id(db, request.item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item não encontrado")
