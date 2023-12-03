import { useFormik } from 'formik';
import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import * as Yup from 'yup';
import api from '../../api';
import config from '../../config';
import toast, { Toaster } from 'react-hot-toast';


export default function UpdateCategory() {
  const location = useLocation()
  const [loading, setloading] = useState(true)
  const [isLoading, setisLoading] = useState(false)
  const { categoryData } = location.state;
  const [category, setcategory] = useState(categoryData)
  const [addedCourses, setaddedCourses] = useState([]);
  const [removedCourses, setremovedCourses] = useState([]);
  const [categoryCourses, setcategoryCourses] = useState([])
  const [allCourses, setallCourses] = useState([])

  useEffect(() => {
    formik.values.name = category.name;
  }, [category])
  function handleCategorySubmit(values){
    setisLoading(true)
    api.put(`${config.api}/categories/${values.id}`, values)
    .then((resp) => {
      toast.success("updated Successfully");
      setcategory(resp.data)
      setisLoading(false)
    }).catch((err) => {
      console.error(err);
      toast.error("error can't update");
      setisLoading(false)
    })
  }
  const validScheme = Yup.object().shape({
    name: Yup.string().required().min(3)
  });

  function getCategoryCourses(category_id, page, per_page) {
    api.get(`${config.api}/categories/${category_id}/courses?page=${page}&per_page=${per_page}`)
    .then((resp) => {
      toast.success("category courses retrived");
      setcategoryCourses(resp.data);
    }).catch((err)=> {
      console.error(err);
      toast.error("something went wrong");
    })
  }
  function getAllCourses(page, per_page) {
    api.get(`${config.api}/courses/noCategory?page=${page}&per_page=${per_page}`)
    .then((resp) => {
      toast.success("all courses retrived");
      setallCourses(resp.data);
    }).catch((err)=> {
      console.error(err);
      toast.error("something went wrong");
    })
  }
  useEffect(() => {
    if (categoryData !== null) {
      setloading(false);
      getAllCourses(1, 100);
      getCategoryCourses(1, 100);
    }
  }, [])
  const formik = useFormik({
    initialValues: {
      id: categoryData.id,
      name: categoryData.name
    },
    validationSchema: validScheme,
    onSubmit: handleCategorySubmit
  })


  // Function to handle selecting/deselecting a course
  const handleCourseSelection = (courseId) => {
    setaddedCourses((prevSelectedCourses) => {
      if (prevSelectedCourses.includes(courseId)) {
        return prevSelectedCourses.filter((id) => id !== courseId);
      } else {
        return [...prevSelectedCourses, courseId];
      }
    });
  };

  const handleAddToCategory = () => {
    setisLoading(true);
    api.put(`${config.api}/categories/${category.id}/add-courses`, addedCourses)
    .then((response) => {
      toast.success(response.message);
    })
    .catch((error) => {
      console.error(error);
      toast.error("error occured")
    })
    setisLoading(false);
    console.log('Adding courses to category:', addedCourses);
    setaddedCourses([]);
  };
  const handleRemoveToCategory = () => {
    setisLoading(true);
    api.put(`${config.api}/categories/${category.id}/remove-courses`, removedCourses)
    .then((response) => {
      toast.success(response.message);
    })
    .catch((error) => {
      console.error(error);
      toast.error("error occured")
    })
    setisLoading(false);
    console.log('removing courses from category:', removedCourses);
    setremovedCourses([]);
  };
  if (loading) {
    return <div className="info">Loading</div>
  } else {
    return <>
      <form onSubmit={formik.handleSubmit}>
        <input 
        type="text"
        name="id"
        id="id"
        value={formik.values.id}
        placeholder='category id'
        disabled
        required
         />
        <input 
        type="text"
        name="name"
        id="name"
        value={formik.values.name}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        placeholder='category name'
        required
         />
         
        {formik.errors.name && formik.touched.name ? 
        <div className="alert alert-danger">{formik.errors.name}</div>:
        null}
        
        {isLoading ?  
        <button type='button' className='register-button'><i className='fas fa-spinner fa-spin'></i></button> :
        <button  className='btn btn-primary btn-lg btn-block' disabled={!formik.dirty && formik.isValid} type="submit" onSubmit={handleCategorySubmit} >update Course</button>}
        <Toaster/>
      </form>
      <br/>



    </>
  }
}
