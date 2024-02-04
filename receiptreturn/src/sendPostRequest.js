async function sendPostRequest(formData) {
    // const formData = new FormData();
    // formData.append('file', fileInputElement.files[0]); // Append the first file from fileInputElement
    // formData.append('user', '1');
    const response = await fetch('http://0.0.0.0:8080/upload', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${await response.text()}`);
    }

    const data = await response.json();
    console.log(data);
}

export default sendPostRequest;
