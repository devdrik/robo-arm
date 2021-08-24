
const setPosition = () => {
    sendGetRequest('/setPosition')
}

sendGetRequest = request => {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
}