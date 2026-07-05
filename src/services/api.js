// Using a base URL for the API endpoints
const API_URL = '/api';

/**
 * Fetches the list of FAQs from the backend.
 * Handles potential network errors or non-OK responses from the server.
 * @returns {Promise<Array<Object>>} A promise that resolves with the list of FAQs.
 */
export const getFAQs = async () => {
    try {
        const response = await fetch(`${API_URL}/faqs`);
        if (!response.ok) {
            throw new Error(`Failed to fetch FAQs. Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching FAQs:", error);
        throw error; // Re-throw to allow caller to handle it
    }
};

/**
 * Sends a user's query to the chatbot backend.
 * Handles potential network errors or non-OK responses from the server.
 * @param {string} query The user's question for the chatbot.
 * @returns {Promise<string>} A promise that resolves with the chatbot's string response.
 */
export const sendChatbotQuery = async (query) => {
    try {
        const response = await fetch(`${API_URL}/chatbot/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: query }),
        });
        if (!response.ok) {
            throw new Error(`Chatbot query failed. Status: ${response.status}`);
        }
        const data = await response.json();
        return data.answer; // Assuming the response is a JSON object with an 'answer' key
    } catch (error) {
        console.error("Error sending chatbot query:", error);
        throw error; // Re-throw to allow caller to handle it
    }
};
