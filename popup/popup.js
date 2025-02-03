fetch('./resultsFound.json') // Path to your JSON file
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); // Automatically parses JSON response
  })
  .then((data) => {
    // Locate the list container using the correct class selector
    const songList = document.querySelector(".songList");
    if (!songList) {
      console.error("Error: Element with class 'songList' not found in the DOM.");
      return;
    }

    // Build the list items
    let listContent = data.map(item => `<div class='songItem'><a >${item.song_name}</a></div>`).join("");

    // Update the innerHTML of the song list
    songList.innerHTML = listContent;

    console.log("Rendered song list:", songList.innerHTML);
  })
  .catch((error) => {
    console.error("Error loading or parsing JSON file:", error);
  });
