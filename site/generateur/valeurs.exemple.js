/* valeurs.exemple.js : le modèle des valeurs habituelles du générateur de prompt.

   Copiez ce fichier en valeurs.local.js, dans ce même dossier, et remplacez les valeurs neutres par les vôtres ; ou
   remplissez « Vos valeurs habituelles » dans la page, puis « Enregistrer mes valeurs habituelles ». valeurs.local.js
   est ignoré par Git et ne se publie jamais. AUCUN SECRET ICI : ni clé, ni mot de passe, ni accès à l'hébergement ;
   ceux-là restent dans les fichiers que les scripts lisent seuls (outils/elevenlabs.json, deploiement/config.json). */
window.VALEURS_HABITUELLES = {
  "auteur": "Prénom NOM",
  "email": "prenom.nom@exemple.fr",
  "github": "compte",
  "hebergement": {
    "url_base": "https://example.org/teaching/",
    "repertoire_base": "/chemin/vers/teaching/"
  },
  "dossier_cours_base": "C:/projets/Cours/",
  "dossier_documents": "Doc_Reference",
  "ecosysteme": {
    "gabarit_technique": "C:/projets/Cours/template_cours",
    "cours_de_reference": [],
    "app_livrables": "",
    "doc_import_app": "",
    "epreuves_reelles": ""
  },
  "filieres": {
    "EADL et ERIS": [
      { "id": "eadl", "code": "EADL", "palette": "emeraude", "rncp": "39765",
        "nom": { "fr": "Expert en Architecture et Développement Logiciel", "en": "Expert in Software Architecture and Development" },
        "court": { "fr": "Architecture et développement logiciel", "en": "Software architecture and development" } },
      { "id": "eris", "code": "ERIS", "palette": "prune", "rncp": "39781",
        "nom": { "fr": "Expert Réseaux, Infrastructures et Sécurité", "en": "Expert in Networks, Infrastructure and Security" },
        "court": { "fr": "Réseaux, infrastructures, sécurité", "en": "Networks, infrastructure, security" } }
    ],
    "CDWFS et ASRC": [
      { "id": "cdwfs", "code": "CDWFS", "palette": "", "rncp": "39608",
        "nom": { "fr": "Concepteur Développeur Web Full Stack" },
        "court": { "fr": "Développeur web full stack" } },
      { "id": "asrc", "code": "ASRC", "palette": "", "rncp": "39611",
        "nom": { "fr": "Administrateur Systèmes, Réseaux et Cybersécurité" },
        "court": { "fr": "Systèmes, réseaux, cybersécurité" } }
    ]
  },
  "habitudes": {
    "palette": "marine",
    "langues": ["fr"],
    "horaires": { "matin": "09:00-12:30", "apres_midi": "13:30-17:00" },
    "ton": "vouvoiement chaleureux, registre d'un collègue expérimenté ; peu d'écrit, beaucoup de pratique",
    "modules": {}
  }
};
