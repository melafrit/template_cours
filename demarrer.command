#!/bin/sh
# Lanceur macOS du site du cours — double-cliquez ce fichier dans le Finder.
# Le Finder démarre le script depuis le dossier personnel : on se replace
# d'abord dans le dépôt, sinon le serveur servirait le mauvais répertoire.
cd "$(dirname "$0")" || exit 1

# « python » seul peut encore être un Python 2 sur d'anciens postes : on ne
# retient un interpréteur qu'après avoir vérifié sa version.
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1      && "$c" -c 'import sys; sys.exit(0 if sys.version_info[0] >= 3 else 1)' 2>/dev/null; then
    PY="$c"
    break
  fi
done

if [ -z "$PY" ]; then
  printf "
  Python 3 est introuvable.
"
  printf "  Installez-le depuis https://www.python.org/downloads/ puis relancez.

"
  printf "  Appuyez sur Entrée pour fermer."
  read -r _ 2>/dev/null
  exit 1
fi

"$PY" demarrer.py "$@"
statut=$?

# Sans ce garde-fou, une erreur au démarrage fermerait la fenêtre aussitôt et
# emporterait avec elle le message qui l'explique.
if [ "$statut" -ne 0 ]; then
  printf "
  Le lanceur s'est arrêté sur une erreur (voir ci-dessus).
"
  printf "  Appuyez sur Entrée pour fermer."
  read -r _ 2>/dev/null
fi

exit "$statut"
