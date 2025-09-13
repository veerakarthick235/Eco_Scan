document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const resultCard = document.getElementById('resultCard');
    const resultItemName = document.getElementById('resultItemName');
    const resultCategory = document.getElementById('resultCategory');
    const resultInstructions = document.getElementById('resultInstructions');
    const resultTip = document.getElementById('resultTip');
    const getLocationBtn = document.getElementById('getLocationBtn');
    const locationDisplay = document.getElementById('locationDisplay');
    const historyList = document.getElementById('historyList');
    const recycledCountEl = document.getElementById('recycledCount');
    const compostedCountEl = document.getElementById('compostedCount');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

    // App State
    const API_URL = 'http://127.0.0.1:5000/classify';
    let userCoordinates = null;

    // --- EVENT LISTENERS ---

    imageUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
            classifyImage(file);
        }
    });

    getLocationBtn.addEventListener('click', () => {
        if (navigator.geolocation) {
            locationDisplay.textContent = "Getting location...";
            navigator.geolocation.getCurrentPosition(position => {
                userCoordinates = {
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                };
                locationDisplay.textContent = `Lat: ${userCoordinates.lat.toFixed(2)}, Lon: ${userCoordinates.lon.toFixed(2)}`;
                console.log("Location obtained:", userCoordinates);
            }, () => {
                locationDisplay.textContent = "Location access denied.";
            });
        } else {
            locationDisplay.textContent = "Geolocation not supported.";
        }
    });

    clearHistoryBtn.addEventListener('click', () => {
        localStorage.removeItem('ecoScanHistory');
        loadHistory();
    });

    // --- CORE FUNCTIONS ---

    async function classifyImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        if (userCoordinates) {
            formData.append('lat', userCoordinates.lat);
            formData.append('lon', userCoordinates.lon);
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            updateResultCard(data);
            updateHistory(data);

        } catch (error) {
            console.error("Error classifying image:", error);
            const errorData = {
                name: "Error",
                category: "Could Not Connect 🔌",
                className: "trash",
                instructions: "Could not connect to the classification server. Please make sure the backend is running and try again.",
                tip: "This project requires two terminals: one for the Python backend and one for the frontend's Live Server."
            };
            updateResultCard(errorData);
        }
    }

    function updateResultCard(item) {
        resultItemName.textContent = item.name;
        resultCategory.textContent = item.category;
        resultCategory.className = `result-category ${item.className}`;
        resultInstructions.textContent = item.instructions;
        resultTip.textContent = item.tip;
        resultCard.classList.remove('hidden');
    }

    // --- HISTORY FUNCTIONS ---

    function updateHistory(item) {
        let history = JSON.parse(localStorage.getItem('ecoScanHistory')) || [];
        history.unshift({ name: item.name, category: item.category, date: new Date().toLocaleTimeString() });
        if (history.length > 10) {
            history.pop();
        }
        localStorage.setItem('ecoScanHistory', JSON.stringify(history));
        loadHistory();
    }

    function loadHistory() {
        let history = JSON.parse(localStorage.getItem('ecoScanHistory')) || [];
        historyList.innerHTML = '';
        let recycledCount = 0;
        let compostedCount = 0;

        history.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.name} (${item.category.split(' ')[0]}) - ${item.date}`;
            historyList.appendChild(listItem);

            if (item.category.includes('Recycle')) recycledCount++;
            if (item.category.includes('Compost')) compostedCount++;
        });

        recycledCountEl.textContent = recycledCount;
        compostedCountEl.textContent = compostedCount;
    }

    // Initial load of history on page start
    loadHistory();
});