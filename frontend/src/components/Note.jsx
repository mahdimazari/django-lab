import React from "react";
import "../styles/Note.css";
import { Button } from "@mui/material";

// type CategoryType =  { value?: string; label?: string; };

function Note({ note, onDelete, key, categories }) {
  const formattedDate = new Date(note.created_at).toLocaleDateString("en-US");
  const getSelectedCategoryLabels = (selectedIds, categories) => {
    return selectedIds
      .map((id) => categories.find((category) => category.value === id)?.label)
      .filter(Boolean); // Filter out undefined values
  };
  // console.log("categories note", categories, note.categories);
  return (
    <div className="note-card" key={key}>
      <p className="note-title">Title: {note.title}</p>
      <p className="note-content">Content: {note.content}</p>
      <p>
        Categories:{" "}
        {getSelectedCategoryLabels(note.categories, categories)
          .map((cat) => cat)
          .join(", ")}
      </p>
      {note.file && (
        <p>
          attachement:{" "}
          <a href={note.file} target="_blank" rel="noopener noreferrer">
            View File
          </a>
        </p>
      )}
      <p className="note-date">Created: {formattedDate}</p>
      <Button
        variant="contained"
        color="error"
        onClick={() => onDelete(note.id)}
      >
        Delete
      </Button>
      {/* <Button variant="contained" color="error" >Contained</Button> */}
    </div>
  );
}

export default Note;
