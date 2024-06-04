import React from 'react';
import StarRateIcon from '@mui/icons-material/StarRate';
import TimelapseIcon from '@mui/icons-material/Timelapse';
import NestCamWiredStandIcon from '@mui/icons-material/NestCamWiredStand';
import './Candidate.css';

const capitalizeFirstLetter = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

const Candidate = ({ infos }) => {
  console.log("infos",infos)
  return (
    <div className="container">
    <h1>Candidate Information</h1>
    <div className="user-details">
      <p><strong>User ID:</strong> {infos.userId}</p>
      <p><strong>Name:</strong> {infos.name}</p>
      <p><strong>Email:</strong> {infos.email}</p>
      <p><strong>Full Time Avaiblity:</strong> {infos.fullTime ? 'Yes' : 'No'}</p>
      <p><strong>Part Time Avaiblity:</strong> {infos.partTime ? 'Yes' : 'No'}</p>
      <p><strong>Part Time Salary Expectation:</strong> ${infos.partTimeSalary}</p>
      <p><strong>Full Time Salary Expectation:</strong> ${infos.fullTimeSalary}</p>
      <p><strong>Skills:</strong></p>
      <ul>
        {infos.skills.map(skill => (
          <li key={skill}>{capitalizeFirstLetter(skill)}</li>
        ))}
      </ul>
      <p><strong>Companies:</strong></p>
      <ul>
        {infos.companies.map(company => (
          <li key={company}>{capitalizeFirstLetter(company)}</li>
        ))}
      </ul>
    </div>
  </div>
  );
}

export default Candidate;
