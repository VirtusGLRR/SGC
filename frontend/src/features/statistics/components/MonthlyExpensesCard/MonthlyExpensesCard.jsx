import PropTypes from 'prop-types';
import { useEffect } from 'react';
import { CreditCard, TrendingUp, TrendingDown } from 'lucide-react';
import './MonthlyExpensesCard.css';

/**
 * Card mostrando gastos do mês atual com comparação com mês anterior
 */
export const MonthlyExpensesCard = ({ monthlyData = [], loading = false, onLoad }) => {
  useEffect(() => {
    if (onLoad) {
      onLoad();
    }
  }, [onLoad]);

  // Pegar o mês atual (último na lista)
  const currentMonth = monthlyData[monthlyData.length - 1];
  const previousMonth = monthlyData[monthlyData.length - 2];

  if (loading) {
    return (
      <div className="monthly-expenses-card">
        <div className="monthly-expenses-card__header">
          <span className="monthly-expenses-card__icon">
            <CreditCard size={24} />
          </span>
          <h3 className="monthly-expenses-card__title">Gastos do Mês</h3>
        </div>
        <div className="monthly-expenses-card__loading">Carregando...</div>
      </div>
    );
  }

  if (!currentMonth) {
    return (
      <div className="monthly-expenses-card">
        <div className="monthly-expenses-card__header">
          <span className="monthly-expenses-card__icon">
            <CreditCard size={24} />
          </span>
          <h3 className="monthly-expenses-card__title">Gastos do Mês</h3>
        </div>
        <div className="monthly-expenses-card__empty">Sem dados disponíveis</div>
      </div>
    );
  }

  const currentValue = currentMonth.total_spent || 0;
  const difference = currentMonth.difference_from_previous || 0;
  const percentage = currentMonth.percentage_change || 0;

  const isIncrease = difference > 0;
  const monthName = getMonthName(currentMonth.month);

  return (
    <div className="monthly-expenses-card">
      <div className="monthly-expenses-card__header">
        <span className="monthly-expenses-card__icon">
          <CreditCard size={24} />
        </span>
        <h3 className="monthly-expenses-card__title">Gastos de {monthName}</h3>
      </div>

      <div className="monthly-expenses-card__value">
        R$ {currentValue.toFixed(2)}
      </div>

      {previousMonth && (
        <div className={`monthly-expenses-card__comparison ${isIncrease ? 'increase' : 'decrease'}`}>
          <span className="monthly-expenses-card__arrow">
            {isIncrease ? <TrendingUp size={18} /> : <TrendingDown size={18} />}
          </span>
          <span className="monthly-expenses-card__percentage">
            {Math.abs(percentage).toFixed(1)}%
          </span>
          <span className="monthly-expenses-card__text">
            {isIncrease ? 'mais que' : 'menos que'} {getMonthName(previousMonth.month)}
          </span>
        </div>
      )}

      <div className="monthly-expenses-card__details">
        <div className="monthly-expenses-card__detail">
          <span className="monthly-expenses-card__detail-label">Transações:</span>
          <span className="monthly-expenses-card__detail-value">
            {currentMonth.transaction_count}
          </span>
        </div>
        {previousMonth && (
          <div className="monthly-expenses-card__detail">
            <span className="monthly-expenses-card__detail-label">{getMonthName(previousMonth.month)}:</span>
            <span className="monthly-expenses-card__detail-value">
              R$ {(previousMonth.total_spent || 0).toFixed(2)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

function getMonthName(month) {
  const months = [
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
  ];
  return months[month - 1] || month;
}

MonthlyExpensesCard.propTypes = {
  monthlyData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      month: PropTypes.number,
      month_label: PropTypes.string,
      transaction_count: PropTypes.number,
      total_spent: PropTypes.number,
      difference_from_previous: PropTypes.number,
      percentage_change: PropTypes.number,
    })
  ),
  loading: PropTypes.bool,
  onLoad: PropTypes.func,
};

