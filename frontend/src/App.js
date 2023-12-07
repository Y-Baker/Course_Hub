
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
import { useState, useEffect, useCallback, useContext } from 'react';
import { jwtDecode } from 'jwt-decode';
import Forbidden from './components/forbidden/Forbidden';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';

import AddCourse from './components/courses-components/AddCourse/AddCourse'
import UpdateCourse from './components/courses-components/UpdateCourse/UpdateCourse'
import UserContextProvider from './components/UserContextProvider/UserContextProvider';
import SearchCourse from './components/courses-components/SearchCourse/SearchCourse';
import ShowCourses from './components/courses-components/show-courses/ShowCourses';
import AddCategory from './components/categories-components/add-category/AddCategory';
import ShowCategories from './components/categories-components/show_categories/ShowCategories';
import SearchCategory from './components/categories-components/search-category/SearchCategory';
import UpdateCategory from './components/categories-components/update-category/UpdateCategory';
import AddSection from './components/section-components/add-section/AddSection';
import SearchSection from './components/section-components/search-sections/SearchSection';
import UpdateSection from './components/section-components/update-section/UpdateSection';
import AddLesson from './components/lesson-components/add-lesson/AddLesson';
import SearchLesson from './components/lesson-components/search-lesson/SearchLesson';
import UpdateLesson from './components/lesson-components/update-lesson/UpdateLesson';
import ApproveCourses from './components/courses-components/approve-courses/ApproveCourses';

import Profile from './components/Profile/profile';


function App() {
  // const [userData, setuserData] = useState({});
  // function TokenToUserData(decodedToken){
  //   return {
  //     'name': decodedToken.name,
  //     'id': decodedToken.sub,
  //     'email': decodedToken.email,
  //     'role': decodedToken.role,
  //   }

  // }


  // const saveUserData = useCallback(() => {
  //   let encodedToken = localStorage.getItem('access_token');
  //   if (encodedToken !== null && encodedToken !== undefined) {
  //     let decodedToken = jwtDecode(encodedToken);
  //     setuserData(TokenToUserData(decodedToken));
  //     return userData;
  //   } else {
  //     setuserData(null);
  //     localStorage.removeItem('access_token');
  //     localStorage.removeItem('refresh_token');
  //     return null;
  //   }
  //   }, []);
  //   useEffect(() => {
  //     saveUserData();
  //   }, [localStorage.getItem('access_token')]);
  let routers = createBrowserRouter([
    // {path: '/', element:<Layout  userData={userData} saveUserData={saveUserData}/>, children:[
      /* using userContext instead of props */
      {path: '/', element:<Layout />, children:[
      {index:true, element: <Home/>},
      {path:'about', element: <About/>},
      {path:'contact-us', element: <ContacUs/>},
      // {path:'login', element: <Login userData={userData} saveUserData={saveUserData}/>},
       /* using userContext instead of props */
      {path:'login', element: <Login/>},

      // {path:'logout', element: <ProtectedRoute userData={userData}><Logout saveUserData={saveUserData}/></ProtectedRoute>},
      /* using userContext instead of props */
      {path:'logout', element: <ProtectedRoute><Logout/></ProtectedRoute>},
      {path: 'Profile', element: <ProtectedRoute><Profile/></ProtectedRoute>},
      {path:'register', element: <Register/>},
      // ,
      // {
      //   path: '/Admin',
      //   // element: <ProtectedRoute userData={userData} saveUserData={saveUserData} roles={['Admin']}><AdminDashboard userData={userData}/></ProtectedRoute>,

      //   element: <ProtectedRoute  roles={['Admin']}><AdminDashboard /></ProtectedRoute>,
      //   children: [],
      // },
      // {
      //   path: 'Instructor',
      //   // element: <ProtectedRoute userData={userData} saveUserData={saveUserData} roles={['Instructor']}><AdminDashboard userData={userData}/></ProtectedRoute>,

      //   element: <ProtectedRoute  roles={['Instructor']}><AdminDashboard /></ProtectedRoute>,

      //   children: [
      //     // {path: 'addCourse', element:<AddCourse userData={userData}/>},
      //     // {path: 'updateCourse', element:<UpdateCourse userData={userData}/>},
      //     {path: 'addCourse', element:<AddCourse />},
      //     {path: 'updateCourse', element:<UpdateCourse />},
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
    element: <ProtectedRoute roles={['Admin']}><AdminDashboard/></ProtectedRoute>,
    children: [
      {index:true, element:<ApproveCourses/>},

      { path: 'showCategories', element: <ShowCategories /> },
      { path: 'SearchCategory', element: <SearchCategory /> },
      { path: 'addCategory', element:<AddCategory />},
      { path: 'updateCategory/:id', element:<UpdateCategory />},

    ],
  },
  {
    path: 'Instructor',
    element: <ProtectedRoute roles={['Instructor']}><AdminDashboard /></ProtectedRoute>,
    children: [
      { index:true, element: <ShowCourses /> },
      {path: 'addCourse', element:<AddCourse/>},
      { path: 'SearchCourse', element: <SearchCourse /> },
      { path: 'updateCourse/:id', element:<UpdateCourse />},
      

      { path: 'SearchCategory', element: <SearchCategory /> },

      { path: 'addSection', element:<AddSection />},
      { path: 'SearchSection', element: <SearchSection /> },
      { path: 'updateSection/:id', element:<UpdateSection />},

      { path: 'addLesson', element:<AddLesson />},
      { path: 'SearchLesson', element: <SearchLesson /> },
      { path: 'updateLesson/:id', element:<UpdateLesson />},
    ],
  },
  ])

  return (
    <UserContextProvider>
        <RouterProvider router={routers}></RouterProvider>
    </UserContextProvider>
  );
}

export default App;
