import React from "react";
import { Link } from "react-router-dom";
import { Card, Button, Row, Col } from "react-bootstrap";
import Image from "../../assets/images/OIF.jpg";
import "./CourseCard.css";

function CourseCard({ course }) {
  return (
    <Card className="my-3 p-3 rounded">
      <Link to={`/courses/${course.id}`}>
        <Card.Img src={Image} variant="top" />
      </Link>
      <Card.Body>
        <Card.Title as="div" className="card-head">
          <Link to={`/courses/${course.id}`} className="link-style">
            <strong style={{ fontSize: "30px" }}>{course.name}</strong>
          </Link>
          <Link
            to={`/users/${course.instructor_id}`}
            className="link-style"
          >
            <p
              style={{ paddingTop: "15px", color: "#373a3c", fontSize: "14px" }}
            >
              by {course.instructor_name}
            </p>
          </Link>
        </Card.Title>
        <Card.Text as="div" style={{ paddingBottom: "16px" }}>
          <p style={{ color: "#333" }}>{course.description}</p>
        </Card.Text>
        <Card.Text as="div" className="d-flex justify-content-between">
          <p style={{ color: "#0C356A", paddingTop: "8px" }}>
            Total Hours: {course.hours}
          </p>
          <Link
            to={`/courses/${course.id}`}>
          <button
            className="btn btn-outline-success"
            type="submit"
          >
            More Details
          </button>
          </Link>
          
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default CourseCard;

{
  /* <button className="btn btn-outline-success" type="submit"
            variant="primary"
            style={{ backgroundColor: "#0C356A", borderColor: "#0C356A", color: "#FFFFFF" }}
          ></button> */
}
