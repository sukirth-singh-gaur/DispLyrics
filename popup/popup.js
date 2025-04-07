const content = document.querySelector(".content");

setInterval(()=>{
  chrome.storage.local.get("status", (result) => {
    const state = result.status || {};
    console.log("Retrieved state in popup:", state);
    if(state["lyrics-available"]){
      content.innerHTML = "The Lyrics of this song are already available";
    }
    else{
      if(state["lyrics-fetched"]){
        content.innerHTML = "The Lyrics are fetched by DispLyrics.";
        if(state["lyrics-displayed"]){
          content.innerHTML = "The Lyrics displayed enjoy your session.";
        }
        else{
          content.innerHTML = "Open the Lyrics tab to view the lyrics.";
        }
      }
      else{
        content.innerHTML = "The Lyrics are being fetched please wait.";
      }
    }
  });
},1000)