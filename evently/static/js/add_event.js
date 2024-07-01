document.addEventListener("DOMContentLoaded", function () {
    var toggleAddEventButton = document.getElementById("toggleAddEventButton");
    var addEventForm = document.getElementById("addEventForm");

    toggleAddEventButton.addEventListener("click", function () {
        if (addEventForm.style.display === "none" || addEventForm.style.display === "") {
            addEventForm.style.display = "block";
        } else {
            addEventForm.style.display = "none";
        }
    });
});