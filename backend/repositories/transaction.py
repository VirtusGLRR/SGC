from sqlalchemy.orm import Session

from models import Transaction

class TransactionRepository:
    @staticmethod
    def find_all(db: Session) -> list[type[Transaction]]:
        """Recupera todas as transações do banco de dados."""
        return db.query(Transaction).all()

    @staticmethod
    def save(db: Session, transaction: Transaction) -> Transaction:
        """Salva ou atualiza uma transação no banco de dados."""
        if transaction.id:
            db.merge(transaction)
        else:
            db.add(transaction)
        db.commit()
        return transaction

    @staticmethod
    def find_by_id(db: Session, id: int) -> Transaction | None:
        """Recupera uma transação pelo seu ID."""
        return db.query(Transaction).filter(Transaction.id == id).first()

    @staticmethod
    def find_by_item_id(db: Session, item_id: int) -> list[type[Transaction]]:
        """Recupera transações pelo ID do item associado."""
        return db.query(Transaction).filter(Transaction.item_id == item_id).all()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        """Verifica se uma transação existe pelo seu ID."""
        return db.query(Transaction).filter(Transaction.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        """Remove uma transação pelo seu ID."""
        transaction = db.query(Transaction).filter(Transaction.id == id).first()
        if transaction is not None:
            db.delete(transaction)
            db.commit()

    @staticmethod
    def find_transaction_summary_by_period(
            db: Session,
            start_date: datetime = None,
            end_date: datetime = None
    ) -> dict:
        """Resumo de entradas e saídas por período"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        transactions = db.query(Transaction).filter(
            and_(
                Transaction.create_at >= start_date.date(),
                Transaction.create_at <= end_date.date()
            )
        ).all()

        total_entries = Decimal('0')
        total_exits = Decimal('0')
        value_entries = Decimal('0')
        value_exits = Decimal('0')
        count_entries = 0
        count_exits = 0

        for trans in transactions:
            if trans.order_type.lower() == 'entrada':
                total_entries += trans.amount
                value_entries += trans.amount * (trans.price or Decimal('0'))
                count_entries += 1
            elif trans.order_type.lower() == 'saida':
                total_exits += trans.amount
                value_exits += trans.amount * (trans.price or Decimal('0'))
                count_exits += 1

        return {
            "period": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            "entries": {
                "count": count_entries,
                "total_amount": float(total_entries),
                "total_value": float(value_entries)
            },
            "exits": {
                "count": count_exits,
                "total_amount": float(total_exits),
                "total_value": float(value_exits)
            },
            "balance": {
                "amount": float(total_entries - total_exits),
                "value": float(value_entries - value_exits)
            }
        }

    @staticmethod
    def find_most_transacted_items(
            db: Session,
            order_type: str = None,
            limit: int = 10
    ) -> list[dict]:
        """Retorna os itens com mais transações (entradas ou saídas)"""
        query = db.query(
            Item.id,
            Item.name,
            func.count(Transaction.id).label('transaction_count'),
            func.sum(Transaction.amount).label('total_amount'),
            func.sum(Transaction.amount * Transaction.price).label('total_value')
        ).join(
            Item, Transaction.item_id == Item.id
        )

        if order_type:
            query = query.filter(Transaction.order_type == order_type)

        results = query.group_by(
            Item.id, Item.name
        ).order_by(
            desc('transaction_count')
        ).limit(limit).all()

        return [
            {
                "item_id": r.id,
                "item_name": r.name,
                "transaction_count": r.transaction_count,
                "total_amount": float(r.total_amount or 0),
                "total_value": float(r.total_value or 0)
            }
            for r in results
        ]

    @staticmethod
    def find_daily_transactions(
            db: Session,
            days: int = 30
    ) -> list[dict]:
        """Retorna contagem de transações por dia"""
        start_date = datetime.now() - timedelta(days=days)

        results = db.query(
            func.date(Transaction.create_at).label('date'),
            Transaction.order_type,
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.amount).label('total_amount')
        ).filter(
            Transaction.create_at >= start_date.date()
        ).group_by(
            func.date(Transaction.create_at),
            Transaction.order_type
        ).order_by(
            func.date(Transaction.create_at)
        ).all()

        return [
            {
                "date": r.date.strftime("%Y-%m-%d"),
                "order_type": r.order_type,
                "count": r.count,
                "total_amount": float(r.total_amount)
            }
            for r in results
        ]

    @staticmethod
    def find_average_transaction_value_by_item(db: Session) -> list[dict]:
        """Retorna valor médio de transação por item"""
        results = db.query(
            Item.id,
            Item.name,
            func.avg(Transaction.price).label('avg_price'),
            func.min(Transaction.price).label('min_price'),
            func.max(Transaction.price).label('max_price'),
            func.count(Transaction.id).label('transaction_count')
        ).join(
            Item, Transaction.item_id == Item.id
        ).filter(
            Transaction.price.isnot(None)
        ).group_by(
            Item.id, Item.name
        ).all()

        return [
            {
                "item_id": r.id,
                "item_name": r.name,
                "avg_price": float(r.avg_price or 0),
                "min_price": float(r.min_price or 0),
                "max_price": float(r.max_price or 0),
                "transaction_count": r.transaction_count
            }
            for r in results
        ]

    @staticmethod
    def find_consumption_rate_by_item(
            db: Session,
            days: int = 30
    ) -> list[dict]:
        """Calcula taxa de consumo (saídas) por item nos últimos N dias"""
        start_date = datetime.now() - timedelta(days=days)

        results = db.query(
            Item.id,
            Item.name,
            Item.amount.label('current_stock'),
            func.sum(Transaction.amount).label('total_consumed')
        ).join(
            Transaction, Item.id == Transaction.item_id
        ).filter(
            and_(
                Transaction.order_type == 'saida',
                Transaction.create_at >= start_date.date()
            )
        ).group_by(
            Item.id, Item.name, Item.amount
        ).all()

        return [
            {
                "item_id": r.id,
                "item_name": r.name,
                "current_stock": float(r.current_stock),
                "total_consumed": float(r.total_consumed or 0),
                "daily_average": float((r.total_consumed or 0) / days),
                "days_until_stockout": (
                    int(r.current_stock / ((r.total_consumed or 0) / days))
                    if r.total_consumed and r.total_consumed > 0
                    else None
                )
            }
            for r in results
        ]
