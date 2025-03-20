import { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [inputImage, setInputImage] = useState(null);
  const [maskImage, setMaskImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/api/predict/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("Full API Response:", response.data);

      setInputImage(response.data.input_image ? `data:image/png;base64,${response.data.input_image}` : null);
      setMaskImage(response.data.mask_image ? `data:image/png;base64,${response.data.mask_image}` : null);
      setResult(response.data.classes || null);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error processing image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-fluid min-vh-100 d-flex flex-column align-items-center justify-content-center bg-light py-4">
      {/* Main Card for Upload and Button */}
      <div className="card shadow-sm p-4 w-100" style={{ maxWidth: "600px" }}>
        <h1 className="text-center text-primary mb-4">Land Cover Segmentation</h1>
        
        {/* File Input */}
        <div className="mb-3">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange} 
            className="form-control"
          />
        </div>
        
        {/* Upload Button */}
        <button
          onClick={handleUpload}
          className="btn btn-primary w-100 py-2"
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Processing...
            </>
          ) : (
            "Upload & Segment"
          )}
        </button>
      </div>

      {/* Results Section */}
      {result && (
        <div className="card shadow-sm p-3 w-100 mt-4" style={{ maxWidth: "600px" }}>
          <h4 className="text-center text-secondary mb-3">Detected Classes</h4>
          <div className="d-flex flex-wrap justify-content-center gap-2">
            {Object.entries(result).map(([key, value]) => (
              <span key={key} className="badge bg-primary rounded-pill p-2">
                {value} <span className="badge bg-light text-dark ms-2">{key}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Images Section */}
      <div className="row mt-4 g-3 w-100" style={{ maxWidth: "1000px" }}>
        {inputImage && (
          <div className="col-md-6">
            <div className="card shadow-sm h-100">
              <div className="card-body text-center">
                <h5 className="card-title text-secondary mb-3">Input Image</h5>
                <img src={inputImage} alt="Uploaded Input" className="img-fluid rounded" />
              </div>
            </div>
          </div>
        )}
        {maskImage && (
          <div className="col-md-6">
            <div className="card shadow-sm h-100">
              <div className="card-body text-center">
                <h5 className="card-title text-secondary mb-3">Predicted Mask</h5>
                <img src={maskImage} alt="Predicted Mask" className="img-fluid rounded" />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;