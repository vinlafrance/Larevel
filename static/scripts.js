function nonConnecte()
{
    alert("Veuillez vous connecter afin d'avoir accès à cette fonctionnalité.");
}

function validerConnexion() 
{
    let usernameRegex = /^[a-zA-Z0-9][a-zA-Z]+[0-9]*$/;
    let passwordRegex = /^[A-Za-z0-9]+(0-9)*$/
    let username = document.forms["formConnexion"]["username"].value.match(usernameRegex);
    let password = document.forms["formConnexion"]["password"].value.match(passwordRegex);
    if (username == null) 
    {
        alert("Format du username invalide.");
        return false;
    }
    if (password == null) 
    {
        alert("Format du mot de passe invalide.");
        return false;
    }
}

function validerInscription()
{
    let usernameRegex = /^[a-zA-Z0-9][a-zA-Z]+[0-9]*$/;
    let passwordRegex = /^[A-Za-z0-9]+(0-9)*$/;
    let nameRegex = /^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u;
    let courrielRegex = /[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+/;
    let username = document.forms["formInscription"]["username"].value.match(usernameRegex);
    let password = document.forms["formInscription"]["password"].value.match(passwordRegex);
    let name = document.forms["formInscription"]["nom"].value.match(nameRegex);
    let courriel = document.forms["formInscription"]["courriel"].value.match(courrielRegex);
    if (username == null) 
    {
        alert("Format du username invalide.");
        return false;
    }
    if (password == null) 
    {
        alert("Format du mot de passe invalide.");
        return false;
    }
    if (name == null) 
    {
        alert("Format du nom invalide.");
        return false;
    }
    if (courriel == null) 
    {
        alert("Format du courriel invalide.");
        return false;
    }
}

function validerConnexionGerant()
{
    let usernameRegex = /^[a-zA-Z0-9][a-zA-Z]+[0-9]*$/;
    let passwordRegex = /^[A-Za-z0-9]+(0-9)*$/
    let username = document.forms["formConnexionGerant"]["username"].value.match(usernameRegex);
    let password = document.forms["formConnexionGerant"]["password"].value.match(passwordRegex);
    if (username == null) 
    {
        alert("Format du username invalide.");
        return false;
    }
    if (password == null) 
    {
        alert("Format du mot de passe invalide.");
        return false;
    }
}

function validerCommande()
{
    let titreRegex = /^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u;
    let quantiteRegex = /^[0-9]+$/;
    let prixRegex = /^\d+(.\d{1,2})?$/;
    let titre = document.forms["formCommande"]["titre"].value.match(titreRegex);
    let quantite = document.forms["formCommande"]["quantite"].value.match(quantiteRegex);
    let typeLivre = document.forms["formCommande"]["type"].value;
    let prix = document.forms["formCommande"]["prix"].value.match(prixRegex);
    if (titre == null) 
    {
        alert("Format du titre invalide.");
        return false;
    }
    if (quantite == null) 
    {
        alert("Format de la quantite invalide.");
        return false;
    }
    if (typeLivre != "souple" && type != "rigide") 
    {
        alert("Format du type invalide.");
        return false;
    }
    if (prix == null) 
    {
        alert("Format du prix invalide.");
        return false;
    }
}

function validerRecherche()
{
    let titreRegex = /^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u;
    let titre = document.forms["formRecherche"]["titreRecherche"].value.match(titreRegex);
    let test = document.forms["formRecherche"]["titreRecherche"].value;
    if (test === "")
    {
        return true;
    }
    if (titre == null) 
    {
        alert("Format du titre invalide.");
        return false;
    }
}