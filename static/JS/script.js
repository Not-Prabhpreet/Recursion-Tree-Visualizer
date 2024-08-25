document.addEventListener("DOMContentLoaded", function () {
  const functionSelect = document.getElementById("function-select");

const predefinedFunctions = {
  factorial: {
    definition: `def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)`,
    call: "factorial(5)"
  },
  fibonacci: {
    definition: `def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)`,
    call: "fibonacci(4)"
  },
  hanoi: {
    definition: `def hanoi(n, source, target, auxiliary):
    if n > 0:
        hanoi(n - 1, source, auxiliary, target)
        print(f"Move disk {n} from {source} to {target}")
        hanoi(n - 1, auxiliary, target, source)`,
    call: 'hanoi(3, "A", "C", "B")'
  }
};

functionSelect.addEventListener("change", function() {
  const selectedFunction = predefinedFunctions[this.value];
  if (selectedFunction) {
    functionDefinition.value = selectedFunction.definition;
    functionCall.value = selectedFunction.call;
  } else {
    functionDefinition.value = "";
    functionCall.value = "";
  }
});
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