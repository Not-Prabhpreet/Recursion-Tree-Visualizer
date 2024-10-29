class RecursiveTreeViz {
  constructor(svg) {
    this.svg = svg;
    this.steps = [];
    this.frames = {};
    this.currentStep = 0;
    this.currentScale = 1;
    
  }
  

  draw() {
    // Store all the frames
    const frames = this.svg.querySelectorAll(".node");
    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      const frameId = frame.querySelector("title").textContent;
      this.frames[frameId] = frame;
      
    }

    // Determine number of steps
    const edges = this.svg.querySelectorAll(".edge");
    for (let i = 0; i < edges.length; i++) {
      const edge = edges[i];
      const edgeTitle = edge.querySelector("title").textContent;
      const edgeText = edge.querySelector("text");
      if (edgeText) {
        let stepNum, isReturn;
        const edgeTextContent = edgeText.textContent;
        stepNum = parseInt(edgeTextContent.match(/\(#(\d+)\)/)?.[1], 10);
        if (isNaN(stepNum)) continue;
        if (edgeTitle.endsWith(":c")) {
          isReturn = true;
          edgeText.textContent = edgeTextContent.split("(#")[0];
        } else {
          edgeText.textContent = "";
          isReturn = false;
        }
        const [parentFrameId, childFrameId] = edgeTitle
          .split(":c")[0]
          .split("->");
        this.steps[stepNum] = {
          parentFrame: this.frames[parentFrameId],
          childFrame: this.frames[childFrameId],
          edge: edge,
          isReturn: isReturn,
        };
      }
    }

    this.currentStep = 0;
    this.drawControls();
    this.toggleSteps();
  }

  drawControls() {
    const controlsDiv = document.createElement("div");
    controlsDiv.classList.add("svg-controls");

    this.prevButton = document.createElement("button");
    this.prevButton.innerText = "< Prev";
    this.prevButton.addEventListener("click", () => this.onPrevClick());

    this.nextButton = document.createElement("button");
    this.nextButton.innerText = "Next >";
    this.nextButton.addEventListener("click", () => this.onNextClick());

    this.slider = document.createElement("input");
    this.slider.type = "range";
    this.slider.min = "0";
    this.slider.max = this.steps.length - 1;
    this.slider.value = this.currentStep;
    this.slider.addEventListener("input", (e) => this.onSliderChange(e));

    controlsDiv.appendChild(this.prevButton);
    controlsDiv.appendChild(this.slider);
    controlsDiv.appendChild(this.nextButton);

    this.svg.parentNode.insertBefore(controlsDiv, this.svg.nextSibling);

    this.fixButtons();
  }

  toggleSteps() {
    this.steps.forEach((step, stepI) => {
      if (stepI === 0) {
        step.parentFrame?.classList.add("activated");
      }
      if (stepI <= this.currentStep) {
        step.edge?.classList.add("activated");
        step.childFrame?.querySelector("rect")?.setAttribute("fill", "#B2DFDB");
      } else {
        step.edge?.classList.remove("activated");
        if (!step.isReturn)
          step.childFrame
            ?.querySelector("rect")
            ?.setAttribute("fill", "#E0F2F1");
      }
    });
  }

  onSliderChange(event) {
    this.currentStep = parseInt(event.target.value, 10);
    this.fixButtons();
    this.toggleSteps();
  }

  onPrevClick() {
    if (this.currentStep > 0) {
      this.currentStep--;
      this.slider.value = this.currentStep;
      this.fixButtons();
      this.toggleSteps();
    }
  }

  onNextClick() {
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++;
      this.slider.value = this.currentStep;
      this.fixButtons();
      this.toggleSteps();
    }
  }

  fixButtons() {
    this.prevButton.disabled = this.currentStep === 0;
    this.nextButton.disabled = this.currentStep === this.steps.length - 1;
  }
}
