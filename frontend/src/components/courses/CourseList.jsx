import React from "react";
import api from "../api";
import config from "../config";
import { useState, useEffect } from "react";
import Loading from "../Loading/loading";
import CourseCard from "../cards/CourseCard";

import {
  MDBCol,
  MDBContainer,
  MDBRow,
} from "mdb-react-ui-kit";

function CourseList({ filter = null }) {
  const [courses, setCourses] = React.useState([]);
  const [loading, setLoading] = useState(true);
  let url_api = config.api + "/";
  if (filter === null) {
    url_api += "courses";
  } else {
    // categories/<category_id>/courses
    url_api += "categories/" + filter.id + "/courses";
  }
  React.useEffect(() => {
    console.log("Fetching courses from " + url_api);
    api
      .get(url_api)
      .then((response) => {
        if (response.status === 200) {
          setCourses(response.data);
          setLoading(false);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  if (loading) {
    return <Loading />;
  } else {
    return (
      <MDBContainer className="py-4">
        <MDBRow>
        {courses.map((course) => (
          <MDBCol lg="4">
            {course.approved && <CourseCard course={course} />}
          </MDBCol>
        ))}
        </MDBRow>
      </MDBContainer>
    );
  }
}

export default CourseList;
