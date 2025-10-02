# Resume Screening Frontend

A modern, dynamic frontend for the Resume Screening with NLP application built with HTML, CSS, and JavaScript.

## Privacy & Security

**Your data stays private**: All processing happens locally in your browser. No personal data is sent to any server or stored externally. The application only uses the job description and resume files you upload for matching analysis, and all data is automatically cleared when you refresh or close the page.

## Features

- **Modern UI Design**: Clean, responsive interface with gradient backgrounds and card-based layout
- **Animations & Transitions**: Smooth animations for elements appearing on screen
- **Interactive Components**: 
  - Drag and drop file uploads
  - Real-time character counter for job descriptions
  - Progress indicators
  - Search and filter functionality
  - Toast notifications
- **Data Visualization**: 
  - Interactive charts for matching scores
  - Skills analysis radar chart
  - Fit/Not Fit distribution doughnut chart
- **Privacy Focused**: 
  - All processing happens locally in the browser
  - No data is sent to external servers
  - Automatic data clearing on page refresh/close
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dynamic Results Display**: Paginated results table with sorting capabilities

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── styles.css          # Styling and animations
├── script.js           # JavaScript functionality
├── server.py           # Simple HTTP server
└── run_frontend.bat    # Windows batch script to run the frontend
```

## How to Run

### Option 1: Using the batch script (Windows)
Double-click on `run_frontend.bat` to start the server and open the application in your browser.

### Option 2: Manual execution
1. Open a terminal/command prompt
2. Navigate to the frontend directory:
   ```
   cd path/to/resume-screening/frontend
   ```
3. Run the server:
   ```
   python server.py
   ```
4. Open your browser and go to http://localhost:8001

## Key Components

### 1. Hero Section
- Animated background with floating elements
- Call-to-action buttons with hover effects

### 2. Screening Section
- Job description text area with character counter
- Drag-and-drop resume upload area
- File list with remove functionality
- Progress bar during processing

### 3. Results Section
- **Interactive Charts**:
  - Bar chart showing matching scores for each candidate
  - Radar chart comparing available vs missing skills
  - Doughnut chart showing fit vs not fit distribution
- Searchable and filterable results table
- Paginated display of candidates
- Color-coded fit decisions
- Export functionality

### 4. Features Section
- Animated feature cards with icons
- Responsive grid layout

### 5. About Section
- Process diagram showing how the application works
- Technology stack display

## Animations Included

- **Float Animation**: Floating elements in the hero section
- **Pop In**: Elements that scale in when appearing
- **Fade In**: Smooth opacity transitions
- **Slide Up**: Elements that slide up when appearing
- **Fade In Up**: Combination of fade and slide effects
- **Hover Effects**: Interactive elements with hover states

## Responsive Design

The frontend is fully responsive and adapts to different screen sizes:
- Desktop: Multi-column layout with full functionality
- Tablet: Adjusted grid layouts and spacing
- Mobile: Single column layout with touch-friendly elements

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Customization

You can easily customize the frontend by modifying:
- **Colors**: Update CSS variables in `:root`
- **Fonts**: Change font family in the CSS
- **Animations**: Adjust timing and effects in the CSS
- **Content**: Edit HTML directly
- **Functionality**: Modify JavaScript behavior

## Integration with Backend

This frontend is designed to work with the Python backend. To connect:
1. Update the JavaScript API calls in `script.js` to point to your backend endpoints
2. Modify the form submission to send data to your Python application
3. Update the results display to show actual data from your backend

## License

This frontend is part of the Resume Screening with NLP project and is licensed under the MIT License.