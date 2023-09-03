let breadcrumbMapping; // Storing the fetched JSON here
let resultHeadings = []; // Store the result headings once fetched
let counter = 0;

// Function to load JSON into script
async function fetchBreadcrumbMapping() {
  try {
    const response = await fetch("/_static/heading_to_breadcrumb_mapping.json");
    breadcrumbMapping = await response.json();
  } catch (error) {
    console.error("Error fetching mapping:", error);
  }
}

fetchBreadcrumbMapping();

// Function to create breadcrumbs so that we can just put in title of results
async function createBreadcrumbs(resultHeading) {
  try {
    // Check if the heading exists in the mapping
    const breadcrumbs =
      breadcrumbMapping["heading_to_breadcrumb"][resultHeading];
    if (!breadcrumbs) {
      throw new Error("No breadcrumbs found for the heading: ", resultHeading);
    }
    return breadcrumbs;
  } catch (error) {
    console.error("Error fetching mapping:", error);
    return [];
  }
}

// Function to add breadcrumbs above each result heading
function addBreadcrumbsToResults() {
  // select the tag being populated with results
  const nucliaResult = document.querySelector("nuclia-search-results");

  if (!nucliaResult) {
    return; // Exit if nuclia-search-results tag is not found
  }

  // need to acces the shadow root
  const shadowRoot = nucliaResult.shadowRoot;

  // Observe changes in the shadow root of nuclia-search-results element
  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === "childList") {
        // Check if the mutation involves the addition of nodes
        if (mutation.addedNodes.length > 0) {
          // Iterate through added nodes and process them
          mutation.addedNodes.forEach((addedNode) => {
            // Check if the added node has the 'result-container' class
            if (
              addedNode.classList &&
              addedNode.classList.contains("result-container")
            ) {
              // Find all h3 tags with the specified class within the result container and adding to resultHeadings
              resultHeadings = Array.from(mutation.addedNodes).flatMap(
                (addedNode) =>
                  Array.from(
                    addedNode.querySelectorAll(
                      "h3.ellipsis.title-m.svelte-1yttzcg"
                    )
                  )
              );

              resultHeadings.forEach((resultHeading) => {
                // Check if the result heading already has breadcrumbs
                if (!resultHeading.dataset.breadcrumbsAdded) {
                  // If Not, Then Mark the element as having breadcrumbs
                  resultHeading.dataset.breadcrumbsAdded = true;
                  // Create breadcrumbs for the result item
                  createBreadcrumbs(resultHeading.innerHTML)
                    .then((breadcrumbObj) => {
                      // Create a container with class breadcrumbs
                      const breadcrumbContainer = document.createElement("div");
                      breadcrumbContainer.className = "breadcrumbs";

                      const breadcrumbNames = Object.keys(breadcrumbObj);
                      const lastBreadcrumb = breadcrumbNames.pop();

                      breadcrumbNames.forEach((breadcrumbName, index) => {
                        // Create anchor
                        const breadcrumbLink = document.createElement("a");
                        breadcrumbLink.href = breadcrumbObj[breadcrumbName]; // URL from JSON
                        breadcrumbLink.textContent = breadcrumbName;

                        // Create a span for this anchor
                        const breadcrumbElement =
                          document.createElement("span");
                        breadcrumbElement.className = "breadcrumb-item"; // Apply the breadcrumb-item class

                        breadcrumbElement.appendChild(breadcrumbLink);

                        // Add the separator " > " between elements
                        if (
                          breadcrumbNames.length > 1 &&
                          counter < breadcrumbNames.length - 1
                        ) {
                          counter = counter + 1;
                          const separator = document.createElement("span");
                          separator.textContent = " > ";
                          separator.className = "pathseparator";
                          breadcrumbContainer.appendChild(separator);
                        }

                        breadcrumbContainer.appendChild(breadcrumbElement);
                      });

                      // Add the last breadcrumb as a non-clickable span
                      const lastBreadcrumbElement =
                        document.createElement("span");
                      lastBreadcrumbElement.className = "last-breadcrumb";
                      lastBreadcrumbElement.textContent = lastBreadcrumb;

                      breadcrumbContainer.appendChild(lastBreadcrumbElement);

                      resultHeading.insertAdjacentElement(
                        "beforebegin",
                        breadcrumbContainer
                      );
                    })
                    .catch((error) => {
                      console.error("Error creating breadcrumbs:", error);
                    });
                }
              });
            }
          });
        }
      }
    }
  });

  // Start observing the shadow root of each nuclia-search-results element
  observer.observe(shadowRoot, {
    childList: true,
    subtree: true,
  });
  // Need To stop Observing when the Nuclia results are populated
  // but I guess they keep updating so need to observe continously.
}
