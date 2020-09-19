import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const Component = styled.div``;

const Signup = () => {
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [confirmpassword, setConfirmPassword] = useState(null);
  const [firstName, setFirstName] = useState(null);
  const [lastName, setLastName] = useState(null);
  const [error, setError] = useState("");

  const handleSignup = (e) => {
    e.preventDefault();
    if (!email || !password) {
      // use regex to make sure password and email are correct format
      setError("Please fill out all fields");
    } else if (password != confirmpassword) {
      setError("Passwords do not match");
    }
    setError("");

    axios
      .post("/signup", {
        email,
        password,
        firstName,
        lastName,
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <form onSubmit={(e) => handleSignup(e)}>
      <h1>Signup</h1>
      <div style={{ color: "red" }}>{error}</div>
      <Component>
        <input
          type="text"
          name="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </Component>
      <Component>
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </Component>
      <Component>
        <input
          type="password"
          name="confirmpassword"
          placeholder="Confirm Password"
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
      </Component>
      <Component>
        <input
          type="text"
          name="firstname"
          placeholder="First Name"
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
      </Component>
      <Component>
        <input
          type="text"
          name="lastname"
          placeholder="Last Name"
          onChange={(e) => setLastName(e.target.value)}
          required
        />
      </Component>
      <input type="submit" value="Submit" />
    </form>
  );
};

export default Signup;
