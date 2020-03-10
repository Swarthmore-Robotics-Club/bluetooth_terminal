import React, {Component} from 'react';
import { Link } from "react-router-dom"
// import logo from './logo.svg';
import './App.css';
// Nav Drawer
import './components/MiniDrawer'
import MiniDrawer from './components/MiniDrawer';
import BluetoothSearchingIcon from '@material-ui/icons/BluetoothSearching';
import WebAssetIcon from '@material-ui/icons/WebAsset';
import TimelineIcon from '@material-ui/icons/Timeline';
// Bluetooth Device List 
import Divider from '@material-ui/core/Divider';
// Terminal window
import Terminal from './components/Terminal'



class App extends Component{
  constructor(props)
  {
    super(props);

    this.state = 
    {
      data: []
    };

  }

    render()
    {
      return (
        <div className="App">
          {/* <header className="App-header">
          
            <Link className="App-link" to="/about">Link to the About Page</Link>
          </header> */}

          
          <MiniDrawer props ={ {'components' : 
          [
            {'name':'Search Devices', 'icon' : BluetoothSearchingIcon, 'func':'undefined'},
           { 'name': 'Terminal', 'icon' : WebAssetIcon, 'func':'undefined'},
            {'name': 'Visualize', 'icon' : TimelineIcon, 'func':'undefined'}]
          
          }}/>

          <Terminal/>


        </div>
      )

    }
  }


export default App;
