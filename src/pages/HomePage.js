import React from 'react';
import Chatbot from '../components/Chatbot';
import FAQList from '../components/FAQList';

const HomePage = () => {
  return (
    <div>
      <h1>Home Page</h1>
      <Chatbot />
      <FAQList />
    </div>
  );
};

export default HomePage;
