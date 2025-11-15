/**
 * AP Biology Score Calculator
 * Calculates predicted AP exam score based on raw scores
 */

// AP Biology scoring conversion table (approximate)
const SCORE_CONVERSION = [
    { min: 72, max: 120, apScore: 5 },
    { min: 58, max: 71, apScore: 4 },
    { min: 43, max: 57, apScore: 3 },
    { min: 28, max: 42, apScore: 2 },
    { min: 0, max: 27, apScore: 1 }
];

// Score interpretations
const SCORE_MEANINGS = {
    5: {
        title: "Extremely Well Qualified",
        description: "Outstanding performance! You've demonstrated exceptional mastery of AP Biology concepts. Most colleges will grant credit and/or placement.",
        color: "#22c55e",
        emoji: "🌟"
    },
    4: {
        title: "Well Qualified",
        description: "Excellent work! You've shown strong understanding of the material. Most colleges will grant credit and/or placement.",
        color: "#10b981",
        emoji: "✨"
    },
    3: {
        title: "Qualified",
        description: "Good job! You've demonstrated competent understanding of AP Biology. Many colleges will grant credit and/or placement.",
        color: "#3b82f6",
        emoji: "👍"
    },
    2: {
        title: "Possibly Qualified",
        description: "You've shown some understanding but may benefit from additional review. Some colleges may grant credit.",
        color: "#f59e0b",
        emoji: "📚"
    },
    1: {
        title: "No Recommendation",
        description: "Consider reviewing the material more thoroughly. Colleges typically do not grant credit for this score.",
        color: "#ef4444",
        emoji: "💪"
    }
};

/**
 * Calculate the AP Biology score
 */
function calculateScore() {
    // Get Multiple Choice scores
    const mcCorrect = parseFloat(document.getElementById('mc-correct').value) || 0;
    const mcIncorrect = parseFloat(document.getElementById('mc-incorrect').value) || 0;
    
    // Validate MC input
    if (mcCorrect + mcIncorrect > 60) {
        alert('Total multiple choice questions cannot exceed 60!');
        return;
    }
    
    // Calculate Section I raw score (no penalty for wrong answers)
    const section1Raw = mcCorrect;
    document.getElementById('section1-score').textContent = section1Raw.toFixed(1);
    
    // Get Free Response scores
    const frq1 = parseFloat(document.getElementById('frq1').value) || 0;
    const frq2 = parseFloat(document.getElementById('frq2').value) || 0;
    const frq3 = parseFloat(document.getElementById('frq3').value) || 0;
    const frq4 = parseFloat(document.getElementById('frq4').value) || 0;
    const frq5 = parseFloat(document.getElementById('frq5').value) || 0;
    const frq6 = parseFloat(document.getElementById('frq6').value) || 0;
    
    // Calculate Section II raw score
    const section2Raw = frq1 + frq2 + frq3 + frq4 + frq5 + frq6;
    document.getElementById('section2-score').textContent = section2Raw.toFixed(1);
    
    // Calculate weighted scores (each section is 50%)
    // Section I: 60 points maximum
    // Section II: 36 points maximum (2x10 + 4x4)
    const mcWeighted = (section1Raw / 60) * 60;  // Out of 60 points
    const frqWeighted = (section2Raw / 36) * 60; // Out of 60 points
    
    // Composite score (out of 120)
    const composite = mcWeighted + frqWeighted;
    
    // Determine AP score
    const apScore = getAPScore(composite);
    const percentage = ((composite / 120) * 100).toFixed(1);
    
    // Display results
    displayResults(apScore, composite, percentage, mcWeighted, frqWeighted);
}

/**
 * Convert composite score to AP score (1-5)
 */
function getAPScore(composite) {
    for (const range of SCORE_CONVERSION) {
        if (composite >= range.min && composite <= range.max) {
            return range.apScore;
        }
    }
    return 1; // Default to 1 if something goes wrong
}

/**
 * Display calculation results
 */
function displayResults(apScore, composite, percentage, mcWeighted, frqWeighted) {
    // Show results box
    const resultsBox = document.getElementById('results');
    resultsBox.style.display = 'block';
    
    // Set main score
    const scoreElement = document.getElementById('ap-score');
    scoreElement.textContent = apScore;
    scoreElement.style.color = SCORE_MEANINGS[apScore].color;
    
    // Set percentage
    document.getElementById('percentage').textContent = `${percentage}% (${composite.toFixed(1)}/120)`;
    
    // Set breakdown
    document.getElementById('mc-weighted').textContent = mcWeighted.toFixed(1);
    document.getElementById('frq-weighted').textContent = frqWeighted.toFixed(1);
    document.getElementById('composite-score').textContent = composite.toFixed(1);
    
    // Set interpretation
    const meaning = SCORE_MEANINGS[apScore];
    document.getElementById('interpretation').innerHTML = `
        <h4 style="color: ${meaning.color}">
            ${meaning.emoji} ${meaning.title}
        </h4>
        <p>${meaning.description}</p>
    `;
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/**
 * Reset calculator to initial state
 */
function resetCalculator() {
    // Reset all input fields
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.value = 0;
    });
    
    // Reset displays
    document.getElementById('section1-score').textContent = '0';
    document.getElementById('section2-score').textContent = '0';
    
    // Hide results
    document.getElementById('results').style.display = 'none';
    
    // Scroll to top of calculator
    document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu.style.display === 'flex') {
        navMenu.style.display = 'none';
    } else {
        navMenu.style.display = 'flex';
        navMenu.style.flexDirection = 'column';
        navMenu.style.position = 'absolute';
        navMenu.style.top = '100%';
        navMenu.style.left = '0';
        navMenu.style.right = '0';
        navMenu.style.background = 'white';
        navMenu.style.padding = '1rem';
        navMenu.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    }
}

/**
 * Initialize calculator on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add input validation
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const max = parseFloat(this.max);
            const min = parseFloat(this.min);
            
            if (value > max) {
                this.value = max;
            }
            if (value < min) {
                this.value = min;
            }
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to calculate
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            calculateScore();
        }
        // Ctrl/Cmd + R to reset (prevent page reload)
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            resetCalculator();
        }
    });
    
    console.log('✅ AP Biology Score Calculator loaded successfully!');
    console.log('💡 Keyboard shortcuts:');
    console.log('   - Ctrl/Cmd + Enter: Calculate score');
    console.log('   - Ctrl/Cmd + R: Reset calculator');
});

/**
 * Export functions for testing (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        calculateScore,
        getAPScore,
        resetCalculator
    };
}

