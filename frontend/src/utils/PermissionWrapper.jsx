// import React from "react";

const PermissionWrapper = ({
  userPermissions,
  requiredPermission,
  children,
}) => {
  console.log("user Permi", userPermissions, requiredPermission);
  // Check if the user has the required permission
  if (!userPermissions.includes(requiredPermission)) {
    return <div>Access Denied</div>;
  }

  return children;
};

export default PermissionWrapper;
