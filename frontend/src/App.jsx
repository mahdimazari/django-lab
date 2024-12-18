// import { useContext } from "react";
import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import SurveyResponseDetail from "./pages/SurveyResponseDetails";
import ProtectedRoute from "./components/ProtectedRoute";
// import SurveyList from "./pages/SurveyList";
import SurveyDetail from "./pages/SurveyDetail";
// import { AuthContext } from "./contexts/AuthContext";
// import { AuthProvider } from "./contexts/AuthProvider";

import { fetchUserPermissions } from "./utils/apiHelpers";

export function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  // const { permissions } = useContext(AuthContext);
  const [permissions, setPermissions] = useState([]);
  const getPermissions = async () => {
    const userPermissions = await fetchUserPermissions();
    setPermissions(userPermissions);
  };
  useEffect(() => {
    getPermissions();
  }, []);

  // console.log("return permissions", permissions);
  return (
    // <AuthProvider>
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home userPermissions={permissions} />
              {/* <Home /> */}
            </ProtectedRoute>
          }
        />
        {/* <Route path="/" exact component={SurveyList} /> */}
        <Route
          path="/survey-responses/:id"
          element={<SurveyResponseDetail />}
        />
        <Route path="/survey/:id" element={<SurveyDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
    // </AuthProvider>
  );
}

export default App;
