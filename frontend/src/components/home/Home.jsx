import React, { useEffect, useState } from "react";
import CourseList from "../courses/CourseList";
import Slider from "../slider/Slider";
import Loading from "../Loading/loading";
import "./home.css";
import api from "../api";
import config from "../config";
import { Container } from "react-bootstrap";
import { MDBCardTitle, MDBContainer, MDBRow } from "mdb-react-ui-kit";

function Home(props) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  let url_api = config.api + "/categories";

  useEffect(() => {
    api
      .get(url_api)
      .then((response) => {
        if (response.status === 200) {
          setCategories(response.data);
          setLoading(false);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <>
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
      <br />
      {loading ? (
        <Loading />
      ) : (
        <div className="row">
          <Container>
            <Slider />
            <br />
            <br />
          </Container>
          <hr />
          <MDBContainer className="py-4">
            <MDBRow>
              {categories.map((category, index) => (
                <div>
                  {category.courses.length > 0 && (
                    <>
                      <div className="SubHeading">
                        <h2>{category.name}</h2>
                      </div>
                      <CourseList filter={category} />
                    </>
                  )}
                </div>
              ))}
            </MDBRow>
          </MDBContainer>
        </div>
      )}
    </>
  );
}
export default Home;
