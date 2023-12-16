import React from "react";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import api from "../api";
import config from "../config";
import Loading from "../Loading/loading";
import CourseList from "../courses/CourseList";

function CategoryPage() {
  const { id } = useParams();
  const url_api =
    config.api +
    "/categories/" +
    id;

  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState([]);

  const navigate = useNavigate();

  const getCategory = (url_api) => {
    api
      .get(url_api)
      .then((res) => {
        if (res.status === 200) {
          setCategory(res.data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error(err);
        navigate("/not-found");
      });
  };

  useEffect(() => {
    getCategory(url_api);
  }, []);

  if (loading) {
    return <Loading />;
  } else {
    return (
      <div>
        <div className="SubHeading course-title course-description">
          <br />
            <Link to="/categories" className="redirect">Categories</Link> / {category.name}
        </div>
        <div className="row">
          <CourseList filter={category}/>
        </div>
      </div>
    );
  }
}

export default CategoryPage;
