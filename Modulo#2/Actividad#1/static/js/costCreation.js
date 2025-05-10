document.getElementById("addCostForm").addEventListener("submit", function (event) {
    event.preventDefault(); 

    const costId = document.getElementById('costId').value;  
    const costName = document.getElementById('costName').value;
    const costValue = parseFloat(document.getElementById('costValue').value);


    const data = {
        costName: costName,
        cost: costValue
    };

    fetch(`/day/${costId}/cost`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Cost added successfully:", data);
        document.getElementById('addCostForm').reset(); 
        window.location.reload();
    })
    .catch((error) => {
        console.error("Error adding cost:", error);
    });
});

function deleteCost(costName) {
    const costId = document.getElementById("costId").value;

    fetch(`/day/${costId}/cost`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ costName: costName }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.day) {
            console.log("Cost deleted successfully:", data);
            window.location.reload();
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch((error) => {
        console.error("Error deleting cost:", error);
    });
}

