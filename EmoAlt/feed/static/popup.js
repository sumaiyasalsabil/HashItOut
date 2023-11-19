function showPopup(data) {
    if (data === 1) {
        document.getElementById("alertPopup").style.display = "block";
    }
}

function showResources() {
    window.location.href = resourcesUrl; // Defined in feed.html
}

function closePopup() {
    document.getElementById("alertPopup").style.display = "none";
}