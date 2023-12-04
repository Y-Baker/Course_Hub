import React from 'react'
import CourseList from '../card/CourseList'
import Container from 'react-bootstrap/Container';
import Slider from '../slider/Slider'

export default function Home(props) {
  return (<>
  <Slider />
  <Container>
    <CourseList/>
  </Container>
  </>)    
}
