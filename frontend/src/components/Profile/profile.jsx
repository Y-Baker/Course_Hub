import React, { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import config from "../config";
import "./profile.css";
import { UserDataContext } from "../UserContextProvider/UserContextProvider";
import { useNavigate } from "react-router-dom";
import Loading from "../Loading/loading";
import CourseCard from "../cards/CourseCard";

import {
  MDBCol,
  MDBCardTitle,
  MDBContainer,
  MDBRow,
  MDBCard,
  MDBCardText,
  MDBCardBody,
  MDBCardImage,
  MDBBtn,
  MDBBreadcrumb,
  MDBBreadcrumbItem,
  MDBProgress,
  MDBProgressBar,
  MDBIcon,
  MDBListGroup,
  MDBListGroupItem,
} from "mdb-react-ui-kit";

function Profile() {
  const userContext = useContext(UserDataContext);
  const [loading, setLoading] = useState(true);
  const userData = userContext.userData;
  const [data, setData] = useState({});
  const navigate = useNavigate();

  let roleApi = "";
  useEffect(() => {
    // make wait for userData to be set

    if (userData === null) {
      navigate("/login");
      return;
    }
    if (userData.role == 1) {
      roleApi = "instructors";
    } else if (userData.role == 2) {
      roleApi = "students";
    }
    const url_api = config.api + "/" + roleApi + "/" + userData.id;
    api
      .get(`${url_api}`)
      .then((res) => {
        if (res.status === 200) {
          setData(res.data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  }, [userData]);
  if (loading) {
    return <Loading />;
  } else {
    return (
      <>
        {console.log(data)}
        <section style={{ backgroundColor: "#eee" }}>
          <MDBContainer className="py-5">
            <MDBRow>
              <MDBCol lg="4">
                <MDBCard className="mb-4">
                  <MDBCardBody className="text-center">
                    <MDBCardImage
                      src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp" //image to add
                      alt="avatar"
                      className="rounded-circle"
                      style={{ width: "150px" }}
                      fluid
                    />
                  </MDBCardBody>
                </MDBCard>
              </MDBCol>
              <MDBCol lg="8">
                <MDBCard className="mb-4">
                  <MDBCardBody>
                    <MDBRow>
                      <MDBCol sm="3">
                        <MDBCardText>Full Name</MDBCardText>
                      </MDBCol>
                      <MDBCol sm="9">
                        <MDBCardText className="text-muted">
                          {data.name}
                        </MDBCardText>
                      </MDBCol>
                    </MDBRow>
                    <hr />
                    <MDBRow>
                      <MDBCol sm="3">
                        <MDBCardText>Email</MDBCardText>
                      </MDBCol>
                      <MDBCol sm="9">
                        <MDBCardText className="text-muted">
                          {data.email}
                        </MDBCardText>
                      </MDBCol>
                    </MDBRow>
                    <hr />
                    <MDBRow>
                      <MDBCol sm="3">
                        <MDBCardText>Role</MDBCardText>
                      </MDBCol>
                      <MDBCol sm="9">
                        <MDBCardText className="text-muted">
                          {config.roles[data.role]}
                        </MDBCardText>
                      </MDBCol>
                    </MDBRow>
                    <hr />
                    {data.role == 1 ? (
                      <>
                        <MDBRow>
                          <MDBCol sm="3">
                            <MDBCardText>Total Courses</MDBCardText>
                          </MDBCol>
                          <MDBCol sm="9">
                            <MDBCardText className="text-muted">
                              {data.courses.length}
                            </MDBCardText>
                          </MDBCol>
                        </MDBRow>
                        <hr />
                        <MDBRow>
                          <MDBCol sm="3">
                            <MDBCardText>Total Students</MDBCardText>
                          </MDBCol>
                          <MDBCol sm="9">
                            <MDBCardText className="text-muted">
                              {data.total_students}
                            </MDBCardText>
                          </MDBCol>
                        </MDBRow>
                      </>
                    ) : (
                      <>
                        <MDBRow>
                          <MDBCol sm="3">
                            <MDBCardText>Interested In</MDBCardText>
                          </MDBCol>
                          <MDBCol sm="9">
                            <MDBCardText className="text-muted">
                              {data.interested.name}
                            </MDBCardText>
                          </MDBCol>
                        </MDBRow>
                        <hr />
                        <MDBRow>
                          <MDBCol sm="3">
                            <MDBCardText>My Courses</MDBCardText>
                          </MDBCol>
                          <MDBCol sm="9">
                            <MDBCardText className="text-muted">
                              {data.courses.length}
                            </MDBCardText>
                          </MDBCol>
                        </MDBRow>
                      </>
                    )}
                  </MDBCardBody>
                </MDBCard>
              </MDBCol>
            </MDBRow>

            <br />
            <br />

            <MDBRow>
              <MDBCardTitle className="SubHeading">
                {data.role == 1 ? "My Courses" : "My Learning"}
              </MDBCardTitle>
              <MDBRow className="py-1">
                {data.courses.length == 0 ? (
                  <strong>No Data!</strong>
                ) : (
                  data.courses.map((course) => (
                    <MDBCol lg="5">
                      {course.approved && <CourseCard course={course} />}
                    </MDBCol>
                  ))
                )}
              </MDBRow>
            </MDBRow>
          </MDBContainer>
        </section>
      </>
    );
  }
}

export default Profile;
