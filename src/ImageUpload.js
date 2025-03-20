import React, { useState } from "react";
import axios from "axios";

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) return alert("Please select an image");

        const formData = new FormData();
        formData.append("image", file);

        setLoading(true);
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData);
            setResult(response.data.output);
        } catch (error) {
            console.error("Upload failed", error);
            alert("Upload failed");
        }
        setLoading(false);
    };

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h2>Upload Image for Prediction</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Uploading..." : "Upload"}
            </button>
            {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
        </div>
    );
};

export default ImageUpload;
