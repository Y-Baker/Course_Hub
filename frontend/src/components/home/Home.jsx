import React, { useEffect, useState } from "react";
import Slider from "../slider/Slider";
import Loading from "../Loading/loading";
import "./home.css";
import api from "../api";
import config from "../config";
import { Container } from "react-bootstrap";
import Categories from "../categories/Categories";

function Home(props) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  let url_api = config.api + "/categories?page=1&per_page=20";

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
        console.error(error);
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
        <button className="btn btn-outline-success basic" type="submit">
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
          <Categories categories={categories}/>
        </div>
      )}
    </>
  );
}
export default Home;
