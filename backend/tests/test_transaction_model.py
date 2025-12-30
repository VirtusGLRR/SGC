from models.transaction import Transaction
from models.item import Item
from tests.conftest import db_session
from datetime import datetime

def test_insert_transaction(db_session):
    item = Item(
        name="Açúcar",
        measure_unity="g",
        amount=1000,
        description="Açúcar refinado"
    )
    db_session.add(item)
    db_session.commit()

    transaction = Transaction(
        item_id=item.id,
        order_type="compra",
        description="Compra de açúcar",
        amount=500,
        price=10.50
    )

    db_session.add(transaction)
    db_session.commit()

    assert transaction.id is not None
    
    filtered_transaction = db_session.query(Transaction).filter_by(description="Compra de açúcar").first()
    assert filtered_transaction.description == transaction.description
    assert filtered_transaction.item_id == item.id

def test_transaction_item_relationship(db_session):
    item = Item(
        name="Farinha",
        measure_unity="g",
        amount=2000,
        description="Farinha de trigo"
    )
    db_session.add(item)
    db_session.commit()

    transaction = Transaction(
        item_id=item.id,
        order_type="venda",
        description="Venda de farinha",
        amount=250,
        price=5.00
    )
    db_session.add(transaction)
    db_session.commit()

    filtered_transaction = db_session.query(Transaction).filter_by(id=transaction.id).first()
    assert filtered_transaction.item is not None
    assert filtered_transaction.item.name == "Farinha"
    assert filtered_transaction.item.id == item.id

def test_transaction_without_price(db_session):
    item = Item(
        name="Leite",
        measure_unity="ml",
        amount=1000,
        description="Leite integral"
    )
    db_session.add(item)
    db_session.commit()

    transaction = Transaction(
        item_id=item.id,
        order_type="ajuste",
        description="Ajuste de estoque",
        amount=100
    )

    db_session.add(transaction)
    db_session.commit()

    assert transaction.id is not None
    assert transaction.price is None
    
    filtered_transaction = db_session.query(Transaction).filter_by(id=transaction.id).first()
    assert filtered_transaction.price is None

def test_multiple_transactions_same_item(db_session):
    item = Item(
        name="Café",
        measure_unity="g",
        amount=500,
        description="Café em grãos"
    )
    db_session.add(item)
    db_session.commit()

    transaction1 = Transaction(
        item_id=item.id,
        order_type="compra",
        description="Primeira compra de café",
        amount=200,
        price=15.00
    )
    
    transaction2 = Transaction(
        item_id=item.id,
        order_type="venda",
        description="Primeira venda de café",
        amount=50,
        price=20.00
    )

    db_session.add_all([transaction1, transaction2])
    db_session.commit()

    transactions = db_session.query(Transaction).filter_by(item_id=item.id).all()
    assert len(transactions) == 2
    
    order_types = [t.order_type for t in transactions]
    assert "compra" in order_types
    assert "venda" in order_types