let connexion = false;
function estConnecte()
{
    if (!connexion)
    {
        alert("Veuiller vous connectez afin de consulter votre panier.");
    }
    location.href("../HTML/Panier.html");
}

function connexionSucces()
{
    connexion = true;
}