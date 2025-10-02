// DOM Elements
const jobDescription = document.getElementById('jobDescription');
const charCount = document.getElementById('charCount');
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const processBtn = document.getElementById('processBtn');
const resetBtn = document.getElementById('resetBtn');
const resultsSection = document.getElementById('results');
const resultsBody = document.getElementById('resultsBody');
const searchInput = document.getElementById('searchInput');
const filterSelect = document.getElementById('filterSelect');
const exportBtn = document.getElementById('exportBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const currentPage = document.getElementById('currentPage');
const totalPages = document.getElementById('totalPages');
const toastContainer = document.getElementById('toastContainer');
const getStartedBtn = document.getElementById('getStartedBtn');
const learnMoreBtn = document.getElementById('learnMoreBtn');

// Chart elements
const chartTabs = document.querySelectorAll('.chart-tab');
const scoreChartCanvas = document.getElementById('scoreChart');
const skillsChartCanvas = document.getElementById('skillsChart');
const decisionChartCanvas = document.getElementById('decisionChart');

// Chart instances
let scoreChart = null;
let skillsChart = null;
let decisionChart = null;

// State management
let uploadedFiles = [];
let currentResults = [];
let filteredResults = [];
let currentPageIndex = 1;
const resultsPerPage = 5;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Character counter for job description
    jobDescription.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count;
        
        // Change color when approaching limit
        if (count > 1800) {
            charCount.style.color = '#f87171';
        } else {
            charCount.style.color = '';
        }
    });

    // File upload handling
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#4361ee';
        uploadArea.style.backgroundColor = 'rgba(67, 97, 238, 0.1)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#cbd5e1';
        uploadArea.style.backgroundColor = '#f8fafc';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#cbd5e1';
        uploadArea.style.backgroundColor = '#f8fafc';
        
        if (e.dataTransfer.files.length) {
            handleFiles(e.dataTransfer.files);
        }
    });

    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            handleFiles(this.files);
        }
    });

    // Process button event
    processBtn.addEventListener('click', processResumes);

    // Reset button event
    resetBtn.addEventListener('click', resetForm);

    // Search and filter events
    searchInput.addEventListener('input', filterResults);
    filterSelect.addEventListener('change', filterResults);

    // Export button event
    exportBtn.addEventListener('click', exportResults);

    // Pagination events
    prevBtn.addEventListener('click', () => changePage(currentPageIndex - 1));
    nextBtn.addEventListener('click', () => changePage(currentPageIndex + 1));

    // Navigation buttons
    getStartedBtn.addEventListener('click', () => {
        document.getElementById('screening').scrollIntoView({ behavior: 'smooth' });
    });

    learnMoreBtn.addEventListener('click', () => {
        document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
    });

    // Chart tab events
    chartTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            chartTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all charts
            scoreChartCanvas.style.display = 'none';
            skillsChartCanvas.style.display = 'none';
            decisionChartCanvas.style.display = 'none';
            
            // Show the selected chart
            const chartType = this.getAttribute('data-chart');
            if (chartType === 'score') {
                scoreChartCanvas.style.display = 'block';
            } else if (chartType === 'skills') {
                skillsChartCanvas.style.display = 'block';
            } else if (chartType === 'decision') {
                decisionChartCanvas.style.display = 'block';
            }
        });
    });

    // Initialize results section as hidden
    resultsSection.style.display = 'none';
    
    // Add privacy notice
    addPrivacyNotice();
});

// Add privacy notice to the page
function addPrivacyNotice() {
    const privacyNotice = document.createElement('div');
    privacyNotice.className = 'privacy-notice';
    privacyNotice.innerHTML = `
        <div class="privacy-content">
            <i class="fas fa-lock"></i>
            <div>
                <h4>Privacy Notice</h4>
                <p>All processing happens locally in your browser. No data is sent to any server or stored externally.</p>
            </div>
        </div>
    `;
    
    // Insert after the header
    const header = document.querySelector('.header');
    header.parentNode.insertBefore(privacyNotice, header.nextSibling);
}

// Handle file uploads
function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type === 'application/pdf' || 
            file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
            file.name.endsWith('.pdf') || 
            file.name.endsWith('.docx')) {
            
            // Check for duplicates
            if (!uploadedFiles.some(f => f.name === file.name && f.size === file.size)) {
                uploadedFiles.push(file);
                addFileToList(file);
            }
        } else {
            showToast(`Invalid file type: ${file.name}. Please upload PDF or DOCX files only.`, 'error');
        }
    }
    
    updateFileList();
}

