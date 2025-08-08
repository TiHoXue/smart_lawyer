// Get the form and file input elements
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const statusMessage = document.getElementById('status');

// Add a submit event listener to the form
form.addEventListener('submit', async (event) => {
    // Prevent the default form submission behavior (which would reload the page)
    event.preventDefault();

    // Create a new FormData object
    // It automatically captures the files from the input
    const formData = new FormData(form);

    // Optional: Log the files to the console to see what you're sending
    for (const file of fileInput.files) {
        console.log(`File selected: ${file.name}, Size: ${file.size}`);
    }

    statusMessage.textContent = 'Uploading...';

    try {
        // Send the FormData to the server using fetch
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
            // Note: No 'Content-Type' header is needed!
            // The browser will automatically set it to 'multipart/form-data'
            // with the correct boundary when you use FormData.
        });

        // Check if the request was successful
        if (response.ok) {
            const result = await response.json();
            statusMessage.textContent = result.message;
            console.log('Server response:', result);
        } else {
            statusMessage.textContent = `Error: ${response.statusText}`;
        }
    } catch (error) {
        statusMessage.textContent = `Upload failed: ${error.message}`;
        console.error('Error uploading files:', error);
    }
});