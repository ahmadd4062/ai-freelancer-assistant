{% extends 'base.html' %}
{% block title %}Edit Proposal - AI Freelancer Assistant{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <h1 class="mb-4">Edit Proposal</h1>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <form method="POST" action="{% url 'proposal_edit' proposal.pk %}">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="client_name" class="form-label">Client Name *</label>
                            <input type="text" name="client_name" class="form-control" id="client_name" value="{{ proposal.client_name }}" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="project_title" class="form-label">Project Title *</label>
                            <input type="text" name="project_title" class="form-control" id="project_title" value="{{ proposal.project_title }}" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="project_description" class="form-label">Project Description *</label>
                            <textarea name="project_description" class="form-control" id="project_description" rows="4" required>{{ proposal.project_description }}</textarea>
                        </div>
                        
                        <div class="mb-3">
                            <label for="skills" class="form-label">Skills (comma separated) *</label>
                            <input type="text" name="skills" class="form-control" id="skills" value="{{ proposal.skills }}" required>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="budget" class="form-label">Budget ($) *</label>
                                <input type="number" name="budget" class="form-control" id="budget" step="0.01" value="{{ proposal.budget }}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="timeline" class="form-label">Timeline *</label>
                                <input type="text" name="timeline" class="form-control" id="timeline" value="{{ proposal.timeline }}" required>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="tone" class="form-label">Tone</label>
                            <select name="tone" class="form-select" id="tone">
                                <option value="professional" {% if proposal.tone == 'professional' %}selected{% endif %}>Professional</option>
                                <option value="casual" {% if proposal.tone == 'casual' %}selected{% endif %}>Casual</option>
                                <option value="friendly" {% if proposal.tone == 'friendly' %}selected{% endif %}>Friendly</option>
                                <option value="persuasive" {% if proposal.tone == 'persuasive' %}selected{% endif %}>Persuasive</option>
                            </select>
                        </div>
                        
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="{% url 'proposal_detail' proposal.pk %}" class="btn btn-secondary">Cancel</a>
                            <button type="submit" class="btn btn-primary">Update Proposal</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="fas fa-lightbulb"></i> Tips</h5>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-success"></i> Update project details</li>
                        <li class="mb-2"><i class="fas fa-check text-success"></i> Modify skills if needed</li>
                        <li class="mb-2"><i class="fas fa-check text-success"></i> Adjust budget or timeline</li>
                        <li class="mb-2"><i class="fas fa-check text-success"></i> Change tone for different clients</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}