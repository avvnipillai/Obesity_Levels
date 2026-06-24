// ========================================================================
// ANALYSIS PAGE - CHARTS & DATA VISUALIZATION
// ========================================================================

// Chart color schemes
const chartColors = {
    primary: '#6366f1',
    secondary: '#ec4899',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
    gradients: [
        { bg: 'rgba(99, 102, 241, 0.1)', border: '#6366f1' },
        { bg: 'rgba(236, 72, 153, 0.1)', border: '#ec4899' },
        { bg: 'rgba(16, 185, 129, 0.1)', border: '#10b981' },
        { bg: 'rgba(245, 158, 11, 0.1)', border: '#f59e0b' },
        { bg: 'rgba(59, 130, 246, 0.1)', border: '#3b82f6' },
        { bg: 'rgba(239, 68, 68, 0.1)', border: '#ef4444' },
        { bg: 'rgba(139, 92, 246, 0.1)', border: '#8b5cf6' }
    ]
};

// Initialize all charts
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    initializeStats();
});

function initializeCharts() {
    // Chart 1: Obesity Distribution
    const obesityCtx = document.getElementById('obesityChart');
    if (obesityCtx) {
        new Chart(obesityCtx, {
            type: 'doughnut',
            data: {
                labels: [
                    'Insufficient Weight',
                    'Normal Weight',
                    'Overweight Level I',
                    'Overweight Level II',
                    'Obesity Type I',
                    'Obesity Type II',
                    'Obesity Type III'
                ],
                datasets: [{
                    data: [5.2, 18.7, 22.4, 19.3, 16.8, 11.2, 6.4],
                    backgroundColor: chartColors.gradients.map(g => g.border),
                    borderColor: 'var(--bg-primary)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 11 },
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => `${context.label}: ${context.parsed}%`
                        }
                    }
                }
            }
        });
    }

    // Chart 2: BMI Distribution
    const bmiCtx = document.getElementById('bmiChart');
    if (bmiCtx) {
        new Chart(bmiCtx, {
            type: 'bar',
            data: {
                labels: ['16-18.5', '18.5-25', '25-30', '30-35', '35-40', '40+'],
                datasets: [{
                    label: 'Number of People',
                    data: [156, 1245, 1876, 1543, 945, 512],
                    backgroundColor: 'rgba(99, 102, 241, 0.7)',
                    borderColor: '#6366f1',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'x',
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    x: {
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    // Chart 3: Age vs Weight
    const ageWeightCtx = document.getElementById('ageWeightChart');
    if (ageWeightCtx) {
        new Chart(ageWeightCtx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Age vs Weight',
                    data: generateScatterData(200),
                    backgroundColor: 'rgba(99, 102, 241, 0.6)',
                    borderColor: '#6366f1',
                    showLine: true,
                    borderWidth: 2,
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Weight (kg)', color: 'var(--text-primary)' },
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    x: {
                        title: { display: true, text: 'Age (years)', color: 'var(--text-primary)' },
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    // Chart 4: Exercise Impact
    const exerciseCtx = document.getElementById('exerciseChart');
    if (exerciseCtx) {
        new Chart(exerciseCtx, {
            type: 'line',
            data: {
                labels: ['0', '1', '2', '3', '4', '5', '6', '7'],
                datasets: [{
                    label: 'Average Weight (kg)',
                    data: [87.2, 82.5, 79.8, 75.3, 72.1, 70.5, 69.2, 68.9],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: 'white',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        title: { display: true, text: 'Average Weight' },
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    x: {
                        title: { display: true, text: 'Exercise Days per Week' },
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                }
            }
        });
    }

    // Chart 5: Diet Impact
    const dietCtx = document.getElementById('dietChart');
    if (dietCtx) {
        new Chart(dietCtx, {
            type: 'bar',
            data: {
                labels: ['No High-Calorie Food', 'Yes High-Calorie Food'],
                datasets: [{
                    label: 'Obesity Rate (%)',
                    data: [22.5, 58.9],
                    backgroundColor: ['rgba(16, 185, 129, 0.7)', 'rgba(239, 68, 68, 0.7)'],
                    borderColor: ['#10b981', '#ef4444'],
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    x: {
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    // Chart 6: Water Impact
    const waterCtx = document.getElementById('waterChart');
    if (waterCtx) {
        new Chart(waterCtx, {
            type: 'line',
            data: {
                labels: ['<1L', '1-2L', '2-3L', '3-4L', '4+L'],
                datasets: [{
                    label: 'Average Weight (kg)',
                    data: [84.5, 78.2, 71.8, 68.5, 65.2],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: 'white',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    x: {
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    // Chart 7: Tech Usage Impact
    const techCtx = document.getElementById('techChart');
    if (techCtx) {
        new Chart(techCtx, {
            type: 'bar',
            data: {
                labels: ['0-2h', '2-4h', '4-6h', '6-8h', '8+h'],
                datasets: [{
                    label: 'Average Weight (kg)',
                    data: [68.3, 72.5, 78.9, 82.1, 85.6],
                    backgroundColor: 'rgba(239, 68, 68, 0.7)',
                    borderColor: '#ef4444',
                    borderWidth: 2,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    x: {
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'var(--text-primary)',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }

    // Chart 8: Feature Importance
    const importanceCtx = document.getElementById('importanceChart');
    if (importanceCtx) {
        new Chart(importanceCtx, {
            type: 'barH',
            type: 'bar',
            data: {
                labels: ['Weight', 'Height', 'Physical Activity', 'High-Calorie Food', 'Water Intake', 'Age', 'Tech Usage', 'Snacking'],
                datasets: [{
                    label: 'Feature Importance',
                    data: [0.285, 0.218, 0.156, 0.112, 0.089, 0.078, 0.038, 0.024],
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(99, 102, 241, 0.7)',
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(139, 92, 246, 0.7)',
                        'rgba(236, 72, 153, 0.8)',
                        'rgba(236, 72, 153, 0.7)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(245, 158, 11, 0.7)'
                    ],
                    borderWidth: 0,
                    borderRadius: 5
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 0.3,
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { color: 'var(--border-color)' }
                    },
                    y: {
                        ticks: { color: 'var(--text-secondary)' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Generate random scatter data
function generateScatterData(count) {
    const data = [];
    for (let i = 0; i < count; i++) {
        const age = Math.floor(Math.random() * 60) + 18;
        const weight = 50 + (age - 18) * 0.3 + Math.random() * 40;
        data.push({ x: age, y: Math.round(weight) });
    }
    return data;
}

// Initialize statistics
function initializeStats() {
    document.getElementById('totalRecords').textContent = '6,278';
    document.getElementById('avgWeight').textContent = '76.2';
    document.getElementById('avgHeight').textContent = '1.71';
    document.getElementById('avgBMI').textContent = '26.3';
    document.getElementById('exerciseRate').textContent = '2.8';
    document.getElementById('waterIntake').textContent = '2.2';
}

// Add click interaction to chart cards
document.querySelectorAll('.chart-card').forEach(card => {
    card.addEventListener('click', function() {
        // Add glow effect
        this.style.boxShadow = '0 0 30px rgba(99, 102, 241, 0.5)';
        setTimeout(() => {
            this.style.boxShadow = 'var(--shadow-medium)';
        }, 500);
    });
});

// Smooth scroll to charts on navigation
document.querySelectorAll('a[href*="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        if (this.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
});
