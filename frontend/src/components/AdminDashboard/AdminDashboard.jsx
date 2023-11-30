import React, { useEffect, useState } from 'react';
import { Outlet , Link} from 'react-router-dom';
import './AdminDashboard.css';
import Header from '../header/Header';
import Footer from '../footer/Footer';

export default function AdminDashboard(props) {
  const [loading, setLoading] = useState(true);
  const [optionsVisibility, setOptionsVisibility] = useState({
    courses: false,
    sections: false,
    lessons: false,
  });

  const toggleOptions = (sectionId) => {
    setOptionsVisibility((prevVisibility) => ({
      ...prevVisibility,
      [sectionId]: !prevVisibility[sectionId],
    }));
  };

  useEffect(() => {
    if (props.userData && props.userData.role !== null && props.userData.role !== undefined) {
      setLoading(false);
    }
  }, [props.userData]);

  if (loading) {
    return <div>Loading...</div>;
  } else {
    return (
      <>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header  userData={props.userData} saveUserData={props.saveUserData}/>
        <div style={{ flex: 1 }}>
        <div className="dashboard">
          <div className="sidebar">
            <div className="dash-section" id="courses">
              <div className="dash-section-title" onClick={() => toggleOptions('courses')}>
                Courses
              </div>
              {optionsVisibility.courses ? (
                <>
                  <div className="options">
                    <div className="option">
                      <Link className="nav-link" to='addCourse'>
                        <span className="icon">+</span> Add
                      </Link>
                    </div>
                    <div className="option">
                      <span className="icon">✎</span> Update
                    </div>
                    <div className="option">
                      <span className="icon">✖</span> Delete
                    </div>
                    {props.userData.role === 0 ? (
                      <>
                        <div className="option">
                          <span className="icon">✎</span> Approve Courses
                        </div>
                      </>
                    ) : null}
                  </div>
                </>
              ) : null}
            </div>
            <div className="dash-section" id="sections">
              <div className="dash-section-title" onClick={() => toggleOptions('sections')}>
                Sections
              </div>
              {optionsVisibility.sections && (
                <div className="options">
                  <div className="option">
                    <span className="icon">+</span> Add
                  </div>
                  <div className="option">
                    <span className="icon">✎</span> Update
                  </div>
                  <div className="option">
                    <span className="icon">✖</span> Delete
                  </div>
                </div>
              )}
            </div>
            <div className="dash-section" id="lessons">
              <div className="dash-section-title" onClick={() => toggleOptions('lessons')}>
                Lessons
              </div>
              {optionsVisibility.lessons && (
                <div className="options">
                  <div className="option">
                    <span className="icon">+</span> Add
                  </div>
                  <div className="option">
                    <span className="icon">✎</span> Update
                  </div>
                  <div className="option">
                    <span className="icon">✖</span> Delete
                  </div>
                </div>
              )}
            </div>
          </div>
          <div className="main-content">
            <Outlet></Outlet>
          </div>
        </div>
        </div>
        <Footer />
    </div>
        
      </>
    );
  }
}
