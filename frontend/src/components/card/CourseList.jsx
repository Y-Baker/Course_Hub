import { useEffect, useState } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/esm/Container';
import CourseCard from './CourseCard';
import Button from 'react-bootstrap/Button'

function CourseList() {

    const api_url= 'http://127.0.0.1:5000/api/courses'
  
    const [courses, setCourses] = useState([]);
  
    useEffect(() => {
      fetch(api_url).then((res) => res.json()).then((data) => setCourses(data));
    }, []);

  return (
  <>
    <Container>
      <Row>
        {courses.map((course) => {
          return (
            <Col xs={3} key={course.id}>
              <CourseCard course={course} />
            </Col>
          );
        })}
      </Row>
    </Container>
  </>
  );
}

export default CourseList;
