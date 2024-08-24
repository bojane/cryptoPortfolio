<!DOCTYPE html>
<html>
<head>
    <!-- Include any necessary styles and scripts here -->
</head>
<body>
    <!-- Your web page content -->
    
    <!-- Add an "update" button -->
    <button id="updateButton">Update Data</button>

    <script>
        // Attach a click event handler to the "update" button
        document.getElementById('updateButton').addEventListener('click', function() {
            // Send an HTTP POST request to trigger the update on the server
            fetch('/update-crypto-data', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Cryptocurrency data updated successfully.');
                    // Refresh the page or update the content as needed
                    location.reload();
                } else {
                    alert('Error updating cryptocurrency data.');
                }
            })
            .catch(error => {
                console.error('An error occurred:', error);
                alert('An error occurred while updating cryptocurrency data.');
            });
        });
    </script>
</body>
</html>