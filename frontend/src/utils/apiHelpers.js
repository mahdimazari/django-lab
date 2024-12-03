import api from "../api";

// Fetch notes with optional search query
export const fetchNotes = async (searchQuery, token) => {
  const url = searchQuery ? `/api/notes/?search=${searchQuery}` : "/api/notes/";
  try {
    const response = await api.get(url, {
      headers: {
        Authorization: `Bearer ${token}`, // Add token for authentication if needed
      },
    });
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