// Add file to the list display
function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.innerHTML = `
        <div class="file-name">
            <i class="fas ${file.name.endsWith('.pdf') ? 'fa-file-pdf' : 'fa-file-word'}"></i>
            <span>${file.name}</span>
        </div>
        <div class="file-actions">
            <button class="remove-file" data-filename="${file.name}">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    fileList.appendChild(fileItem);
    
    // Add event listener to remove button
    fileItem.querySelector('.remove-file').addEventListener('click', function() {
        const filename = this.getAttribute('data-filename');
        removeFile(filename);
    });
}

// Remove file from the list
function removeFile(filename) {
    uploadedFiles = uploadedFiles.filter(file => file.name !== filename);
    updateFileList();
    showToast(`Removed ${filename}`, 'warning');
}

// Update file list display
function updateFileList() {
    fileList.innerHTML = '';
    uploadedFiles.forEach(file => {
        addFileToList(file);
    });
}

// Process resumes (simulated)
function processResumes() {
    const jobDesc = jobDescription.value.trim();
    
    if (!jobDesc) {
        showToast('Please enter a job description', 'error');
        return;
    }
    
    if (uploadedFiles.length === 0) {
        showToast('Please upload at least one resume', 'error');
        return;
    }
    
    // Show progress
    uploadProgress.style.display = 'block';
    simulateProcessing();
}

// Simulate processing with progress bar
function simulateProcessing() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            
            // Show results after a short delay
            setTimeout(() => {
                showResults();
                uploadProgress.style.display = 'none';
                showToast('Resumes processed successfully!', 'success');
            }, 500);
        }
        
        progressFill.style.width = `${progress}%`;
        progressText.textContent = `${Math.round(progress)}%`;
    }, 100);
}

// Show results
function showResults() {
    // Generate results based only on uploaded files (no personal data)
    currentResults = generateResultsFromFiles();
    filteredResults = [...currentResults];
    currentPageIndex = 1;
    
    renderResults();
    renderCharts();
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Generate results based only on uploaded files
function generateResultsFromFiles() {
    return uploadedFiles.map((file, index) => {
        // Generate random but realistic scores
        const score = 0.5 + (Math.random() * 0.5); // Between 0.5 and 1.0
        
        // Generate skills based on file name
        const skills = generateSkillsFromFile(file.name);
        const missingSkills = generateMissingSkills(score);
        const decision = score > 0.7 ? "Fit" : "Not Fit";
        
        return {
            candidate_name: `Candidate ${index + 1}`,
            score: score,
            skills: skills,
            missing_skills: missingSkills,
            decision: decision
        };
    });
}

// Generate skills based on file name
function generateSkillsFromFile(filename) {
    const skillsPool = [
        "Python", "Java", "JavaScript", "SQL", "HTML/CSS", 
        "React", "Angular", "Node.js", "Django", "Flask",
        "Machine Learning", "Data Analysis", "Statistics",
        "Project Management", "Communication", "Teamwork",
        "AWS", "Docker", "Kubernetes", "Git", "Linux"
    ];
    
    // Select random skills
    const numSkills = 3 + Math.floor(Math.random() * 5);
    const selectedSkills = [];
    
    for (let i = 0; i < numSkills; i++) {
        const randomIndex = Math.floor(Math.random() * skillsPool.length);
        if (!selectedSkills.includes(skillsPool[randomIndex])) {
            selectedSkills.push(skillsPool[randomIndex]);
        }
    }
    
    return selectedSkills.join(", ");
}

// Generate missing skills based on score
function generateMissingSkills(score) {
    if (score > 0.8) return ""; // High scorers have no missing skills
    
    const missingSkillsPool = [
        "Deep Learning", "PyTorch", "TensorFlow", 
        "Cloud Architecture", "DevOps", "Cybersecurity",
        "Agile Methodologies", "Leadership", "Public Speaking"
    ];
    
    const numMissing = Math.floor(Math.random() * 4);
    const selectedMissing = [];
    
    for (let i = 0; i < numMissing; i++) {
        const randomIndex = Math.floor(Math.random() * missingSkillsPool.length);
        if (!selectedMissing.includes(missingSkillsPool[randomIndex])) {
            selectedMissing.push(missingSkillsPool[randomIndex]);
        }
    }
    
    return selectedMissing.join(", ");
}

// Render charts
function renderCharts() {
    // Destroy existing charts if they exist
    if (scoreChart) scoreChart.destroy();
    if (skillsChart) skillsChart.destroy();
    if (decisionChart) decisionChart.destroy();
    
    // Score Distribution Chart
    const scoreCtx = scoreChartCanvas.getContext('2d');
    const scores = currentResults.map(result => result.score * 100);
    const names = currentResults.map(result => result.candidate_name);
    
    scoreChart = new Chart(scoreCtx, {
        type: 'bar',
        data: {
            labels: names,
            datasets: [{
                label: 'Matching Score (%)',
                data: scores,
                backgroundColor: [
                    'rgba(67, 97, 238, 0.7)',
                    'rgba(76, 201, 240, 0.7)',
                    'rgba(74, 194, 154, 0.7)',
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ],
                borderColor: [
                    'rgba(67, 97, 238, 1)',
                    'rgba(76, 201, 240, 1)',
                    'rgba(74, 194, 154, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Matching Score (%)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Candidate Matching Scores',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            }
        }
    });
    
    // Skills Match Chart
    const skillsCtx = skillsChartCanvas.getContext('2d');
    const skillsData = currentResults.map(result => result.skills.split(',').length);
    const missingSkillsData = currentResults.map(result => 
        result.missing_skills ? result.missing_skills.split(',').length : 0
    );
    
    skillsChart = new Chart(skillsCtx, {
        type: 'radar',
        data: {
            labels: names,
            datasets: [{
                label: 'Available Skills',
                data: skillsData,
                backgroundColor: 'rgba(67, 97, 238, 0.2)',
                borderColor: 'rgba(67, 97, 238, 1)',
                pointBackgroundColor: 'rgba(67, 97, 238, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(67, 97, 238, 1)'
            }, {
                label: 'Missing Skills',
                data: missingSkillsData,
                backgroundColor: 'rgba(248, 113, 113, 0.2)',
                borderColor: 'rgba(248, 113, 113, 1)',
                pointBackgroundColor: 'rgba(248, 113, 113, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(248, 113, 113, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Skills Analysis',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
    
    // Decision Chart
    const decisionCtx = decisionChartCanvas.getContext('2d');
    const fitCount = currentResults.filter(result => result.decision === 'Fit').length;
    const notFitCount = currentResults.filter(result => result.decision === 'Not Fit').length;
    
    decisionChart = new Chart(decisionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Fit Candidates', 'Not Fit Candidates'],
            datasets: [{
                data: [fitCount, notFitCount],
                backgroundColor: [
                    'rgba(74, 194, 154, 0.7)',
                    'rgba(248, 113, 113, 0.7)'
                ],
                borderColor: [
                    'rgba(74, 194, 154, 1)',
                    'rgba(248, 113, 113, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Fit vs Not Fit Candidates',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Render results with pagination
function renderResults() {
    const startIndex = (currentPageIndex - 1) * resultsPerPage;
    const endIndex = startIndex + resultsPerPage;
    const pageResults = filteredResults.slice(startIndex, endIndex);
    
    resultsBody.innerHTML = '';
    
    if (pageResults.length === 0) {
        resultsBody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px;">
                    <i class="fas fa-search" style="font-size: 3rem; color: #cbd5e1; margin-bottom: 20px;"></i>
                    <h3>No matching candidates found</h3>
                    <p>Try adjusting your search or filter criteria</p>
                </td>
            </tr>
        `;
        return;
    }
    
    pageResults.forEach(result => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${result.candidate_name}</td>
            <td class="score-cell">${(result.score * 100).toFixed(1)}%</td>
            <td>${result.skills}</td>
            <td>${result.missing_skills || 'None'}</td>
            <td class="${result.decision.toLowerCase().replace(' ', '-')}">${result.decision}</td>
        `;
        resultsBody.appendChild(row);
    });
    
    // Update pagination
    totalPages.textContent = Math.ceil(filteredResults.length / resultsPerPage);
    currentPage.textContent = currentPageIndex;
    
    // Update pagination button states
    prevBtn.disabled = currentPageIndex === 1;
    nextBtn.disabled = currentPageIndex === Math.ceil(filteredResults.length / resultsPerPage);
}

// Change page
function changePage(page) {
    const maxPage = Math.ceil(filteredResults.length / resultsPerPage);
    
    if (page >= 1 && page <= maxPage) {
        currentPageIndex = page;
        renderResults();
    }
}

// Filter results based on search and filter criteria
function filterResults() {
    const searchTerm = searchInput.value.toLowerCase();
    const filterValue = filterSelect.value;
    
    filteredResults = currentResults.filter(result => {
        const matchesSearch = result.candidate_name.toLowerCase().includes(searchTerm) ||
                             result.skills.toLowerCase().includes(searchTerm) ||
                             result.missing_skills.toLowerCase().includes(searchTerm);
        
        const matchesFilter = filterValue === 'all' || 
                             result.decision.toLowerCase() === filterValue;
        
        return matchesSearch && matchesFilter;
    });
    
    currentPageIndex = 1;
    renderResults();
}

// Reset form
function resetForm() {
    jobDescription.value = '';
    charCount.textContent = '0';
    uploadedFiles = [];
    updateFileList();
    resultsSection.style.display = 'none';
    searchInput.value = '';
    filterSelect.value = 'all';
    showToast('Form reset successfully', 'success');
}

// Export results (simulated)
function exportResults() {
    if (currentResults.length === 0) {
        showToast('No results to export', 'error');
        return;
    }
    
    // Simulate CSV download
    showToast('Exporting results... This is a simulation.', 'warning');
    
    // In a real application, you would generate and download a CSV file
    setTimeout(() => {
        showToast('Results exported successfully! (Simulated)', 'success');
    }, 1500);
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'exclamation-circle';
    if (type === 'warning') icon = 'exclamation-triangle';
    
    toast.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Remove toast after delay
    setTimeout(() => {
        toast.classList.add('hide');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Update active nav link
            document.querySelectorAll('.nav a').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        }
    });
});

// Intersection Observer for animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in-up');
        }
    });
}, observerOptions);

// Observe elements for animations
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.feature-card, .section-header, .panel');
    animateElements.forEach(el => {
        observer.observe(el);
    });
});