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
import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

function App() {

  const [userData, setuserData] = useState(null);
  function TokenToUserData(decodedToken){
    return {
      'name': decodedToken.name,
      'id': decodedToken.sub,
      'email': decodedToken.email,
      'role': decodedToken.role,
    }

  }


  function saveUserData() {
    let encodedToken = localStorage.getItem('access_token');
    if (encodedToken !== null) {
      let decodedToken = jwtDecode(encodedToken);
      setuserData(TokenToUserData(decodedToken));
    } else {
      setuserData(null);
    }
    return userData;
  }

  let routers = createBrowserRouter([
    {path: '/', element:<Layout  userData={userData} saveUserData={saveUserData}/>, children:[
      {index:true, element: <Home/>},
      {path:'about', element: <About/>},
      {path:'contact-us', element: <ContacUs/>},
      {path:'login', element: <Login saveUserData={saveUserData}/>},
      {path:'logout', element: <ProtectedRoute><Logout saveUserData={saveUserData}/></ProtectedRoute>},
      {path:'register', element: <Register/>},
      {path:'courses', element: <Courses/>, children:[

      ]},
      {path:'*', element: <NotFound/>},
    ]}
  ])
  useEffect(() => {
    saveUserData();
  }, []); 
  return (
    <RouterProvider router={routers}></RouterProvider>
  );
}

export default App;
