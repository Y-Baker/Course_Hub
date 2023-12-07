import { useFormik } from 'formik';
import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import * as Yup from 'yup';
import api from '../../api';
import config from '../../config';
import toast, { Toaster } from 'react-hot-toast';
import './updateCategory.css'

export default function UpdateCategory() {
  const location = useLocation()
  const [loading, setloading] = useState(true)
  const [isLoading, setisLoading] = useState(false)
  const { categoryData } = location.state;
  const [category, setcategory] = useState(categoryData)
  const [addedCourses, setaddedCourses] = useState([]);
  const [removedCourses, setremovedCourses] = useState([]);
  const [categoryCourses, setcategoryCourses] = useState([])
  const [noCategoryCourses, setnoCategoryCourses] = useState([])

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
  function getnoCategoryCourses(page, per_page) {
    api.get(`${config.api}/courses/noCategory?page=${page}&per_page=${per_page}`)
    .then((resp) => {
      toast.success("all courses retrived");
      setnoCategoryCourses(resp.data);
    }).catch((err)=> {
      console.error(err);
      toast.error("something went wrong");
    })
  }
  useEffect(() => {
    if (categoryData !== null) {
      setloading(false);
      getnoCategoryCourses(1, 100);
      getCategoryCourses(category.id, 1, 100);
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
  const handleAddCourseSelection = (courseId) => {
    setaddedCourses((prevSelectedCourses) => {
      if (prevSelectedCourses.includes(courseId)) {
        return prevSelectedCourses.filter((id) => id !== courseId);
      } else {
        return [...prevSelectedCourses, courseId];
      }
    });
  };

  const handleRemoveCourseSelection = (courseId) => {
    setremovedCourses((prevSelectedCourses) => {
      if (prevSelectedCourses.includes(courseId)) {
        return prevSelectedCourses.filter((id) => id !== courseId);
      } else {
        return [...prevSelectedCourses, courseId];
      }
    });
  };

  const handleAddToCategory = () => {
    setisLoading(true);
    const data = {
      'courses': addedCourses
    }
    api.put(`${config.api}/categories/${category.id}/add-courses`, data)
    .then((response) => {
      toast.success(response.data.message);
    })
    .catch((error) => {
      console.error(error);
      toast.error("error occured")
    })
    setisLoading(false);
    setaddedCourses([]);
  };
  const handleRemoveToCategory = () => {
    const data = {
      'courses': removedCourses
    }
    setisLoading(true);
    api.put(`${config.api}/categories/${category.id}/remove-courses`, data)
    .then((response) => {
      toast.success(response.data.message);
    })
    .catch((error) => {
      console.error(error);
      toast.error("error occured")
    })
    setisLoading(false);
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

      <div>
      <div className="category-box">
        <h2>Add Category To Courses</h2>
        <ul>
          {noCategoryCourses.map((course, index) => (
              <li key={course.id}>
              <label htmlFor={`course${index}`}>{course.name}</label>
                <input
                  name={`course${index}`}
                  type="checkbox"
                  checked={addedCourses.includes(course.id)}
                  onChange={() => handleAddCourseSelection(course.id)}
                />
              </li>
            ))}
        </ul>
        <button className='btn btn-secondary' disabled={addedCourses.length === 0} onClick={handleAddToCategory}>Add to Category</button>
      </div>

      <br/>

      <div className="category-box">
        <h2>Remove Courses from Category</h2>
        <ul>
          {categoryCourses.map((course, index) => (
              <li key={course.id}>
                <label htmlFor={`courseToRemove${index}`}>
                {course.name}
                </label>
                  <input
                    name={`courseToRemove${index}`}
                    type="checkbox"
                    checked={removedCourses.includes(course.id)}
                    onChange={() => handleRemoveCourseSelection(course.id)}
                  />

              </li>
            ))}
        </ul>
        <button className='btn btn-danger' disabled={removedCourses.length === 0} onClick={handleRemoveToCategory}>Remove from Category</button>
      </div>
    </div>


    </>
  }
}
