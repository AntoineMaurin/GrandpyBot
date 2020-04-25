let form = document.querySelector("#user_text_form");

function postFormData(url, data) {
  return fetch(url, {
      method: "POST",
      body: data
  })
  .then(reponse => reponse.json())
  .catch(error => console.log(error));
}

form.addEventListener("submit", function (event){
  event.preventDefault();
  console.log("Formulaire envoyé !");

  //Envoyer contenu formulaire au serveur
  postFormData("/ajax", new FormData(form))
  .then(response => {
    console.log(response);
  })

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
//   var node = document.createElement("p");
//   node.innerHTML = "Water";
//   document.getElementById("masection").appendChild(node);
// }
// </script>
