console.log("CONTENT IS LOADED")

chrome.runtime.onMessage.addListener(async function(request, sender, sendResponse) {
  if (request.data) {
    const result = await navigator.clipboard.writeText(request.data);
    alert("Command copied")
  }
});
