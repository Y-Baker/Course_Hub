import logo from './logo.svg';
import './App.css';
import Layout from './components/layout/Layout';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import Home from './components/home/Home';
import About from './components/about/About';
import ContacUs from './components/contact-us/ContactUs';
import Login from './components/login/Login';
import Logout from './components/logout/Logout';
import Register from './components/register/Register';
import Courses from './components/courses/Courses'
import NotFound from './components/not-found/NotFound'
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute'
import { useState, useEffect, useCallback } from 'react';
import { jwtDecode } from 'jwt-decode';
import Forbidden from './components/forbidden/Forbidden';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';

import AddCourse from './components/instructor-components/AddCourse/AddCourse'
import UpdateCourse from './components/instructor-components/UpdateCourse/UpdateCourse'


function App() {

  const [userData, setuserData] = useState({});
  function TokenToUserData(decodedToken){
    return {
      'name': decodedToken.name,
      'id': decodedToken.sub,
      'email': decodedToken.email,
      'role': decodedToken.role,
    }

  }


  const saveUserData = useCallback(() => {
    let encodedToken = localStorage.getItem('access_token');
    if (encodedToken !== null && encodedToken !== undefined) {
      let decodedToken = jwtDecode(encodedToken);
      setuserData(TokenToUserData(decodedToken));
      return userData;
    } else {
      setuserData(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return null;
    }
    }, []);
    useEffect(() => {
      saveUserData();
    }, [localStorage.getItem('access_token')]);
  let routers = createBrowserRouter([
    {path: '/', element:<Layout  userData={userData} saveUserData={saveUserData}/>, children:[
      {index:true, element: <Home/>},
      {path:'about', element: <About/>},
      {path:'contact-us', element: <ContacUs/>},
      {path:'login', element: <Login userData={userData} saveUserData={saveUserData}/>},
      {path:'logout', element: <ProtectedRoute userData={userData}><Logout saveUserData={saveUserData}/></ProtectedRoute>},
      {path:'register', element: <Register/>},
      // ,
      // {
      //   path: '/Admin',
      //   element: <ProtectedRoute userData={userData} saveUserData={saveUserData} roles={['Admin']}><AdminDashboard userData={userData}/></ProtectedRoute>,
      //   children: [],
      // },
      // {
      //   path: 'Instructor',
      //   element: <ProtectedRoute userData={userData} saveUserData={saveUserData} roles={['Instructor']}><AdminDashboard userData={userData}/></ProtectedRoute>,
      //   children: [
      //     {path: 'addCourse', element:<AddCourse userData={userData}/>},
      //     {path: 'updateCourse', element:<UpdateCourse userData={userData}/>},
      //   ],
      // },
      {path:'courses', element: <Courses/>, children:[
      
      ]},
      {path:'*', element: <NotFound/>},
      {path:'forbidden', element: <Forbidden/>}
    ]
  }
  ,
  {
    path: '/Admin',
    element: <ProtectedRoute userData={userData} saveUserData={saveUserData} roles={['Admin']}><AdminDashboard userData={userData}/></ProtectedRoute>,
    children: [],
  },
  {
    path: 'Instructor',
    element: <ProtectedRoute userData={userData} saveUserData={saveUserData} roles={['Instructor']}><AdminDashboard userData={userData}/></ProtectedRoute>,
    children: [
      {path: 'addCourse', element:<AddCourse userData={userData}/>},
      {path: 'updateCourse', element:<UpdateCourse userData={userData}/>},
    ],
  },
  ])

  return (
    <RouterProvider router={routers}></RouterProvider>
  );
}

export default App;