import React, { useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import "./profile.css";
import { UserDataContext } from "../UserContextProvider/UserContextProvider";

function Profile(props) {
  let userContext = useContext(UserDataContext);
  let userData = userContext.userData;
  useEffect(() => {
    console.log("userData changed");
  }, [userData]);
  return (
    <>
      <div className="profile-container">

      </div>
    </>
  );
}

export default Profile;
