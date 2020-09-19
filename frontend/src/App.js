import React from "react";
import { Route, BrowserRouter as Router, Redirect } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";

import Request from "./components/Request";
import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { user: null };
  }

  addUser = (user) => {
    this.setState({ user });
  };

  render() {
    return (
      <div className="App">
        <Router>
          <Login path="/login" addUser={this.addUser} redirect={false} />
          <Signup path="/signup" addUser={this.addUser} />
          <Request path="/" />
        </Router>
      </div>
    );
  }
}

export default App;
