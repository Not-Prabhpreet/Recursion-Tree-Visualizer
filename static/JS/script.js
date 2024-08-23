document.addEventListener('DOMContentLoaded', function() {
    const functionDefinition = document.getElementById('function-definition');
    const functionCall = document.getElementById('function-call');
    const visualizeBtn = document.getElementById('visualize-btn');
    const svgContainer = document.getElementById('svg-container');
    const errorMessage = document.getElementById('error-message');

    visualizeBtn.addEventListener('click', function() {
        const functionDefinitionValue = functionDefinition.value;
        const functionCallValue = functionCall.value;

        console.log("Sending function definition:", functionDefinitionValue);
        console.log("Sending function call:", functionCallValue);

        fetch(`/visualize?definition=${encodeURIComponent(functionDefinitionValue)}&call=${encodeURIComponent(functionCallValue)}`)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP error! status: ${response.status}, message: ${text}`);
                });
            }
            return response.text();
        })
        .then(data => {
            console.log("Raw server response:", data);
            if (data.startsWith('Error:')) {
                errorMessage.textContent = data;
                svgContainer.style.display = 'none';
                errorMessage.style.display = 'block';
            } else {
                fetch(`/rendered/${data}`)
                    .then(response => response.text())
                    .then(dotContent => {
                        // Use viz.js to render the dot content
                        const svg = Viz(dotContent, { format: "svg" });
                        svgContainer.innerHTML = svg;
                        svgContainer.style.display = 'block';
                        errorMessage.style.display = 'none';
                        
                        // Initialize the RecursiveTreeViz
                        const svgElement = svgContainer.querySelector('svg');
                        new RecursiveTreeViz(svgElement).draw();
                    });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = `Error: ${error.message}`;
            svgContainer.style.display = 'none';
            errorMessage.style.display = 'block';
        });
    });
});