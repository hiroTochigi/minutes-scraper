import logo from './logo.svg';
import './App.css';
import {data} from './street.js'
import TreeMap from "react-d3-treemap";
// Include its styles in you build process as well
import "react-d3-treemap/dist/react.d3.treemap.css";

 

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <TreeMap
      id="myTreeMap"
      height={1800}
      width={1200}
      data={data}
      valueUnit={"Times"}
      />
      </header>
    </div>
  );
}

export default App;
