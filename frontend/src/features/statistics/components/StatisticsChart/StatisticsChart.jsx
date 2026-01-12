import PropTypes from 'prop-types';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { BarChart3 } from 'lucide-react';
import { CHART_COLORS } from '../../types/statistics.types';
import './StatisticsChart.css';

/**
 * Componente genérico de gráfico usando Recharts
 * @param {Object} props
 * @param {Array} props.data - Dados para o gráfico
 * @param {string} props.type - Tipo: 'line', 'bar', 'area', 'pie'
 * @param {string} props.title - Título do gráfico
 * @param {Array} props.dataKeys - Array de objetos {key, color, name}
 * @param {number} props.height - Altura do gráfico (padrão: 300)
 * @param {boolean} props.loading - Estado de carregamento
 * @param {string} props.xAxisKey - Chave para o eixo X (padrão: 'date')
 */
export const StatisticsChart = ({
  data = [],
  type = 'line',
  title,
  dataKeys = [],
  height = 300,
  loading = false,
  xAxisKey = 'date',
}) => {
  if (loading) {
    return (
      <div className="statistics-chart statistics-chart--loading">
        <h3 className="statistics-chart__title">{title}</h3>
        <div className="statistics-chart__skeleton">
          <div className="statistics-chart__skeleton-line"></div>
          <div className="statistics-chart__skeleton-line"></div>
          <div className="statistics-chart__skeleton-line"></div>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="statistics-chart statistics-chart--empty">
        <h3 className="statistics-chart__title">{title}</h3>
        <div className="statistics-chart__empty-state">
          <span className="statistics-chart__empty-icon">
            <BarChart3 size={48} />
          </span>
          <p className="statistics-chart__empty-text">Nenhum dado disponível</p>
        </div>
      </div>
    );
  }

  /**
   * Tooltip customizado para gráficos de quantidade
   */
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const value = payload[0].value;
      let formattedValue = value;

      // Formatar com unidades
      if (value >= 1000) {
        formattedValue = `${(value / 1000).toFixed(1)} kg`;
      } else if (value >= 10) {
        formattedValue = `${value.toFixed(1)} un`;
      } else {
        formattedValue = `${value.toFixed(2)} un`;
      }

      return (
        <div style={{
          backgroundColor: 'white',
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '10px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
        }}>
          <p style={{ margin: 0, fontWeight: 600, marginBottom: '5px' }}>{label}</p>
          <p style={{ margin: 0, color: payload[0].color }}>
            Quantidade: <strong>{formattedValue}</strong>
          </p>
        </div>
      );
    }
    return null;
  };

  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 5, right: 30, left: 20, bottom: 5 },
    };

    switch (type) {
      case 'line':
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey={xAxisKey} stroke="#999" fontSize={12} />
            <YAxis stroke="#999" fontSize={12} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '8px',
              }}
            />
            <Legend />
            {dataKeys.map((item) => (
              <Line
                key={item.key}
                type="monotone"
                dataKey={item.key}
                stroke={item.color || CHART_COLORS.primary}
                strokeWidth={2}
                name={item.name || item.key}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            ))}
          </LineChart>
        );

      case 'bar':
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey={xAxisKey} stroke="#999" fontSize={12} />
            <YAxis stroke="#999" fontSize={12} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            {dataKeys.map((item) => (
              <Bar
                key={item.key}
                dataKey={item.key}
                fill={item.color || CHART_COLORS.primary}
                name={item.name || item.key}
                radius={[4, 4, 0, 0]}
              />
            ))}
          </BarChart>
        );

      case 'area':
        return (
          <AreaChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey={xAxisKey} stroke="#999" fontSize={12} />
            <YAxis stroke="#999" fontSize={12} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '8px',
              }}
            />
            <Legend />
            {dataKeys.map((item) => (
              <Area
                key={item.key}
                type="monotone"
                dataKey={item.key}
                stroke={item.color || CHART_COLORS.primary}
                fill={item.color || CHART_COLORS.primary}
                fillOpacity={0.3}
                name={item.name || item.key}
              />
            ))}
          </AreaChart>
        );

      case 'pie':
        return (
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey={dataKeys[0]?.key || 'value'}
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={dataKeys[index]?.color || CHART_COLORS.primary}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        );

      default:
        return <div>Tipo de gráfico não suportado</div>;
    }
  };

  return (
    <div className="statistics-chart">
      {title && <h3 className="statistics-chart__title">{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
};

StatisticsChart.propTypes = {
  data: PropTypes.array,
  type: PropTypes.oneOf(['line', 'bar', 'area', 'pie']),
  title: PropTypes.string,
  dataKeys: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      color: PropTypes.string,
      name: PropTypes.string,
    })
  ),
  height: PropTypes.number,
  loading: PropTypes.bool,
  xAxisKey: PropTypes.string,
};

