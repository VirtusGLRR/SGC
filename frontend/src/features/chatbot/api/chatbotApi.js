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
   * POST /bot/image_message
   * Envia uma mensagem com imagem para o chatbot
   */
  sendImageMessage: async (messageData) => {
    const response = await api.post('/bot/image_message', messageData);
    return response.data;
  },

  /**
   * POST /bot/audio_message
   * Envia uma mensagem com áudio para o chatbot
   */
  sendAudioMessage: async (messageData) => {
    const response = await api.post('/bot/audio_message', messageData);
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

