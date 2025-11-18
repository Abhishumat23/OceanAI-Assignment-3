import React, { useState } from 'react';
import { projectsAPI } from '../api';

function CreateProjectModal({ onClose, onProjectCreated }) {
  const [step, setStep] = useState(1);
  const [title, setTitle] = useState('');
  const [documentType, setDocumentType] = useState('docx');
  const [mainTopic, setMainTopic] = useState('');
  const [sections, setSections] = useState([
    { title: '', order: 0 },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleNext = () => {
    if (step === 1) {
      if (!title || !documentType || !mainTopic) {
        setError('Please fill in all fields');
        return;
      }
    }
    setError('');
    setStep(step + 1);
  };

  const handleBack = () => {
    setStep(step - 1);
    setError('');
  };

  const addSection = () => {
    setSections([...sections, { title: '', order: sections.length }]);
  };

  const removeSection = (index) => {
    const newSections = sections.filter((_, i) => i !== index);
    // Update order
    newSections.forEach((section, i) => {
      section.order = i;
    });
    setSections(newSections);
  };

  const updateSection = (index, title) => {
    const newSections = [...sections];
    newSections[index].title = title;
    setSections(newSections);
  };

  const handleCreate = async () => {
    // Validate sections
    const validSections = sections.filter(s => s.title.trim());
    if (validSections.length === 0) {
      setError('Please add at least one section');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await projectsAPI.create({
        title,
        document_type: documentType,
        main_topic: mainTopic,
        sections: validSections,
      });
      onProjectCreated(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        {step === 1 && (
          <>
            <h3>Create New Project - Step 1</h3>
            {error && <div className="error">{error}</div>}
            <div className="form-group">
              <label>Project Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., Q4 Business Report"
              />
            </div>
            <div className="form-group">
              <label>Document Type</label>
              <select
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
              >
                <option value="docx">Microsoft Word (.docx)</option>
                <option value="pptx">Microsoft PowerPoint (.pptx)</option>
              </select>
            </div>
            <div className="form-group">
              <label>Main Topic / Prompt</label>
              <textarea
                value={mainTopic}
                onChange={(e) => setMainTopic(e.target.value)}
                placeholder="Describe what this document should be about..."
                rows="4"
              />
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button className="btn" onClick={handleNext}>
                Next
              </button>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <h3>Create New Project - Step 2</h3>
            <p style={{ marginBottom: '20px', color: '#666' }}>
              Define the structure of your {documentType === 'docx' ? 'document' : 'presentation'}
            </p>
            {error && <div className="error">{error}</div>}
            <div className="sections-config">
              {sections.map((section, index) => (
                <div key={index} className="section-input">
                  <input
                    type="text"
                    value={section.title}
                    onChange={(e) => updateSection(index, e.target.value)}
                    placeholder={
                      documentType === 'docx'
                        ? `Section ${index + 1} heading...`
                        : `Slide ${index + 1} title...`
                    }
                  />
                  {sections.length > 1 && (
                    <button onClick={() => removeSection(index)}>Remove</button>
                  )}
                </div>
              ))}
              <button className="add-section-btn" onClick={addSection}>
                + Add {documentType === 'docx' ? 'Section' : 'Slide'}
              </button>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={handleBack}>
                Back
              </button>
              <button className="btn" onClick={handleCreate} disabled={loading}>
                {loading ? 'Creating...' : 'Create Project'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default CreateProjectModal;
