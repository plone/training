let breadcrumbMapping; // Storing the fetched JSON here
let resultHeading=""; // Store the result headings once fetched
const nucliaResult = document.querySelector("nuclia-search-results");
const shadowRoot = nucliaResult.shadowRoot;

async function fetchBreadcrumbMapping() {
  try {
    const response = await fetch("/_static/heading_mapping.json");
    breadcrumbMapping = await response.json();
  } catch (error) {
    console.error("Error fetching mapping:", error);
  }
}

fetchBreadcrumbMapping();

function createBreadcrumbs(Container) {

  let ContainerHeading = Container.querySelector("div");
  resultHeading = ContainerHeading.querySelector("h3").innerText;

  try {
    insertBreadcrumbDiv(resultHeading, ContainerHeading);
  } catch (error) {
    console.error("Error in createBreadcrumbs:", error);
  }
}

function insertBreadcrumbDiv(resultHeading, ContainerHeading) {
  const jsonData =
      breadcrumbMapping["heading_to_breadcrumb"][resultHeading];
    if (!jsonData) {
      throw new Error("No breadcrumbs found for the heading: ", resultHeading);
  }

  if (!ContainerHeading.querySelector("div.breadcrumbs")) {
    let breadcrumbContainer = document.createElement("div");
    breadcrumbContainer.className = "breadcrumbs";

    let i = 0;
    Object.keys(jsonData).forEach(key => {
      const value = jsonData[key];

      // Create a span element for each breadcrumb
      let breadcrumbSpan = document.createElement("span");
      // Create a breadcrumb link or span based on whether it's the last breadcrumb
      if (i < Object.keys(jsonData).length - 1) {
        let breadcrumbLink = document.createElement("a");
        breadcrumbLink.href = value;
        breadcrumbLink.textContent = key;
        breadcrumbLink.classList.add("breadcrumb-link");
        breadcrumbSpan.appendChild(breadcrumbLink);

        // Add a separator between breadcrumb links (e.g., '>')
        let separator = document.createTextNode(" > ");
        breadcrumbSpan.appendChild(separator);
      } else {
        // If it's the last breadcrumb, create a non-clickable span
        breadcrumbSpan.textContent = key;
        breadcrumbSpan.classList.add("breadcrumb-last");
      }
      i++;

      breadcrumbContainer.appendChild(breadcrumbSpan);
  });

    ContainerHeading.insertAdjacentElement(
      "afterbegin",
      breadcrumbContainer
    );
  }
}


function isMatch(element) {
  return (
    element &&
    element.nodeName === "DIV" &&
    element.classList &&
    element.classList.contains("result-title-container") &&
    element.classList.length === 2
  );
}

// Function to process added nodes within the shadow DOM
function processAddedNodes(addedNodes) {
  addedNodes.forEach((addedNode) => {
    if (isMatch(addedNode)) {
      createBreadcrumbs(addedNode);
    }
  });
}

function addBreadcrumbsToResults() {
  if (!nucliaResult) {
    console.error("Nuclia-search-result tag not found");
    return;
  }
  let observer = new MutationObserver(callback);

  observer.observe(shadowRoot, {
    childList: true,
    subtree: true,
  });
}

const callback = function (mutationsList, observer) {
  for (const mutation of mutationsList) {
    if (mutation.type === "childList") {
      processAddedNodes(mutation.addedNodes);
    }
  }
};

const style = document.createElement('style');
style.textContent = `
  
/* Breadcrumb container */
.breadcrumbs {
  font-size: 16px;
  margin: 10px 0;
}

/* Breadcrumb links */
.breadcrumbs a {
  text-decoration: none;
  color: #007bff;
  transition: color 0.2s;
}

/* Style for the last breadcrumb */
.breadcrumbs span:last-child {
  color: #555; 
}

/* Separator between breadcrumbs */
.breadcrumbs .separator {
  margin: 0 5px;
  color: #777; 
}

/* Hover effect for breadcrumb links */
.breadcrumbs a:hover {
  color: #0056b3;
}

`;
// Append the style element to the shadow DOM
shadowRoot.appendChild(style);
