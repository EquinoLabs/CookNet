// components/CreatePostForm.jsx
import React, { useState } from 'react';
import { Camera, Video, X } from 'lucide-react';

const CreatePostForm = ({ onPostCreated, onClose }) => {
  const [formData, setFormData] = useState({
    content: '',
    recipe_title: '',
    ingredients: '',
    instructions: '',
    cooking_time: '',
    servings: '',
    difficulty: '',
    cuisine_type: '',
    is_public: true
  });
  
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => setImagePreview(e.target.result);
      reader.readAsDataURL(file);
      
      // Clear video if image is selected
      setSelectedVideo(null);
    }
  };

  const handleVideoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedVideo(file);
      // Clear image if video is selected
      setSelectedImage(null);
      setImagePreview(null);
    }
  };

  const removeMedia = () => {
    setSelectedImage(null);
    setSelectedVideo(null);
    setImagePreview(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Create FormData for multipart/form-data
      const formDataToSend = new FormData();
      
      // Add text fields
      Object.keys(formData).forEach(key => {
        if (formData[key] !== '' && formData[key] !== null) {
          formDataToSend.append(key, formData[key]);
        }
      });
      
      // Add media files
      if (selectedImage) {
        formDataToSend.append('image', selectedImage);
      }
      if (selectedVideo) {
        formDataToSend.append('video', selectedVideo);
      }

      const response = await fetch('/api/posts', {
        method: 'POST',
        body: formDataToSend,
        credentials: 'include'
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create post');
      }

      const newPost = await response.json();
      
      // Reset form
      setFormData({
        content: '',
        recipe_title: '',
        ingredients: '',
        instructions: '',
        cooking_time: '',
        servings: '',
        difficulty: '',
        cuisine_type: '',
        is_public: true
      });
      setSelectedImage(null);
      setSelectedVideo(null);
      setImagePreview(null);
      
      // Notify parent component
      onPostCreated?.(newPost);
      onClose?.();
      
    } catch (error) {
      console.error('Error creating post:', error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-post-form">
      <div className="form-header">
        <h2>Create New Recipe Post</h2>
        {onClose && (
          <button onClick={onClose} className="close-btn">
            <X size={24} />
          </button>
        )}
      </div>

      <form onSubmit={handleSubmit}>
        {/* Media Upload Section */}
        <div className="media-section">
          {imagePreview ? (
            <div className="media-preview">
              <img src={imagePreview} alt="Preview" />
              <button type="button" onClick={removeMedia} className="remove-media">
                <X size={20} />
              </button>
            </div>
          ) : selectedVideo ? (
            <div className="media-preview">
              <video controls>
                <source src={URL.createObjectURL(selectedVideo)} type={selectedVideo.type} />
              </video>
              <button type="button" onClick={removeMedia} className="remove-media">
                <X size={20} />
              </button>
            </div>
          ) : (
            <div className="media-upload-buttons">
              <label className="upload-btn">
                <Camera size={20} />
                Add Photo
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  style={{ display: 'none' }}
                />
              </label>
              <label className="upload-btn">
                <Video size={20} />
                Add Video
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleVideoChange}
                  style={{ display: 'none' }}
                />
              </label>
            </div>
          )}
        </div>

        {/* Recipe Details */}
        <div className="form-group">
          <input
            type="text"
            name="recipe_title"
            placeholder="Recipe Title (e.g., Chocolate Chip Cookies)"
            value={formData.recipe_title}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <textarea
            name="content"
            placeholder="Tell us about your recipe..."
            value={formData.content}
            onChange={handleInputChange}
            className="form-textarea"
            rows="3"
          />
        </div>

        <div className="form-row">
          <select
            name="difficulty"
            value={formData.difficulty}
            onChange={handleInputChange}
            className="form-select"
          >
            <option value="">Select Difficulty</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          <input
            type="number"
            name="cooking_time"
            placeholder="Cooking Time (min)"
            value={formData.cooking_time}
            onChange={handleInputChange}
            className="form-input"
            min="1"
          />

          <input
            type="number"
            name="servings"
            placeholder="Servings"
            value={formData.servings}
            onChange={handleInputChange}
            className="form-input"
            min="1"
          />
        </div>

        <div className="form-group">
          <input
            type="text"
            name="cuisine_type"
            placeholder="Cuisine Type (e.g., Italian, Mexican)"
            value={formData.cuisine_type}
            onChange={handleInputChange}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <textarea
            name="ingredients"
            placeholder="Ingredients (one per line)&#10;• 2 cups flour&#10;• 1 cup sugar&#10;• 3 eggs"
            value={formData.ingredients}
            onChange={handleInputChange}
            className="form-textarea"
            rows="4"
          />
        </div>

        <div className="form-group">
          <textarea
            name="instructions"
            placeholder="Instructions&#10;1. Preheat oven to 350°F&#10;2. Mix dry ingredients&#10;3. Add wet ingredients..."
            value={formData.instructions}
            onChange={handleInputChange}
            className="form-textarea"
            rows="5"
          />
        </div>

        <div className="form-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="is_public"
              checked={formData.is_public}
              onChange={handleInputChange}
            />
            Make this post public
          </label>
        </div>

        <div className="form-actions">
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Creating Post...' : 'Share Recipe'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreatePostForm;
