import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectsAPI, sectionsAPI, exportAPI } from '../api';

function Editor() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [refiningSection, setRefiningSection] = useState(null);
  const [refinementPrompts, setRefinementPrompts] = useState({});

  useEffect(() => {
    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    try {
      const response = await projectsAPI.getById(projectId);
      setProject(response.data);
    } catch (err) {
      setError('Failed to load project');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateContent = async () => {
    setGenerating(true);
    setError('');
    try {
      const response = await projectsAPI.generateContent(projectId);
      setProject(response.data);
    } catch (err) {
      setError('Failed to generate content');
    } finally {
      setGenerating(false);
    }
  };

  const handleRefine = async (sectionId) => {
    const prompt = refinementPrompts[sectionId];
    if (!prompt || !prompt.trim()) {
      alert('Please enter a refinement prompt');
      return;
    }

    setRefiningSection(sectionId);
    try {
      const response = await sectionsAPI.refine(sectionId, { prompt });
      // Update the section in the project
      const updatedSections = project.sections.map(s =>
        s.id === sectionId ? response.data : s
      );
      setProject({ ...project, sections: updatedSections });
      // Clear the prompt
      setRefinementPrompts({ ...refinementPrompts, [sectionId]: '' });
    } catch (err) {
      alert('Failed to refine content');
    } finally {
      setRefiningSection(null);
    }
  };

  const handleFeedback = async (sectionId, isLiked) => {
    try {
      await sectionsAPI.addFeedback(sectionId, { is_liked: isLiked });
      // Update UI to show feedback was recorded
      alert(`Feedback recorded: ${isLiked ? '👍 Liked' : '👎 Disliked'}`);
    } catch (err) {
      alert('Failed to record feedback');
    }
  };

  const handleAddComment = async (sectionId) => {
    const comment = prompt('Enter your comment:');
    if (comment) {
      try {
        await sectionsAPI.addFeedback(sectionId, { comment });
        alert('Comment saved!');
      } catch (err) {
        alert('Failed to save comment');
      }
    }
  };

  const handleExport = async () => {
    try {
      const response = await exportAPI.exportDocument(projectId);
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      const extension = project.document_type === 'docx' ? 'docx' : 'pptx';
      link.setAttribute('download', `${project.title}.${extension}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to export document');
    }
  };

  if (loading) {
    return <div className="loading">Loading project...</div>;
  }

  if (!project) {
    return <div className="error">Project not found</div>;
  }

  const hasContent = project.sections.some(s => s.content);

  return (
    <div className="container">
      <div className="editor-container">
        <div className="editor-header">
          <div>
            <h2>{project.title}</h2>
            <p style={{ color: '#666', marginTop: '5px' }}>
              {project.document_type === 'docx' ? '📄 Word Document' : '📊 PowerPoint Presentation'}
            </p>
            <p style={{ color: '#888', fontSize: '14px', marginTop: '5px' }}>
              {project.main_topic}
            </p>
          </div>
          <div className="editor-actions">
            <button className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
              ← Back to Dashboard
            </button>
            {!hasContent && (
              <button
                className="btn"
                onClick={handleGenerateContent}
                disabled={generating}
              >
                {generating ? '✨ Generating...' : '✨ Generate Content'}
              </button>
            )}
            {hasContent && (
              <button className="btn" onClick={handleExport}>
                📥 Export Document
              </button>
            )}
          </div>
        </div>

        {error && <div className="error">{error}</div>}

        {!hasContent && !generating && (
          <div style={{ textAlign: 'center', padding: '60px', color: '#666' }}>
            <h3>Ready to generate content</h3>
            <p>Click "Generate Content" to use AI to create content for all sections</p>
          </div>
        )}

        {generating && (
          <div className="loading">
            🤖 AI is generating content for your {project.document_type === 'docx' ? 'document' : 'presentation'}...
            <br />
            This may take a minute.
          </div>
        )}

        {hasContent && (
          <div className="sections-list">
            {project.sections
              .sort((a, b) => a.order - b.order)
              .map((section) => (
                <div key={section.id} className="section-card">
                  <div className="section-header">
                    <h3>{section.title}</h3>
                  </div>

                  <div className={`section-content ${!section.content ? 'empty' : ''}`}>
                    {section.content || 'No content generated yet'}
                  </div>

                  {section.content && (
                    <div className="refinement-panel">
                      <div className="refinement-input">
                        <input
                          type="text"
                          placeholder="Ask AI to refine this content (e.g., 'Make it more formal', 'Add more details')"
                          value={refinementPrompts[section.id] || ''}
                          onChange={(e) =>
                            setRefinementPrompts({
                              ...refinementPrompts,
                              [section.id]: e.target.value,
                            })
                          }
                          disabled={refiningSection === section.id}
                        />
                        <button
                          className="btn btn-small"
                          onClick={() => handleRefine(section.id)}
                          disabled={refiningSection === section.id}
                        >
                          {refiningSection === section.id ? 'Refining...' : 'Refine'}
                        </button>
                      </div>

                      <div className="feedback-buttons">
                        <button
                          className="feedback-btn"
                          onClick={() => handleFeedback(section.id, true)}
                          title="Like this content"
                        >
                          👍
                        </button>
                        <button
                          className="feedback-btn"
                          onClick={() => handleFeedback(section.id, false)}
                          title="Dislike this content"
                        >
                          👎
                        </button>
                        <button
                          className="btn btn-small btn-secondary"
                          onClick={() => handleAddComment(section.id)}
                        >
                          💬 Add Comment
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Editor;
