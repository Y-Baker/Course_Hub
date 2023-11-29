import React from 'react'

export default function Courses() {
  return <>
  <div>courses</div>
            {/* Search bar in the middle */}
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
  </>
    
  
}
