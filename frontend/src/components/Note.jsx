import React from "react";
import "../styles/Note.css"
import { Button }  from '@mui/material'

function Note({ note, onDelete, key }) {
    const formattedDate = new Date(note.created_at).toLocaleDateString("en-US")

    return (
            <div className="note-card" key={key}>
            <p className="note-title">Title: {note.title}</p>
            <p className="note-content">Content: {note.content}</p>
            <p>Categories: {note.categories.map(cat => cat).join(', ')}</p>
            {note.file && (
            <p>
              attachement: <a href={note.file} target="_blank" rel="noopener noreferrer">View File</a>
            </p>
            )}
            <p className="note-date">Created: {formattedDate}</p>
            <Button variant="contained" color="error" onClick={() => onDelete(note.id)}>
                Delete
            </Button>
            {/* <Button variant="contained" color="error" >Contained</Button> */}
            </div>

    );
}

export default Note