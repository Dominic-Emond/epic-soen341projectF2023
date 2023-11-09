async function getPropertyData() {

    const url = "http://127.0.0.1:8000/brokers/1";

    console.log("Sending Response!");
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);

    getBroker(data);
}

function getBroker(data) {
    const broker = document.getElementById('broker-name');
    broker.textContent = data.First_Name + " " + data.Last_Name;
}

window.addEventListener('load', getPropertyData);