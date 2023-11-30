import React, { useState } from 'react'
import { useFormik } from 'formik';
import { Link, useNavigate } from 'react-router-dom';
import './login.css'
import axios from 'axios';
import * as yup from 'yup';
import config from '../config';

export default function Login(props) {

  const [isLoading, setisLoading] = useState(false)
  const [errorMessage, seterrorMessage] = useState('')
  const nav = useNavigate();
  async function handleLogin(values) {
    try {
      setisLoading(true);
      let response = await axios.post(`${config.baseUrl}${config.auth}/login`, values);
      if (response.status === 200)
      {
        localStorage.setItem("access_token", response.data.data.access_token);
        localStorage.setItem("refresh_token", response.data.data.refresh_token);
        props.saveUserData();
        setisLoading(false);
        console.log(response.data )
        if (response.data.data.role === 1) {
          nav('/Instructor')
        } else if (response.data.data.role === 0) {
          nav('/admin')
        }
        else {
          nav('/')
        }
        
      } else {
        setisLoading(false);
      }
   } catch (error) {
    setisLoading(false);
    seterrorMessage(`${JSON.stringify(error.response.data.error)}`);
  }
  setisLoading(false);
  }

  const validShceme = yup.object({
    email: yup.string().email().required(),
    password: yup.string().required().matches("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", 'Minimum eight characters, at least one uppercase letter, one lowercase letter and one number'),
    remember: yup.boolean()
  })
  let formik = useFormik({
    initialValues : {
      email: '',
      password: ''
    },
    validationSchema:validShceme,
    onSubmit: handleLogin
  });
  return <>
<div className="registration-container">
  <h3>Login Now</h3>
    {errorMessage.length > 0 ?   
    <div className="alert alert-danger">
    {errorMessage}
  </div> :
  null
  }
      <form onSubmit={formik.handleSubmit}>
        <label htmlFor='email'>Email :</label>
        <input
          type="email"
          name="email"
          id = "email"
          value={formik.values.email}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          required
        />
        {formik.errors.email && formik.touched.email ? <div className="alert alert-danger">{formik.errors.email}</div> : null}

        <label htmlFor='password'>Password :</label>
        <input
          type="password"
          name="password"
          id = "password"

          value={formik.values.password}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}

          required
        />
        {formik.errors.password && formik.touched.password ? <div className="alert alert-danger">{formik.errors.password}</div> : null}

        {/* <div className='rem-checkbox'>
            <label id='remember-label' htmlFor='remember'>
            Remember Me
            </label>
            <input
              type="checkbox"
              name="remember"
              id = "remember"
              checked={formik.values.remember}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
          </div> */}

        {isLoading ?  
        <button type='button' className='register-button'><i className='fas fa-spinner fa-spin'></i></button> :
        <button  className='register-button' disabled={!formik.dirty && formik.isValid} type="submit" onSubmit={handleLogin} >Login</button>}
      </form>
      <div className="container">
        dont Have An Account ?  
        <Link to="/register">  Register Here</Link>
      </div>
    </div>
    </>
}