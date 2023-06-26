// Import '../sass/index.sass';
import { createRoot } from 'react-dom/client';
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './components/App/App.tsx';

const container = document.getElementById('app');
const root = createRoot(container);
root.render(
    <Router>
        <App />
    </Router>
);
