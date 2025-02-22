function observeNodeInsertion(selector, callback) {
  document.querySelectorAll(selector).forEach(callback);

  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === "childList") {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE && node.matches(selector)) {
            if (callback)
              callback(node);
          }
        }
      }
    }
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
}