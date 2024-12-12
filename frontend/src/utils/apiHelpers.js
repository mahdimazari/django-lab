import api from "../api";

// Fetch notes with optional search query
export const fetchNotes = async (searchQuery, filters, token) => {
  let url = "/api/notes/";
  const params = new URLSearchParams();
  // console.log("filters", searchQuery, filters);
  if (searchQuery) params.append("search", searchQuery);
  // if (filters.title) params.append("title", filters.title);
  if (filters.categories)
    filters.categories.forEach((cat) => params.append("categories", cat));
  if (filters.dateRange?.start)
    params.append("created_at_after", filters.dateRange.start);
  if (filters.dateRange?.end)
    params.append("created_at_before", filters.dateRange.end);

  url += `?${params.toString()}`;
  // console.log("url", url);
  // const url = searchQuery ? `/api/notes/?search=${searchQuery}` : "/api/notes/";
  try {
    const response = await api.get(url, {
      headers: {
        Authorization: `Bearer ${token}`, // Add token for authentication if needed
      },
    });
    // console.log("response note", response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching notes:", error);
    throw error;
  }
};

// Fetch categories
export const getCategories = async () => {
  try {
    const response = await api.get("/api/categories/");
    return response.data.map((category) => ({
      value: category.id,
      label: category.name,
    }));
  } catch (error) {
    console.error("Error fetching categories:", error);
    throw error;
  }
};

// Create a new note
export const createNote = async (noteData, token) => {
  try {
    const response = await api.post("/api/notes/", noteData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating note:", error);
    throw error;
  }
};

// Delete a note
export const deleteNote = async (id, token) => {
  try {
    const response = await api.delete(`/api/notes/delete/${id}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.status === 204;
  } catch (error) {
    console.error("Error deleting note:", error);
    throw error;
  }
};

export const createSurvey = (data) => api.post("/api/surveys/create/", data);

export const fetchUserPermissions = async () => {
  try {
    const response = await api.get("/api/user-permissions/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`, // Si vous utilisez JWT
      },
    });
    return response.data.permissions; // Retourne la liste des permissions
  } catch (error) {
    console.error("Erreur lors de la récupération des permissions :", error);
    return [];
  }
};