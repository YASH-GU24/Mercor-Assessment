// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route,Navigate } from 'react-router-dom';
import './App.css';
import ParentComponent from './ParentComponent';
function App() {


  return (
    <Router>
      <div className="App">
        {/* Render the Navbar only if not on the Login or Signup route */}
     
   
        <div className="content">
          <Routes>
            <Route path="/chat" element={<ParentComponent />} />
            <Route path="/"  element={<ParentComponent />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
