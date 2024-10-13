document.getElementById('urlForm').onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    const url = event.target.original_url.value; // Get the URL from the input

    fetch('/api/shorten/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({ original_url: url })
    })
    .then(response => response.json())
    .then(data => {
        const successAlert = document.querySelector('.alert-success');
        const errorAlert = document.querySelector('.alert-danger');

        if (data.short_url) {
            successAlert.innerHTML = `Shortened URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
            successAlert.style.display = 'block';
            errorAlert.style.display = 'none';
        } else {
            errorAlert.textContent = `Error: ${data.error || 'Something went wrong.'}`;
            errorAlert.style.display = 'block';
            successAlert.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.querySelector('.alert-danger').textContent = 'An error occurred. Please try again.';
        document.querySelector('.alert-danger').style.display = 'block';
    });
}




document.getElementById('urlForm').onsubmit = function(event) {
    event.preventDefault();
    const url = event.target.original_url.value;
    const shortenedUrlDiv = document.getElementById('shortenedUrl');

    shortenedUrlDiv.style.display = 'none';
    shortenedUrlDiv.classList.remove('alert-success', 'alert-danger');

    fetch('/api/shorten/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({ original_url: url })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.short_url) {
            shortenedUrlDiv.innerHTML = `Shortened URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
            shortenedUrlDiv.classList.add('alert-success');
            event.target.reset(); // Reset form after successful submission
        } else {
            shortenedUrlDiv.textContent = `Error: ${data.error || 'Something went wrong.'}`;
            shortenedUrlDiv.classList.add('alert-danger');
        }
        shortenedUrlDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        shortenedUrlDiv.textContent = 'An error occurred. Please try again.';
        shortenedUrlDiv.classList.add('alert-danger');
        shortenedUrlDiv.style.display = 'block';
    });
};

