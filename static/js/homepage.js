// Interactive features for homepage
$(document).ready(function() {
    // Live test countdown
    function updateLiveTestCountdown() {
        const testTime = new Date();
        testTime.setHours(18, 0, 0); // 6 PM today
        
        const now = new Date();
        const diff = testTime - now;
        
        if (diff > 0) {
            const hours = Math.floor(diff / 3600000);
            const minutes = Math.floor((diff % 3600000) / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            
            $('#live-countdown').html(`${hours}h ${minutes}m ${seconds}s`);
        } else {
            $('#live-countdown').html('Live Now!');
        }
    }
    
    updateLiveTestCountdown();
    setInterval(updateLiveTestCountdown, 1000);
    
    // Personalized recommendation slider
    let currentRecommendation = 0;
    const recommendations = [
        "Based on your performance, practice Time & Work problems",
        "You're strong in Algebra! Try advanced level questions",
        "Focus on Reading Comprehension - 60% accuracy",
        "Your rank improved by 15% this week! Keep going!"
    ];
    
    setInterval(() => {
        currentRecommendation = (currentRecommendation + 1) % recommendations.length;
        $('#recommendation-text').fadeOut(300, function() {
            $(this).text(recommendations[currentRecommendation]).fadeIn(300);
        });
    }, 5000);
    
    // Daily challenge progress simulation
    let dailyProgress = 0;
    setInterval(() => {
        dailyProgress = (dailyProgress + 5) % 100;
        $('#daily-progress').css('width', dailyProgress + '%');
        if (dailyProgress === 0) {
            $('#daily-progress').css('width', '0%');
        }
    }, 3000);
});