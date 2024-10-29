document.addEventListener("DOMContentLoaded", function () {
  const functionSelect = document.getElementById("function-select");

  const predefinedFunctions = {
    factorial: {
      definition: `def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)`,
      call: "factorial(5)",
    },
    fibonacci: {
      definition: `def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)`,
      call: "fibonacci(4)",
    },
    tail_fibonacci: {
      definition: `def tail_fibonacci(n, a=0, b=1):
    if n == 0:
        return a
    if n == 1:
        return b
    return tail_fibonacci(n - 1, b, a + b)`,
      call: "tail_fibonacci(4)",
    },
    hanoi: {
      definition: `def hanoi(n, source, target, auxiliary):
    if n > 0:
        hanoi(n - 1, source, auxiliary, target)
        print(f"Move disk {n} from {source} to {target}")
        hanoi(n - 1, auxiliary, target, source)`,
      call: 'hanoi(3, "A", "C", "B")',
    },
    binary_search: {
      definition: `def binary_search(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)`,
      call: "binary_search([1,2,3,4,5,6,7,8,9], 6)",
    },
    merge_sort: {
      definition: `def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result`,
      call: "merge_sort([64, 34, 25, 12, 22, 11, 90])",
    },
    gcd: {
      definition: `def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)`,
      call: "gcd(48, 18)",
    },
    sum_natural: {
      definition: `def sum_natural(n):
    if n <= 1:
        return n
    return n + sum_natural(n-1)`,
      call: "sum_natural(5)",
    },
    power: {
      definition: `def power(base, exponent):
    if exponent == 0:
        return 1
    if exponent < 0:
        return 1/power(base, -exponent)
    return base * power(base, exponent-1)`,
      call: "power(2, 4)",
    },
  };
  functionSelect.addEventListener("change", function () {
    console.log("Selected value:", this.value);  // Add this line
    const selectedFunction = predefinedFunctions[this.value];
    console.log("Selected function:", selectedFunction); 
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
