import { useState, useEffect } from "react";
import api from "../api";
import Note from "../components/Note"
// import Note from "../components/Note"
import SearchBar from "../components/SearchBar"
import "../styles/Home.css"
import { useNavigate } from "react-router-dom";
import Select from 'react-select';

function Home() {
    const [notes, setNotes] = useState([]);
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");
    const [categories, setCategories] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [file, setFile] = useState(null); 

    const [searchQuery, setSearchQuery] = useState("");

    const navigate = useNavigate();



   

    // const fetchNotes = () => {
    //     api
    //         .get("/api/notes/")
    //         .then((res) => res.data)
    //         .then((data) => {
    //             setNotes(data);
    //             console.log(data);
    //         })
    //         .catch((err) => alert(err));
    // };


      // Fonction pour récupérer les notes
  const fetchNotes = (query = "") => {
    const url = query ? `/api/notes/?search=${query}` : '/api/notes/';
    api.get(url, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`, // Authentification si nécessaire
      }
    })
    .then(response => setNotes(response.data))
    .catch(error => console.error(error));
  };

  useEffect(() => {
    fetchNotes(searchQuery); // Récupère les notes à chaque changement de recherche
  }, [searchQuery]);


    const getCategories = async () => {
       await api
            .get("/api/categories/")
            .then((res) => res.data)
            .then((data) => {
              const categoryOptions = data.map((category) => ({
                value: category.id,
                label: category.name,
              }));
                setCategories(categoryOptions);
                console.log(data);
            })
            .catch((err) => alert(err));


            // const categoryOptions = await response.data.map(category => ({
            //   value: category.id,
            //   label: category.name,
            // }));
            // setCategories(categoryOptions);
            console.log('cat', categories)
          };

          useEffect(() => {
            getCategories();
        }, []);
  

          const handleCategoryChange = (selectedOptions) => {
            console.log('handle')
            const selectedIds = selectedOptions ? selectedOptions.map(option => option.value) : [];
            setSelectedCategories(selectedIds); // Update the selected categories state with the category IDs
          };

      const handleFileChange = (e) => {
        setFile(e.target.files[0]); // Récupère le fichier sélectionné
      };
    const deleteNote = (id) => {
        api
            .delete(`/api/notes/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Note deleted!");
                else alert("Failed to delete note.");
                fetchNotes();
            })
            .catch((error) => alert(error));
    };

    const createNote = async (e) => {


      const formData = new FormData();
      formData.append("title", title); // Add title
      formData.append("content", content); 
      if(file){
      formData.append("file", file); // Add the file (ensure 'file' is from a file input)
      }
      selectedCategories.forEach((id) => {
          formData.append("categories", id);
      });
      console.log('selectedCat',formData, title, content, selectedCategories)
        e.preventDefault();
        try {
          const response = await api.post("/api/notes/", formData, {
              headers: {
                  "Content-Type": "multipart/form-data", // Axios will handle the boundary
              },
          });
  
          if (response.status === 201) {
              alert("Note created!");
              fetchNotes(); // Refresh notes after creating
          } else {
              alert("Failed to create note.");
          }
      } catch (error) {
          console.error("Error creating note:", error);
          alert("Error creating note.");
      }
    };
console.log('notes', notes);
   return (
    <>
    <div>
        <div>
            <button onClick={() => navigate("/logout")}>Logout</button>
        </div>
            <div>
                <h2>Notes</h2>
                <SearchBar onSearch={(query) => setSearchQuery(query)} />
        <div className="notes-container">
                {notes.map((note) => (
                    <Note note={note} onDelete={deleteNote} key={note.id} />
                ))}
        </div>

            </div>
            <h2>Create a Note</h2>
            <form onSubmit={createNote}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="content">Content:</label>
                <br />
                <textarea
                    id="content"
                    name="content"
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                ></textarea>
                <br />

                  <div>
        <label>Fichier</label>
        <input 
          type="file" 
          onChange={handleFileChange} 
        />
      </div>
                <br />
                <div>
                <label htmlFor="categories">Categories</label>
                <Select
          isMulti
          options={categories} // Categories to be displayed in Select
          onChange={handleCategoryChange} // Handler for category selection
          value={categories.filter(cat => selectedCategories.includes(cat.value))} // Controlled value based on selected categories
        />
              {/* <select
                id="categories"
                multiple 
                value={selectedCategories}
                // checked={selectedCategories.includes(category.id)}
            onChange={handleCategoryChange}
              >
                 {categories.map(category => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select> */}
        </div>
              
                <input type="submit" value="Submit"></input>
            </form>
        </div>
        </>
    );
}

export default Home;


