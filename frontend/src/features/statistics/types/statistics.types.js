/**
 * @typedef {Object} Transaction
 * @property {number} id - ID da transação
 * @property {number} item_id - ID do item relacionado
 * @property {string} item_name - Nome do item
 * @property {string} type - Tipo da transação ('entrada' ou 'saida')
 * @property {number} quantity - Quantidade transacionada
 * @property {number} price - Preço unitário
 * @property {number} total_value - Valor total (quantity * price)
 * @property {string} date - Data da transação (ISO string)
 * @property {string} [description] - Descrição opcional
 * @property {string} created_at - Data de criação
 * @property {string} updated_at - Data de atualização
 */

/**
 * @typedef {Object} TransactionSummary
 * @property {number} total_transactions - Total de transações no período
 * @property {number} total_entradas - Total de entradas
 * @property {number} total_saidas - Total de saídas
 * @property {number} valor_total_entradas - Valor total de entradas
 * @property {number} valor_total_saidas - Valor total de saídas
 * @property {number} saldo_periodo - Saldo do período (entradas - saídas)
 * @property {number} valor_medio_transacao - Valor médio por transação
 * @property {number} items_distintos - Quantidade de itens diferentes
 */

/**
 * @typedef {Object} DailyTransaction
 * @property {string} date - Data (formato: YYYY-MM-DD)
 * @property {number} entrada - Quantidade de entradas
 * @property {number} saida - Quantidade de saídas
 * @property {number} total - Total de transações do dia
 * @property {number} valor_entrada - Valor total de entradas
 * @property {number} valor_saida - Valor total de saídas
 */

/**
 * @typedef {Object} MostTransactedItem
 * @property {number} item_id - ID do item
 * @property {string} item_name - Nome do item
 * @property {number} total_quantity - Quantidade total transacionada
 * @property {number} total_entradas - Total de entradas
 * @property {number} total_saidas - Total de saídas
 * @property {number} total_transactions - Número de transações
 * @property {number} valor_total - Valor total movimentado
 */

/**
 * @typedef {Object} ConsumptionRate
 * @property {number} item_id - ID do item
 * @property {string} item_name - Nome do item
 * @property {number} total_consumido - Total consumido no período
 * @property {number} taxa_diaria - Taxa média de consumo por dia
 * @property {number} estoque_atual - Estoque atual do item
 * @property {number|null} dias_para_esgotamento - Dias estimados até esgotar (null se não for esgotar)
 * @property {string} status - Status: 'critico', 'alerta', 'normal'
 */

/**
 * @typedef {Object} PriceAnalysis
 * @property {number} item_id - ID do item
 * @property {string} item_name - Nome do item
 * @property {number} preco_medio - Preço médio das transações
 * @property {number} preco_minimo - Menor preço registrado
 * @property {number} preco_maximo - Maior preço registrado
 * @property {number} variacao_percentual - Variação percentual (max-min)/min
 * @property {number} total_transacoes - Total de transações do item
 * @property {string} tendencia - Tendência: 'alta', 'baixa', 'estavel'
 */

/**
 * @typedef {Object} DashboardData
 * @property {InventorySummary} inventory - Resumo do inventário
 * @property {TransactionSummary} transactions_30d - Transações dos últimos 30 dias
 * @property {number} low_stock_count - Quantidade de itens com estoque baixo
 * @property {number} expiring_soon_count - Quantidade de itens próximos ao vencimento
 * @property {number} feasible_recipes_count - Quantidade de receitas possíveis
 */

/**
 * @typedef {Object} InventorySummary
 * @property {number} total_items - Total de itens cadastrados
 * @property {number} total_quantity - Quantidade total em estoque
 * @property {number} total_value - Valor total do inventário
 * @property {number} average_price - Preço médio dos itens
 * @property {number} items_low_stock - Itens com estoque baixo
 */

/**
 * @typedef {Object} TransactionRequest
 * @property {number} item_id - ID do item
 * @property {string} type - Tipo: 'entrada' ou 'saida'
 * @property {number} quantity - Quantidade
 * @property {number} price - Preço unitário
 * @property {string} [date] - Data da transação (ISO string, opcional)
 * @property {string} [description] - Descrição (opcional)
 */

/**
 * @typedef {Object} StatisticsState
 * @property {TransactionSummary|null} summary - Resumo de transações
 * @property {DailyTransaction[]} dailyTransactions - Transações diárias
 * @property {MostTransactedItem[]} mostTransacted - Itens mais transacionados
 * @property {ConsumptionRate[]} consumptionRate - Taxa de consumo
 * @property {PriceAnalysis[]} priceAnalysis - Análise de preços
 * @property {DashboardData|null} dashboardData - Dados do dashboard
 * @property {Transaction[]} recentTransactions - Transações recentes
 * @property {boolean} loading - Estado de carregamento
 * @property {string|null} error - Mensagem de erro
 */

/**
 * @typedef {Object} PeriodOption
 * @property {number} value - Valor em dias
 * @property {string} label - Label para exibição
 * @property {string} key - Chave única
 */

export const PERIOD_OPTIONS = [
  { value: 7, label: '7 dias', key: '7d' },
  { value: 30, label: '30 dias', key: '30d' },
  { value: 90, label: '90 dias', key: '90d' },
  { value: 180, label: '6 meses', key: '180d' },
  { value: 365, label: '1 ano', key: '365d' }
];

export const TRANSACTION_TYPES = {
  ENTRADA: 'entrada',
  SAIDA: 'saida',
  ALL: 'all'
};

export const CONSUMPTION_STATUS = {
  CRITICO: 'critico',    // < 7 dias
  ALERTA: 'alerta',      // 7-14 dias
  NORMAL: 'normal'       // > 14 dias ou sem previsão
};

export const CHART_COLORS = {
  primary: '#2196f3',      // Azul principal
  success: '#4caf50',      // Verde (entradas)
  danger: '#f44336',       // Vermelho (saídas)
  warning: '#ff9800',      // Laranja (alertas)
  info: '#00bcd4',         // Ciano (informações)
  purple: '#9c27b0',       // Roxo
  teal: '#009688',         // Teal
  gray: '#9e9e9e',         // Cinza
};

export const CATEGORY_COLORS = [
  '#2196f3', '#4caf50', '#ff9800', '#9c27b0',
  '#00bcd4', '#f44336', '#009688', '#ff5722'
];

