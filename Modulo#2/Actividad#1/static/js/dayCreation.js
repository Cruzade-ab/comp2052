const dateInput = document.getElementById('dayDate');

document.getElementById("addDayForm").addEventListener("submit", function (event) {
    event.preventDefault();  // Prevent form reload

    const data = { day: dateInput.value };  // ✅ Get input value

    console.log("data: ", data);

    fetch("/day", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),  
    })
    .then((response) => {
        if (response.ok) {
            return response.json(); 
        } else {
            console.error("Failed to create day");
        }
    })
    .then((result) => {
        if (result?.redirectUrl) {
            window.location.href = result.redirectUrl; 
        }
    })
    .catch((error) => {
        console.error("Error:", error);
    });
});
