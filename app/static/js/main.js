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
