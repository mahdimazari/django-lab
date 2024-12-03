import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSearch = (e) => {
    setQuery(e.target.value);
    onSearch(e.target.value); // Appelle la fonction parent avec le texte recherché
  };

  return (
    
      <input
        type="text"
        value={query}
        onChange={handleSearch}
        placeholder="Rechercher des notes..."
        style={{
          padding: '10px',
          width: '50%',
          borderRadius: '5px',
          border: '1px solid #ccc',
          marginBottom: '20px'
        }}
      />
    
  );
};

export default SearchBar;