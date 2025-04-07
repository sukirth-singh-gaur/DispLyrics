console.log('Displyrics console log is working!');

let state = {
    "lyrics-available" : true,
    "lyrics-fetched" : false,
    "lyrics-displayed" : false
};
  
chrome.storage.local.set({ status: state }, () => {
    console.log("State saved from content script");
});
  

const style = document.createElement("style");
style.textContent = `
.container-style {
  display: block; /* Makes sure it behaves like a normal div */
  text-align: left; /* Aligns text to the left */
  justify-content: flex-start; /* Just in case flex is inherited */
  align-items: flex-start;
  font-size: xx-large;
  font-weight: 1000;
  padding-left: 4rem;
  padding-top: 4rem;
  background: rgb(0 61 0);
  color: rgb(255, 255, 255);
}

.credits {
  padding-left: 4rem;
  padding-top: 2rem;
  padding-bottom: 4rem;
  background: rgb(0 61 0);
  color: rgb(116 228 136);
}

`;
document.head.appendChild(style);

let songTitleOld = null;
let songTitle = null;
let songData = null;

setInterval(()=>{
    try {
        let lyricsButton = document.querySelector("button[data-testid='lyrics-button']");
        let songTitleNew = document.querySelector("a[data-testid='context-item-link']").innerHTML;
        //console.log(songTitleNew.innerHTML);
        
        if(songTitleOld !== songTitleNew){
            songTitleOld = songTitle;
            songTitle = songTitleNew;  
        }
        lyricsButton.removeAttribute("disabled");
        
        const dataActive = lyricsButton.getAttribute('data-active');
        const ariaPressed = lyricsButton.getAttribute('aria-pressed');
        
        lyricsButton.addEventListener('click',()=>{
            
            
            const newdataActive = dataActive === "true" ? "false" : "true" ;
            const newdariaPressed = ariaPressed === "true" ? "false" : "true" ;
            
            lyricsButton.setAttribute('data-active',newdataActive);
            lyricsButton.setAttribute('aria-pressed',newdariaPressed);
            lyricsButton.classList.toggle('RK45o6dbvO1mb0wQtSwq');
            lyricsButton.classList.toggle('EHxL6K_6WWDlTCZP6x5w');
            if(newdataActive === "true") window.location.href = "https://open.spotify.com/lyrics";
        })

    } catch (error) {
        console.log("Dom content loading",error)
    } 

},2000)

setInterval(()=>{
    let lyricsButton = document.querySelector("button[data-testid='lyrics-button']");
    if(songTitle!= songTitleOld){
        lyricsFetched = false;
        console.log(songTitle); 
        // aria-label = "Looks like we don't have the lyrics for this song."
        if(lyricsButton.getAttribute('aria-label') === "Looks like we don't have the lyrics for this song."){
            if(!lyricsFetched){
                lyricsFetched = true; // prevent double fetch
                console.log("fetching lyrics from server...");   
                fetchLyricsFromServer(songTitle); 
            }
        }
        if(lyricsButton.getAttribute('aria-pressed') === 'true'){
            try {
                let container = document.querySelector('.vkO5F4KbLk8mbjZoy1Lf');
                //console.log(container.innerHTML);
            
                if(
                    !lyricsFetched && (
                    container.innerHTML === "Looks like we don't have the lyrics for this song." || 
                    container.innerHTML === "You'll have to guess the lyrics for this one." || 
                    container.innerHTML === "Hmm. We don't know the lyrics for this one." ||
                    container.innerHTML === "You caught us, we're still working on getting lyrics for this one.")){
                        lyricsFetched = true;
                        console.log("fetching lyrics from server...");
                        fetchLyricsFromServer(songTitle);
                    }
            } catch (error) {
                console.log("Lyrics are already available")
            }
            
        }
    }
},2000)

