import React, { useContext, useEffect, useState } from 'react';
import { Outlet , Link} from 'react-router-dom';
import './AdminDashboard.css';
import Header from '../header/Header';
import Footer from '../footer/Footer';
import { UserDataContext } from '../UserContextProvider/UserContextProvider';

export default function AdminDashboard(props) {
  const userContext = useContext(UserDataContext);
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
    if (userContext.userData && userContext.userData.role !== null && userContext.userData.role !== undefined) {
      setLoading(false);
    }
  }, [userContext.userData]);

  if (loading) {
    return <div>Loading...</div>;
  } else {
    return (
      <>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header  userData={userContext.userData} saveUserData={userContext.saveUserData}/>
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
                  <Link className="nav-link" to='searchCourse'>
                    <div className="option">
                        <span className="icon">+</span> search
                    </div>
                    </Link>
                  <Link className="nav-link" to='addCourse'>
                    <div className="option">
                        <span className="icon">+</span> Add
                    </div>
                    </Link>
                  <Link className="nav-link" to='updateCourse'>
                    <div className="option">
                      <span className="icon">✎</span> Update
                    </div>
                    </Link>

                    <div className="option">
                      <span className="icon">✖</span> Delete
                    </div>
                    {userContext.userData.role === 0 ? (
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
          {/* <div className="card">
            <div className="card-body">
              <h5 className="card-title">Welcome Back</h5>
              <p className="card-text">{userContext.userData.name}</p>
            </div>
          </div> */}
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
