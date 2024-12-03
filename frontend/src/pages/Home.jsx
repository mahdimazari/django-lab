import { useState, useEffect } from "react";
import {
  fetchNotes,
  getCategories,
  createNote,
  deleteNote,
} from "../utils/apiHelpers";
import "../styles/Home.css";
import Note from "../components/Note";
import SearchBar from "../components/SearchBar";
import Select from "react-select";
import { useNavigate } from "react-router-dom";

function Home() {
  const [notes, setNotes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // Fetch notes
  useEffect(() => {
    fetchNotes(searchQuery, token)
      .then((data) => setNotes(data))
      .catch((error) => alert("Error fetching notes.", error));
    console.log("notes", notes);
  }, [searchQuery]);

  // Fetch categories
  useEffect(() => {
    getCategories()
      .then((data) => setCategories(data))
      .catch((error) => alert("Error fetching categories.", error));
  }, []);

  const handleCategoryChange = (selectedOptions) => {
    const selectedIds = selectedOptions
      ? selectedOptions.map((option) => option.value)
      : [];
    setSelectedCategories(selectedIds);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleCreateNote = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    if (file) formData.append("file", file);
    selectedCategories.forEach((id) => formData.append("categories", id));

    try {
      await createNote(formData, token);
      alert("Note created!");
      fetchNotes("", token).then((data) => setNotes(data)); // Refresh notes
    } catch (error) {
      alert("Error creating note.", error);
    }
  };

  const handleDeleteNote = async (id) => {
    try {
      const success = await deleteNote(id, token);
      if (success) {
        alert("Note deleted!");
        fetchNotes("", token).then((data) => setNotes(data)); // Refresh notes
      } else {
        alert("Failed to delete note.");
      }
    } catch (error) {
      alert("Error deleting note.", error);
    }
  };

  return (
    <div>
      <button onClick={() => navigate("/logout")}>Logout</button>
      <h2>Notes</h2>
      <SearchBar onSearch={(query) => setSearchQuery(query)} />
      <div className="notes-container">
        {notes.map((note) => (
          <Note
            note={note}
            onDelete={handleDeleteNote}
            key={note.id}
            categories={categories}
          />
        ))}
      </div>
      <h2>Create a Note</h2>
      <form onSubmit={handleCreateNote}>
        <label>Title:</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <label>Content:</label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <label>File:</label>
        <input type="file" onChange={handleFileChange} />
        <label>Categories:</label>
        <Select
          isMulti
          options={categories}
          onChange={handleCategoryChange}
          value={categories.filter((cat) =>
            selectedCategories.includes(cat.value)
          )}
        />

        <input value="submit" type="submit" />
      </form>
    </div>
  );
}

export default Home;