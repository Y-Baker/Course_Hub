import React, { useState } from 'react'
import { useFormik } from 'formik';
import { Link, useNavigate } from 'react-router-dom';
import './register.css'
import axios from 'axios';
import * as yup from 'yup';
import config from '../config';

export default function Register() {

  const [isLoading, setisLoading] = useState(false)
  const [errorMessage, seterrorMessage] = useState('')
  const nav = useNavigate();
  async function handleRegister(values) {
    try {
      setisLoading(true);
      let response = await axios.post(`${config.baseUrl}/${config.auth}/sign-up`, values);
      console.log(response.status)
      if (response.status === 201)
      {
        setisLoading(false);
        nav('/login')
      } else {
        setisLoading(false);
      }
   } catch (error) {
    console.error(error);
    setisLoading(false);
    seterrorMessage(`${JSON.stringify(error.response.data.validation_error)}`);
  }
  setisLoading(false);
  }

  const validShceme = yup.object({
    name: yup.string().required().min(3, 'name cannot be less than 3 characters').max(142, 'name cannot be more than 142 characters'),
    email: yup.string().email().required(),
    password: yup.string().required().matches("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", 'Minimum eight characters, at least one uppercase letter, one lowercase letter and one number'),
    confirmPassword: yup.string().required().matches("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", 'Minimum eight characters, at least one uppercase letter, one lowercase letter and one number').oneOf([yup.ref('password')], "password doesn't match"),
    role: yup.string().required(),
    age: yup.number().min(16).max(60)

  })
  let formik = useFormik({
    initialValues : {
      email: '',
      name: '',
      password: '',
      confirmPassword: '',
      role: '',
      age: '',
    },
    validationSchema:validShceme,
    onSubmit: handleRegister
  });
  const roleOptions = [
    {
      name: "Student",
      val: 2
    },
    {
      name: "Instructor",
      val: 1
  }
  ]

  return <>
<div className="registration-container">
  <h3>Register Now</h3>
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

        <label htmlFor='name'>Name :</label>
        <input
          type="text"
          name="name"
          id="name"
          value={formik.values.name}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          required
        />
        {formik.errors.name && formik.touched.name ? <div className="alert alert-danger">{formik.errors.name}</div> : null}

        <label htmlFor='password'>Password :</label>
        <input
          type="password"
          name="password"
          value={formik.values.password}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}

          required
        />
        {formik.errors.password && formik.touched.password ? <div className="alert alert-danger">{formik.errors.password}</div> : null}

        <label htmlFor='confirmPassword'>Confirm Password :</label>
        <input
          type="password"
          name="confirmPassword"
          id="confirmPassword"
          value={formik.values.confirmPassword}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}

          required
        />
        {formik.errors.confirmPassword && formik.touched.confirmPassword ? <div className="alert alert-danger">{formik.errors.confirmPassword}</div> : null}

        <label htmlFor='age'>Age :</label>
        <input
          type="number"
          min="16" 
          max="60"
          id="age"
          name="age"
          value={formik.values.age}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}

        />
        {formik.errors.age && formik.touched.age ? <div className="alert alert-danger">{formik.errors.age}</div> : null}

        <label htmlFor="role">Register As :</label>
        <select
          id="role"
          name="role"
          value={formik.values.role}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}

          required
        >
          <option value="" disabled>
            Register As :
          </option>
          {roleOptions.map((option) => (
            <option key={option.name} value={option.val}>
              {option.name}
            </option>
          ))}
        </select>
        {formik.errors.role && formik.touched.role ? <div className="alert alert-danger">{formik.errors.role}</div> : null}
        
        {isLoading ?  
        <button type='button' className='register-button'><i className='fas fa-spinner fa-spin'></i></button> :
        <button  className='register-button' disabled={!formik.dirty && formik.isValid} type="submit" onSubmit={handleRegister} >Register</button>}
      </form>
      <div className="container">
        Already Have An Account ?  
        <Link to="/login">  Login Here</Link>
      </div>
    </div>
    </>
}
