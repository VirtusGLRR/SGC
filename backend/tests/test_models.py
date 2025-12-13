from models.receita import Receita
from models.item import Item
from models.receita_item import ReceitaItem
from tests.conftest import db_session 

def test_insert_item(db_session):
    
    farinha = Item(
        name="Farinha",
        measure_unity="g",
        amount=1000,
        description="Farinha de trigo"
    )

    db_session.add(farinha)
    db_session.commit()

    assert farinha.id is not None
    
    item = db_session.query(Item).filter_by(name="Farinha").first()
    assert item.name == farinha.name

def test_insert_receita(db_session):

    receita = Receita(
        title="Bolo simples",
        steps="Misture tudo e asse",
        description="Bolo básico"
    )

    db_session.add(receita)
    db_session.commit()

    assert receita.id is not None

    objeto = db_session.query(Receita).filter_by(title="Bolo simples").first()
    assert objeto.title == receita.title