import React, { useState, useEffect } from 'react';
import { getFAQs } from '../services/api';

const FAQList = () => {
    const [faqs, setFaqs] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchFAQs = async () => {
            try {
                const data = await getFAQs();
                setFaqs(data);
            } catch (err) {
                setError('Failed to load FAQs. Please try again later.');
                console.error(err);
            }
        };

        fetchFAQs();
    }, []);

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="faq-list">
            <h2>Frequently Asked Questions</h2>
            {faqs.length > 0 ? (
                <ul>
                    {faqs.map(faq => (
                        <li key={faq.id}>
                            <h3 className="faq-question">{faq.question}</h3>
                            <p className="faq-answer">{faq.answer}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Loading FAQs...</p>
            )}
        </div>
    );
};

export default FAQList;
