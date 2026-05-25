document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('ats-form');

    
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resume-file');
    const fileDetails = document.getElementById('file-details');
    const fileNameSpan = document.getElementById('file-name');
    const fileSizeSpan = document.getElementById('file-size');
    const removeFileBtn = document.getElementById('remove-file');
    
    const jdText = document.getElementById('jd-text');
    const clearJdBtn = document.getElementById('clear-jd');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    const resultsEmpty = document.getElementById('results-empty');
    const resultsLoading = document.getElementById('results-loading');
    const resultsError = document.getElementById('results-error');
    const resultsContent = document.getElementById('results-content');
    
    const loaderTitle = document.getElementById('loader-title');
    const loaderText = document.getElementById('loader-text');
    const errorMessage = document.getElementById('error-message');
    const retryBtn = document.getElementById('retry-btn');
    
    const matchPctSpan = document.getElementById('match-pct');
    const scoreLabel = document.getElementById('score-label');
    const gaugeFill = document.getElementById('gauge-fill');
    
    const factorsList = document.getElementById('factors-list');
    const matchingPills = document.getElementById('matching-pills');
    const missingPills = document.getElementById('missing-pills');
    const recommendationSummaryText = document.getElementById('recommendation-summary-text');
    const suggestionsList = document.getElementById('suggestions-list');

    // State Variables
    let selectedFile = null;
    let loadingInterval = null;



    // Drag and Drop Zone Event Listeners
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    // Click to Browse
    dropZone.addEventListener('click', (e) => {
        // Prevent click trigger if they clicked remove file button
        if (e.target.closest('#remove-file') || e.target.closest('#file-details')) {
            return;
        }
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileSelection(fileInput.files[0]);
        }
    });

    // Remove file selection
    removeFileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        resetFileSelection();
    });

    // File selection logic
    function handleFileSelection(file) {
        const allowedExtensions = ['.pdf', '.docx', '.txt'];
        const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        
        if (!allowedExtensions.includes(fileExt)) {
            alert('Unsupported file type. Please upload a PDF, DOCX, or TXT file.');
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert('File size exceeds the 5MB limit.');
            return;
        }

        selectedFile = file;
        fileNameSpan.textContent = file.name;
        fileSizeSpan.textContent = formatBytes(file.size);
        
        // Update UI states
        dropZone.querySelector('.drop-zone-content').classList.add('hidden');
        fileDetails.classList.remove('hidden');
        dropZone.style.borderStyle = 'solid';
        dropZone.style.borderColor = 'var(--primary)';
    }

    function resetFileSelection() {
        selectedFile = null;
        fileInput.value = '';
        dropZone.querySelector('.drop-zone-content').classList.remove('hidden');
        fileDetails.classList.add('hidden');
        dropZone.style.borderStyle = 'dashed';
        dropZone.style.borderColor = 'rgba(255, 255, 255, 0.15)';
    }

    // Clear JD textarea
    clearJdBtn.addEventListener('click', () => {
        jdText.value = '';
        jdText.focus();
    });

    // Format bytes to readable string
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    // Dismiss Error
    retryBtn.addEventListener('click', () => {
        resultsError.classList.add('hidden');
        resultsEmpty.classList.remove('hidden');
    });

    // Form submission / Analyze action
    analyzeBtn.addEventListener('click', async () => {
        // Validation check
        if (!selectedFile) {
            alert('Please upload a resume file (PDF or DOCX).');
            return;
        }

        const jd = jdText.value.trim();
        if (!jd) {
            alert('Please paste a Job Description to compare against.');
            return;
        }

        // Setup dynamic loading phases
        const loadingPhases = [
            { title: "Uploading resume document...", text: "Sending your file to the parsing engine" },
            { title: "Extracting resume text...", text: "Identifying sections, layouts, and structures" },
            { title: "Contacting Gemini AI...", text: "Connecting to the LLM model for processing" },
            { title: "Matching job keywords...", text: "Aligning skills, experience, and education matches" },
            { title: "Simulating ATS criteria...", text: "Running compliance tests and scoring factors" },
            { title: "Generating recommendations...", text: "Assembling specific suggestions for improvement" }
        ];

        // UI Reset and Transition to Loading
        resultsEmpty.classList.add('hidden');
        resultsError.classList.add('hidden');
        resultsContent.classList.add('hidden');
        resultsLoading.classList.remove('hidden');
        
        analyzeBtn.disabled = true;
        analyzeBtn.querySelector('.btn-text').classList.add('hidden');
        analyzeBtn.querySelector('.btn-loader').classList.remove('hidden');

        let phaseIndex = 0;
        const updateLoader = () => {
            if (phaseIndex < loadingPhases.length) {
                loaderTitle.textContent = loadingPhases[phaseIndex].title;
                loaderText.textContent = loadingPhases[phaseIndex].text;
                phaseIndex++;
            }
        };

        updateLoader();
        // Cycle loaders every 2 seconds
        loadingInterval = setInterval(updateLoader, 2000);

        // Prepare request payload
        const formData = new FormData();
        formData.append('resume', selectedFile);
        formData.append('jd', jd);
        
        try {
            const apiBase = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && window.location.port === '8000'
                ? ''
                : 'http://localhost:8000';
            const response = await fetch(`${apiBase}/api/analyze`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            clearInterval(loadingInterval);

            if (!response.ok) {
                throw new Error(data.error || 'Server returned an error during analysis.');
            }

            renderResults(data);

        } catch (error) {
            console.error('Analysis error:', error);
            clearInterval(loadingInterval);
            
            errorMessage.textContent = error.message || 'An unexpected connection error occurred. Please check the backend server terminal and your API key config.';
            resultsLoading.classList.add('hidden');
            resultsError.classList.remove('hidden');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.querySelector('.btn-text').classList.remove('hidden');
            analyzeBtn.querySelector('.btn-loader').classList.add('hidden');
        }
    });

    // Render results on success
    function renderResults(data) {
        // 1. Hide loader, show content
        resultsLoading.classList.add('hidden');
        resultsContent.classList.remove('hidden');

        // 2. Score Gauge Animation
        const score = data.match_percentage || 0;
        
        // Animate number count-up
        let currentScore = 0;
        const countInterval = setInterval(() => {
            if (currentScore >= score) {
                matchPctSpan.textContent = score;
                clearInterval(countInterval);
            } else {
                currentScore++;
                matchPctSpan.textContent = currentScore;
            }
        }, 12);

        // Score description label HSL tailoring
        scoreLabel.textContent = getScoreLabelText(score);
        scoreLabel.style.color = getScoreColor(score);

        // SVG circle gauge stroke transition
        // circumference is 2 * PI * r = 2 * PI * 40 = 251.327
        const radius = 40;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (score / 100) * circumference;
        
        // Update color and fill offset
        gaugeFill.style.stroke = getScoreColor(score);
        gaugeFill.style.strokeDashoffset = offset;

        // 3. ATS Factors Progress Bars
        factorsList.innerHTML = '';
        if (data.ats_score_factors && typeof data.ats_score_factors === 'object') {
            Object.entries(data.ats_score_factors).forEach(([factor, factorScore]) => {
                const item = document.createElement('div');
                item.className = 'factor-item';
                
                item.innerHTML = `
                    <div class="factor-info">
                        <span class="factor-name">${escapeHtml(factor)}</span>
                        <span class="factor-value">${factorScore}%</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: 0%; background: linear-gradient(90deg, var(--primary) 0%, ${getScoreColor(factorScore)} 100%)"></div>
                    </div>
                `;
                factorsList.appendChild(item);
                
                // Trigger width transition on next animation frame
                requestAnimationFrame(() => {
                    item.querySelector('.progress-bar-fill').style.width = `${factorScore}%`;
                });
            });
        } else {
            factorsList.innerHTML = '<p class="text-muted">No details provided.</p>';
        }

        // 4. Matching Skills Pills
        matchingPills.innerHTML = '';
        if (data.matching_skills && data.matching_skills.length > 0) {
            data.matching_skills.forEach(skill => {
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = skill;
                matchingPills.appendChild(pill);
            });
        } else {
            matchingPills.innerHTML = '<span class="text-muted">No overlapping skills found. Match structure is low.</span>';
        }

        // 5. Missing Skills Pills
        missingPills.innerHTML = '';
        if (data.missing_skills && data.missing_skills.length > 0) {
            data.missing_skills.forEach(skill => {
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = skill;
                missingPills.appendChild(pill);
            });
        } else {
            missingPills.innerHTML = '<span class="text-muted">Excellent! No major missing skills identified.</span>';
        }

        // 6. Recommendation Summary
        recommendationSummaryText.textContent = data.recommendation_summary || 'No summary evaluation provided.';

        // 7. Actionable Suggestions Checklist
        suggestionsList.innerHTML = '';
        if (data.improvement_suggestions && data.improvement_suggestions.length > 0) {
            data.improvement_suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.className = 'checklist-item';
                li.innerHTML = `
                    <div class="checkbox-bullet">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                    </div>
                    <span>${escapeHtml(suggestion)}</span>
                `;
                suggestionsList.appendChild(li);
            });
        } else {
            suggestionsList.innerHTML = '<li class="checklist-item"><div class="checkbox-bullet"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div><span>No improvements required! Your resume matches the job description parameters perfectly.</span></li>';
        }

        // Scroll to results section smoothly
        resultsContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Helper functions
    function getScoreLabelText(score) {
        if (score >= 85) return 'Strong Match';
        if (score >= 70) return 'Good Match';
        if (score >= 50) return 'Moderate Match';
        return 'Weak Match';
    }

    function getScoreColor(score) {
        if (score >= 85) return '#10b981'; // success (green)
        if (score >= 70) return '#6366f1'; // primary (indigo)
        if (score >= 50) return '#f59e0b'; // warning (amber)
        return '#f43f5e'; // error (rose)
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
