import React from 'react';
import './App.css';
//import { NavBar } from './components/NavBar';
import { Login } from './components/Login.js';
//import { OffersTable } from './components/OffersTable';

class App extends React.Component{
  render() {
    return (
      <div>
        <Login />
      </div>
    );
  }
}

export default App;
