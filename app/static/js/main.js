let form = document.querySelector("#user_text_form");

function postFormData(url, data) {
  return fetch(url, {
      method: "POST",
      body: data
  })
  .then(reponse => reponse.json())
  .catch(error => console.log(error));
}

function printInfos(data) {
  var grandpy_msg = document.createElement("p");
  var user_msg = document.createElement("p");
  user_msg.classList.add("user-msg");
  if ('error_msg' in data) {
    grandpy_msg.innerHTML = data['error_msg'];
    user_msg.innerHTML = data['user_text'];
  } else {
    user_msg.innerHTML = data['user_text'];
    grandpy_msg.innerHTML = data['wiki_response'];
  }
  document.getElementById("text-section").appendChild(user_msg);
  document.getElementById("text-section").appendChild(grandpy_msg);
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
  .catch(error => printInfos(error));


});

// <div class="madiv">
//   <section id="masection">
//     <p>Coffee</p>
//     <p>Tea</p>
//   </section>
// </div>
//
// <button onclick="myFunction()">Try it</button>
//
// <script>
// function myFunction() {
//   var msg = document.createElement("p");
//   msg.innerHTML = "Water";
//   document.getElementById("masection").appendChild(msg);
// }
// </script>
