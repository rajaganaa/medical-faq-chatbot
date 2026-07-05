import React, { useState } from 'react';
import { sendChatbotQuery } from '../services/api';

/**
 * A chatbot component for user interaction.
 * It includes an input field for questions, a display for responses,
 * and a disclaimer about not entering Personal Health Information (PHI).
 * Chat history is not persisted on the client-side.
 */
const Chatbot = () => {
    const [inputValue, setInputValue] = useState('');
    // The messages state will only last for the component's lifecycle and is not persisted.
    const [messages, setMessages] = useState([]);

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const query = inputValue.trim();
        if (!query) {
            return;
        }

        const userMessage = { sender: 'user', text: query };
        
        // Update messages to display user query immediately.
        setMessages(prevMessages => [...prevMessages, userMessage]);
        
        // Clear input field.
        setInputValue('');

        try {
            const response = await sendChatbotQuery(query);
            const botMessage = { sender: 'bot', text: response };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error("Failed to send chatbot query:", error);
            const errorMessage = { sender: 'bot', text: "Sorry, I\'m having trouble connecting. Please try again later." };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
            <div style={{ height: '400px', overflowY: 'auto', border: '1px solid #eee', padding: '1rem', marginBottom: '1rem' }}>
                {messages.length === 0 && <p>Ask me a question to start the conversation.</p>}
                {messages.map((message, index) => (
                    <div key={index} style={{ marginBottom: '0.5rem', textAlign: message.sender === 'user' ? 'right' : 'left' }}>
                        <span style={{ 
                            background: message.sender === 'user' ? '#007bff' : '#e9ecef', 
                            color: message.sender === 'user' ? 'white' : 'black',
                            padding: '0.5rem 1rem', 
                            borderRadius: '1rem' 
                        }}>
                            {message.text}
                        </span>
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} style={{ display: 'flex' }}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    placeholder="Type your question here..."
                    aria-label="Chatbot input"
                    style={{ flex: 1, padding: '0.5rem', border: '1px solid #ccc', borderRadius: '4px' }}
                />
                <button type="submit" style={{ marginLeft: '0.5rem', padding: '0.5rem 1rem', border: 'none', background: '#007bff', color: 'white', borderRadius: '4px' }}>Send</button>
            </form>
            <p style={{ marginTop: '1rem', color: '#dc3545', textAlign: 'center', fontWeight: 'bold' }}>
                Disclaimer: Please do not enter Personal Health Information (PHI).
            </p>
        </div>
    );
};

export default Chatbot;
