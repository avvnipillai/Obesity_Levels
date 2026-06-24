// ========================================================================
// FORM HANDLING & PREDICTION
// ========================================================================

const form = document.getElementById('assessmentForm');
const submitBtn = document.getElementById('submitBtn');
const resultsSection = document.getElementById('resultsSection');
const assessmentSection = document.getElementById('assessmentSection');

// Update range slider labels in real-time
const ranges = document.querySelectorAll('input[type="range"]');
ranges.forEach(range => {
    range.addEventListener('input', (e) => {
        const valueDisplay = document.getElementById(`${e.target.id}Value`);
        if (valueDisplay) {
            const value = parseFloat(e.target.value).toFixed(1);
            valueDisplay.textContent = `${value}x`;
        }
    });
});

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    // Validate required fields
    if (!validateForm(data)) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    btnText.style.display = 'none';
    btnLoader.style.display = 'flex';

    try {
        // Send prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const result = await response.json();

        if (result.success) {
            displayResults(result);
        } else {
            showNotification(result.error || 'An error occurred', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error making prediction. Please try again.', 'error');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});

// Form validation
function validateForm(data) {
    const required = [
        'gender', 'age', 'height', 'weight',
        'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP', 'CAEC',
        'CH2O', 'CALC', 'SMOKE', 'SCC', 'FAF', 'TUE', 'MTRANS'
    ];

    for (let field of required) {
        if (!data[field] || data[field].toString().trim() === '') {
            console.warn(`Missing field: ${field}`);
            return false;
        }
    }

    // Validate numeric fields
    const numFields = {
        age: { min: 1, max: 120 },
        height: { min: 0.5, max: 3 },
        weight: { min: 20, max: 300 },
        FCVC: { min: 0, max: 5 },
        NCP: { min: 1, max: 5 },
        CH2O: { min: 0, max: 10 },
        FAF: { min: 0, max: 10 },
        TUE: { min: 0, max: 16 }
    };

    for (let [field, limits] of Object.entries(numFields)) {
        const value = parseFloat(data[field]);
        if (isNaN(value) || value < limits.min || value > limits.max) {
            console.warn(`Invalid value for ${field}: ${value}`);
            return false;
        }
    }

    return true;
}

// Display results
function displayResults(result) {
    const prediction = result.prediction;
    const bmi = result.bmi;
    const probabilities = result.probabilities;
    const recommendations = result.recommendations;

    // Hide form, show results
    assessmentSection.style.display = 'none';
    resultsSection.style.display = 'block';

    // Update result card
    const resultCard = document.getElementById('resultCard');
    resultCard.style.borderLeftColor = getColorForRisk(prediction.risk_level);

    document.getElementById('resultTitle').textContent = prediction.name;
    document.getElementById('resultRisk').textContent = prediction.risk_level;
    document.getElementById('resultRisk').className = `result-risk risk-${prediction.risk_level.toLowerCase().replace(/\s+/g, '-')}`;
    document.getElementById('resultMessage').textContent = prediction.message;

    // Update BMI display
    document.getElementById('bmiValue').textContent = bmi;
    document.getElementById('bmiStatus').textContent = prediction.name;

    // Display probability bars
    displayProbabilities(probabilities);

    // Display recommendations
    displayRecommendations(recommendations);

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        window.animateProgressBars();
    }, 100);
}

// Display probability chart
function displayProbabilities(probabilities) {
    const container = document.getElementById('probabilityBars');
    container.innerHTML = '';

    const obesityLevels = [
        'Insufficient Weight',
        'Normal Weight',
        'Overweight Level I',
        'Overweight Level II',
        'Obesity Type I',
        'Obesity Type II',
        'Obesity Type III'
    ];

    const entries = Object.entries(probabilities).map(([key, value]) => ({
        label: key,
        value: (value * 100).toFixed(1)
    })).sort((a, b) => b.value - a.value);

    entries.forEach(entry => {
        const bar = document.createElement('div');
        bar.className = 'probability-bar';
        bar.innerHTML = `
            <div class="bar-label">${entry.label}</div>
            <div class="bar-background">
                <div class="bar-fill" style="width: ${entry.value}%"></div>
            </div>
            <div class="bar-value">${entry.value}%</div>
        `;
        container.appendChild(bar);
    });
}

// Display recommendations
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '';

    recommendations.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.style.animation = 'slideInLeft 0.6s ease-out backwards';

        let suggestionsHTML = '<ul>';
        rec.suggestions.forEach(suggestion => {
            suggestionsHTML += `<li>${suggestion}</li>`;
        });
        suggestionsHTML += '</ul>';

        card.innerHTML = `
            <h4>${rec.title}</h4>
            ${suggestionsHTML}
        `;
        container.appendChild(card);
    });
}

// Get color for risk level
function getColorForRisk(riskLevel) {
    const colors = {
        'healthy': '#10b981',
        'low': '#3b82f6',
        'moderate': '#f59e0b',
        'moderate-high': '#f97316',
        'high': '#ef4444',
        'very-high': '#dc2626',
        'critical': '#7f1d1d'
    };
    return colors[riskLevel.toLowerCase().replace(/\s+/g, '-')] || '#6366f1';
}

// Add CSS for risk level styling
const style = document.createElement('style');
style.textContent = `
    .result-risk {
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        color: white;
    }

    .risk-healthy {
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
    }

    .risk-low {
        background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
    }

    .risk-moderate {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
    }

    .risk-moderate-high {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    }

    .risk-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }

    .risk-very-high {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }

    .risk-critical {
        background: linear-gradient(135deg, #7f1d1d 0%, #5a1010 100%);
    }
`;
document.head.appendChild(style);

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        background: ${type === 'error' ? '#ef4444' : '#10b981'};
        color: white;
        font-weight: 600;
        z-index: 1000;
        animation: slideInLeft 0.3s ease-out;
        max-width: 400px;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(30px);
        }
    }
`;
document.head.appendChild(notificationStyle);

// Modify assessment button - allow going back
function resetForm() {
    form.reset();
    resultsSection.style.display = 'none';
    assessmentSection.style.display = 'block';
    document.getElementById('scaleValue').textContent = '0';
}

// Export for use in other scripts
window.resetForm = resetForm;
window.showNotification = showNotification;
