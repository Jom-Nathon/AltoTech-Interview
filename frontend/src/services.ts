// frontend/src/services/chatService.ts
const API_URL = 'http://localhost:8000';

export const chatService = {
  // async postView() {
  //   const response = await axios.post(`http://localhost:8000/chat/`);
  //   return response.data;
  // },
  async sendMessage(message: string) {
    try {
      const response = await fetch(`${API_URL}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ message: message })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }
};