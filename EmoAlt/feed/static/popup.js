function showPopup(data) {
    //if (data === 1) {
    document.getElementById("alertPopup").style.display = "block";
    //}
}

function showResources() {
    window.location.href = resourcesUrl; // Defined in feed.html
}

function closePopup() {
    document.getElementById("alertPopup").style.display = "none";
}

function getRandomInterval(min, max) {
    return Math.random() * (max - min) + min;
}

function setupPopupInterval() {
    var interval = getRandomInterval(20000, 30000); 
    setTimeout(function() {
        showPopup();
        //setupPopupInterval(); 
    }, interval);
}

setupPopupInterval();
