const { switchMap } = rxjs;
const nucliaResult = document.querySelector("nuclia-search-results");
const shadowRoot = nucliaResult.shadowRoot;

const nuclia = new window.NucliaSDK.Nuclia({
  backend: "https://nuclia.cloud/api",
  zone: "europe-1",
  knowledgeBox: "62407006-2711-4631-9c03-761d156de289",
});

function createBreadcrumbs(Container) {

  // Container hash gets the md5 value of resource but i am unable to find resource by passing that hash
  // let ContainerHash = Container.querySelector(
  //   "div > div.sw-field-metadata > div > div:nth-child(2) > span.title-xxs"
  // ).innerText;

  let ContainerHeading = Container.querySelector("div");

  // One of The hash that works 79e4d894189842acb0902b5d879c2fe6
  try {
    nuclia.db
      .getKnowledgeBox()
      .pipe(
        switchMap((knowledgeBox) =>
          knowledgeBox.getResource("79e4d894189842acb0902b5d879c2fe6", [
            "extra",
          ])
        )
      )
      .subscribe(
        (resource) => {
          insertBreadcrumbDiv(resource, ContainerHeading);
        },
        (error) => {
          console.error("Error fetching resource:", error);
        }
      );
  } catch (error) {
    console.error("Error in createBreadcrumbs:", error);
  }
}

function insertBreadcrumbDiv(resource, ContainerHeading) {
  let array = resource.extra.metadata["breadcrumbs"];
  if (!ContainerHeading.querySelector("div.breadcrumbs")) {
    let breadcrumbContainer = document.createElement("div");
    breadcrumbContainer.className = "breadcrumbs";
    for (let i = 0; i < array.length; i++) {
      let dict = array[i];

      // Create a span element for each breadcrumb
      let breadcrumbSpan = document.createElement("span");

      // Create a breadcrumb link or span based on whether it's the last breadcrumb
      if (i < array.length - 1) {
        let breadcrumbLink = document.createElement("a");
        breadcrumbLink.href = dict.url;
        breadcrumbLink.textContent = dict.label;
        breadcrumbLink.classList.add("breadcrumb-link");
        breadcrumbSpan.appendChild(breadcrumbLink);

        // Add a separator between breadcrumb links (e.g., '>')
        let separator = document.createTextNode(" > ");
        breadcrumbSpan.appendChild(separator);
      } else {
        // If it's the last breadcrumb, create a non-clickable span
        breadcrumbSpan.textContent = dict.label;
        breadcrumbSpan.classList.add("breadcrumb-last");
      }

      breadcrumbContainer.appendChild(breadcrumbSpan);
    }
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
