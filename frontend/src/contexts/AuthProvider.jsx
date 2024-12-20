import { useState, useEffect } from "react";
import { getPermissions } from "../utils/authService";
import { AuthContext } from "./AuthContext"; // Import du contexte

// Définition et exportation du fournisseur
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [permissions, setPermissions] = useState([]);

  useEffect(() => {
    const loadPermissions = async () => {
      try {
        const userPermissions = await getPermissions();
        setPermissions(userPermissions);
      } catch (error) {
        console.error("Failed to fetch permissions:", error);
      }
    };

    if (localStorage.getItem("access")) {
      loadPermissions();
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, permissions }}>
      {children}
    </AuthContext.Provider>
  );
};