async function fetchLyricsFromServer(songTitle) {
    try {
        //const response = await fetch(`http://127.0.0.1:5000/get_lyrics?song=${encodeURIComponent(songTitle)}`);
        //const data = await response.json();
        const data = {
                "lyrics": "The club isn't the best place to find a lover<br>So the bar is where I go (mmmm)<br>Me and my friends at the table doing shots<br>Drinking fast and then we talk slow (mmmm)<br>And you come over and start up a conversation with just me<br>And trust me I'll give it a chance now (mmmm)<br>Take my hand, stop, put Van The Man on the jukebox<br>And then we start to dance<br>And now I'm singing like<br>Girl, you know I want your love<br>Your love was handmade for somebody like me<br>Come on now, follow my lead<br>I may be crazy, don't mind me<br>Say, boy, let's not talk too much<br>Grab on my waist and put that body on me<br>Come on now, follow my lead<br>Come, come on now, follow my lead (mmmm)<br>I'm in love with the shape of you<br>We push and pull like a magnet do<br>Although my heart is falling too<br>I'm in love with your body<br>Last night you were in my room<br>And now my bedsheets smell like you<br>Every day discovering something brand new<br>I'm in love with your body<br>Oh I oh I oh I oh I<br>I'm in love with your body<br>Oh I oh I oh I oh I<br>I'm in love with your body<br>Oh I oh I oh I oh I<br>I'm in love with your body<br>Every day discovering something brand new<br>I'm in love with the shape of you<br>One week in we let the story begin<br>We're going out on our first date (mmmm)<br>You and me are thrifty, so go all you can eat<br>Fill up your bag and I fill up a plate (mmmm)<br>We talk for hours and hours about the sweet and the sour<br>And how your family is doing okay (mmmm)<br>And leave and get in a taxi, then kiss in the backseat<br>Tell the driver make the radio play<br>And I'm singing like<br>Girl, you know I want your love<br>Your love was handmade for somebody like me<br>Come on now, follow my lead<br>I may be crazy, don't mind me<br>Say, boy, let's not talk too much<br>Grab on my waist and put that body on me<br>Come on now, follow my lead<br>Come, come on now, follow my lead (mmmm)<br>I'm in love with the shape of you<br>We push and pull like a magnet do<br>Although my heart is falling too<br>I'm in love with your body<br>Last night you were in my room<br>And now my bedsheets smell like you<br>Every day discovering something brand new<br>I'm in love with your body<br>Oh I oh I oh I oh I<br>I'm in love with your body<br>Oh I oh I oh I oh I<br>I'm in love with your body<br>Oh I oh I oh I oh I<br>I'm in love with your body<br>Every day discovering something brand new<br>I'm in love with the shape of you<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>I'm in love with the shape of you<br>We push and pull like a magnet do<br>Although my heart is falling too<br>I'm in love with your body<br>Last night you were in my room<br>And now my bedsheets smell like you<br>Every day discovering something brand new<br>I'm in love with your body<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>I'm in love with your body<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>I'm in love with your body<br>Come on, be my baby, come on<br>Come on, be my baby, come on<br>I'm in love with your body<br>Every day discovering something brand new<br>I'm in love with the shape of you",
                "song": "1. \"Shape Of You\" - Ed Sheeran"
            }

        if (data.lyrics) {
            console.log("Lyrics received from Flask:", data.lyrics);

            // Inject lyrics into the container
            let lyricsContainer = document.querySelector('.e7eFLioNSG5PAi1qVFT4');
            if (lyricsContainer) {
                lyricsContainer.innerHTML = data.lyrics;
                lyricsContainer.classList.add("container-style");
                const credits = document.createElement('div');
                credits.classList.add('credits');
                credits.innerText = "Lyrics provided by DispLyrics";
                lyricsContainer.insertAdjacentElement('afterend',credits);
            }
        } else {
            console.log("Lyrics not found:", data.error || "Unknown error");
        }
    } catch (error) {
        console.error("Error fetching lyrics:", error);
    }
}
