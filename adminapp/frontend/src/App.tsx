import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

interface IProps {
}

interface IState {
  workplaces: Array<{ id: number; faculty_id: number; abbreviation: string; name: string }>;
}

class App extends Component<IProps, IState> {

    constructor(props:IProps) {
        super(props);
        this.state = {
            workplaces: []
        };
    }

    componentDidMount() {
         fetch("http://localhost:8001/workplaces/")
          .then(response => response.json())
          .then((workplaces_list: Array<{ id: number; faculty_id: number; abbreviation: string; name: string }>) => {
            this.setState({
              workplaces: workplaces_list
            });
          });
    }

    render() {
        if (!this.state.workplaces) {
            return <h2>Loading...</h2>
        }
        const workplaces_list: JSX.Element[] = this.state.workplaces.map((workplace: {id: number; faculty_id: number; abbreviation: string; name: string }, i: number) => (
            <li key={workplace.id}>{workplace.abbreviation}</li>))
        return (
            <div className="App">
              <header className="App-header">
                <h1>Seznam pracovišť</h1>
                  <ul>
                      {workplaces_list}
                  </ul>
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                  Edit <code>src/App.tsx</code> and save to reload.
                </p>
                <a
                  className="App-link"
                  href="https://reactjs.org"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Learn React
                </a>
              </header>
            </div>
          );
    }
}

export default App;
