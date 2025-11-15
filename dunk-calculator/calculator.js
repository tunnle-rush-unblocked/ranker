/**
 * Dunk Calculator - Advanced Basketball Vertical Jump Calculator
 */

let currentUnit = 'imperial';

// Conversion constants
const CM_PER_INCH = 2.54;
const INCHES_PER_FOOT = 12;

// Clearance needed above rim (in inches)
const CLEARANCE = {
    tip: 6,        // Just tip it in
    comfortable: 9, // Comfortable dunk
    powerful: 12    // Powerful dunk
};

// Hand size adjustments (inches)
const HAND_ADJUSTMENT = {
    small: -1,
    medium: 0,
    large: 1
};

/**
 * Set the unit system (imperial or metric)
 */
function setUnit(unit) {
    currentUnit = unit;
    
    // Update button states
    document.querySelectorAll('.unit-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-unit="${unit}"]`).classList.add('active');
    
    // Show/hide appropriate inputs
    if (unit === 'imperial') {
        document.getElementById('imperial-inputs').style.display = 'block';
        document.getElementById('metric-inputs').style.display = 'none';
    } else {
        document.getElementById('imperial-inputs').style.display = 'none';
        document.getElementById('metric-inputs').style.display = 'block';
    }
    
    // Recalculate
    calculateDunk();
}

/**
 * Convert imperial measurements to inches
 */
function getImperialMeasurements() {
    const heightFeet = parseFloat(document.getElementById('height-feet').value) || 0;
    const heightInches = parseFloat(document.getElementById('height-inches').value) || 0;
    const wingspanFeet = parseFloat(document.getElementById('wingspan-feet').value) || 0;
    const wingspanInches = parseFloat(document.getElementById('wingspan-inches').value) || 0;
    const vertical = parseFloat(document.getElementById('vertical-inches').value) || 0;
    const rimHeight = parseFloat(document.getElementById('rim-height').value) || 10;
    
    return {
        height: (heightFeet * INCHES_PER_FOOT) + heightInches,
        wingspan: (wingspanFeet * INCHES_PER_FOOT) + wingspanInches,
        vertical: vertical,
        rimHeight: rimHeight * INCHES_PER_FOOT
    };
}

/**
 * Convert metric measurements to inches
 */
function getMetricMeasurements() {
    const heightCm = parseFloat(document.getElementById('height-cm').value) || 0;
    const wingspanCm = parseFloat(document.getElementById('wingspan-cm').value) || 0;
    const verticalCm = parseFloat(document.getElementById('vertical-cm').value) || 0;
    const rimHeightCm = parseFloat(document.getElementById('rim-height-cm').value) || 305;
    
    return {
        height: heightCm / CM_PER_INCH,
        wingspan: wingspanCm / CM_PER_INCH,
        vertical: verticalCm / CM_PER_INCH,
        rimHeight: rimHeightCm / CM_PER_INCH
    };
}

/**
 * Calculate standing reach based on height and wingspan
 */
function calculateStandingReach(height, wingspan) {
    // Standing reach is approximately: height + (wingspan - height) * 1.25
    // This accounts for shoulder width and arm angle
    const wingspanDiff = wingspan - height;
    return height + (wingspanDiff * 1.25);
}

/**
 * Calculate required clearance based on dunk type and hand size
 */
function getRequiredClearance() {
    const dunkType = document.getElementById('dunk-type').value;
    const handSize = document.getElementById('hand-size').value;
    
    let clearance = CLEARANCE[dunkType];
    clearance += HAND_ADJUSTMENT[handSize];
    
    return clearance;
}

/**
 * Main calculation function
 */
function calculateDunk() {
    // Get measurements based on current unit
    const measurements = currentUnit === 'imperial' 
        ? getImperialMeasurements() 
        : getMetricMeasurements();
    
    const { height, wingspan, vertical, rimHeight } = measurements;
    
    // Validate inputs
    if (height <= 0 || wingspan <= 0) {
        return;
    }
    
    // Calculate standing reach
    const standingReach = calculateStandingReach(height, wingspan);
    
    // Calculate max touch height
    const maxTouch = standingReach + vertical;
    
    // Calculate required height to dunk
    const requiredClearance = getRequiredClearance();
    const neededHeight = rimHeight + requiredClearance;
    
    // Calculate vertical needed to dunk
    const verticalNeeded = neededHeight - standingReach;
    
    // Calculate how much more vertical is needed
    const verticalDifference = verticalNeeded - vertical;
    
    // Display results
    displayResults({
        standingReach,
        maxTouch,
        neededHeight,
        verticalNeeded,
        verticalDifference,
        currentVertical: vertical,
        rimHeight
    });
}

/**
 * Format inches to feet and inches
 */
function formatHeight(inches) {
    if (currentUnit === 'metric') {
        return `${(inches * CM_PER_INCH).toFixed(1)} cm`;
    }
    const feet = Math.floor(inches / INCHES_PER_FOOT);
    const remainingInches = inches % INCHES_PER_FOOT;
    return `${feet}'${remainingInches.toFixed(1)}"`;
}

/**
 * Format vertical jump
 */
function formatVertical(inches) {
    if (currentUnit === 'metric') {
        return `${(inches * CM_PER_INCH).toFixed(1)} cm`;
    }
    return `${inches.toFixed(1)}"`;
}

/**
 * Display calculation results
 */
function displayResults(data) {
    const resultsBox = document.getElementById('results');
    resultsBox.style.display = 'block';
    
    // Update stats
    document.getElementById('standing-reach').textContent = formatHeight(data.standingReach);
    document.getElementById('max-touch').textContent = formatHeight(data.maxTouch);
    document.getElementById('needed-height').textContent = formatHeight(data.neededHeight);
    document.getElementById('needed-vertical').textContent = formatVertical(data.verticalNeeded);
    
    // Determine verdict
    let icon, verdict, detail, tips;
    
    if (data.verticalDifference <= 0) {
        // Can dunk!
        const excess = Math.abs(data.verticalDifference);
        icon = '🎉';
        verdict = 'YES, YOU CAN DUNK!';
        detail = `You have ${formatVertical(excess)} more than needed. You're ready to dunk!`;
        tips = generateSuccessTips(excess);
    } else if (data.verticalDifference <= 4) {
        // Very close
        icon = '🔥';
        verdict = 'SO CLOSE!';
        detail = `You need ${formatVertical(data.verticalDifference)} more vertical to dunk!`;
        tips = generateCloseTips(data.verticalDifference);
    } else if (data.verticalDifference <= 8) {
        // Within reach
        icon = '💪';
        verdict = 'WITHIN REACH!';
        detail = `You need ${formatVertical(data.verticalDifference)} more vertical. Keep training!`;
        tips = generateModereTips(data.verticalDifference);
    } else {
        // Need more work
        icon = '🏋️';
        verdict = 'KEEP TRAINING!';
        detail = `You need ${formatVertical(data.verticalDifference)} more vertical. You can do it!`;
        tips = generateBeginnerTips(data.verticalDifference);
    }
    
    document.getElementById('result-icon').textContent = icon;
    document.getElementById('verdict').textContent = verdict;
    document.getElementById('detail').textContent = detail;
    
    // Update progress bar
    const progress = Math.min(100, (data.currentVertical / data.verticalNeeded) * 100);
    document.getElementById('progress-fill').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = 
        `${progress.toFixed(1)}% of the way there!`;
    
    // Display tips
    const tipsElement = document.getElementById('tips');
    tipsElement.innerHTML = `
        <h4>${icon} Your Training Plan</h4>
        <ul>
            ${tips.map(tip => `<li>${tip}</li>`).join('')}
        </ul>
    `;
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/**
 * Generate tips for someone who can already dunk
 */
function generateSuccessTips(excess) {
    return [
        'Congratulations! You can dunk comfortably.',
        'Focus on perfecting your dunk technique and style.',
        'Try different types of dunks: one-handed, two-handed, reverse dunks.',
        'Work on your approach and timing for game situations.',
        'Consider learning advanced dunks like windmill or 360.',
        'Maintain your vertical with regular jump training 2-3x per week.'
    ];
}

/**
 * Generate tips for someone very close to dunking
 */
function generateCloseTips(needed) {
    return [
        `You're only ${formatVertical(needed)} away from dunking!`,
        'Focus on explosive plyometric exercises (box jumps, depth jumps).',
        'Add weight to your squats and increase leg strength.',
        'Practice approach jumps to improve your takeoff technique.',
        'Work on ankle flexibility and calf strength.',
        'You could be dunking in 1-2 months with consistent training!',
        'Try dunking on a slightly lower rim (9-9.5 feet) to practice technique.'
    ];
}

/**
 * Generate tips for someone moderately close
 */
function generateModereTips(needed) {
    return [
        `You need to add ${formatVertical(needed)} to your vertical jump.`,
        'Follow a structured 8-12 week vertical jump program.',
        'Combine strength training (squats, deadlifts) with plyometrics.',
        'Train 3-4 times per week with proper rest days.',
        'Focus on: Box jumps, depth jumps, single-leg exercises.',
        'Improve your approach technique - a good approach adds 4-6 inches.',
        'Expected timeline: 3-6 months with dedicated training.',
        'Track your progress by testing vertical monthly.'
    ];
}

/**
 * Generate tips for beginners
 */
function generateBeginnerTips(needed) {
    return [
        `You need to improve your vertical by ${formatVertical(needed)}.`,
        'Start with a comprehensive 6-12 month training program.',
        'Build a foundation with strength training: squats, lunges, calf raises.',
        'Gradually introduce plyometric exercises as you get stronger.',
        'Focus on proper form and technique to prevent injury.',
        'Key exercises: Squats, deadlifts, box jumps, jump rope, calf raises.',
        'Be patient - most people can add 8-12 inches with proper training.',
        'Set milestone goals: First touch the rim, then grab it, then dunk.',
        'Consider working with a trainer for personalized guidance.'
    ];
}

/**
 * Reset calculator to initial state
 */
function resetCalculator() {
    // Reset imperial inputs
    document.getElementById('height-feet').value = 6;
    document.getElementById('height-inches').value = 0;
    document.getElementById('wingspan-feet').value = 6;
    document.getElementById('wingspan-inches').value = 2;
    document.getElementById('vertical-inches').value = 24;
    document.getElementById('rim-height').value = 10;
    
    // Reset metric inputs
    document.getElementById('height-cm').value = 183;
    document.getElementById('wingspan-cm').value = 188;
    document.getElementById('vertical-cm').value = 61;
    document.getElementById('rim-height-cm').value = 305;
    
    // Reset selects
    document.getElementById('hand-size').value = 'medium';
    document.getElementById('dunk-type').value = 'comfortable';
    
    // Hide results
    document.getElementById('results').style.display = 'none';
    
    // Scroll to top
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
 * Sync imperial and metric inputs
 */
function syncUnits() {
    if (currentUnit === 'imperial') {
        // Convert imperial to metric
        const imperial = getImperialMeasurements();
        document.getElementById('height-cm').value = Math.round(imperial.height * CM_PER_INCH);
        document.getElementById('wingspan-cm').value = Math.round(imperial.wingspan * CM_PER_INCH);
        document.getElementById('vertical-cm').value = Math.round(imperial.vertical * CM_PER_INCH);
        document.getElementById('rim-height-cm').value = Math.round(imperial.rimHeight * CM_PER_INCH);
    } else {
        // Convert metric to imperial
        const metric = getMetricMeasurements();
        const heightFeet = Math.floor(metric.height / INCHES_PER_FOOT);
        const heightInches = metric.height % INCHES_PER_FOOT;
        const wingspanFeet = Math.floor(metric.wingspan / INCHES_PER_FOOT);
        const wingspanInches = metric.wingspan % INCHES_PER_FOOT;
        
        document.getElementById('height-feet').value = heightFeet;
        document.getElementById('height-inches').value = Math.round(heightInches);
        document.getElementById('wingspan-feet').value = wingspanFeet;
        document.getElementById('wingspan-inches').value = Math.round(wingspanInches);
        document.getElementById('vertical-inches').value = Math.round(metric.vertical);
        document.getElementById('rim-height').value = (metric.rimHeight / INCHES_PER_FOOT).toFixed(1);
    }
}

/**
 * Initialize calculator
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add input validation
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            syncUnits();
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            calculateDunk();
        }
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            resetCalculator();
        }
    });
    
    console.log('🏀 Dunk Calculator loaded successfully!');
    console.log('💡 Keyboard shortcuts:');
    console.log('   - Ctrl/Cmd + Enter: Calculate');
    console.log('   - Ctrl/Cmd + R: Reset');
});

