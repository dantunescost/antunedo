import React from 'react';
import './App.css';
import { NavBar } from './components/NavBar';
import { OffersTable } from './components/OffersTable';

class App extends React.Component{
  render() {
    return (
      <div>
        <NavBar></NavBar>
        <OffersTable />
      </div>
    );
  }
}

export default App;
