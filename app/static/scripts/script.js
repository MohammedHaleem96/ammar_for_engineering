function toggleSolarPanelQuestion() {
    // Enable/disable fields based on electricity availability selection
    const is_electricity_available = document.getElementById("is_electricity_available").value;
    const electricity_available_hours = document.getElementById("electricity_available_hours");
    const is_want_panels = document.getElementById("is_want_panels");

    if (is_electricity_available === "yes") {
        electricity_available_hours.disabled = false;
        is_want_panels.disabled = false;
    } else {
        electricity_available_hours.disabled = true;
        electricity_available_hours.value = 0;
        is_want_panels.disabled = true;
        is_want_panels.value = "yes";
    }
                                    }

let loadCounts = {
    "room": 0,
    "aircond" : 0,
    "fridge": 0,
    "motor": 0,

    // Add additional load counts here as needed
};

function increaseLoad(loadType) {
    loadCounts[loadType]++;
    document.getElementById(`${loadType}-count`).innerText = loadCounts[loadType];
    updateLoadEstimate();
}

function decreaseLoad(loadType) {
    if (loadCounts[loadType] > 0) loadCounts[loadType]--;
    document.getElementById(`${loadType}-count`).innerText = loadCounts[loadType];
    updateLoadEstimate();
}

function updateLoadEstimate() {
    let load = 0;
    document.getElementById("estimatedCost").innerText = 0;
    load += loadCounts["room"] * 120; // Example cost per room
    load += loadCounts["aircond"] * 120; // Example cost per Aircond
    load += loadCounts["fridge"] * 180; // Example cost per fridge
    load += loadCounts["motor"] * 350; // Example cost per motor
    document.getElementById("estimatedLoad").innerText = load;
    
    if (load > 0 && load < 1000 ){
    document.getElementById("estimatedCost").innerText =    "1";
    document.getElementById("total_load").value = load;
    }
    if (load > 1000 && load <3000){
        document.getElementById("estimatedCost").innerText = "2";
        document.getElementById("total_load").value = load;

    }
    if (load > 3000 && load <5200){
        document.getElementById("estimatedCost").innerText = "3";
        document.getElementById("total_load").value = load;

    }
    if (load > 5200 && load <10400){
        document.getElementById("estimatedCost").innerText = "4";
        document.getElementById("total_load").value = load;

    }
    if (load > 10400){
        document.getElementById("estimatedCost").innerText = "5" ;
        document.getElementById("total_load").value = load;
    }
                             }
