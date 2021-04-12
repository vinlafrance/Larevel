function nonConnecte()
{
    alert("Veuillez vous connecter afin d'avoir accès à cette fonctionnalité.");
}

function validerConnexion() 
{
    let usernameRegex = /^[a-zA-Z0-9][a-zA-Z]+[0-9]*$/;
    let passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/
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
    let passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/;
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
    let passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$/
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