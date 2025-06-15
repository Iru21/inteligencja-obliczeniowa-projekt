document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const cloudBtn = document.getElementById('cloudBtn');
    const clearBtn = document.getElementById('clearBtn');
    const subjectInput = document.getElementById('subject');
    const resultsSection = document.getElementById('results');

    const sentimentResultsWrapper = document.getElementById('sentimentResultsWrapper');
    const sentimentLoading = document.getElementById('sentimentLoading');
    const sentimentResults = document.getElementById('sentimentResults');
    const yearlyChart = document.getElementById('yearlyChart');
    const monthlyChart = document.getElementById('monthlyChart');

    const cloudResultsWrapper = document.getElementById('cloudResultsWrapper');
    const cloudLoading = document.getElementById('cloudLoading');
    const cloudResults = document.getElementById('cloudResults');
    const wordCloud = document.getElementById('wordCloud');

    const modal = document.getElementById('imageZoomModal');
    const zoomedImage = document.getElementById('zoomedImage');
    const closeBtn = document.querySelector('.zoom-close');
    const zoomInBtn = document.getElementById('zoomIn');
    const zoomOutBtn = document.getElementById('zoomOut');
    const zoomResetBtn = document.getElementById('zoomReset');

    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    let isDragging = false;
    let startX, startY, initialTranslateX, initialTranslateY;

    async function runPythonScript(script, subject) {
        try {
            const response = await fetch(`/run_script?script=${script}&subject=${encodeURIComponent(subject)}`, {
                method: 'GET'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error running script:', error);
            return { success: false, error: error.message };
        }
    }

    analyzeBtn.addEventListener('click', async function() {
        const subject = subjectInput.value.trim();

        if (!subject) {
            alert('Please enter a subject to analyze');
            return;
        }

        resultsSection.classList.remove('hidden');
        sentimentLoading.classList.remove('hidden');
        sentimentResults.classList.add('hidden');

        cloudResultsWrapper.classList.add('hidden');

        try {
            const result = await runPythonScript('analyze_sentiment.py', subject);

            if (result.success) {
                const timestamp = new Date().getTime();
                const subjectSlug = subject.toLowerCase().replace(/\s+/g, '-');

                yearlyChart.src = `sentiments/${subjectSlug}-years.png?t=${timestamp}`;
                monthlyChart.src = `sentiments/${subjectSlug}-months.png?t=${timestamp}`;

                sentimentLoading.classList.add('hidden');
                sentimentResults.classList.remove('hidden');
            } else {
                throw new Error(result.error || 'Failed to analyze sentiment');
            }
        } catch (error) {
            console.error('Error:', error);
            sentimentLoading.textContent = `Error: ${error.message}`;
            sentimentLoading.classList.remove('loading');
            sentimentLoading.classList.add('text-red-500');
        }
    });

    cloudBtn.addEventListener('click', async function() {
        const subject = subjectInput.value.trim();

        if (!subject) {
            alert('Please enter a subject to generate word cloud');
            return;
        }

        resultsSection.classList.remove('hidden');
        cloudLoading.classList.remove('hidden');
        cloudResults.classList.add('hidden');

        sentimentResultsWrapper.classList.add('hidden');

        try {
            const result = await runPythonScript('cloud.py', subject);

            if (result.success) {
                const timestamp = new Date().getTime();
                const subjectSlug = subject.toLowerCase().replace(/\s+/g, '_');

                wordCloud.src = `wordclouds/${subjectSlug}_wordcloud.png?t=${timestamp}`;

                cloudLoading.classList.add('hidden');
                cloudResults.classList.remove('hidden');
            } else {
                throw new Error(result.error || 'Failed to generate word cloud');
            }
        } catch (error) {
            console.error('Error:', error);
            cloudLoading.textContent = `Error: ${error.message}`;
            cloudLoading.classList.remove('loading');
            cloudLoading.classList.add('text-red-500');
        }
    });

    clearBtn.addEventListener('click', function() {
        resultsSection.classList.add('hidden');

        sentimentResultsWrapper.classList.remove('hidden');
        sentimentLoading.classList.add('hidden');
        sentimentResults.classList.add('hidden');
        sentimentLoading.textContent = 'Analyzing sentiment...';
        sentimentLoading.classList.add('loading');
        sentimentLoading.classList.remove('text-red-500');

        cloudResultsWrapper.classList.remove('hidden');
        cloudLoading.classList.add('hidden');
        cloudResults.classList.add('hidden');
        cloudLoading.textContent = 'Generating word cloud...';
        cloudLoading.classList.add('loading');
        cloudLoading.classList.remove('text-red-500');

        yearlyChart.src = '';
        monthlyChart.src = '';
        wordCloud.src = '';
    });

    function updateTransform() {
        zoomedImage.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }

    function resetZoom() {
        scale = 1;
        translateX = 0;
        translateY = 0;
        updateTransform();
    }

    document.querySelectorAll('.zoomable').forEach(img => {
        img.addEventListener('click', function() {
            zoomedImage.src = this.src;
            modal.style.display = 'block';
            resetZoom();
        });
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    zoomInBtn.addEventListener('click', function() {
        scale *= 1.2;
        updateTransform();
    });

    zoomOutBtn.addEventListener('click', function() {
        scale = Math.max(0.1, scale / 1.2);
        updateTransform();
    });

    zoomResetBtn.addEventListener('click', resetZoom);

    zoomedImage.addEventListener('wheel', function(e) {
        e.preventDefault();
        const delta = e.deltaY;

        if (delta > 0) {
            scale = Math.max(0.1, scale / 1.1);
        } else {
            scale *= 1.1;
        }

        updateTransform();
    });


    zoomedImage.addEventListener('mousedown', function(e) {
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        initialTranslateX = translateX;
        initialTranslateY = translateY;
        zoomedImage.style.cursor = 'grabbing';
    });

    document.addEventListener('mousemove', function(e) {
        if (isDragging) {
            translateX = initialTranslateX + (e.clientX - startX);
            translateY = initialTranslateY + (e.clientY - startY);
            updateTransform();
        }
    });

    document.addEventListener('mouseup', function() {
        isDragging = false;
        zoomedImage.style.cursor = 'move';
    });
});
