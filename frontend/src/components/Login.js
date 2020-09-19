import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const Component = styled.div``;

const Login = () => {
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    if (!email || !password) {
      // use regex to make sure password and email are correct format
      setError("Please fill out all fields");
    }
    setError("");
    console.log(email, password);
    axios
      .post("/login", {
        email,
        password,
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <form onSubmit={(e) => handleLogin(e)}>
      <h1>Login</h1>
      <div style={{ color: "red" }}>{error}</div>
      <Component>
        <input
          type="text"
          name="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />
      </Component>
      <Component>
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
      </Component>
      <input type="submit" value="Submit" />
    </form>
  );
};

export default Login;
