/**
 * Fallacy Tarot - UI Logic
 * Handles data fetching, slider navigation, and voting interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    let allEntries = [];
    let currentEntries = [];
    let currentIndex = 0;
    
    // Load voted state from localStorage
    const votes = JSON.parse(localStorage.getItem('fallacy_votes') || '{}');

    // DOM Elements
    const contentArea = document.getElementById('content');
    const cardTemplate = document.getElementById('card-template');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const counterDisplay = document.getElementById('card-counter');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const lastUpdatedDisplay = document.getElementById('last-updated');

    // Initialize
    fetchData();

    // Event Listeners
    prevBtn.addEventListener('click', showPrevCard);
    nextBtn.addEventListener('click', showNextCard);
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') showPrevCard();
        if (e.key === 'ArrowRight') showNextCard();
    });

    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            tabBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            applyFilter(e.target.dataset.filter);
        });
    });

    // Functions
    async function fetchData() {
        try {
            // Add cache-busting parameter to prevent stale data
            const response = await fetch(`data/fallacies.json?t=${new Date().getTime()}`);
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            allEntries = data.entries || [];
            
            // Format date safely
            try {
                const updateDate = new Date(data.metadata?.last_updated || new Date());
                lastUpdatedDisplay.textContent = `Last updated: ${updateDate.toLocaleString()}`;
            } catch (e) {
                lastUpdatedDisplay.textContent = 'Last updated: Recently';
            }
            
            if (allEntries.length === 0) {
                showError("No logical fallacies have been analyzed yet. Check back soon!");
                return;
            }

            // Start with newest filter
            applyFilter('newest');
            
        } catch (error) {
            console.error('Error fetching data:', error);
            showError("Could not load the tarot readings. The mystic connection is severed.");
        }
    }

    function applyFilter(filterType) {
        // Create a working copy to sort
        let entries = [...allEntries];
        
        switch (filterType) {
            case 'newest':
                // Already sorted by newest first from Python script
                currentEntries = entries;
                break;
            case 'hot':
                // Sort by Wilson score interval (simplified) or combined score + recency
                // For client side, we'll do a simple hotness algorithm: score / (age_hours + 2)^1.5
                const now = new Date().getTime();
                currentEntries = entries.sort((a, b) => {
                    const ageA = (now - new Date(a.timestamp).getTime()) / (1000 * 60 * 60);
                    const ageB = (now - new Date(b.timestamp).getTime()) / (1000 * 60 * 60);
                    const scoreA = (a.upvotes || 0) - (a.downvotes || 0);
                    const scoreB = (b.upvotes || 0) - (b.downvotes || 0);
                    const hotA = scoreA / Math.pow(ageA + 2, 1.5);
                    const hotB = scoreB / Math.pow(ageB + 2, 1.5);
                    return hotB - hotA;
                });
                break;
            case 'best':
                // Highest net score
                currentEntries = entries.sort((a, b) => {
                    const scoreA = (a.upvotes || 0) - (a.downvotes || 0);
                    const scoreB = (b.upvotes || 0) - (b.downvotes || 0);
                    return scoreB - scoreA;
                });
                break;
        }

        // Reset index and render
        currentIndex = 0;
        renderCurrentCard();
    }

    function renderCurrentCard() {
        if (currentEntries.length === 0) return;

        const entry = currentEntries[currentIndex];
        
        // Clear content area
        contentArea.innerHTML = '';
        
        // Clone template
        const templateContent = cardTemplate.content.cloneNode(true);
        const card = templateContent.querySelector('.card');
        
        // Populate data
        card.querySelector('.card-number').textContent = romanize(currentIndex + 1);
        card.querySelector('.fallacy-title').textContent = entry.fallacy_type;
        card.querySelector('.explanation-text').textContent = entry.explanation;
        
        // Handle quote
        const quoteEl = card.querySelector('.fallacy-quote');
        if (entry.quote && entry.quote.trim() !== '' && entry.quote !== 'None') {
            quoteEl.textContent = `"${entry.quote}"`;
        } else {
            quoteEl.style.display = 'none';
        }
        
        // Source info
        card.querySelector('.subreddit').textContent = `r/${entry.subreddit}`;
        card.querySelector('.author').textContent = `u/${entry.author}`;
        card.querySelector('.reddit-score').textContent = `⭐ ${entry.reddit_score}`;
        card.querySelector('.post-title').textContent = entry.title;
        card.querySelector('.post-text').textContent = entry.content;
        
        const sourceLink = card.querySelector('.source-link');
        if (entry.source_url) {
            sourceLink.href = entry.source_url;
        } else {
            sourceLink.style.display = 'none';
        }
        
        // Image
        const imgEl = card.querySelector('.tarot-image');
        // Handle path logic whether running locally or on GitHub Pages
        imgEl.src = entry.image_url || 'assets/placeholders/fallback_card.svg';
        imgEl.alt = `${entry.fallacy_type} Tarot Card`;
        
        // Handle image error fallback
        imgEl.onerror = function() {
            this.onerror = null;
            this.src = 'assets/placeholders/fallback_card.svg';
        };

        // Confidence badge
        const confBadge = card.querySelector('.confidence-badge');
        const confLevel = entry.confidence_level || 'Medium';
        confBadge.textContent = `${confLevel} Confidence`;
        confBadge.classList.add(`conf-${confLevel.toLowerCase()}`);
        
        // Voting setup
        setupVoting(card, entry);
        
        // Add to DOM and show
        contentArea.appendChild(card);
        // Small delay to allow browser to render before adding animation class
        setTimeout(() => card.classList.add('active'), 50);
        
        updateNavigation();
    }

    function setupVoting(card, entry) {
        const upBtn = card.querySelector('.upvote');
        const downBtn = card.querySelector('.downvote');
        const scoreDisplay = card.querySelector('.vote-score');
        
        // Calculate initial display values
        let upCount = entry.upvotes || 0;
        let downCount = entry.downvotes || 0;
        let netScore = upCount - downCount;
        
        // Check if user already voted
        const userVote = votes[entry.post_id];
        
        if (userVote === 'up') upBtn.classList.add('voted-up');
        if (userVote === 'down') downBtn.classList.add('voted-down');
        
        // Update display
        upBtn.querySelector('.count').textContent = upCount;
        downBtn.querySelector('.count').textContent = downCount;
        scoreDisplay.textContent = netScore > 0 ? `+${netScore}` : netScore;
        
        // Attach events (simulate client-side only voting for v1)
        upBtn.addEventListener('click', () => {
            if (userVote === 'up') return; // Already upvoted
            
            // Update UI state immediately for responsive feel
            if (userVote === 'down') {
                downBtn.classList.remove('voted-down');
                downCount--;
            }
            
            upBtn.classList.add('voted-up');
            upCount++;
            
            // Save state
            votes[entry.post_id] = 'up';
            localStorage.setItem('fallacy_votes', JSON.stringify(votes));
            
            // Update display
            upBtn.querySelector('.count').textContent = upCount;
            downBtn.querySelector('.count').textContent = downCount;
            netScore = upCount - downCount;
            scoreDisplay.textContent = netScore > 0 ? `+${netScore}` : netScore;
        });
        
        downBtn.addEventListener('click', () => {
            if (userVote === 'down') return; // Already downvoted
            
            // Update UI state immediately
            if (userVote === 'up') {
                upBtn.classList.remove('voted-up');
                upCount--;
            }
            
            downBtn.classList.add('voted-down');
            downCount++;
            
            // Save state
            votes[entry.post_id] = 'down';
            localStorage.setItem('fallacy_votes', JSON.stringify(votes));
            
            // Update display
            upBtn.querySelector('.count').textContent = upCount;
            downBtn.querySelector('.count').textContent = downCount;
            netScore = upCount - downCount;
            scoreDisplay.textContent = netScore > 0 ? `+${netScore}` : netScore;
        });
    }

    function showNextCard() {
        if (currentIndex < currentEntries.length - 1) {
            currentIndex++;
            renderCurrentCard();
        }
    }

    function showPrevCard() {
        if (currentIndex > 0) {
            currentIndex--;
            renderCurrentCard();
        }
    }

    function updateNavigation() {
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex === currentEntries.length - 1;
        counterDisplay.textContent = `${currentIndex + 1} / ${currentEntries.length}`;
    }

    function showError(message) {
        contentArea.innerHTML = `
            <div class="error-state fade-in">
                <h3>⚠️ Vision Clouded</h3>
                <p>${message}</p>
            </div>
        `;
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        counterDisplay.textContent = '0 / 0';
    }

    // Helper to generate roman numerals for card numbers
    function romanize(num) {
        if (isNaN(num)) return NaN;
        var digits = String(+num).split(""),
            key = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM",
                   "","X","XX","XXX","XL","L","LX","LXX","LXXX","XC",
                   "","I","II","III","IV","V","VI","VII","VIII","IX"],
            roman = "",
            i = 3;
        while (i--)
            roman = (key[+digits.pop() + (i * 10)] || "") + roman;
        return Array(+digits.join("") + 1).join("M") + roman;
    }
});