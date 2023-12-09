import React, { useContext, useEffect, useState } from "react";
import api from "../api";
import config from "../config";
import { UserDataContext } from "../UserContextProvider/UserContextProvider";
import { useNavigate } from "react-router-dom";
import Loading from "../Loading/loading";
import UserProfile from "./userProfile";

function Profile() {
  const userContext = useContext(UserDataContext);
  const [loading, setLoading] = useState(true);
  const userData = userContext.userData;
  const [data, setData] = useState({});
  const navigate = useNavigate();

  let roleApi = "";
  useEffect(() => {
    // make wait for userData to be set

    if (userData === null) {
      navigate("/login");
      return;
    }
    if (userData.role == 1) {
      roleApi = "instructors";
    } else if (userData.role == 2) {
      roleApi = "students";
    }
    const url_api = config.api + "/" + roleApi + "/" + userData.id;
    api
      .get(`${url_api}`)
      .then((res) => {
        if (res.status === 200) {
          setData(res.data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  }, [userData]);
  if (loading) {
    return <Loading />;
  } else {
    return <UserProfile data={data} />;
  }
}

export default Profile;
