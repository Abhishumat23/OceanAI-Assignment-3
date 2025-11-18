import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectsAPI } from '../api';
import CreateProjectModal from './CreateProjectModal';

function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      setError('Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (projectId) => {
    navigate(`/editor/${projectId}`);
  };

  const handleDeleteProject = async (e, projectId) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await projectsAPI.delete(projectId);
        setProjects(projects.filter(p => p.id !== projectId));
      } catch (err) {
        alert('Failed to delete project');
      }
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) {
    return <div className="loading">Loading projects...</div>;
  }

  return (
    <div className="container">
      <div className="dashboard">
        <div className="dashboard-header">
          <h2>My Projects</h2>
          <button className="btn" onClick={() => setShowModal(true)}>
            + New Project
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {projects.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '60px', color: '#666' }}>
            <h3>No projects yet</h3>
            <p>Click "New Project" to create your first document</p>
          </div>
        ) : (
          <div className="projects-grid">
            {projects.map((project) => (
              <div
                key={project.id}
                className="project-card"
                onClick={() => handleProjectClick(project.id)}
              >
                <span className="project-type">
                  {project.document_type === 'docx' ? '📄 Word' : '📊 PowerPoint'}
                </span>
                <h3>{project.title}</h3>
                <p className="project-topic">{project.main_topic}</p>
                <p className="project-date">
                  Created: {formatDate(project.created_at)}
                </p>
                <div className="project-actions">
                  <button
                    className="btn btn-small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleProjectClick(project.id);
                    }}
                  >
                    Open
                  </button>
                  <button
                    className="btn btn-small btn-secondary"
                    onClick={(e) => handleDeleteProject(e, project.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <CreateProjectModal
          onClose={() => setShowModal(false)}
          onProjectCreated={(project) => {
            setShowModal(false);
            navigate(`/editor/${project.id}`);
          }}
        />
      )}
    </div>
  );
}

export default Dashboard;
