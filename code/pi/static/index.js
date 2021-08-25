
const setPosition = () => {
    sendGetRequest('/setPosition')
}

const saveToFile = () => {
    sendGetRequest('/saveToFile')
}

const runActions = () => {
    sendGetRequest('/runActions')
}

const clearActions = () => {
    sendGetRequest('/clearActions')
}

sendGetRequest = request => {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
}