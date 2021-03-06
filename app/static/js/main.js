let form = document.querySelector("#user_text_form");

function postFormData(url, data) {
  return fetch(url, {
      method: "POST",
      body: data
  })
  .then(reponse => reponse.json())
  .catch(error => console.log(error));
}

function createMap(placement, lat, lng) {
  coordinates = {lat: lat, lng: lng}

  var map = new google.maps.Map(placement, {
    center: coordinates,
    zoom: 15
  });
  var marker = new google.maps.Marker({position: coordinates, map: map});
}

function printMessages(user_msg, grandpy_msg){
  document.getElementById("user_text").value="";
  document.getElementById("text-zone").appendChild(user_msg);
  document.getElementById("text-zone").appendChild(grandpy_msg);
}

function printInfos(data) {
  var grandpy_msg = document.createElement("p");

  var user_msg = document.createElement("p");
  user_msg.classList.add("user-msg");

  var map_msg = document.createElement("div");
  map_msg.setAttribute("id", "chat");

  if ('special_text' in data) {
    user_msg.innerText = data['user_text'];
    grandpy_msg.innerHTML = data['special_text'];
    printMessages(user_msg, grandpy_msg);
  }
   else if ('url' in data) {
     var url_elt = document.createElement("a");
     url_elt.setAttribute("href", data['url']);
     url_elt.innerHTML = "  En savoir plus sur wikipédia";
     user_msg.innerText = data['user_text'];
     grandpy_msg.innerHTML = data['grandpy_msg']
     grandpy_msg.appendChild(url_elt);
     createMap(map_msg, data['lat'], data['lng']);
     printMessages(user_msg, grandpy_msg);
     document.getElementById("text-zone").appendChild(map_msg);
   }
   else {
     user_msg.innerText = data['user_text'];
     grandpy_msg.innerHTML = data['grandpy_msg'];
     createMap(map_msg, data['lat'], data['lng']);
     printMessages(user_msg, grandpy_msg);
     document.getElementById("text-zone").appendChild(map_msg);
  }
  document.getElementById('loading_circle').style.display = 'none';
}

form.addEventListener("submit", function (event){
  document.getElementById('loading_circle').style.display = 'inline-block';
  event.preventDefault();

  postFormData("/answer", new FormData(form))
  .then(response => {
    printInfos(response);
  })
  .catch(error => console.log(error));

});
