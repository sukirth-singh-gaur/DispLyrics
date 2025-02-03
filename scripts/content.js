let songName = null;

// Initial timeout to capture the song name after 5 seconds
window.setTimeout(() => {
    let songName1 = document.querySelector('a[data-testid="context-item-link"]');
    if (songName1) {
        songName = songName1;
        console.log(`Title: ${songName.innerHTML}`);
    } else {
        console.log("Initial song name element not found.");
    }
}, 5000);

// Interval to check for song name updates
window.setInterval(() => {
    if (songName !== null) {
        let songName2 = document.querySelector('a[data-testid="context-item-link"]');
        if (songName2 && songName.textContent !== songName2.textContent) {
            songName = songName2;
            console.log(`Title: ${songName.innerHTML}`);

            // Start a new interval to check for lyrics
            let lyricsCheckInterval = setInterval(() => {
                let lyricsContainer = document.querySelector('span[class="vkO5F4KbLk8mbjZoy1Lf"]');
                if (lyricsContainer) {
                    console.log("We Found It!");
                    console.log(lyricsContainer.textContent);

                    // Clear lyrics content and stop the interval
                    lyricsContainer.innerHTML = `hola amigo`;
                    //clearInterval(lyricsCheckInterval);
                }
            }, 1000); // Check every 1000ms
        }
    } else {
        console.log("Song name is not initialized.");
    }
}, 1000);
