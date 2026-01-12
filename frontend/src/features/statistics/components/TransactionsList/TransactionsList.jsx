import PropTypes from 'prop-types';
import { ArrowDownCircle, ArrowUpCircle } from 'lucide-react';
import './TransactionsList.css';

/**
 * Lista de transações recentes
 * @param {Object} props
 * @param {Array} props.transactions - Lista de transações
 * @param {number} props.limit - Limite de transações (padrão: 10)
 * @param {Function} props.onViewDetails - Callback ao clicar em uma transação
 * @param {boolean} props.loading - Estado de carregamento
 */
export const TransactionsList = ({
  transactions = [],
  limit = 10,
  onViewDetails = null,
  loading = false,
}) => {
  const limitedTransactions = transactions.slice(0, limit);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Agora mesmo';
    if (diffMins < 60) return `${diffMins}min atrás`;
    if (diffHours < 24) return `${diffHours}h atrás`;
    if (diffDays < 7) return `${diffDays}d atrás`;

    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const getTypeIcon = (type) => {
    return type === 'entrada' ? <ArrowUpCircle size={20} /> : <ArrowDownCircle size={20} />;
  };

  const getTypeClass = (type) => {
    return type === 'entrada' ? 'entrada' : 'saida';
  };

  const getTypeLabel = (type) => {
    return type === 'entrada' ? 'Entrada' : 'Saída';
  };

  if (loading) {
    return (
      <div className="transactions-list">
        <h3 className="transactions-list__title">Transações Recentes</h3>
        <div className="transactions-list__loading">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="transactions-list__skeleton-item"></div>
          ))}
        </div>
      </div>
    );
  }

  if (limitedTransactions.length === 0) {
    return (
      <div className="transactions-list">
        <h3 className="transactions-list__title">Transações Recentes</h3>
        <div className="transactions-list__empty">
          <span className="transactions-list__empty-icon">📋</span>
          <p className="transactions-list__empty-text">Nenhuma transação encontrada</p>
        </div>
      </div>
    );
  }

  return (
    <div className="transactions-list">
      <h3 className="transactions-list__title">Transações Recentes</h3>

      <div className="transactions-list__items">
        {limitedTransactions.map((transaction) => (
          <div
            key={transaction.id}
            className={`transactions-list__item ${
              onViewDetails ? 'transactions-list__item--clickable' : ''
            }`}
            onClick={() => onViewDetails && onViewDetails(transaction)}
          >
            <div className="transactions-list__item-left">
              <span
                className={`transactions-list__type-icon transactions-list__type-icon--${getTypeClass(
                  transaction.type
                )}`}
              >
                {getTypeIcon(transaction.type)}
              </span>

              <div className="transactions-list__item-details">
                <span className="transactions-list__item-name">
                  {transaction.item_name}
                </span>
                <span className="transactions-list__item-meta">
                  <span
                    className={`transactions-list__badge transactions-list__badge--${getTypeClass(
                      transaction.type
                    )}`}
                  >
                    {getTypeLabel(transaction.type)}
                  </span>
                  <span className="transactions-list__item-date">
                    {formatDate(transaction.date || transaction.created_at)}
                  </span>
                </span>
              </div>
            </div>

            <div className="transactions-list__item-right">
              <div className="transactions-list__item-values">
                <span className="transactions-list__item-quantity">
                  {transaction.quantity || 0} un
                </span>
                <span
                  className={`transactions-list__item-value transactions-list__item-value--${getTypeClass(
                    transaction.type
                  )}`}
                >
                  {transaction.type === 'entrada' ? '+' : '-'}R${' '}
                  {transaction.total_value?.toFixed(2) ||
                    ((transaction.price || 0) * (transaction.quantity || 0)).toFixed(2)}
                </span>
              </div>
              {onViewDetails && (
                <span className="transactions-list__item-arrow">›</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

TransactionsList.propTypes = {
  transactions: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      item_name: PropTypes.string.isRequired,
      type: PropTypes.oneOf(['entrada', 'saida']).isRequired,
      quantity: PropTypes.number.isRequired,
      price: PropTypes.number.isRequired,
      total_value: PropTypes.number,
      date: PropTypes.string,
      created_at: PropTypes.string,
      description: PropTypes.string,
    })
  ),
  limit: PropTypes.number,
  onViewDetails: PropTypes.func,
  loading: PropTypes.bool,
};

