import React from "react";
import { Link } from "react-router-dom";
import { Card, Button, Row, Col } from "react-bootstrap";
import Image from "../../assets/images/OIF.jpg";
import { useNavigate } from "react-router-dom";
import "./CourseCard-Profile.css";

function CourseCardProfile({ course, owner }) {
  const navigate = useNavigate();
  function handleEdit(course) {
    navigate(`/instructor/updateCourse/${course.id}`, {
      state: { courseData: course },
    });
  }

  return (
    <Card className="my-3 p-3 rounded">
      <Card.Img src={Image} variant="top" />
      <Card.Body>
        <Card.Title as="div" className="card-head">
          <Link to={`/courses/${course.id}`} className="link-style">
            <strong style={{ fontSize: "30px" }}>{course.name}</strong>
          </Link>
          <div
            style={{
              paddingTop: "15px",
              color: "#373a3c",
              fontSize: "16px",
              fontWeight: "bold",
            }}
          >
            {course.approved ? (
              <p style={{ color: "#27ae60" }}>Approved</p>
            ) : (
              <p style={{ color: "#F92F60" }}>Not Approved</p>
            )}
          </div>
        </Card.Title>
        <Card.Text as="div" style={{ paddingBottom: "16px" }}>
          <p style={{ color: "#333" }}>{course.description}</p>
        </Card.Text>
        <Card.Text as="div" className="d-flex justify-content-between">
          <p style={{ color: "#0C356A", paddingTop: "8px" }}>
            Total Hours: {course.hours}
          </p>
          {course.approved ? (
            <div>
              {owner && (
                <button
                  className="btn btn-outline-success mr edit"
                  type="submit"
                  onClick={() => handleEdit(course)}
                >
                  Edit
                </button>
              )}
              <Link to={`/courses/${course.id}`}>
                <button className="btn btn-outline-success basic" type="submit">
                  More Details
                </button>
              </Link>
            </div>
          ) : (
            <button
              className="btn btn-outline-success edit"
              type="submit"
              onClick={() => handleEdit(course)}
            >
              Edit
            </button>
          )}
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default CourseCardProfile;