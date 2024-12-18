import { useState, useEffect } from "react";
import {
  fetchNotes,
  getCategories,
  createNote,
  deleteNote,
} from "../utils/apiHelpers";
import "../styles/Home.css";
import "../styles/filters.css";
import Note from "../components/Note";
import SearchBar from "../components/SearchBar";
import Select from "react-select";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useNavigate } from "react-router-dom";
import SurveyForm from "../components/SurveyForm";
// import PermissionWrapper from "../utils/PermissionWrapper";
import SurveyList from "./SurveyList";
import { PERMISSIONS } from "../utils/constants";
import { ACCESS_TOKEN } from "../constants";
// import { AuthContext } from "../contexts/AuthContext";
// import { SurveyWizard } from "../components/SurveyWizard";

function Home({ userPermissions }) {
  const [notes, setNotes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState([]);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  // const { permissions } = useContext(AuthContext);
  console.log("tokeb", token);
  // Fetch notes
  useEffect(() => {
    fetchNotes(searchQuery, filters, token)
      .then((data) => setNotes(data))
      .catch((error) => alert("Error fetching notes.", error));
    // console.log("notes", notes);
  }, [searchQuery, filters]);

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
      fetchNotes("", null, token).then((data) => setNotes(data)); // Refresh notes
    } catch (error) {
      alert("Error creating note.", error);
    }
  };

  const handleDeleteNote = async (id) => {
    try {
      const success = await deleteNote(id, token);
      if (success) {
        alert("Note deleted!");
        fetchNotes("", null, token).then((data) => setNotes(data)); // Refresh notes
      } else {
        alert("Failed to delete note.");
      }
    } catch (error) {
      alert("Error deleting note.", error);
    }
  };
  // const requiredPermissions = Array.isArray(requiredPermission)
  // ? requiredPermission
  // : [requiredPermission];
  // const hasPermission = requiredPermissions.some((perm) =>
  //   permissions.includes(perm)
  // );
  // console.log("filters home", filters);
  // console.log("userPermission", permissions);
  return (
    <div>
      <button className="logout-button" onClick={() => navigate("/logout")}>
        <i className="fa fa-sign-out"></i> Logout
      </button>
      {userPermissions.includes(PERMISSIONS.VIEW_NOTE) && (
        <div>
          <h2>Filters</h2>
          <div className="filter-bar">
            {/* <!-- Search Bar --> */}
            <div className="filter-item">
              <label htmlFor="search">Search:</label>
              <SearchBar onSearch={(query) => setSearchQuery(query)} />
            </div>

            {/* <!-- Categories Dropdown -->s */}
            <div className="filter-item">
              <label htmlFor="categories">Categories:</label>
              <Select
                isMulti
                options={categories}
                classNamePrefix="react-select"
                onChange={(selectedOptions) =>
                  setFilters({
                    ...filters,
                    categories: selectedOptions.map((option) => option.value),
                  })
                }
              />
            </div>

            {/* <!-- Start Date Picker --> */}
            <div className="filter-item">
              <label htmlFor="start-date">Start Date:</label>
              <DatePicker
                selected={filters.dateRange?.start}
                onChange={(date) =>
                  setFilters({
                    ...filters,
                    dateRange: {
                      ...filters.dateRange,
                      start: date.toISOString().split("T")[0],
                    },
                  })
                }
                placeholderText="Start Date"
              />
            </div>

            {/* <!-- End Date Picker --> */}
            <div className="filter-item">
              <label htmlFor="end-date">End Date:</label>
              <DatePicker
                selected={filters.dateRange?.end}
                onChange={(date) =>
                  setFilters({
                    ...filters,
                    dateRange: {
                      ...filters.dateRange,
                      end: date.toISOString().split("T")[0],
                    },
                  })
                }
                placeholderText="End Date"
              />
            </div>
          </div>
          <h2>Notes</h2>
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
      )}

      {userPermissions.includes(PERMISSIONS.VIEW_SURVEY) && (
        <>
          <div>
            <h2>Survey Form</h2>
            <SurveyForm />
          </div>

          <div>
            <h2>Surveys List</h2>
            <SurveyList />
          </div>
        </>
      )}
    </div>
  );
}

export default Home;
