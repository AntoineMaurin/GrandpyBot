let form = document.querySelector("#user_text_form");

function postFormData(url, data) {
  return fetch(url, {
      method: "POST",
      body: data
  })
  .then(reponse => reponse.json())
  .catch(error => console.log(error));
}

function initMap(placement, lat, lng) {
  coordinates = {lat: lat, lng: lng}

  var map = new google.maps.Map(placement, {
    center: coordinates,
    zoom: 15
  });
  var marker = new google.maps.Marker({position: coordinates, map: map});
}

function printInfos(data) {
  var grandpy_msg = document.createElement("p");
  var user_msg = document.createElement("p");
  user_msg.classList.add("user-msg");
  var map_msg = document.createElement("div");
  map_msg.setAttribute("id", "chat");
  if ('error_msg' in data) {
    user_msg.innerHTML = data['user_text'];
    grandpy_msg.innerHTML = data['error_msg'];
    document.getElementById("text-zone").appendChild(user_msg);
    document.getElementById("text-zone").appendChild(grandpy_msg);
  } else {
    user_msg.innerHTML = data['user_text'];
    grandpy_msg.innerHTML = data['wiki_response'];
    initMap(map_msg, data['lat'], data['lng']);
    document.getElementById("text-zone").appendChild(user_msg);
    document.getElementById("text-zone").appendChild(grandpy_msg);
    document.getElementById("text-zone").appendChild(map_msg);
  }
}

form.addEventListener("submit", function (event){
  event.preventDefault();
  console.log("Formulaire envoyé !");

  //Envoyer contenu formulaire au serveur
  postFormData("/ajax", new FormData(form))
  .then(response => {
    printInfos(response)
    console.log(response['wiki_response'], response['lat'], response['lng']);
  })
  .catch(error => console.log(error));

});
