/**
 * Scroll to active navigation element
 */


var sbRunWhenDOMLoaded = (cb) => {
  console.debug("*** sbRunWhenDOMLoaded", cb);
    if (document.readyState != "loading") {
      cb();
    } else if (document.addEventListener) {
      document.addEventListener("DOMContentLoaded", cb);
    } else {
      document.attachEvent("onreadystatechange", function () {
        if (document.readyState == "complete") cb();
      });
    }
  };
  
  var scrollToActive = () => {
    let active_navigation_item = [...document.querySelectorAll("li.current.active")].pop();
    if (active_navigation_item) {
      active_navigation_item.scrollIntoView();

      let article = [...document.querySelectorAll("article")].pop();
      article.scrollIntoView({inline: "start" });
    }
  };  
  
  sbRunWhenDOMLoaded(scrollToActive);
  