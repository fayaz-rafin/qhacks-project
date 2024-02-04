

async function sendPostRequest() {
    const response = await fetch('https://example.com/api/some-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            key1: 'value1',
            key2: 'value2'
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);
}

export default sendPostRequest;