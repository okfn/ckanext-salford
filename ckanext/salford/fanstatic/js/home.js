
// twitter
twitterFetcher.fetch({
  "id": '554608153607032832',
  "domId": 'tweets',
  "maxTweets": 5,
  "enableLinks": true,
  "customCallback":handleTweets,
});


function handleTweets(tweets){
  var i=0;
  var j=tweets.length;
  var l="<ul class='carousel-inner'>";
  while(i<j){
    l+="<li class='item' id='tweet"+i+"'>"+tweets[i]+"</li>";
    i++;
  }
  l+="</ul>";
  document.getElementById("tweets").innerHTML=l;
  var n=(j-1);
  
  $( "#tweet0" ).addClass( "active" );
  
  $('.carousel').carousel({
    interval: 10000
  })
} 

