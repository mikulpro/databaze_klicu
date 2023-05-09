import React, { useState, useEffect } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import logo from './logo.svg';
import './App.css';
import Navbar from './components/navbar/components/Navbar';



const theme = createTheme();


const App: React.FC = () => {
    const [workplaces, setWorkplaces] = useState<Array<{ id: number; faculty_id: number; abbreviation: string; name: string }>>([]);

    useEffect(() => {
        fetch("http://localhost:8001/workplaces/")
            .then(response => response.json())
            .then((workplaces_list: Array<{ id: number; faculty_id: number; abbreviation: string; name: string }>) => {
                setWorkplaces(workplaces_list);
            });
    }, []);

    if (!workplaces) {
        return <h2>Loading...</h2>
    }

    const workplaces_list: JSX.Element[] = workplaces.map((workplace: {id: number; faculty_id: number; abbreviation: string; name: string }, i: number) => (
        <li key={workplace.id}>{workplace.abbreviation}</li>))

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <div className="App">
                <Navbar/>
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
        </ThemeProvider>
    );
};

export default App;


// import React, { Component } from 'react';
// import { createTheme, ThemeProvider } from '@mui/material/styles';
// import CssBaseline from '@mui/material/CssBaseline';
// import logo from './logo.svg';
// import './App.css';
// import Header from "./Header";
//
// interface IProps {
// }
//
// interface IState {
//   workplaces: Array<{ id: number; faculty_id: number; abbreviation: string; name: string }>;
// }
//
// const sections = [
//   { title: 'Technology', url: '#' },
//   { title: 'Design', url: '#' },
//   { title: 'Culture', url: '#' },
//   { title: 'Business', url: '#' },
//   { title: 'Politics', url: '#' },
//   { title: 'Opinion', url: '#' },
//   { title: 'Science', url: '#' },
//   { title: 'Health', url: '#' },
//   { title: 'Style', url: '#' },
//   { title: 'Travel', url: '#' },
// ];
//
// const theme = createTheme();
//
// // React.Component<PropType, StateType>
// class App extends Component<IProps, IState> {
//
//     constructor(props:IProps) {
//         super(props);
//         this.state = {
//             workplaces: []
//         };
//     }
//
//     componentDidMount() {
//          fetch("http://localhost:8001/workplaces/")
//           .then(response => response.json())
//           .then((workplaces_list: Array<{ id: number; faculty_id: number; abbreviation: string; name: string }>) => {
//             this.setState({
//               workplaces: workplaces_list
//             });
//           });
//     }
//
//     render() {
//         if (!this.state.workplaces) {
//             return <h2>Loading...</h2>
//         }
//         const workplaces_list: JSX.Element[] = this.state.workplaces.map((workplace: {id: number; faculty_id: number; abbreviation: string; name: string }, i: number) => (
//             <li key={workplace.id}>{workplace.abbreviation}</li>))
//         return (
//             <ThemeProvider theme={theme}>
//                 <CssBaseline />
//             <div className="App">
//                 <Header sections={sections} title='Aplikace pro správu klíčů CPTO'/>
//               <header className="App-header">
//                 <h1>Seznam pracovišť</h1>
//                   <ul>
//                       {workplaces_list}
//                   </ul>
//                 <img src={logo} className="App-logo" alt="logo" />
//                 <p>
//                   Edit <code>src/App.tsx</code> and save to reload.
//                 </p>
//                 <a
//                   className="App-link"
//                   href="https://reactjs.org"
//                   target="_blank"
//                   rel="noopener noreferrer"
//                 >
//                   Learn React
//                 </a>
//               </header>
//             </div>
//             </ThemeProvider>
//           );
//     }
// }
//
// export default App;
