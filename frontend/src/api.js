import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

// const apiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// api.interceptors.response.use(
//   (response) => response, // Si la réponse est réussie, retournez-la telle quelle
//   async (error) => {
//     const originalRequest = error.config;

//     // Si l'erreur est une 401 et que ce n'est pas une tentative de refresh
//     if (error.response?.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true; // Empêche les boucles infinies

//       try {
//         // Rafraîchir le token
//         const refresh = localStorage.getItem(REFRESH_TOKEN);
//         if (refresh) {
//           const { data } = await api.post("/api/auth/token/refresh/", {
//             refresh,
//           });
//           const newAccessToken = data.access;

//           // Stocker le nouveau token et réessayer la requête originale
//           localStorage.setItem(ACCESS_TOKEN, newAccessToken);
//           api.defaults.headers.common["Authorization"] =
//             `Bearer ${newAccessToken}`;
//           originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

//           return api(originalRequest); // Relance la requête initiale
//         }
//       } catch (refreshError) {
//         console.error(
//           "Le token de rafraîchissement est invalide ou expiré :",
//           refreshError
//         );
//         localStorage.removeItem(ACCESS_TOKEN);
//         localStorage.removeItem(REFRESH_TOKEN);
//         window.location.href = "/login"; // Redirige vers la page de connexion
//       }
//     }

//     return Promise.reject(error); // Retourne l'erreur si elle ne peut pas être résolue
// }
// );

export default api;
