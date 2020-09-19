import React from "react";
import styled from "styled-components";

const Component = styled.div``;

const Signup = () => {
  return (
    <form>
      <h1>Signup</h1>
      <Component><input type="text" name="email" placeholder="Email" /></Component>
      <Component><input type="password" name="password" placeholder="Password" /></Component>
      <Component><input type="password" name="confirmpassword" placeholder="Confirm Password" /></Component>
      <input type="submit" value="Submit" />
    </form>
  );
};

export default Signup;
