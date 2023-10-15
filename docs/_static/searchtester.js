const { switchMap } = rxjs;
const nucliaResult = document.querySelector("nuclia-search-results");
const shadowRoot = nucliaResult.shadowRoot;

const nuclia = new window.NucliaSDK.Nuclia({
  backend: "https://nuclia.cloud/api",
  zone: "europe-1",
  knowledgeBox: "62407006-2711-4631-9c03-761d156de289",
});

function createBreadcrumbs(resultTitleContainer,ContainerHash) {

  let ContainerHeading = resultTitleContainer.querySelector("div:nth-child(2)");

  try {
    nuclia.db
      .getKnowledgeBox()
      .pipe(
        switchMap((knowledgeBox) =>
          knowledgeBox.getResource(ContainerHash, [
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

        // Add a separator between breadcrumb links 
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
    element.classList.contains("sw-result-row") &&
    element.classList.length === 2
  );
}

// Function to process added nodes within the shadow DOM
function processAddedNodes(addedNodes) {
  addedNodes.forEach((addedNode) => {
    if (isMatch(addedNode)) {
      let resultTitleContainer = addedNode.querySelector('.result-title-container')
      let ContainerHash = addedNode.getAttribute('data-nuclia-rid');
      if (ContainerHash.length == 32) { // To be removed when Null result issue get solved
        createBreadcrumbs(resultTitleContainer,ContainerHash);
      }
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
:host {
  --pst-color-primary: #579aca;
  --color-on-hover: #0056b3;
  --color-of-separator: #777;
  --color-of-lastbreadcrumb: #CECECE;
  --size-of-title-m: 22px;
}

/* Breadcrumb container */
.breadcrumbs {
  margin: 10px 0;
}

/* Breadcrumb links */
.breadcrumbs a {
  font-size: var(--font-size-small);
  text-decoration: none;
  color: var(--pst-color-primary);
  transition: color 0.2s;
}

/* Style for the last breadcrumb */
.breadcrumbs span:last-child {
  font-size: var(--font-size-small);
  color: var(--color-of-lastbreadcrumb); 
}

/* Separator between breadcrumbs */
.breadcrumbs .separator {
  font-size: var(--font-size-small);
  margin: 0 5px;
  color: var(--color-of-separator); 
}

/* Hover effect for breadcrumb links */
.breadcrumbs a:hover {
  color: var(--color-on-hover);
}

/*Heading of the results*/
h3.ellipsis.title-m{
    color: var(--pst-color-primary);
    font-size: var(--size-of-title-m);
}

/*Subheading of the results*/
.sw-paragraph-result {
  color: var(--pst-color-primary);
}
/*Gap between results*/
.results, .search-results {
  gap: var(--rhythm-7);
}
/*Gap between widget and answer generation*/
.sw-initial-answer {
  margin-top: var(--rhythm-3);
}
`;
// Append the style element to the shadow DOM
shadowRoot.appendChild(style);

function handleThemeChange(mutationsList) {
  mutationsList.forEach((mutation) => {
      if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
          const newMode = htmlSelector.getAttribute('data-theme');
          const nucliaSearchResults = document.querySelector('nuclia-search-results');
          const nucliaSearchBar = document.querySelector('nuclia-search-bar');
          const currentMode = nucliaSearchResults.getAttribute('mode');

          if (newMode === 'dark' && currentMode !== 'dark') {
              nucliaSearchResults.setAttribute('mode', 'dark');
            nucliaSearchBar.setAttribute('mode', 'dark');
          } else if (newMode === 'light' && currentMode !== 'light') {
              nucliaSearchResults.setAttribute('mode', 'light');
            nucliaSearchBar.setAttribute('mode', 'light');
          }
      }
  });
}

// Select the HTML element and configure the observer
const htmlSelector = document.querySelector('html');
const observer = new MutationObserver(handleThemeChange);

// Start observing changes in the data-theme attribute
observer.observe(htmlSelector, { attributes: true, attributeFilter: ['data-theme'] });