
// Function to update the current time every second
function updateTime() {
    var now = new Date();
    var hours = now.getHours().toString().padStart(2, '0');
    var minutes = now.getMinutes().toString().padStart(2, '0');
    var seconds = now.getSeconds().toString().padStart(2, '0');
    var timeString = hours + ':' + minutes + ':' + seconds;
    document.getElementById('current-time').textContent = timeString;
}

// Update time immediately and then every second
updateTime();
setInterval(updateTime, 1000);




    // Function to display the current day of the week
    function displayCurrentDay() {
        var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        var currentDate = new Date();
        var dayOfWeek = daysOfWeek[currentDate.getDay()];
        document.getElementById('day').innerHTML = dayOfWeek;
    }

    // Call the function to display the current day when the window loads
    window.onload = function() {
        displayCurrentDay();
    };


