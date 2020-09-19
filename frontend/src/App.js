import React from "react";
import Login from "./components/Login";
import Signup from "./components/Signup"

import Request from "./components/Request"
import "./App.css";

function App() {

  return (
    <div className="App">
      <Login />
      <Signup />
      <Request />
    </div>
  );
}

export default App;
