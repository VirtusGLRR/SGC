import api from '../../../config/api';

/**
 * Chatbot API Service
 * Mapeamento completo das rotas do backend para o chatbot
 */

export const chatbotApi = {
  /**
   * POST /bot/message
   * Envia uma mensagem para o chatbot e recebe uma resposta
   */
  sendMessage: async (messageData) => {
    const response = await api.post('/bot/message', messageData);
    return response.data;
  },

  /**
   * GET /bot/history
   * Retorna o histórico de conversas do chatbot
   */
  getChatHistory: async () => {
    const response = await api.get('/bot/history');
    return response.data;
  }
};

