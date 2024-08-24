document.addEventListener("DOMContentLoaded", function () {
  const functionDefinition = document.getElementById("function-definition");
  const functionCall = document.getElementById("function-call");
  const visualizeBtn = document.getElementById("visualize-btn");
  const svgContainer = document.getElementById("svg-container");
  const errorMessage = document.getElementById("error-message");

  const darkModeToggle = document.getElementById("dark-mode-toggle");

  darkModeToggle.addEventListener("change", function () {
  document.body.classList.toggle("dark-mode");
  });
  visualizeBtn.addEventListener("click", function () {
    const functionDefinitionValue = functionDefinition.value;
    const functionCallValue = functionCall.value;

    fetch("/visualize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        definition: functionDefinitionValue,
        call: functionCallValue,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          errorMessage.textContent = data.error;
          svgContainer.innerHTML = "";
          errorMessage.style.display = "block";
        } else {
          errorMessage.style.display = "none";
          svgContainer.innerHTML = data.svg;

          // Initialize the RecursiveTreeViz
          const svgElement = svgContainer.querySelector("svg");
          if (svgElement) {
            const viz = new RecursiveTreeViz(svgElement);
            viz.draw();
          } else {
            console.error("SVG element not found");
          }
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        errorMessage.textContent = `Error: ${error.message}`;
        svgContainer.innerHTML = "";
        errorMessage.style.display = "block";
      });
  });
});