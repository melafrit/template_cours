#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lance le site du cours en local et ouvre la page d'accueil.

    Le serveur sert le dossier site/ : ce que voit le navigateur est
    exactement ce qui sera mis en ligne, ni plus ni moins.

    python3 demarrer.py              # port 8765, ou le premier libre au-dessus
    python3 demarrer.py --port 9000  # port imposé
    python3 demarrer.py --sans-navigateur

Sous macOS, double-cliquez « demarrer.command ». Sous Windows, « demarrer.bat ».

Le serveur envoie « Cache-Control: no-store ». Le serveur de développement de
Python ne le fait pas, et le navigateur ressert alors l'ancien JavaScript après
un git pull : on croit la modification ratée, on cherche un défaut qui n'existe
pas. Ce piège nous a coûté assez de temps pour être fermé ici.

Arrêt : Ctrl+C, ou fermez la fenêtre.
"""

import argparse
import http.server
import os
import re
import socket
import socketserver
import sys
import threading
import webbrowser

# Le site vit dans site/, pas a la racine du depot : celle-ci porte aussi
# les outils, les fiches et la documentation, qui n'ont rien a faire en ligne.
DEPOT = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(DEPOT, "site")
PORT_PAR_DEFAUT = 8765

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


class Handler(http.server.SimpleHTTPRequestHandler):
    """Sert la racine du dépôt, sans cache, et sans journaliser chaque fichier."""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RACINE, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Une ligne par image et par capsule noierait la console : on ne garde
        # que ce qui signale un vrai problème. La position du code varie selon
        # l'appelant : on retient le premier argument qui ressemble à un code
        # HTTP, plutôt qu'un rang fixe.
        for a in args:
            a = str(a)
            if re.fullmatch(r"[45]\d\d", a):
                sys.stdout.write("  %s  %s\n" % (a, self.path))
                sys.stdout.flush()
                return

    def log_error(self, *a, **kw):
        # send_error journalise l'erreur, puis la réponse qu'il envoie la
        # journalise à son tour : chaque 404 s'affichait en double. On ne garde
        # que le second passage, qui connaît le code réellement envoyé.
        pass


def port_libre(depart, essais=20):
    """Premier port réellement disponible à partir de `depart`.

    Sans SO_REUSEADDR, volontairement : sous Windows cette option autorise à se
    lier à un port DÉJÀ pris, là où Unix le refuse. La sonde répondait « libre »
    pour un port occupé, et le serveur se posait par-dessus un autre.
    """
    for p in range(depart, depart + essais):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    return None


def main():
    ap = argparse.ArgumentParser(description="Lance le site du cours en local.")
    ap.add_argument("--port", type=int, default=PORT_PAR_DEFAUT)
    ap.add_argument("--sans-navigateur", action="store_true",
                    help="ne pas ouvrir la page d'accueil automatiquement")
    args = ap.parse_args()

    if not os.path.isfile(os.path.join(RACINE, "index.html")):
        sys.exit("site/index.html est introuvable : ce script doit rester à la racine du dépôt.")

    port = port_libre(args.port)
    if port is None:
        sys.exit("Aucun port libre entre %d et %d." % (args.port, args.port + 19))
    if port != args.port:
        print("  Le port %d est occupé — on prend le %d." % (args.port, port))

    url = "http://localhost:%d/index.html" % port
    print("")
    print("  Template de site de cours")
    print("  " + "-" * 42)
    print("  Site servi depuis : %s" % RACINE)
    print("  Adresse           : %s" % url)
    print("  Cache désactivé   : un simple rechargement suffit après un git pull")
    print("")
    print("  Ctrl+C pour arrêter.")
    print("")

    # Même raison : réutiliser l'adresse aide sous Unix à relancer aussitôt après
    # un arrêt (état TIME_WAIT), mais sous Windows cela laisserait deux serveurs
    # se partager le même port sans que rien ne le signale.
    socketserver.TCPServer.allow_reuse_address = (os.name != "nt")

    # ThreadingHTTPServer, et non le serveur simple : celui-ci traite UNE
    # requete a la fois, et un navigateur qui garde sa connexion ouverte
    # (keep-alive) bloque alors tout autre client — un second onglet, un
    # curl de verification. Le symptome est un simple gel, difficile a
    # rattacher a sa cause.
    class Serveur(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    with Serveur(("127.0.0.1", port), Handler) as httpd:
        if not args.sans_navigateur:
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Serveur arrêté.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
