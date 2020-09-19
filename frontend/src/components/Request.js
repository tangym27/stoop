import React, {useState} from "react";
import styled from "styled-components";
import StyledInput from "./Input";

const Form = styled.form``;
const Container = styled.div``;

const GroceryList = styled.div`
  background-color: #969595;
  border: 1px solid black;
  color: white;
  font-weight: bold;
  font-size: 20px;
  border-radius: 5px;
  font-family: Georgia;
  text-transform: lowercase;
  transition: 0.2s filter;
`;

const GroceryItem = styled.div`
`;
const Component = styled.div``;

const Request = () => {
  const [items, setItems] = useState("");
  const [grocerys, setGrocerys] = useState([]);
  var currentVal="";
  function groceryList(e){
    e.preventDefault();
    setItems(e.target.value);
  }
  function addItem(e){
    e.preventDefault();
    grocerys.push(items);
    setGrocerys(grocerys);
    console.log(grocerys)
  }
  function handleSubmit(event){
    event.preventDefault();
    setGrocerys([...grocerys,items]);
    setItems("");
  }

  function removeItem(event){
    event.preventDefault();
    console.log(event.target.value);
    var filteredAry = grocerys.filter(function(e) { return e != event.target.value })
    setGrocerys(filteredAry);
  }

  return (
    <div>
    <Container>
    <Form>
      <h1>Request</h1>
      <Component><input type="Store" name="email" placeholder="Store" /></Component>

      {/*Grocery List*/}
      <form onSubmit={handleSubmit}>
        <input type ="text" value = {items} onChange = { event => { setItems(event.target.value);}}/>
        <button> add item </button>
      </form> {/* end of grocery list */}

      <Component><input type="PickUp By" name="pickup" placeholder="ie 3:00pm" /></Component>
      <input type="submit" value="Submit" />
    </Form>
    </Container>
    <GroceryList>
    {grocerys.map((grocery, i) => {
        return <GroceryItem> {grocery} <button onClick={removeItem} key={grocery} value={grocery}> remove </button> </GroceryItem>;
      })}
    </GroceryList>
    </div>
  );
};

export default Request;
