import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Results.css';
import Candidate from './Candidate';

const Results = ({ results }) => {
  const itemsPerPage = 4; // Number of movie cards per page
  const [currentPage, setCurrentPage] = useState(1);

  // Calculate the range of movies to display on the current page
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const moviesToDisplay = results.slice(startIndex, endIndex);

  const totalPages = Math.ceil(results.length / itemsPerPage);

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  return (
    <div className='main-container'>
    <div className="results-container">
      {moviesToDisplay.map((movie, index) => (
   
        <div key={index} className="movie-container">
          <Candidate infos={movie} />
        </div>
      ))}
      
    </div>
    <div className="pagination">
        {Array.from({ length: totalPages }).map((_, index) => (
          <button
            key={index}
            onClick={() => handlePageChange(index + 1)}
            className={currentPage === index + 1 ? 'active' : ''}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Results;
