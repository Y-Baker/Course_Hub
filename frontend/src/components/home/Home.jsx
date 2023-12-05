import React from 'react'
import CourseList from '../courses/CourseList'
import Slider from '../slider/Slider'

export default function Home(props) {
  return <>
  <div>Home</div>
  <form className="d-flex mx-auto">
    <input
      className="form-control me-2 custom-search-input"
      type="search"
      placeholder="Search"
      aria-label="Search"
    />
    <button className="btn btn-outline-success" type="submit">
      Search
    </button>
  </form>
  <div className="row">
    {/* <Container> */}
      <Slider />
      <CourseList />
    {/* </Container> */}
  </div>
  </>
    
  
}
