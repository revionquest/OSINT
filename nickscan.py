









from __future__ import annotations
import sys
import subprocess
import importlib.metadata
import threading
import queue
import copy
import heapq
import shutil
import tempfile
import zipfile
import io
import platform
import urllib.request
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor

DEPENDENCIES = {"undetected-chromedriver": "3.5.5", "selenium": "4.49.0",
                "beautifulsoup4": "4.15.0", "setuptools": "80.10.2"}

def dependencies_ok():
    try:
        return all(importlib.metadata.version(name) == version
                   for name, version in DEPENDENCIES.items())
    except importlib.metadata.PackageNotFoundError:
        return False

if __name__ == "__main__" and sys.argv[1:] == ["--check-deps"]:
    raise SystemExit(0 if dependencies_ok() else 1)
if __name__ == "__main__" and sys.argv[1:] == ["--install"]:
    raise SystemExit(subprocess.call([sys.executable, "-m", "pip", "install",
                                     *[f"{k}=={v}" for k, v in DEPENDENCIES.items()]]))


import json
BUNDLED_SITES = json.loads('{"$schema": "data.schema.json", "1337x": {"errorMsg": ["<title>Error something went wrong.</title>", "<head><title>404 Not Found</title></head>"], "errorType": "message", "regexCheck": "^[A-Za-z0-9]{4,12}$", "url": "https://www.1337x.to/user/{}/", "urlMain": "https://www.1337x.to/", "username_claimed": "FitGirl"}, "2Dimensions": {"errorType": "status_code", "url": "https://2Dimensions.com/a/{}", "urlMain": "https://2Dimensions.com/", "username_claimed": "blue"}, "7Cups": {"errorType": "status_code", "url": "https://www.7cups.com/@{}", "urlMain": "https://www.7cups.com/", "username_claimed": "blue"}, "9GAG": {"errorType": "status_code", "url": "https://www.9gag.com/u/{}", "urlMain": "https://www.9gag.com/", "username_claimed": "blue"}, "APClips": {"errorMsg": "Amateur Porn Content Creators", "errorType": "message", "isNSFW": true, "url": "https://apclips.com/{}", "urlMain": "https://apclips.com/", "username_claimed": "onlybbyraq"}, "About.me": {"errorType": "status_code", "url": "https://about.me/{}", "urlMain": "https://about.me/", "username_claimed": "blue"}, "Academia.edu": {"errorType": "status_code", "regexCheck": "^[^.]*$", "url": "https://independent.academia.edu/{}", "urlMain": "https://www.academia.edu/", "username_claimed": "blue"}, "AdmireMe.Vip": {"errorMsg": "Page Not Found", "errorType": "message", "isNSFW": true, "url": "https://admireme.vip/{}", "urlMain": "https://admireme.vip/", "username_claimed": "DemiDevil"}, "Airbit": {"errorType": "status_code", "url": "https://airbit.com/{}", "urlMain": "https://airbit.com/", "username_claimed": "airbit"}, "Airliners": {"errorType": "status_code", "url": "https://www.airliners.net/user/{}/profile/photos", "urlMain": "https://www.airliners.net/", "username_claimed": "yushinlin"}, "All Things Worn": {"errorMsg": "Sell Used Panties", "errorType": "message", "isNSFW": true, "url": "https://www.allthingsworn.com/profile/{}", "urlMain": "https://www.allthingsworn.com", "username_claimed": "pink"}, "AllMyLinks": {"errorMsg": "Page not found", "errorType": "message", "regexCheck": "^[a-z0-9][a-z0-9-]{2,32}$", "url": "https://allmylinks.com/{}", "urlMain": "https://allmylinks.com/", "username_claimed": "blue"}, "AniWorld": {"errorMsg": "Dieses Profil ist nicht verf\\u00fcgbar", "errorType": "message", "url": "https://aniworld.to/user/profil/{}", "urlMain": "https://aniworld.to/", "username_claimed": "blue"}, "Anilist": {"errorType": "status_code", "regexCheck": "^[A-Za-z0-9]{2,20}$", "request_method": "POST", "request_payload": {"query": "query($name:String){User(name:$name){id}}", "variables": {"name": "{}"}}, "url": "https://anilist.co/user/{}/", "urlMain": "https://anilist.co/", "urlProbe": "https://graphql.anilist.co/", "username_claimed": "Josh"}, "Apple Developer": {"errorType": "status_code", "url": "https://developer.apple.com/forums/profile/{}", "urlMain": "https://developer.apple.com", "username_claimed": "lio24d"}, "Apple Discussions": {"errorMsg": "Looking for something in Apple Support Communities?", "errorType": "message", "url": "https://discussions.apple.com/profile/{}", "urlMain": "https://discussions.apple.com", "username_claimed": "jason"}, "Aparat": {"errorType": "status_code", "request_method": "GET", "url": "https://www.aparat.com/{}/", "urlMain": "https://www.aparat.com/", "urlProbe": "https://www.aparat.com/api/fa/v1/user/user/information/username/{}", "username_claimed": "jadi"}, "Archive of Our Own": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://archiveofourown.org/users/{}", "urlMain": "https://archiveofourown.org/", "username_claimed": "test"}, "Archive.org": {"__comment__": "\'The resource could not be found\' relates to archive downtime", "errorMsg": ["could not fetch an account with user item identifier", "The resource could not be found", "Internet Archive services are temporarily offline"], "errorType": "message", "url": "https://archive.org/details/@{}", "urlMain": "https://archive.org", "urlProbe": "https://archive.org/details/@{}?noscript=true", "username_claimed": "blue"}, "Arduino Forum": {"errorType": "status_code", "url": "https://forum.arduino.cc/u/{}/summary", "urlMain": "https://forum.arduino.cc/", "username_claimed": "system"}, "ArtStation": {"errorType": "status_code", "url": "https://www.artstation.com/{}", "urlMain": "https://www.artstation.com/", "urlProbe": "https://www.artstation.com/users/{}.json", "username_claimed": "Blue"}, "Asciinema": {"errorType": "status_code", "url": "https://asciinema.org/~{}", "urlMain": "https://asciinema.org", "username_claimed": "red"}, "Ask Fedora": {"errorType": "status_code", "url": "https://ask.fedoraproject.org/u/{}", "urlMain": "https://ask.fedoraproject.org/", "username_claimed": "red"}, "Atcoder": {"errorType": "status_code", "url": "https://atcoder.jp/users/{}", "urlMain": "https://atcoder.jp/", "username_claimed": "ksun48"}, "Vjudge": {"errorType": "status_code", "url": "https://VJudge.net/user/{}", "urlMain": "https://VJudge.net/", "username_claimed": "tokitsukaze"}, "Audiojungle": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9_]+$", "url": "https://audiojungle.net/user/{}", "urlMain": "https://audiojungle.net/", "username_claimed": "blue"}, "Autofrage": {"errorType": "status_code", "url": "https://www.autofrage.net/nutzer/{}", "urlMain": "https://www.autofrage.net/", "username_claimed": "autofrage"}, "Avizo": {"errorType": "response_url", "errorUrl": "https://www.avizo.cz/", "url": "https://www.avizo.cz/{}/", "urlMain": "https://www.avizo.cz/", "username_claimed": "blue"}, "AWS Skills Profile": {"errorType": "message", "errorMsg": "shareProfileAccepted\\":false", "url": "https://skillsprofile.skillbuilder.aws/user/{}/", "urlMain": "https://skillsprofile.skillbuilder.aws", "username_claimed": "mayank04pant"}, "BOOTH": {"errorType": "response_url", "errorUrl": "https://booth.pm/", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.booth.pm/", "urlMain": "https://booth.pm/", "username_claimed": "blue"}, "Bandcamp": {"errorType": "status_code", "url": "https://www.bandcamp.com/{}", "urlMain": "https://www.bandcamp.com/", "username_claimed": "blue"}, "Bazar.cz": {"errorType": "response_url", "errorUrl": "https://www.bazar.cz/error404.aspx", "url": "https://www.bazar.cz/{}/", "urlMain": "https://www.bazar.cz/", "username_claimed": "pianina"}, "Behance": {"errorType": "status_code", "url": "https://www.behance.net/{}", "urlMain": "https://www.behance.net/", "username_claimed": "blue"}, "Bezuzyteczna": {"errorType": "status_code", "url": "https://bezuzyteczna.pl/uzytkownicy/{}", "urlMain": "https://bezuzyteczna.pl", "username_claimed": "Jackson"}, "BiggerPockets": {"errorType": "status_code", "url": "https://www.biggerpockets.com/users/{}", "urlMain": "https://www.biggerpockets.com/", "username_claimed": "blue"}, "BioHacking": {"errorType": "status_code", "url": "https://forum.dangerousthings.com/u/{}", "urlMain": "https://forum.dangerousthings.com/", "username_claimed": "blue"}, "BitBucket": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9-_]{1,30}$", "url": "https://bitbucket.org/{}/", "urlMain": "https://bitbucket.org/", "username_claimed": "white"}, "Bitwarden Forum": {"errorType": "status_code", "regexCheck": "^(?![.-])[a-zA-Z0-9_.-]{3,20}$", "url": "https://community.bitwarden.com/u/{}/summary", "urlMain": "https://bitwarden.com/", "username_claimed": "blue"}, "Blipfoto": {"errorType": "status_code", "url": "https://www.blipfoto.com/{}", "urlMain": "https://www.blipfoto.com/", "username_claimed": "blue"}, "Blitz Tactics": {"errorMsg": "That page doesn\'t exist", "errorType": "message", "url": "https://blitztactics.com/{}", "urlMain": "https://blitztactics.com/", "username_claimed": "Lance5500"}, "Blogger": {"errorType": "status_code", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://{}.blogspot.com", "urlMain": "https://www.blogger.com/", "username_claimed": "blue"}, "Bluesky": {"errorType": "status_code", "url": "https://bsky.app/profile/{}.bsky.social", "urlProbe": "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={}.bsky.social", "urlMain": "https://bsky.app/", "username_claimed": "mcuban"}, "BongaCams": {"errorType": "status_code", "isNSFW": true, "url": "https://pt.bongacams.com/profile/{}", "urlMain": "https://pt.bongacams.com", "username_claimed": "asuna-black"}, "Bookcrossing": {"errorType": "status_code", "url": "https://www.bookcrossing.com/mybookshelf/{}/", "urlMain": "https://www.bookcrossing.com/", "username_claimed": "blue"}, "BoardGameGeek": {"errorMsg": "\\"isValid\\":true", "errorType": "message", "url": "https://boardgamegeek.com/user/{}", "urlMain": "https://boardgamegeek.com/", "urlProbe": "https://api.geekdo.com/api/accounts/validate/username?username={}", "username_claimed": "blue"}, "BraveCommunity": {"errorType": "status_code", "url": "https://community.brave.com/u/{}/", "urlMain": "https://community.brave.com/", "username_claimed": "blue"}, "BreachSta.rs Forum": {"errorMsg": "<title>Error - BreachStars</title>", "errorType": "message", "url": "https://breachsta.rs/profile/{}", "urlMain": "https://breachsta.rs/", "username_claimed": "Sleepybubble"}, "BugCrowd": {"errorType": "status_code", "url": "https://bugcrowd.com/{}", "urlMain": "https://bugcrowd.com/", "username_claimed": "ppfeister"}, "BuyMeACoffee": {"errorType": "status_code", "regexCheck": "[a-zA-Z0-9]{3,15}", "url": "https://buymeacoff.ee/{}", "urlMain": "https://www.buymeacoffee.com/", "urlProbe": "https://www.buymeacoffee.com/{}", "username_claimed": "red"}, "BuzzFeed": {"errorType": "status_code", "url": "https://buzzfeed.com/{}", "urlMain": "https://buzzfeed.com/", "username_claimed": "blue"}, "Cfx.re Forum": {"errorType": "status_code", "url": "https://forum.cfx.re/u/{}/summary", "urlMain": "https://forum.cfx.re", "username_claimed": "hightowerlssd"}, "CGTrader": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://www.cgtrader.com/{}", "urlMain": "https://www.cgtrader.com", "username_claimed": "blue"}, "CNET": {"errorType": "status_code", "regexCheck": "^[a-z].*$", "url": "https://www.cnet.com/profiles/{}/", "urlMain": "https://www.cnet.com/", "username_claimed": "melliott"}, "CSSBattle": {"errorType": "status_code", "url": "https://cssbattle.dev/player/{}", "urlMain": "https://cssbattle.dev", "username_claimed": "beo"}, "CTAN": {"errorType": "status_code", "url": "https://ctan.org/author/{}", "urlMain": "https://ctan.org/", "username_claimed": "briggs"}, "Caddy Community": {"errorType": "status_code", "url": "https://caddy.community/u/{}/summary", "urlMain": "https://caddy.community/", "username_claimed": "taako_magnusen"}, "Car Talk Community": {"errorType": "status_code", "url": "https://community.cartalk.com/u/{}/summary", "urlMain": "https://community.cartalk.com/", "username_claimed": "always_fixing"}, "Carbonmade": {"errorType": "response_url", "errorUrl": "https://carbonmade.com/fourohfour?domain={}.carbonmade.com", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.carbonmade.com", "urlMain": "https://carbonmade.com/", "username_claimed": "jenny"}, "Carrd": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9_-]{3,50}$", "url": "https://{}.carrd.co/", "urlMain": "https://carrd.co/", "username_claimed": "blue"}, "Career.habr": {"errorMsg": "<h1>\\u041e\\u0448\\u0438\\u0431\\u043a\\u0430 404</h1>", "errorType": "message", "url": "https://career.habr.com/{}", "urlMain": "https://career.habr.com/", "username_claimed": "blue"}, "CashApp": {"errorType": "status_code", "url": "https://cash.app/${}", "urlMain": "https://cash.app", "username_claimed": "hotdiggitydog"}, "Championat": {"errorType": "status_code", "url": "https://www.championat.com/user/{}", "urlMain": "https://www.championat.com/", "username_claimed": "blue"}, "Chaos": {"errorType": "status_code", "url": "https://chaos.social/@{}", "urlMain": "https://chaos.social/", "username_claimed": "ordnung"}, "Chatujme.cz": {"errorMsg": "Neexistujic\\u00ed profil", "errorType": "message", "regexCheck": "^[a-zA-Z][a-zA-Z1-9_-]*$", "url": "https://profil.chatujme.cz/{}", "urlMain": "https://chatujme.cz/", "username_claimed": "david"}, "ChaturBate": {"errorType": "status_code", "isNSFW": true, "url": "https://chaturbate.com/{}", "urlMain": "https://chaturbate.com", "username_claimed": "cute18cute"}, "Chess": {"errorMsg": "Username is valid", "errorType": "message", "regexCheck": "^[a-zA-Z0-9_]{3,25}$", "url": "https://www.chess.com/member/{}", "urlMain": "https://www.chess.com/", "urlProbe": "https://www.chess.com/callback/user/valid?username={}", "username_claimed": "blue"}, "Choice Community": {"errorType": "status_code", "url": "https://choice.community/u/{}/summary", "urlMain": "https://choice.community/", "username_claimed": "gordon"}, "Clapper": {"errorType": "status_code", "url": "https://clapperapp.com/{}", "urlMain": "https://clapperapp.com/", "username_claimed": "blue"}, "CloudflareCommunity": {"errorType": "status_code", "url": "https://community.cloudflare.com/u/{}", "urlMain": "https://community.cloudflare.com/", "username_claimed": "blue"}, "Clozemaster": {"errorMsg": "Oh no! Player not found.", "errorType": "message", "url": "https://www.clozemaster.com/players/{}", "urlMain": "https://www.clozemaster.com", "username_claimed": "green"}, "Clubhouse": {"errorType": "status_code", "url": "https://www.clubhouse.com/@{}", "urlMain": "https://www.clubhouse.com", "username_claimed": "waniathar"}, "Code Snippet Wiki": {"errorMsg": "This user has not filled out their profile page yet", "errorType": "message", "url": "https://codesnippets.fandom.com/wiki/User:{}", "urlMain": "https://codesnippets.fandom.com", "username_claimed": "bob"}, "Codeberg": {"errorType": "status_code", "url": "https://codeberg.org/{}", "urlMain": "https://codeberg.org/", "username_claimed": "blue"}, "Codecademy": {"errorMsg": "This profile could not be found", "errorType": "message", "url": "https://www.codecademy.com/profiles/{}", "urlMain": "https://www.codecademy.com/", "username_claimed": "blue"}, "Codechef": {"errorType": "response_url", "errorUrl": "https://www.codechef.com/", "url": "https://www.codechef.com/users/{}", "urlMain": "https://www.codechef.com/", "username_claimed": "blue"}, "Codeforces": {"errorType": "status_code", "url": "https://codeforces.com/profile/{}", "urlMain": "https://codeforces.com/", "urlProbe": "https://codeforces.com/api/user.info?handles={}", "username_claimed": "tourist"}, "Codepen": {"errorType": "status_code", "url": "https://codepen.io/{}", "urlMain": "https://codepen.io/", "username_claimed": "blue"}, "Coders Rank": {"errorMsg": "not a registered member", "errorType": "message", "regexCheck": "^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$", "url": "https://profile.codersrank.io/user/{}/", "urlMain": "https://codersrank.io/", "username_claimed": "rootkit7628"}, "Coderwall": {"errorType": "status_code", "url": "https://coderwall.com/{}", "urlMain": "https://coderwall.com", "username_claimed": "hacker"}, "CodeSandbox": {"errorType": "message", "errorMsg": "Could not find user with username", "regexCheck": "^[a-zA-Z0-9_-]{3,30}$", "url": "https://codesandbox.io/u/{}", "urlProbe": "https://codesandbox.io/api/v1/users/{}", "urlMain": "https://codesandbox.io", "username_claimed": "icyjoseph"}, "Codewars": {"errorType": "status_code", "url": "https://www.codewars.com/users/{}", "urlMain": "https://www.codewars.com", "username_claimed": "example"}, "Codolio": {"errorType": "message", "errorMsg": "<title>Page Not Found | Codolio</title>", "url": "https://codolio.com/profile/{}", "urlMain": "https://codolio.com/", "username_claimed": "testuser", "regexCheck": "^[a-zA-Z0-9_-]{3,30}$"}, "Coinvote": {"errorType": "status_code", "url": "https://coinvote.cc/profile/{}", "urlMain": "https://coinvote.cc/", "username_claimed": "blue"}, "ColourLovers": {"errorType": "status_code", "url": "https://www.colourlovers.com/lover/{}", "urlMain": "https://www.colourlovers.com/", "username_claimed": "blue"}, "Contently": {"errorType": "response_url", "errorUrl": "https://contently.com", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://{}.contently.com/", "urlMain": "https://contently.com/", "username_claimed": "jordanteicher"}, "Coroflot": {"errorType": "status_code", "url": "https://www.coroflot.com/{}", "urlMain": "https://coroflot.com/", "username_claimed": "blue"}, "Cplusplus": {"errorType": "message", "errorMsg": "<title>404 Page Not Found</title>", "url": "https://cplusplus.com/user/{}", "urlMain": "https://cplusplus.com", "username_claimed": "mbozzi"}, "Cracked": {"errorType": "response_url", "errorUrl": "https://www.cracked.com/", "url": "https://www.cracked.com/members/{}/", "urlMain": "https://www.cracked.com/", "username_claimed": "blue"}, "Cracked Forum": {"errorType": "status_code", "url": "https://cracked.ax/{}", "urlMain": "https://cracked.ax/", "username_claimed": "Blue"}, "Credly": {"errorType": "status_code", "url": "https://www.credly.com/users/{}", "urlMain": "https://www.credly.com/", "username_claimed": "credly"}, "Crevado": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.crevado.com", "urlMain": "https://crevado.com/", "username_claimed": "blue"}, "Crowdin": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9._-]{2,255}$", "url": "https://crowdin.com/profile/{}", "urlMain": "https://crowdin.com/", "username_claimed": "blue"}, "CryptoHack": {"errorType": "response_url", "errorUrl": "https://cryptohack.org/", "url": "https://cryptohack.org/user/{}/", "urlMain": "https://cryptohack.org/", "username_claimed": "blue"}, "Cryptomator Forum": {"errorType": "status_code", "url": "https://community.cryptomator.org/u/{}", "urlMain": "https://community.cryptomator.org/", "username_claimed": "michael"}, "Cults3D": {"errorMsg": "Oh dear, this page is not working!", "errorType": "message", "url": "https://cults3d.com/en/users/{}/creations", "urlMain": "https://cults3d.com/en", "username_claimed": "brown"}, "CyberDefenders": {"errorType": "status_code", "regexCheck": "^[^\\\\/:*?\\"<>|@]{3,50}$", "request_method": "GET", "url": "https://cyberdefenders.org/p/{}", "urlMain": "https://cyberdefenders.org/", "username_claimed": "mlohn"}, "DEV Community": {"errorType": "status_code", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://dev.to/{}", "urlMain": "https://dev.to/", "username_claimed": "blue"}, "DMOJ": {"errorMsg": "No such user", "errorType": "message", "url": "https://dmoj.ca/user/{}", "urlMain": "https://dmoj.ca/", "username_claimed": "junferno"}, "DailyMotion": {"errorType": "status_code", "url": "https://www.dailymotion.com/{}", "urlMain": "https://www.dailymotion.com/", "username_claimed": "blue"}, "dcinside": {"errorType": "status_code", "url": "https://gallog.dcinside.com/{}", "urlMain": "https://www.dcinside.com/", "username_claimed": "anrbrb"}, "Dealabs": {"errorMsg": "La page que vous essayez", "errorType": "message", "regexCheck": "[a-z0-9]{4,16}", "url": "https://www.dealabs.com/profile/{}", "urlMain": "https://www.dealabs.com/", "username_claimed": "blue"}, "DeviantArt": {"errorType": "message", "errorMsg": "Llama Not Found", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://www.deviantart.com/{}", "urlMain": "https://www.deviantart.com/", "username_claimed": "blue"}, "DigitalSpy": {"errorMsg": "The page you were looking for could not be found.", "errorType": "message", "url": "https://forums.digitalspy.com/profile/{}", "urlMain": "https://forums.digitalspy.com/", "username_claimed": "blue", "regexCheck": "^\\\\w{3,20}$"}, "Discogs": {"errorType": "status_code", "url": "https://www.discogs.com/user/{}", "urlMain": "https://www.discogs.com/", "username_claimed": "blue"}, "Discord": {"errorType": "message", "url": "https://discord.com", "urlMain": "https://discord.com/", "urlProbe": "https://discord.com/api/v9/unique-username/username-attempt-unauthed", "errorMsg": ["{\\"taken\\":false}", "The resource is being rate limited"], "request_method": "POST", "request_payload": {"username": "{}"}, "headers": {"Content-Type": "application/json"}, "username_claimed": "blue"}, "Discord.bio": {"errorType": "message", "errorMsg": "<title>Server Error (500)</title>", "url": "https://discords.com/api-v2/bio/details/{}", "urlMain": "https://discord.bio/", "username_claimed": "robert"}, "Discuss.Elastic.co": {"errorType": "status_code", "url": "https://discuss.elastic.co/u/{}", "urlMain": "https://discuss.elastic.co/", "username_claimed": "blue"}, "Diskusjon.no": {"errorMsg": "{\\"result\\":\\"ok\\"}", "errorType": "message", "regexCheck": "^[a-zA-Z0-9_.-]{3,40}$", "urlProbe": "https://www.diskusjon.no/?app=core&module=system&controller=ajax&do=usernameExists&input={}", "url": "https://www.diskusjon.no", "urlMain": "https://www.diskusjon.no", "username_claimed": "blue"}, "Disqus": {"errorType": "status_code", "url": "https://disqus.com/{}", "urlMain": "https://disqus.com/", "username_claimed": "blue"}, "Docker Hub": {"errorType": "status_code", "url": "https://hub.docker.com/u/{}/", "urlMain": "https://hub.docker.com/", "urlProbe": "https://hub.docker.com/v2/users/{}/", "username_claimed": "blue"}, "Dribbble": {"errorMsg": "Whoops, that page is gone.", "errorType": "message", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://dribbble.com/{}", "urlMain": "https://dribbble.com/", "username_claimed": "blue"}, "Duolingo": {"errorMsg": "{\\"users\\":[]}", "errorType": "message", "url": "https://www.duolingo.com/profile/{}", "urlMain": "https://duolingo.com/", "urlProbe": "https://www.duolingo.com/2017-06-30/users?username={}", "username_claimed": "blue"}, "Eintracht Frankfurt Forum": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://community.eintracht.de/fans/{}", "urlMain": "https://community.eintracht.de/", "username_claimed": "mmammu"}, "Empretienda AR": {"__comment__": "Note that Error Connecting responses may be indicative of unclaimed handles", "errorType": "status_code", "url": "https://{}.empretienda.com.ar", "urlMain": "https://empretienda.com", "username_claimed": "camalote"}, "Envato Forum": {"errorType": "status_code", "url": "https://forums.envato.com/u/{}", "urlMain": "https://forums.envato.com/", "username_claimed": "enabled"}, "Erome": {"errorType": "status_code", "isNSFW": true, "url": "https://www.erome.com/{}", "urlMain": "https://www.erome.com/", "username_claimed": "bob"}, "Exposure": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9-]{1,63}$", "url": "https://{}.exposure.co/", "urlMain": "https://exposure.co/", "username_claimed": "jonasjacobsson"}, "exophase": {"errorType": "status_code", "url": "https://www.exophase.com/user/{}/", "urlMain": "https://www.exophase.com/", "username_claimed": "blue"}, "EyeEm": {"errorType": "status_code", "url": "https://www.eyeem.com/u/{}", "urlMain": "https://www.eyeem.com/", "username_claimed": "blue"}, "F3.cool": {"errorType": "status_code", "url": "https://f3.cool/{}/", "urlMain": "https://f3.cool/", "username_claimed": "blue"}, "Fameswap": {"errorType": "status_code", "url": "https://fameswap.com/user/{}", "urlMain": "https://fameswap.com/", "username_claimed": "fameswap"}, "Fandom": {"errorType": "status_code", "url": "https://www.fandom.com/u/{}", "urlMain": "https://www.fandom.com/", "username_claimed": "Jungypoo"}, "Fanpop": {"errorType": "response_url", "errorUrl": "https://www.fanpop.com/", "url": "https://www.fanpop.com/fans/{}", "urlMain": "https://www.fanpop.com/", "username_claimed": "blue"}, "Finanzfrage": {"errorType": "status_code", "url": "https://www.finanzfrage.net/nutzer/{}", "urlMain": "https://www.finanzfrage.net/", "username_claimed": "finanzfrage"}, "Flickr": {"errorType": "status_code", "url": "https://www.flickr.com/people/{}", "urlMain": "https://www.flickr.com/", "username_claimed": "blue"}, "Flightradar24": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9_]{3,20}$", "url": "https://my.flightradar24.com/{}", "urlMain": "https://www.flightradar24.com/", "username_claimed": "jebbrooks"}, "Flipboard": {"errorType": "status_code", "regexCheck": "^([a-zA-Z0-9_]){1,15}$", "url": "https://flipboard.com/@{}", "urlMain": "https://flipboard.com/", "username_claimed": "blue"}, "Football": {"errorMsg": "\\u041f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c \\u0441 \\u0442\\u0430\\u043a\\u0438\\u043c \\u0438\\u043c\\u0435\\u043d\\u0435\\u043c \\u043d\\u0435 \\u043d\\u0430\\u0439\\u0434\\u0435\\u043d", "errorType": "message", "url": "https://www.rusfootball.info/user/{}/", "urlMain": "https://www.rusfootball.info/", "username_claimed": "solo87"}, "FortniteTracker": {"errorType": "status_code", "url": "https://fortnitetracker.com/profile/all/{}", "urlMain": "https://fortnitetracker.com/challenges", "username_claimed": "blue"}, "Forum Ophilia": {"errorMsg": "that user does not exist", "errorType": "message", "isNSFW": true, "url": "https://www.forumophilia.com/profile.php?mode=viewprofile&u={}", "urlMain": "https://www.forumophilia.com/", "username_claimed": "bob"}, "Fosstodon": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9_]{1,30}$", "url": "https://fosstodon.org/@{}", "urlMain": "https://fosstodon.org/", "username_claimed": "blue"}, "Framapiaf": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9_]{1,30}$", "url": "https://framapiaf.org/@{}", "urlMain": "https://framapiaf.org", "username_claimed": "pylapp"}, "Freelancer": {"errorMsg": "\\"users\\":{}", "errorType": "message", "url": "https://www.freelancer.com/u/{}", "urlMain": "https://www.freelancer.com/", "urlProbe": "https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D={}&compact=true", "username_claimed": "red0xff"}, "Freesound": {"errorType": "status_code", "url": "https://freesound.org/people/{}/", "urlMain": "https://freesound.org/", "username_claimed": "blue"}, "GNOME VCS": {"errorType": "response_url", "errorUrl": "https://gitlab.gnome.org/{}", "regexCheck": "^(?!-)[a-zA-Z0-9_.-]{2,255}(?<!\\\\.)$", "url": "https://gitlab.gnome.org/{}", "urlMain": "https://gitlab.gnome.org/", "username_claimed": "adam"}, "GaiaOnline": {"errorMsg": "No user ID specified or user does not exist", "errorType": "message", "url": "https://www.gaiaonline.com/profiles/{}", "urlMain": "https://www.gaiaonline.com/", "username_claimed": "adam"}, "Gamespot": {"errorType": "status_code", "url": "https://www.gamespot.com/profile/{}/", "urlMain": "https://www.gamespot.com/", "username_claimed": "blue"}, "GameFAQs": {"errorType": "status_code", "url": "https://gamefaqs.gamespot.com/community/{}", "urlMain": "https://gamefaqs.gamespot.com", "username_claimed": "blue"}, "GeeksforGeeks": {"errorMsg": "false   | GeeksforGeeks Profile", "errorType": "message", "url": "https://auth.geeksforgeeks.org/user/{}", "urlMain": "https://www.geeksforgeeks.org/", "username_claimed": "adam"}, "Genius (Artists)": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9]{5,50}$", "url": "https://genius.com/artists/{}", "urlMain": "https://genius.com/", "username_claimed": "genius"}, "Genius (Users)": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9]*?$", "url": "https://genius.com/{}", "urlMain": "https://genius.com/", "username_claimed": "genius"}, "Gesundheitsfrage": {"errorType": "status_code", "url": "https://www.gesundheitsfrage.net/nutzer/{}", "urlMain": "https://www.gesundheitsfrage.net/", "username_claimed": "gutefrage"}, "GetMyUni": {"errorType": "status_code", "url": "https://www.getmyuni.com/user/{}", "urlMain": "https://getmyuni.com/", "username_claimed": "Upneet.Grover17"}, "Giant Bomb": {"errorType": "status_code", "url": "https://www.giantbomb.com/profile/{}/", "urlMain": "https://www.giantbomb.com/", "username_claimed": "bob"}, "Giphy": {"errorType": "message", "errorMsg": "<title> GIFs - Find &amp; Share on GIPHY</title>", "url": "https://giphy.com/{}", "urlMain": "https://giphy.com/", "username_claimed": "red"}, "GitBook": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.gitbook.io/", "urlMain": "https://gitbook.com/", "username_claimed": "gitbook"}, "GitHub": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$", "url": "https://www.github.com/{}", "urlMain": "https://www.github.com/", "username_claimed": "blue"}, "Warframe Market": {"errorType": "status_code", "request_method": "GET", "url": "https://warframe.market/profile/{}", "urlMain": "https://warframe.market/", "urlProbe": "https://api.warframe.market/v2/user/{}", "username_claimed": "kaiallalone"}, "GitLab": {"errorMsg": "[]", "errorType": "message", "url": "https://gitlab.com/{}", "urlMain": "https://gitlab.com/", "urlProbe": "https://gitlab.com/api/v4/users?username={}", "username_claimed": "blue"}, "Gitea": {"errorType": "status_code", "url": "https://gitea.com/{}", "urlMain": "https://gitea.com/", "username_claimed": "xorm"}, "Gitee": {"errorType": "status_code", "url": "https://gitee.com/{}", "urlMain": "https://gitee.com/", "username_claimed": "wizzer"}, "GoodReads": {"errorType": "status_code", "url": "https://www.goodreads.com/{}", "urlMain": "https://www.goodreads.com/", "username_claimed": "blue"}, "Google Play": {"errorMsg": "the requested URL was not found on this server", "errorType": "message", "url": "https://play.google.com/store/apps/developer?id={}", "urlMain": "https://play.google.com", "username_claimed": "GitHub"}, "Gradle": {"errorType": "status_code", "regexCheck": "^(?!-)[a-zA-Z0-9-]{3,}(?<!-)$", "url": "https://plugins.gradle.org/u/{}", "urlMain": "https://gradle.org/", "username_claimed": "jetbrains"}, "Grailed": {"errorType": "response_url", "errorUrl": "https://www.grailed.com/{}", "url": "https://www.grailed.com/{}", "urlMain": "https://www.grailed.com/", "username_claimed": "blue"}, "Gravatar": {"errorType": "status_code", "regexCheck": "^((?!\\\\.).)*$", "url": "http://en.gravatar.com/{}", "urlMain": "http://en.gravatar.com/", "username_claimed": "blue"}, "Gumroad": {"errorMsg": "Page not found (404) - Gumroad", "errorType": "message", "regexCheck": "^[^.]*?$", "url": "https://www.gumroad.com/{}", "urlMain": "https://www.gumroad.com/", "username_claimed": "blue"}, "Gutefrage": {"errorType": "status_code", "url": "https://www.gutefrage.net/nutzer/{}", "urlMain": "https://www.gutefrage.net/", "username_claimed": "gutefrage"}, "HackTheBox": {"errorType": "status_code", "url": "https://forum.hackthebox.com/u/{}", "urlMain": "https://forum.hackthebox.com/", "username_claimed": "angar"}, "Hackaday": {"errorType": "status_code", "url": "https://hackaday.io/{}", "urlMain": "https://hackaday.io/", "username_claimed": "adam"}, "HackenProof (Hackers)": {"errorMsg": "Page not found", "errorType": "message", "regexCheck": "^[\\\\w-]{,34}$", "url": "https://hackenproof.com/hackers/{}", "urlMain": "https://hackenproof.com/", "username_claimed": "blazezaria"}, "HackerEarth": {"errorType": "status_code", "url": "https://hackerearth.com/@{}", "urlMain": "https://hackerearth.com/", "username_claimed": "naveennamani877"}, "HackerNews": {"__comment__": "First errMsg invalid, second errMsg rate limited. Not ideal. Adjust for better rate limit filtering.", "errorMsg": ["No such user.", "Sorry."], "errorType": "message", "url": "https://news.ycombinator.com/user?id={}", "urlMain": "https://news.ycombinator.com/", "username_claimed": "blue"}, "HackerOne": {"errorMsg": "Page not found", "errorType": "message", "url": "https://hackerone.com/{}", "urlMain": "https://hackerone.com/", "username_claimed": "stok"}, "HackerRank": {"errorMsg": "Something went wrong", "errorType": "message", "regexCheck": "^[^.]*?$", "url": "https://hackerrank.com/{}", "urlMain": "https://hackerrank.com/", "username_claimed": "satznova"}, "HackerSploit": {"errorType": "status_code", "url": "https://forum.hackersploit.org/u/{}", "urlMain": "https://forum.hackersploit.org/", "username_claimed": "hackersploit"}, "HackMD": {"errorType": "status_code", "url": "https://hackmd.io/@{}", "urlMain": "https://hackmd.io/", "username_claimed": "blue"}, "Harvard Scholar": {"errorType": "status_code", "url": "https://scholar.harvard.edu/{}", "urlMain": "https://scholar.harvard.edu/", "username_claimed": "ousmanekane"}, "Hashnode": {"errorType": "status_code", "url": "https://hashnode.com/@{}", "urlMain": "https://hashnode.com", "username_claimed": "blue"}, "Heavy-R": {"errorMsg": "Channel not found", "errorType": "message", "isNSFW": true, "url": "https://www.heavy-r.com/user/{}", "urlMain": "https://www.heavy-r.com/", "username_claimed": "kilroy222"}, "Hive Blog": {"errorMsg": "<title>User Not Found - Hive</title>", "errorType": "message", "url": "https://hive.blog/@{}", "urlMain": "https://hive.blog/", "username_claimed": "mango-juice"}, "Holopin": {"errorMsg": "true", "errorType": "message", "request_method": "POST", "request_payload": {"username": "{}"}, "url": "https://holopin.io/@{}", "urlMain": "https://holopin.io", "urlProbe": "https://www.holopin.io/api/auth/username", "username_claimed": "red"}, "Houzz": {"errorType": "status_code", "url": "https://houzz.com/user/{}", "urlMain": "https://houzz.com/", "username_claimed": "blue"}, "HubPages": {"errorType": "status_code", "url": "https://hubpages.com/@{}", "urlMain": "https://hubpages.com/", "username_claimed": "blue"}, "Hubski": {"errorMsg": "No such user", "errorType": "message", "url": "https://hubski.com/user/{}", "urlMain": "https://hubski.com/", "username_claimed": "blue"}, "HudsonRock": {"errorMsg": "This username is not associated", "errorType": "message", "url": "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={}", "urlMain": "https://hudsonrock.com", "username_claimed": "testadmin"}, "Hugging Face": {"errorType": "status_code", "url": "https://huggingface.co/{}", "urlMain": "https://huggingface.co/", "username_claimed": "Pasanlaksitha"}, "IFTTT": {"errorType": "status_code", "regexCheck": "^[A-Za-z0-9]{3,35}$", "url": "https://www.ifttt.com/p/{}", "urlMain": "https://www.ifttt.com/", "username_claimed": "blue"}, "Ifunny": {"errorType": "status_code", "url": "https://ifunny.co/user/{}", "urlMain": "https://ifunny.co/", "username_claimed": "agua"}, "IRC-Galleria": {"errorType": "response_url", "errorUrl": "https://irc-galleria.net/users/search?username={}", "url": "https://irc-galleria.net/user/{}", "urlMain": "https://irc-galleria.net/", "username_claimed": "appas"}, "Icons8 Community": {"errorType": "status_code", "url": "https://community.icons8.com/u/{}/summary", "urlMain": "https://community.icons8.com/", "username_claimed": "thefourCraft"}, "Image Fap": {"errorMsg": "Not found", "errorType": "message", "isNSFW": true, "url": "https://www.imagefap.com/profile/{}", "urlMain": "https://www.imagefap.com/", "username_claimed": "blue"}, "ImgUp.cz": {"errorType": "status_code", "url": "https://imgup.cz/{}", "urlMain": "https://imgup.cz/", "username_claimed": "adam"}, "Imgur": {"errorType": "status_code", "url": "https://imgur.com/user/{}", "urlMain": "https://imgur.com/", "urlProbe": "https://api.imgur.com/account/v1/accounts/{}?client_id=546c25a59c58ad7", "username_claimed": "blue"}, "imood": {"errorType": "status_code", "url": "https://www.imood.com/users/{}", "urlMain": "https://www.imood.com/", "username_claimed": "blue"}, "Instagram": {"errorType": "status_code", "url": "https://instagram.com/{}", "urlMain": "https://instagram.com/", "urlProbe": "https://imginn.com/{}", "username_claimed": "instagram"}, "Instapaper": {"errorType": "status_code", "request_method": "GET", "url": "https://www.instapaper.com/p/{}", "urlMain": "https://www.instapaper.com/", "username_claimed": "john"}, "Instructables": {"errorType": "status_code", "url": "https://www.instructables.com/member/{}", "urlMain": "https://www.instructables.com/", "urlProbe": "https://www.instructables.com/json-api/showAuthorExists?screenName={}", "username_claimed": "blue"}, "Intigriti": {"errorType": "status_code", "regexCheck": "[a-z0-9_]{1,25}", "request_method": "GET", "url": "https://app.intigriti.com/profile/{}", "urlMain": "https://app.intigriti.com", "urlProbe": "https://api.intigriti.com/user/public/profile/{}", "username_claimed": "blue"}, "Ionic Forum": {"errorType": "status_code", "url": "https://forum.ionicframework.com/u/{}", "urlMain": "https://forum.ionicframework.com/", "username_claimed": "theblue222"}, "Issuu": {"errorType": "status_code", "url": "https://issuu.com/{}", "urlMain": "https://issuu.com/", "username_claimed": "jenny"}, "Itch.io": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.itch.io/", "urlMain": "https://itch.io/", "username_claimed": "blue"}, "Itemfix": {"errorMsg": "<title>ItemFix - Channel: </title>", "errorType": "message", "url": "https://www.itemfix.com/c/{}", "urlMain": "https://www.itemfix.com/", "username_claimed": "blue"}, "Jellyfin Weblate": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9@._-]{1,150}$", "url": "https://translate.jellyfin.org/user/{}/", "urlMain": "https://translate.jellyfin.org/", "username_claimed": "EraYaN"}, "Jimdo": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.jimdosite.com", "urlMain": "https://jimdosite.com/", "username_claimed": "jenny"}, "Joplin Forum": {"errorType": "status_code", "url": "https://discourse.joplinapp.org/u/{}", "urlMain": "https://discourse.joplinapp.org/", "username_claimed": "laurent"}, "Jupyter Community Forum": {"errorMsg": "Oops! That page doesn\\u2019t exist or is private.", "errorType": "message", "url": "https://discourse.jupyter.org/u/{}/summary", "urlMain": "https://discourse.jupyter.org", "username_claimed": "choldgraf"}, "Kaggle": {"errorType": "status_code", "url": "https://www.kaggle.com/{}", "urlMain": "https://www.kaggle.com/", "username_claimed": "dansbecker"}, "kaskus": {"errorType": "status_code", "url": "https://www.kaskus.co.id/@{}", "urlMain": "https://www.kaskus.co.id", "urlProbe": "https://www.kaskus.co.id/api/users?username={}", "request_method": "GET", "username_claimed": "l0mbart"}, "Keybase": {"errorType": "status_code", "url": "https://keybase.io/{}", "urlMain": "https://keybase.io/", "username_claimed": "blue"}, "Kick": {"__comment__": "Cloudflare. Only viable when proxied.", "errorType": "status_code", "url": "https://kick.com/{}", "urlMain": "https://kick.com/", "urlProbe": "https://kick.com/api/v2/channels/{}", "username_claimed": "blue"}, "Kik": {"errorMsg": "The page you requested was not found", "errorType": "message", "url": "https://kik.me/{}", "urlMain": "http://kik.me/", "urlProbe": "https://ws2.kik.com/user/{}", "username_claimed": "blue"}, "Kongregate": {"errorType": "status_code", "headers": {"Accept": "text/html"}, "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://www.kongregate.com/accounts/{}", "urlMain": "https://www.kongregate.com/", "username_claimed": "blue"}, "Kvinneguiden": {"errorMsg": "{\\"result\\":\\"ok\\"}", "errorType": "message", "regexCheck": "^[a-zA-Z0-9_.-]{3,18}$", "urlProbe": "https://forum.kvinneguiden.no/?app=core&module=system&controller=ajax&do=usernameExists&input={}", "url": "https://forum.kvinneguiden.no", "urlMain": "https://forum.kvinneguiden.no", "username_claimed": "blue"}, "LOR": {"errorType": "status_code", "url": "https://www.linux.org.ru/people/{}/profile", "urlMain": "https://linux.org.ru/", "username_claimed": "red"}, "Laracast": {"errorType": "status_code", "url": "https://laracasts.com/@{}", "urlMain": "https://laracasts.com/", "regexCheck": "^[a-zA-Z0-9_-]{3,}$", "username_claimed": "user1"}, "Launchpad": {"errorType": "status_code", "url": "https://launchpad.net/~{}", "urlMain": "https://launchpad.net/", "username_claimed": "blue"}, "LeetCode": {"errorType": "status_code", "url": "https://leetcode.com/{}", "urlMain": "https://leetcode.com/", "username_claimed": "blue"}, "LemmyWorld": {"errorType": "message", "errorMsg": "<h1>Error!</h1>", "url": "https://lemmy.world/u/{}", "urlMain": "https://lemmy.world", "username_claimed": "blue"}, "LessWrong": {"url": "https://www.lesswrong.com/users/{}", "urlMain": "https://www.lesswrong.com/", "errorType": "response_url", "errorUrl": "https://www.lesswrong.com/", "username_claimed": "habryka"}, "Letterboxd": {"errorMsg": "Sorry, we can\\u2019t find the page you\\u2019ve requested.", "errorType": "message", "url": "https://letterboxd.com/{}", "urlMain": "https://letterboxd.com/", "username_claimed": "blue"}, "LibraryThing": {"errorMsg": "<p>Error: This user doesn\'t exist</p>", "errorType": "message", "headers": {"Cookie": "LTAnonSessionID=3159599315; LTUnifiedCookie=%7B%22areyouhuman%22%3A1%7D; "}, "url": "https://www.librarything.com/profile/{}", "urlMain": "https://www.librarything.com/", "username_claimed": "blue"}, "Lichess": {"errorType": "status_code", "url": "https://lichess.org/@/{}", "urlMain": "https://lichess.org", "username_claimed": "john"}, "LinkedIn": {"errorType": "status_code", "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}, "regexCheck": "^[a-zA-Z0-9]{3,100}$", "request_method": "GET", "url": "https://linkedin.com/in/{}", "urlMain": "https://linkedin.com", "username_claimed": "paulpfeister"}, "Linktree": {"errorMsg": "\\"statusCode\\":404", "errorType": "message", "regexCheck": "^[\\\\w\\\\.]{2,30}$", "url": "https://linktr.ee/{}", "urlMain": "https://linktr.ee/", "username_claimed": "anne"}, "LinuxFR.org": {"errorType": "status_code", "url": "https://linuxfr.org/users/{}", "urlMain": "https://linuxfr.org/", "username_claimed": "pylapp"}, "Listed": {"errorType": "response_url", "errorUrl": "https://listed.to/@{}", "url": "https://listed.to/@{}", "urlMain": "https://listed.to/", "username_claimed": "listed"}, "LiveJournal": {"errorType": "status_code", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://{}.livejournal.com", "urlMain": "https://www.livejournal.com/", "username_claimed": "blue"}, "Lobsters": {"errorType": "status_code", "regexCheck": "[A-Za-z0-9][A-Za-z0-9_-]{0,24}", "url": "https://lobste.rs/u/{}", "urlMain": "https://lobste.rs/", "username_claimed": "jcs"}, "LottieFiles": {"errorType": "status_code", "url": "https://lottiefiles.com/{}", "urlMain": "https://lottiefiles.com/", "username_claimed": "lottiefiles"}, "LushStories": {"errorType": "response_url", "errorUrl": "https://www.lushstories.com/login", "isNSFW": true, "url": "https://www.lushstories.com/profile/{}", "urlMain": "https://www.lushstories.com/", "username_claimed": "chris_brown"}, "MMORPG Forum": {"errorType": "status_code", "url": "https://forums.mmorpg.com/profile/{}", "urlMain": "https://forums.mmorpg.com/", "username_claimed": "goku"}, "Mamot": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9_]{1,30}$", "url": "https://mamot.fr/@{}", "urlMain": "https://mamot.fr/", "username_claimed": "anciensEnssat"}, "Medium": {"errorMsg": "<body", "errorType": "message", "url": "https://medium.com/@{}", "urlMain": "https://medium.com/", "urlProbe": "https://medium.com/feed/@{}", "username_claimed": "blue"}, "Memrise": {"errorType": "status_code", "url": "https://www.memrise.com/user/{}/", "urlMain": "https://www.memrise.com/", "username_claimed": "blue"}, "Minecraft": {"errorMsg": "Couldn\'t find any profile with name", "errorType": "message", "regexCheck": "^.{1,25}$", "url": "https://api.mojang.com/users/profiles/minecraft/{}", "urlMain": "https://minecraft.net/", "username_claimed": "blue"}, "MixCloud": {"errorType": "status_code", "url": "https://www.mixcloud.com/{}/", "urlMain": "https://www.mixcloud.com/", "urlProbe": "https://api.mixcloud.com/{}/", "username_claimed": "jenny"}, "Monkeytype": {"errorType": "status_code", "url": "https://monkeytype.com/profile/{}", "urlMain": "https://monkeytype.com/", "urlProbe": "https://api.monkeytype.com/users/{}/profile", "username_claimed": "Lost_Arrow"}, "Motherless": {"errorMsg": "no longer a member", "errorType": "message", "isNSFW": true, "url": "https://motherless.com/m/{}", "urlMain": "https://motherless.com/", "username_claimed": "hacker"}, "Motorradfrage": {"errorType": "status_code", "url": "https://www.motorradfrage.net/nutzer/{}", "urlMain": "https://www.motorradfrage.net/", "username_claimed": "gutefrage"}, "MuseScore": {"errorType": "status_code", "url": "https://musescore.com/{}", "urlMain": "https://musescore.com/", "username_claimed": "arrangeme", "request_method": "GET"}, "MyAnimeList": {"errorType": "status_code", "url": "https://myanimelist.net/profile/{}", "urlMain": "https://myanimelist.net/", "username_claimed": "blue"}, "MyMiniFactory": {"errorType": "status_code", "url": "https://www.myminifactory.com/users/{}", "urlMain": "https://www.myminifactory.com/", "username_claimed": "blue"}, "Mydramalist": {"errorMsg": "The requested page was not found", "errorType": "message", "url": "https://www.mydramalist.com/profile/{}", "urlMain": "https://mydramalist.com", "username_claimed": "elhadidy12398"}, "Myspace": {"errorType": "status_code", "url": "https://myspace.com/{}", "urlMain": "https://myspace.com/", "username_claimed": "blue"}, "NICommunityForum": {"errorMsg": "The page you were looking for could not be found.", "errorType": "message", "url": "https://community.native-instruments.com/profile/{}", "urlMain": "https://www.native-instruments.com/forum/", "username_claimed": "jambert"}, "namuwiki": {"__comment__": "This is a Korean site and it\'s expected to return false negatives in certain other regions.", "errorType": "status_code", "url": "https://namu.wiki/w/%EC%82%AC%EC%9A%A9%EC%9E%90:{}", "urlMain": "https://namu.wiki/", "username_claimed": "namu"}, "NationStates Nation": {"errorMsg": "Was this your nation? It may have ceased to exist due to inactivity, but can rise again!", "errorType": "message", "url": "https://nationstates.net/nation={}", "urlMain": "https://nationstates.net", "username_claimed": "the_holy_principality_of_saint_mark"}, "NationStates Region": {"errorMsg": "does not exist.", "errorType": "message", "url": "https://nationstates.net/region={}", "urlMain": "https://nationstates.net", "username_claimed": "the_west_pacific"}, "Naver": {"errorType": "status_code", "url": "https://blog.naver.com/{}", "urlMain": "https://naver.com", "username_claimed": "blue"}, "Needrom": {"errorType": "status_code", "url": "https://www.needrom.com/author/{}/", "urlMain": "https://www.needrom.com/", "username_claimed": "needrom"}, "Newgrounds": {"errorType": "status_code", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://{}.newgrounds.com", "urlMain": "https://newgrounds.com", "username_claimed": "blue"}, "Nextcloud Forum": {"errorType": "status_code", "regexCheck": "^(?![.-])[a-zA-Z0-9_.-]{3,20}$", "url": "https://help.nextcloud.com/u/{}/summary", "urlMain": "https://nextcloud.com/", "username_claimed": "blue"}, "Nightbot": {"errorType": "status_code", "url": "https://nightbot.tv/t/{}/commands", "urlMain": "https://nightbot.tv/", "urlProbe": "https://api.nightbot.tv/1/channels/t/{}", "username_claimed": "green"}, "Ninja Kiwi": {"errorType": "response_url", "errorUrl": "https://ninjakiwi.com/profile/{}", "url": "https://ninjakiwi.com/profile/{}", "urlMain": "https://ninjakiwi.com/", "username_claimed": "Kyruko"}, "NintendoLife": {"errorType": "status_code", "url": "https://www.nintendolife.com/users/{}", "urlMain": "https://www.nintendolife.com/", "username_claimed": "goku"}, "NitroType": {"errorMsg": "<title>Nitro Type | Competitive Typing Game | Race Your Friends</title>", "errorType": "message", "url": "https://www.nitrotype.com/racer/{}", "urlMain": "https://www.nitrotype.com/", "username_claimed": "jianclash"}, "NotABug.org": {"errorType": "status_code", "url": "https://notabug.org/{}", "urlMain": "https://notabug.org/", "urlProbe": "https://notabug.org/{}/followers", "username_claimed": "red"}, "Nothing Community": {"errorType": "status_code", "url": "https://nothing.community/u/{}", "urlMain": "https://nothing.community/", "username_claimed": "Carl"}, "Nyaa.si": {"errorType": "status_code", "url": "https://nyaa.si/user/{}", "urlMain": "https://nyaa.si/", "username_claimed": "blue"}, "ObservableHQ": {"errorType": "message", "errorMsg": "Page not found", "url": "https://observablehq.com/@{}", "urlMain": "https://observablehq.com/", "username_claimed": "mbostock"}, "Open Collective": {"errorType": "status_code", "url": "https://opencollective.com/{}", "urlMain": "https://opencollective.com/", "username_claimed": "sindresorhus"}, "OpenGameArt": {"errorType": "status_code", "url": "https://opengameart.org/users/{}", "urlMain": "https://opengameart.org", "username_claimed": "ski"}, "OpenStreetMap": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://www.openstreetmap.org/user/{}", "urlMain": "https://www.openstreetmap.org/", "username_claimed": "blue"}, "Odysee": {"errorMsg": "<link rel=\\"canonical\\" content=\\"odysee.com\\"/>", "errorType": "message", "url": "https://odysee.com/@{}", "urlMain": "https://odysee.com/", "username_claimed": "Odysee"}, "Opensource": {"errorType": "status_code", "url": "https://opensource.com/users/{}", "urlMain": "https://opensource.com/", "username_claimed": "red"}, "OurDJTalk": {"errorMsg": "The specified member cannot be found", "errorType": "message", "url": "https://ourdjtalk.com/members?username={}", "urlMain": "https://ourdjtalk.com/", "username_claimed": "steve"}, "Outgress": {"errorMsg": "Outgress - Error", "errorType": "message", "url": "https://outgress.com/agents/{}", "urlMain": "https://outgress.com/", "username_claimed": "pylapp"}, "PCGamer": {"errorMsg": "The specified member cannot be found. Please enter a member\'s entire name.", "errorType": "message", "url": "https://forums.pcgamer.com/members/?username={}", "urlMain": "https://pcgamer.com", "username_claimed": "admin"}, "PSNProfiles.com": {"errorType": "response_url", "errorUrl": "https://psnprofiles.com/?psnId={}", "url": "https://psnprofiles.com/{}", "urlMain": "https://psnprofiles.com/", "username_claimed": "blue"}, "Packagist": {"errorType": "response_url", "errorUrl": "https://packagist.org/search/?q={}&reason=vendor_not_found", "url": "https://packagist.org/packages/{}/", "urlMain": "https://packagist.org/", "username_claimed": "psr"}, "Pastebin": {"errorMsg": "Not Found (#404)", "errorType": "message", "url": "https://pastebin.com/u/{}", "urlMain": "https://pastebin.com/", "username_claimed": "blue"}, "Patched": {"errorMsg": "The member you specified is either invalid or doesn\'t exist.", "errorType": "message", "url": "https://patched.sh/User/{}", "urlMain": "https://patched.sh/", "username_claimed": "blue"}, "Patreon": {"errorType": "status_code", "url": "https://www.patreon.com/{}", "urlMain": "https://www.patreon.com/", "username_claimed": "blue"}, "PentesterLab": {"errorType": "status_code", "regexCheck": "^[\\\\w]{4,30}$", "url": "https://pentesterlab.com/profile/{}", "urlMain": "https://pentesterlab.com/", "username_claimed": "0day"}, "HotUKdeals": {"errorType": "status_code", "url": "https://www.hotukdeals.com/profile/{}", "urlMain": "https://www.hotukdeals.com/", "username_claimed": "Blue", "request_method": "GET"}, "Mydealz": {"errorType": "status_code", "url": "https://www.mydealz.de/profile/{}", "urlMain": "https://www.mydealz.de/", "username_claimed": "blue", "request_method": "GET"}, "Chollometro": {"errorType": "status_code", "url": "https://www.chollometro.com/profile/{}", "urlMain": "https://www.chollometro.com/", "username_claimed": "blue", "request_method": "GET"}, "PepperNL": {"errorType": "status_code", "url": "https://nl.pepper.com/profile/{}", "urlMain": "https://nl.pepper.com/", "username_claimed": "Dynaw", "request_method": "GET"}, "PepperPL": {"errorType": "status_code", "url": "https://www.pepper.pl/profile/{}", "urlMain": "https://www.pepper.pl/", "username_claimed": "FireChicken", "request_method": "GET"}, "Preisjaeger": {"errorType": "status_code", "url": "https://www.preisjaeger.at/profile/{}", "urlMain": "https://www.preisjaeger.at/", "username_claimed": "Stefan", "request_method": "GET"}, "Pepperdeals": {"errorType": "status_code", "url": "https://www.pepperdeals.se/profile/{}", "urlMain": "https://www.pepperdeals.se/", "username_claimed": "Mark", "request_method": "GET"}, "PepperealsUS": {"errorType": "status_code", "url": "https://www.pepperdeals.com/profile/{}", "urlMain": "https://www.pepperdeals.com/", "username_claimed": "Stepan", "request_method": "GET"}, "Promodescuentos": {"errorType": "status_code", "url": "https://www.promodescuentos.com/profile/{}", "urlMain": "https://www.promodescuentos.com/", "username_claimed": "blue", "request_method": "GET"}, "Periscope": {"errorType": "status_code", "url": "https://www.periscope.tv/{}/", "urlMain": "https://www.periscope.tv/", "username_claimed": "blue"}, "Pinkbike": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://www.pinkbike.com/u/{}/", "urlMain": "https://www.pinkbike.com/", "username_claimed": "blue"}, "pixelfed.social": {"errorType": "status_code", "url": "https://pixelfed.social/{}/", "urlMain": "https://pixelfed.social", "username_claimed": "pylapp"}, "PlayStore": {"errorType": "status_code", "url": "https://play.google.com/store/apps/developer?id={}", "urlMain": "https://play.google.com/store", "username_claimed": "Facebook"}, "Playstrategy": {"errorType": "status_code", "url": "https://playstrategy.org/@/{}", "urlMain": "https://playstrategy.org", "username_claimed": "oruro"}, "Plurk": {"errorMsg": "User Not Found!", "errorType": "message", "url": "https://www.plurk.com/{}", "urlMain": "https://www.plurk.com/", "username_claimed": "plurkoffice"}, "PocketStars": {"errorMsg": "Join Your Favorite Adult Stars", "errorType": "message", "isNSFW": true, "url": "https://pocketstars.com/{}", "urlMain": "https://pocketstars.com/", "username_claimed": "hacker"}, "Pokemon Showdown": {"errorType": "status_code", "url": "https://pokemonshowdown.com/users/{}", "urlMain": "https://pokemonshowdown.com", "username_claimed": "blue"}, "Polarsteps": {"errorType": "status_code", "url": "https://polarsteps.com/{}", "urlMain": "https://polarsteps.com/", "urlProbe": "https://api.polarsteps.com/users/byusername/{}", "username_claimed": "james"}, "Polygon": {"errorType": "status_code", "url": "https://www.polygon.com/users/{}", "urlMain": "https://www.polygon.com/", "username_claimed": "swiftstickler"}, "Polymart": {"errorType": "response_url", "errorUrl": "https://polymart.org/user/-1", "url": "https://polymart.org/user/{}", "urlMain": "https://polymart.org/", "username_claimed": "craciu25yt"}, "Pornhub": {"errorType": "status_code", "isNSFW": true, "url": "https://pornhub.com/users/{}", "urlMain": "https://pornhub.com/", "username_claimed": "blue"}, "ProductHunt": {"errorType": "status_code", "url": "https://www.producthunt.com/@{}", "urlMain": "https://www.producthunt.com/", "username_claimed": "jenny"}, "programming.dev": {"errorMsg": "Error!", "errorType": "message", "url": "https://programming.dev/u/{}", "urlMain": "https://programming.dev", "username_claimed": "pylapp"}, "Pychess": {"errorType": "message", "errorMsg": "404", "url": "https://www.pychess.org/@/{}", "urlMain": "https://www.pychess.org", "username_claimed": "gbtami"}, "PromoDJ": {"errorType": "status_code", "url": "http://promodj.com/{}", "urlMain": "http://promodj.com/", "username_claimed": "blue"}, "Pronouns.page": {"errorType": "status_code", "url": "https://pronouns.page/@{}", "urlMain": "https://pronouns.page/", "username_claimed": "andrea"}, "PyPi": {"errorType": "status_code", "url": "https://pypi.org/user/{}", "urlProbe": "https://pypi.org/_includes/administer-user-include/{}", "urlMain": "https://pypi.org", "username_claimed": "Blue"}, "Python.org Discussions": {"errorMsg": "Oops! That page doesn\\u2019t exist or is private.", "errorType": "message", "url": "https://discuss.python.org/u/{}/summary", "urlMain": "https://discuss.python.org", "username_claimed": "pablogsal"}, "Rajce.net": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.rajce.idnes.cz/", "urlMain": "https://www.rajce.idnes.cz/", "username_claimed": "blue"}, "Rarible": {"errorType": "status_code", "url": "https://rarible.com/marketplace/api/v4/urls/{}", "urlMain": "https://rarible.com/", "username_claimed": "blue"}, "Rate Your Music": {"errorType": "status_code", "url": "https://rateyourmusic.com/~{}", "urlMain": "https://rateyourmusic.com/", "username_claimed": "blue"}, "Rclone Forum": {"errorType": "status_code", "url": "https://forum.rclone.org/u/{}", "urlMain": "https://forum.rclone.org/", "username_claimed": "ncw"}, "RedTube": {"errorType": "status_code", "isNSFW": true, "url": "https://www.redtube.com/users/{}", "urlMain": "https://www.redtube.com/", "username_claimed": "hacker"}, "Redbubble": {"errorType": "status_code", "url": "https://www.redbubble.com/people/{}", "urlMain": "https://www.redbubble.com/", "username_claimed": "blue"}, "Reddit": {"errorMsg": "Sorry, nobody on Reddit goes by that name.", "errorType": "message", "headers": {"accept-language": "en-US,en;q=0.9"}, "url": "https://www.reddit.com/user/{}", "urlMain": "https://www.reddit.com/", "username_claimed": "blue"}, "Realmeye": {"errorMsg": "Sorry, but we either:", "errorType": "message", "url": "https://www.realmeye.com/player/{}", "urlMain": "https://www.realmeye.com/", "username_claimed": "rotmg"}, "Reisefrage": {"errorType": "status_code", "url": "https://www.reisefrage.net/nutzer/{}", "urlMain": "https://www.reisefrage.net/", "username_claimed": "reisefrage"}, "Replit.com": {"errorType": "status_code", "url": "https://replit.com/@{}", "urlMain": "https://replit.com/", "username_claimed": "blue"}, "ResearchGate": {"errorType": "response_url", "errorUrl": "https://www.researchgate.net/directory/profiles", "regexCheck": "\\\\w+_\\\\w+", "url": "https://www.researchgate.net/profile/{}", "urlMain": "https://www.researchgate.net/", "username_claimed": "John_Smith"}, "ReverbNation": {"errorMsg": "Sorry, we couldn\'t find that page", "errorType": "message", "url": "https://www.reverbnation.com/{}", "urlMain": "https://www.reverbnation.com/", "username_claimed": "blue"}, "Roblox": {"errorType": "status_code", "url": "https://www.roblox.com/user.aspx?username={}", "urlMain": "https://www.roblox.com/", "username_claimed": "bluewolfekiller"}, "RocketTube": {"errorMsg": "OOPS! Houston, we have a problem", "errorType": "message", "isNSFW": true, "url": "https://www.rockettube.com/{}", "urlMain": "https://www.rockettube.com/", "username_claimed": "Tatteddick5600"}, "RoyalCams": {"errorType": "status_code", "url": "https://royalcams.com/profile/{}", "urlMain": "https://royalcams.com", "username_claimed": "asuna-black"}, "Ruby Forums": {"errorMsg": "Oops! That page doesn\\u2019t exist or is private.", "errorType": "message", "url": "https://ruby-forum.com/u/{}/summary", "urlMain": "https://ruby-forums.com", "username_claimed": "rishard"}, "RubyGems": {"errorType": "status_code", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]{1,40}", "url": "https://rubygems.org/profiles/{}", "urlMain": "https://rubygems.org/", "username_claimed": "blue"}, "Rumble": {"errorType": "status_code", "url": "https://rumble.com/user/{}", "urlMain": "https://rumble.com/", "username_claimed": "John"}, "RuneScape": {"errorMsg": "{\\"error\\":\\"NO_PROFILE\\",\\"loggedIn\\":\\"false\\"}", "errorType": "message", "regexCheck": "^(?! )[\\\\w -]{1,12}(?<! )$", "url": "https://apps.runescape.com/runemetrics/app/overview/player/{}", "urlMain": "https://www.runescape.com/", "urlProbe": "https://apps.runescape.com/runemetrics/profile/profile?user={}", "username_claimed": "L33"}, "SWAPD": {"errorType": "status_code", "url": "https://swapd.co/u/{}", "urlMain": "https://swapd.co/", "username_claimed": "swapd"}, "Sbazar.cz": {"errorType": "status_code", "url": "https://www.sbazar.cz/{}", "urlMain": "https://www.sbazar.cz/", "username_claimed": "blue"}, "Scratch": {"errorType": "status_code", "url": "https://scratch.mit.edu/users/{}", "urlMain": "https://scratch.mit.edu/", "username_claimed": "griffpatch"}, "Scribd": {"errorMsg": "Page not found", "errorType": "message", "url": "https://www.scribd.com/{}", "urlMain": "https://www.scribd.com/", "username_claimed": "blue"}, "SEOForum": {"errorType": "status_code", "url": "https://seoforum.com/@{}", "urlMain": "https://www.seoforum.com/", "username_claimed": "ko"}, "Shelf": {"errorType": "status_code", "url": "https://www.shelf.im/{}", "urlMain": "https://www.shelf.im/", "username_claimed": "blue"}, "ShitpostBot5000": {"errorType": "status_code", "url": "https://www.shitpostbot.com/user/{}", "urlMain": "https://www.shitpostbot.com/", "username_claimed": "blue"}, "Signal": {"errorMsg": "Oops! That page doesn\\u2019t exist or is private.", "errorType": "message", "url": "https://community.signalusers.org/u/{}", "urlMain": "https://community.signalusers.org", "username_claimed": "jlund"}, "Sketchfab": {"errorType": "status_code", "url": "https://sketchfab.com/{}", "urlMain": "https://sketchfab.com/", "username_claimed": "blue"}, "Slack": {"errorType": "status_code", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://{}.slack.com", "urlMain": "https://slack.com", "username_claimed": "blue"}, "Slant": {"errorType": "status_code", "regexCheck": "^.{2,32}$", "url": "https://www.slant.co/users/{}", "urlMain": "https://www.slant.co/", "username_claimed": "blue"}, "Slashdot": {"errorMsg": "user you requested does not exist", "errorType": "message", "url": "https://slashdot.org/~{}", "urlMain": "https://slashdot.org", "username_claimed": "blue"}, "SlideShare": {"errorType": "message", "errorMsg": "<title>Page no longer exists</title>", "url": "https://slideshare.net/{}", "urlMain": "https://slideshare.net/", "username_claimed": "blue"}, "Slides": {"errorCode": 204, "errorType": "status_code", "url": "https://slides.com/{}", "urlMain": "https://slides.com/", "username_claimed": "blue"}, "SmugMug": {"errorType": "status_code", "regexCheck": "^[a-zA-Z]{1,35}$", "url": "https://{}.smugmug.com", "urlMain": "https://smugmug.com", "username_claimed": "winchester"}, "Smule": {"errorMsg": "Smule | Page Not Found (404)", "errorType": "message", "url": "https://www.smule.com/{}", "urlMain": "https://www.smule.com/", "username_claimed": "blue"}, "Snapchat": {"errorType": "status_code", "regexCheck": "^[a-z][a-z-_.]{3,15}", "request_method": "GET", "url": "https://www.snapchat.com/add/{}", "urlMain": "https://www.snapchat.com", "username_claimed": "teamsnapchat"}, "SOOP": {"errorType": "status_code", "url": "https://www.sooplive.co.kr/station/{}", "urlMain": "https://www.sooplive.co.kr/", "urlProbe": "https://api-channel.sooplive.co.kr/v1.1/channel/{}/station", "username_claimed": "udkn"}, "SoundCloud": {"errorType": "status_code", "url": "https://soundcloud.com/{}", "urlMain": "https://soundcloud.com/", "username_claimed": "blue"}, "SourceForge": {"errorType": "status_code", "url": "https://sourceforge.net/u/{}", "urlMain": "https://sourceforge.net/", "username_claimed": "blue"}, "SpaceHey": {"errorType": "message", "errorMsg": "Not Found (Error 404) | SpaceHey", "url": "https://spacehey.com/{}", "urlMain": "https://spacehey.com/", "username_claimed": "blue"}, "SoylentNews": {"errorMsg": "The user you requested does not exist, no matter how much you wish this might be the case.", "errorType": "message", "url": "https://soylentnews.org/~{}", "urlMain": "https://soylentnews.org", "username_claimed": "adam"}, "SpeakerDeck": {"errorType": "status_code", "url": "https://speakerdeck.com/{}", "urlMain": "https://speakerdeck.com/", "username_claimed": "pylapp"}, "Speedrun.com": {"errorType": "status_code", "url": "https://speedrun.com/users/{}", "urlMain": "https://speedrun.com/", "username_claimed": "example"}, "Spells8": {"errorType": "status_code", "url": "https://forum.spells8.com/u/{}", "urlMain": "https://spells8.com", "username_claimed": "susurrus"}, "Splice": {"errorType": "status_code", "url": "https://splice.com/{}", "urlMain": "https://splice.com/", "username_claimed": "splice"}, "Splits.io": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://splits.io/users/{}", "urlMain": "https://splits.io", "username_claimed": "cambosteve"}, "Sporcle": {"errorType": "status_code", "url": "https://www.sporcle.com/user/{}/people", "urlMain": "https://www.sporcle.com/", "username_claimed": "blue"}, "Sportlerfrage": {"errorType": "status_code", "url": "https://www.sportlerfrage.net/nutzer/{}", "urlMain": "https://www.sportlerfrage.net/", "username_claimed": "sportlerfrage"}, "SportsRU": {"errorType": "status_code", "url": "https://www.sports.ru/profile/{}/", "urlMain": "https://www.sports.ru/", "username_claimed": "blue"}, "Spotify": {"errorType": "status_code", "url": "https://open.spotify.com/user/{}", "urlMain": "https://open.spotify.com/", "username_claimed": "blue"}, "Star Citizen": {"errorMsg": "404", "errorType": "message", "url": "https://robertsspaceindustries.com/citizens/{}", "urlMain": "https://robertsspaceindustries.com/", "username_claimed": "blue"}, "Status Cafe": {"errorMsg": "Page Not Found", "errorType": "message", "url": "https://status.cafe/users/{}", "urlMain": "https://status.cafe/", "username_claimed": "blue"}, "Steam Community (Group)": {"errorMsg": "No group could be retrieved for the given URL", "errorType": "message", "url": "https://steamcommunity.com/groups/{}", "urlMain": "https://steamcommunity.com/", "username_claimed": "blue"}, "Steam Community (User)": {"errorMsg": "The specified profile could not be found", "errorType": "message", "url": "https://steamcommunity.com/id/{}/", "urlMain": "https://steamcommunity.com/", "username_claimed": "blue"}, "Strava": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://www.strava.com/athletes/{}", "urlMain": "https://www.strava.com/", "username_claimed": "blue"}, "Substack": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9][a-zA-Z0-9_-]{1,60}$", "url": "https://{}.substack.com/", "urlMain": "https://substack.com/", "username_claimed": "green"}, "SublimeForum": {"errorType": "status_code", "url": "https://forum.sublimetext.com/u/{}", "urlMain": "https://forum.sublimetext.com/", "username_claimed": "blue"}, "TETR.IO": {"errorMsg": "No such user!", "errorType": "message", "url": "https://ch.tetr.io/u/{}", "urlMain": "https://tetr.io", "urlProbe": "https://ch.tetr.io/api/users/{}", "username_claimed": "osk"}, "TheMovieDB": {"errorType": "status_code", "url": "https://www.themoviedb.org/u/{}", "urlMain": "https://www.themoviedb.org/", "username_claimed": "blue"}, "TikTok": {"url": "https://www.tiktok.com/@{}", "urlMain": "https://www.tiktok.com", "errorType": "message", "errorMsg": ["\\"statusCode\\":10221", "Govt. of India decided to block 59 apps"], "username_claimed": "charlidamelio"}, "Tiendanube": {"url": "https://{}.mitiendanube.com/", "urlMain": "https://www.tiendanube.com/", "errorType": "status_code", "username_claimed": "blue"}, "Topcoder": {"errorType": "status_code", "url": "https://profiles.topcoder.com/{}/", "urlMain": "https://topcoder.com/", "username_claimed": "USER", "urlProbe": "https://api.topcoder.com/v5/members/{}", "regexCheck": "^[a-zA-Z0-9_.]+$"}, "Topmate": {"errorType": "status_code", "url": "https://topmate.io/{}", "urlMain": "https://topmate.io/", "username_claimed": "blue"}, "TRAKTRAIN": {"errorType": "status_code", "url": "https://traktrain.com/{}", "urlMain": "https://traktrain.com/", "username_claimed": "traktrain"}, "Telegram": {"errorMsg": ["<title>Telegram Messenger</title>", "If you have <strong>Telegram</strong>, you can contact <a class=\\"tgme_username_link\\" href=\\"tg://resolve?domain="], "errorType": "message", "regexCheck": "^[a-zA-Z0-9_]{3,32}[^_]$", "url": "https://t.me/{}", "urlMain": "https://t.me/", "username_claimed": "blue"}, "Tellonym.me": {"errorType": "status_code", "url": "https://tellonym.me/{}", "urlMain": "https://tellonym.me/", "username_claimed": "blue"}, "Tenor": {"errorType": "status_code", "regexCheck": "^[A-Za-z0-9_]{2,32}$", "url": "https://tenor.com/users/{}", "urlMain": "https://tenor.com/", "username_claimed": "red"}, "Terraria Forums": {"errorMsg": "The following members could not be found", "errorType": "message", "url": "https://forums.terraria.org/index.php?search/42798315/&c[users]={}&o=relevance", "urlMain": "https://forums.terraria.org/index.php", "username_claimed": "blue"}, "ThemeForest": {"errorType": "status_code", "url": "https://themeforest.net/user/{}", "urlMain": "https://themeforest.net/", "username_claimed": "user"}, "tistory": {"errorType": "status_code", "url": "https://{}.tistory.com/", "urlMain": "https://www.tistory.com/", "username_claimed": "notice"}, "TnAFlix": {"errorType": "status_code", "isNSFW": true, "url": "https://www.tnaflix.com/profile/{}", "urlMain": "https://www.tnaflix.com/", "username_claimed": "hacker"}, "TradingView": {"errorType": "status_code", "request_method": "GET", "url": "https://www.tradingview.com/u/{}/", "urlMain": "https://www.tradingview.com/", "username_claimed": "blue"}, "Trakt": {"errorType": "status_code", "regexCheck": "^[^.]*$", "url": "https://www.trakt.tv/users/{}", "urlMain": "https://www.trakt.tv/", "username_claimed": "blue"}, "TrashboxRU": {"errorType": "status_code", "regexCheck": "^[A-Za-z0-9_-]{3,16}$", "url": "https://trashbox.ru/users/{}", "urlMain": "https://trashbox.ru/", "username_claimed": "blue"}, "Trawelling": {"errorType": "status_code", "url": "https://traewelling.de/@{}", "urlMain": "https://traewelling.de/", "username_claimed": "lassestolley"}, "Trello": {"errorMsg": "model not found", "errorType": "message", "url": "https://trello.com/{}", "urlMain": "https://trello.com/", "urlProbe": "https://trello.com/1/Members/{}", "username_claimed": "blue"}, "TryHackMe": {"errorMsg": "{\\"success\\":false}", "errorType": "message", "regexCheck": "^[a-zA-Z0-9.]{1,16}$", "url": "https://tryhackme.com/p/{}", "urlMain": "https://tryhackme.com/", "urlProbe": "https://tryhackme.com/api/user/exist/{}", "username_claimed": "ashu"}, "Tuna": {"errorType": "status_code", "regexCheck": "^[a-z0-9]{4,40}$", "url": "https://tuna.voicemod.net/user/{}", "urlMain": "https://tuna.voicemod.net/", "username_claimed": "bob"}, "Tweakers": {"errorType": "status_code", "url": "https://tweakers.net/gallery/{}", "urlMain": "https://tweakers.net", "username_claimed": "femme"}, "Twitch": {"errorMsg": "content=\'Twitch is the world&#39;s leading video platform and community for gamers.\'", "errorType": "message", "url": "https://www.twitch.tv/{}", "urlMain": "https://www.twitch.tv", "username_claimed": "xqc"}, "Trovo": {"errorMsg": "Uh Ohhh...", "errorType": "message", "url": "https://trovo.live/s/{}/", "urlMain": "https://trovo.live", "username_claimed": "Aimilios"}, "Twitter": {"errorMsg": ["<div class=\\"error-panel\\"><span>User ", "<title>429 Too Many Requests</title>"], "errorType": "message", "regexCheck": "^[a-zA-Z0-9_]{1,15}$", "url": "https://x.com/{}", "urlMain": "https://x.com/", "urlProbe": "https://nitter.privacydev.net/{}", "username_claimed": "blue"}, "Typeracer": {"errorMsg": "Profile Not Found", "errorType": "message", "url": "https://data.typeracer.com/pit/profile?user={}", "urlMain": "https://typeracer.com", "username_claimed": "blue"}, "Ultimate-Guitar": {"errorType": "status_code", "url": "https://ultimate-guitar.com/u/{}", "urlMain": "https://ultimate-guitar.com/", "username_claimed": "blue"}, "Unsplash": {"errorType": "status_code", "regexCheck": "^[a-z0-9_]{1,60}$", "url": "https://unsplash.com/@{}", "urlMain": "https://unsplash.com/", "username_claimed": "jenny"}, "Untappd": {"errorType": "status_code", "url": "https://untappd.com/user/{}", "urlMain": "https://untappd.com/", "username_claimed": "untappd"}, "Valorant Forums": {"errorMsg": "The page you requested could not be found.", "errorType": "message", "url": "https://valorantforums.com/u/{}", "urlMain": "https://valorantforums.com", "username_claimed": "Wolves"}, "VK": {"errorType": "response_url", "errorUrl": "https://www.quora.com/profile/{}", "url": "https://vk.com/{}", "urlMain": "https://vk.com/", "username_claimed": "brown"}, "VSCO": {"errorType": "status_code", "url": "https://vsco.co/{}", "urlMain": "https://vsco.co/", "username_claimed": "blue"}, "Velog": {"errorType": "status_code", "url": "https://velog.io/@{}/posts", "urlMain": "https://velog.io/", "username_claimed": "qlgks1"}, "Velomania": {"errorMsg": "\\u041f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c \\u043d\\u0435 \\u0437\\u0430\\u0440\\u0435\\u0433\\u0438\\u0441\\u0442\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d \\u0438 \\u043d\\u0435 \\u0438\\u043c\\u0435\\u0435\\u0442 \\u043f\\u0440\\u043e\\u0444\\u0438\\u043b\\u044f \\u0434\\u043b\\u044f \\u043f\\u0440\\u043e\\u0441\\u043c\\u043e\\u0442\\u0440\\u0430.", "errorType": "message", "url": "https://forum.velomania.ru/member.php?username={}", "urlMain": "https://forum.velomania.ru/", "username_claimed": "red"}, "Venmo": {"errorMsg": ["Venmo | Page Not Found"], "errorType": "message", "headers": {"Host": "account.venmo.com"}, "url": "https://account.venmo.com/u/{}", "urlMain": "https://venmo.com/", "urlProbe": "https://test1.venmo.com/u/{}", "username_claimed": "jenny"}, "Vero": {"errorMsg": "Not Found", "errorType": "message", "request_method": "GET", "url": "https://vero.co/{}", "urlMain": "https://vero.co/", "username_claimed": "blue"}, "Vimeo": {"errorType": "status_code", "url": "https://vimeo.com/{}", "urlMain": "https://vimeo.com/", "username_claimed": "blue"}, "VirusTotal": {"errorType": "status_code", "request_method": "GET", "url": "https://www.virustotal.com/gui/user/{}", "urlMain": "https://www.virustotal.com/", "urlProbe": "https://www.virustotal.com/ui/users/{}/avatar", "username_claimed": "blue"}, "VLR": {"errorType": "status_code", "url": "https://www.vlr.gg/user/{}", "urlMain": "https://www.vlr.gg", "username_claimed": "optms"}, "WICG Forum": {"errorType": "status_code", "regexCheck": "^(?![.-])[a-zA-Z0-9_.-]{3,20}$", "url": "https://discourse.wicg.io/u/{}/summary", "urlMain": "https://discourse.wicg.io/", "username_claimed": "stefano"}, "Wakatime": {"errorType": "status_code", "url": "https://wakatime.com/@{}", "urlMain": "https://wakatime.com/", "username_claimed": "blue"}, "Warrior Forum": {"errorType": "status_code", "url": "https://www.warriorforum.com/members/{}.html", "urlMain": "https://www.warriorforum.com/", "username_claimed": "blue"}, "Wattpad": {"errorType": "status_code", "url": "https://www.wattpad.com/user/{}", "urlMain": "https://www.wattpad.com/", "urlProbe": "https://www.wattpad.com/api/v3/users/{}/", "username_claimed": "Dogstho7951"}, "WebNode": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.webnode.cz/", "urlMain": "https://www.webnode.cz/", "username_claimed": "radkabalcarova"}, "Weblate": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9@._-]{1,150}$", "url": "https://hosted.weblate.org/user/{}/", "urlMain": "https://hosted.weblate.org/", "username_claimed": "adam"}, "Weebly": {"errorType": "status_code", "regexCheck": "^[a-zA-Z0-9-]{1,63}$", "url": "https://{}.weebly.com/", "urlMain": "https://weebly.com/", "username_claimed": "blue"}, "Wikidot": {"errorMsg": "User does not exist.", "errorType": "message", "url": "http://www.wikidot.com/user:info/{}", "urlMain": "http://www.wikidot.com/", "username_claimed": "blue"}, "Wikipedia": {"errorMsg": "centralauth-admin-nonexistent:", "errorType": "message", "url": "https://en.wikipedia.org/wiki/Special:CentralAuth/{}?uselang=qqx", "urlMain": "https://www.wikipedia.org/", "username_claimed": "Hoadlck"}, "Windy": {"errorType": "status_code", "url": "https://community.windy.com/user/{}", "urlMain": "https://windy.com/", "username_claimed": "blue"}, "Wix": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.wix.com", "urlMain": "https://wix.com/", "username_claimed": "support"}, "WolframalphaForum": {"errorType": "status_code", "url": "https://community.wolfram.com/web/{}/home", "urlMain": "https://community.wolfram.com/", "username_claimed": "unico"}, "WordPress": {"errorType": "response_url", "errorUrl": "wordpress.com/typo/?subdomain=", "regexCheck": "^[a-zA-Z][a-zA-Z0-9_-]*$", "url": "https://{}.wordpress.com/", "urlMain": "https://wordpress.com", "username_claimed": "blue"}, "WordPressOrg": {"errorType": "response_url", "errorUrl": "https://wordpress.org", "url": "https://profiles.wordpress.org/{}/", "urlMain": "https://wordpress.org/", "username_claimed": "blue"}, "Wordnik": {"errorMsg": "Page Not Found", "errorType": "message", "regexCheck": "^[a-zA-Z0-9_.+-]{1,40}$", "url": "https://www.wordnik.com/users/{}", "urlMain": "https://www.wordnik.com/", "username_claimed": "blue"}, "Wykop": {"errorType": "status_code", "url": "https://www.wykop.pl/ludzie/{}", "urlMain": "https://www.wykop.pl", "username_claimed": "blue"}, "Xbox Gamertag": {"errorType": "status_code", "url": "https://xboxgamertag.com/search/{}", "urlMain": "https://xboxgamertag.com/", "username_claimed": "red"}, "Xvideos": {"errorType": "status_code", "isNSFW": true, "url": "https://xvideos.com/profiles/{}", "urlMain": "https://xvideos.com/", "username_claimed": "blue"}, "YandexMusic": {"__comment__": "The first and third errorMsg relate to geo-restrictions and bot detection/captchas.", "errorMsg": ["\\u041e\\u0448\\u0438\\u0431\\u043a\\u0430 404", "<meta name=\\"description\\" content=\\"\\u041e\\u0442\\u043a\\u0440\\u044b\\u0432\\u0430\\u0439\\u0442\\u0435 \\u043d\\u043e\\u0432\\u0443\\u044e \\u043c\\u0443\\u0437\\u044b\\u043a\\u0443 \\u043a\\u0430\\u0436\\u0434\\u044b\\u0439 \\u0434\\u0435\\u043d\\u044c.", "<input type=\\"submit\\" class=\\"CheckboxCaptcha-Button\\""], "errorType": "message", "url": "https://music.yandex/users/{}/playlists", "urlMain": "https://music.yandex", "username_claimed": "ya.playlist"}, "YouNow": {"errorMsg": "No users found", "errorType": "message", "url": "https://www.younow.com/{}/", "urlMain": "https://www.younow.com/", "urlProbe": "https://api.younow.com/php/api/broadcast/info/user={}/", "username_claimed": "blue"}, "YouPic": {"errorType": "status_code", "url": "https://youpic.com/photographer/{}/", "urlMain": "https://youpic.com/", "username_claimed": "blue"}, "YouPorn": {"errorType": "status_code", "isNSFW": true, "url": "https://youporn.com/uservids/{}", "urlMain": "https://youporn.com", "username_claimed": "blue"}, "YouTube": {"errorType": "status_code", "url": "https://www.youtube.com/@{}", "urlMain": "https://www.youtube.com/", "username_claimed": "youtube"}, "akniga": {"errorType": "status_code", "errorCode": 404, "request_method": "GET", "url": "https://akniga.org/profile/{}", "urlMain": "https://akniga.org/", "username_claimed": "blue"}, "authorSTREAM": {"errorType": "status_code", "url": "http://www.authorstream.com/{}/", "urlMain": "http://www.authorstream.com/", "username_claimed": "blue"}, "babyblogRU": {"errorType": "response_url", "errorUrl": "https://www.babyblog.ru/", "url": "https://www.babyblog.ru/user/{}", "urlMain": "https://www.babyblog.ru/", "username_claimed": "blue"}, "chaos.social": {"errorType": "status_code", "url": "https://chaos.social/@{}", "urlMain": "https://chaos.social/", "username_claimed": "rixx"}, "couchsurfing": {"errorType": "status_code", "url": "https://www.couchsurfing.com/people/{}", "urlMain": "https://www.couchsurfing.com/", "username_claimed": "blue"}, "d3RU": {"errorType": "status_code", "url": "https://d3.ru/user/{}/posts", "urlMain": "https://d3.ru/", "username_claimed": "blue"}, "dailykos": {"errorMsg": "{\\"result\\":true,\\"message\\":null}", "errorType": "message", "url": "https://www.dailykos.com/user/{}", "urlMain": "https://www.dailykos.com", "urlProbe": "https://www.dailykos.com/signup/check_nickname?nickname={}", "username_claimed": "blue"}, "datingRU": {"errorType": "status_code", "url": "http://dating.ru/{}", "urlMain": "http://dating.ru", "username_claimed": "blue"}, "devRant": {"errorType": "response_url", "errorUrl": "https://devrant.com/", "url": "https://devrant.com/users/{}", "urlMain": "https://devrant.com/", "username_claimed": "blue"}, "drive2": {"errorType": "status_code", "url": "https://www.drive2.ru/users/{}", "urlMain": "https://www.drive2.ru/", "username_claimed": "blue"}, "eGPU": {"errorType": "status_code", "url": "https://egpu.io/forums/profile/{}/", "urlMain": "https://egpu.io/", "username_claimed": "blue"}, "eintracht": {"errorType": "status_code", "regexCheck": "^[^.]*?$", "url": "https://community.eintracht.de/fans/{}", "urlMain": "https://eintracht.de", "username_claimed": "blue"}, "fixya": {"errorType": "status_code", "url": "https://www.fixya.com/users/{}", "urlMain": "https://www.fixya.com", "username_claimed": "adam"}, "fl": {"errorType": "status_code", "url": "https://www.fl.ru/users/{}", "urlMain": "https://www.fl.ru/", "username_claimed": "blue"}, "forum_guns": {"errorMsg": "action=https://forum.guns.ru/forummisc/blog/search", "errorType": "message", "url": "https://forum.guns.ru/forummisc/blog/{}", "urlMain": "https://forum.guns.ru/", "username_claimed": "red"}, "freecodecamp": {"errorType": "status_code", "url": "https://www.freecodecamp.org/{}", "urlMain": "https://www.freecodecamp.org/", "urlProbe": "https://api.freecodecamp.org/api/users/get-public-profile?username={}", "username_claimed": "naveennamani"}, "furaffinity": {"errorMsg": "This user cannot be found.", "errorType": "message", "url": "https://www.furaffinity.net/user/{}", "urlMain": "https://www.furaffinity.net", "username_claimed": "jesus"}, "geocaching": {"errorType": "status_code", "url": "https://www.geocaching.com/p/default.aspx?u={}", "urlMain": "https://www.geocaching.com/", "username_claimed": "blue"}, "habr": {"errorType": "status_code", "url": "https://habr.com/ru/users/{}", "urlMain": "https://habr.com/", "username_claimed": "blue"}, "hackster": {"errorType": "status_code", "url": "https://www.hackster.io/{}", "urlMain": "https://www.hackster.io", "username_claimed": "blue"}, "hunting": {"errorMsg": "\\u0423\\u043a\\u0430\\u0437\\u0430\\u043d\\u043d\\u044b\\u0439 \\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c \\u043d\\u0435 \\u043d\\u0430\\u0439\\u0434\\u0435\\u043d. \\u041f\\u043e\\u0436\\u0430\\u043b\\u0443\\u0439\\u0441\\u0442\\u0430, \\u0432\\u0432\\u0435\\u0434\\u0438\\u0442\\u0435 \\u0434\\u0440\\u0443\\u0433\\u043e\\u0435 \\u0438\\u043c\\u044f.", "errorType": "message", "url": "https://www.hunting.ru/forum/members/?username={}", "urlMain": "https://www.hunting.ru/forum/", "username_claimed": "red"}, "igromania": {"errorMsg": "\\u041f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c \\u043d\\u0435 \\u0437\\u0430\\u0440\\u0435\\u0433\\u0438\\u0441\\u0442\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d \\u0438 \\u043d\\u0435 \\u0438\\u043c\\u0435\\u0435\\u0442 \\u043f\\u0440\\u043e\\u0444\\u0438\\u043b\\u044f \\u0434\\u043b\\u044f \\u043f\\u0440\\u043e\\u0441\\u043c\\u043e\\u0442\\u0440\\u0430.", "errorType": "message", "url": "http://forum.igromania.ru/member.php?username={}", "urlMain": "http://forum.igromania.ru/", "username_claimed": "blue"}, "interpals": {"errorMsg": "The requested user does not exist or is inactive", "errorType": "message", "url": "https://www.interpals.net/{}", "urlMain": "https://www.interpals.net/", "username_claimed": "blue"}, "irecommend": {"errorType": "status_code", "url": "https://irecommend.ru/users/{}", "urlMain": "https://irecommend.ru/", "username_claimed": "blue"}, "jbzd.com.pl": {"errorType": "status_code", "url": "https://jbzd.com.pl/uzytkownik/{}", "urlMain": "https://jbzd.com.pl/", "username_claimed": "blue"}, "jeuxvideo": {"errorType": "status_code", "request_method": "GET", "url": "https://www.jeuxvideo.com/profil/{}", "urlMain": "https://www.jeuxvideo.com", "urlProbe": "https://www.jeuxvideo.com/profil/{}?mode=infos", "username_claimed": "adam"}, "kofi": {"errorType": "response_url", "errorUrl": "https://ko-fi.com/art?=redirect", "url": "https://ko-fi.com/{}", "urlMain": "https://ko-fi.com", "username_claimed": "yeahkenny"}, "kwork": {"errorType": "status_code", "url": "https://kwork.ru/user/{}", "urlMain": "https://www.kwork.ru/", "username_claimed": "blue"}, "last.fm": {"errorType": "status_code", "url": "https://last.fm/user/{}", "urlMain": "https://last.fm/", "username_claimed": "blue"}, "leasehackr": {"errorType": "status_code", "url": "https://forum.leasehackr.com/u/{}/summary/", "urlMain": "https://forum.leasehackr.com/", "username_claimed": "adam"}, "livelib": {"errorType": "status_code", "url": "https://www.livelib.ru/reader/{}", "urlMain": "https://www.livelib.ru/", "username_claimed": "blue"}, "mastodon.cloud": {"errorType": "status_code", "url": "https://mastodon.cloud/@{}", "urlMain": "https://mastodon.cloud/", "username_claimed": "TheAdmin"}, "mastodon.social": {"errorType": "status_code", "url": "https://mastodon.social/@{}", "urlMain": "https://chaos.social/", "username_claimed": "Gargron"}, "mastodon.xyz": {"errorType": "status_code", "url": "https://mastodon.xyz/@{}", "urlMain": "https://mastodon.xyz/", "username_claimed": "TheKinrar"}, "mstdn.social": {"errorType": "status_code", "url": "https://mstdn.social/@{}", "urlMain": "https://mstdn.social/", "username_claimed": "MagicLike"}, "mercadolivre": {"errorType": "status_code", "url": "https://www.mercadolivre.com.br/perfil/{}", "urlMain": "https://www.mercadolivre.com.br", "username_claimed": "blue"}, "minds": {"errorMsg": "\\"valid\\":true", "errorType": "message", "url": "https://www.minds.com/{}/", "urlMain": "https://www.minds.com", "urlProbe": "https://www.minds.com/api/v3/register/validate?username={}", "username_claimed": "john"}, "moikrug": {"errorType": "status_code", "url": "https://moikrug.ru/{}", "urlMain": "https://moikrug.ru/", "username_claimed": "blue"}, "mstdn.io": {"errorType": "status_code", "url": "https://mstdn.io/@{}", "urlMain": "https://mstdn.io/", "username_claimed": "blue"}, "nairaland.com": {"errorType": "status_code", "url": "https://www.nairaland.com/{}", "urlMain": "https://www.nairaland.com/", "username_claimed": "red"}, "n8n Community": {"errorType": "status_code", "url": "https://community.n8n.io/u/{}/summary", "urlMain": "https://community.n8n.io/", "username_claimed": "n8n"}, "nnRU": {"errorType": "status_code", "regexCheck": "^[\\\\w@-]+?$", "url": "https://{}.www.nn.ru/", "urlMain": "https://www.nn.ru/", "username_claimed": "blue"}, "note": {"errorType": "status_code", "url": "https://note.com/{}", "urlMain": "https://note.com/", "username_claimed": "blue"}, "npm": {"errorType": "status_code", "url": "https://www.npmjs.com/~{}", "urlMain": "https://www.npmjs.com/", "username_claimed": "kennethsweezy"}, "omg.lol": {"errorMsg": "\\"available\\": true", "errorType": "message", "url": "https://{}.omg.lol", "urlMain": "https://home.omg.lol", "urlProbe": "https://api.omg.lol/address/{}/availability", "username_claimed": "adam"}, "opennet": {"errorMsg": "\\u0418\\u043c\\u044f \\u0443\\u0447\\u0430\\u0441\\u0442\\u043d\\u0438\\u043a\\u0430 \\u043d\\u0435 \\u043d\\u0430\\u0439\\u0434\\u0435\\u043d\\u043e", "errorType": "message", "regexCheck": "^[^-]*$", "url": "https://www.opennet.ru/~{}", "urlMain": "https://www.opennet.ru/", "username_claimed": "anonismus"}, "osu!": {"errorType": "status_code", "url": "https://osu.ppy.sh/users/{}", "urlMain": "https://osu.ppy.sh/", "username_claimed": "blue"}, "phpRU": {"errorMsg": "\\u0423\\u043a\\u0430\\u0437\\u0430\\u043d\\u043d\\u044b\\u0439 \\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c \\u043d\\u0435 \\u043d\\u0430\\u0439\\u0434\\u0435\\u043d. \\u041f\\u043e\\u0436\\u0430\\u043b\\u0443\\u0439\\u0441\\u0442\\u0430, \\u0432\\u0432\\u0435\\u0434\\u0438\\u0442\\u0435 \\u0434\\u0440\\u0443\\u0433\\u043e\\u0435 \\u0438\\u043c\\u044f.", "errorType": "message", "url": "https://php.ru/forum/members/?username={}", "urlMain": "https://php.ru/forum/", "username_claimed": "apple"}, "pikabu": {"errorType": "status_code", "url": "https://pikabu.ru/@{}", "urlMain": "https://pikabu.ru/", "username_claimed": "blue"}, "Pinterest": {"errorType": "status_code", "errorUrl": "https://www.pinterest.com/", "url": "https://www.pinterest.com/{}/", "urlProbe": "https://www.pinterest.com/oembed.json?url=https://www.pinterest.com/{}/", "urlMain": "https://www.pinterest.com/", "username_claimed": "blue"}, "pr0gramm": {"errorType": "status_code", "url": "https://pr0gramm.com/user/{}", "urlMain": "https://pr0gramm.com/", "urlProbe": "https://pr0gramm.com/api/profile/info?name={}", "username_claimed": "cha0s"}, "prog.hu": {"errorType": "response_url", "errorUrl": "https://prog.hu/azonosito/info/{}", "url": "https://prog.hu/azonosito/info/{}", "urlMain": "https://prog.hu/", "username_claimed": "Sting"}, "satsisRU": {"errorType": "status_code", "url": "https://satsis.info/user/{}", "urlMain": "https://satsis.info/", "username_claimed": "red"}, "sessionize": {"errorType": "status_code", "url": "https://sessionize.com/{}", "urlMain": "https://sessionize.com/", "username_claimed": "jason-mayes"}, "social.tchncs.de": {"errorType": "status_code", "url": "https://social.tchncs.de/@{}", "urlMain": "https://social.tchncs.de/", "username_claimed": "Milan"}, "spletnik": {"errorType": "status_code", "url": "https://spletnik.ru/user/{}", "urlMain": "https://spletnik.ru/", "username_claimed": "blue"}, "svidbook": {"errorType": "status_code", "url": "https://www.svidbook.ru/user/{}", "urlMain": "https://www.svidbook.ru/", "username_claimed": "green"}, "threads": {"errorMsg": "<title>Threads \\u2022 Log in</title>", "errorType": "message", "headers": {"Sec-Fetch-Mode": "navigate"}, "url": "https://www.threads.net/@{}", "urlMain": "https://www.threads.net/", "username_claimed": "zuck"}, "toster": {"errorType": "status_code", "url": "https://www.toster.ru/user/{}/answers", "urlMain": "https://www.toster.ru/", "username_claimed": "adam"}, "tumblr": {"errorType": "status_code", "url": "https://{}.tumblr.com/", "urlMain": "https://www.tumblr.com/", "username_claimed": "goku"}, "uid": {"errorType": "status_code", "url": "http://uid.me/{}", "urlMain": "https://uid.me/", "username_claimed": "blue"}, "write.as": {"errorType": "status_code", "url": "https://write.as/{}", "urlMain": "https://write.as", "username_claimed": "pylapp"}, "xHamster": {"errorType": "status_code", "isNSFW": true, "url": "https://xhamster.com/users/{}", "urlMain": "https://xhamster.com", "urlProbe": "https://xhamster.com/users/{}?old_browser=true", "username_claimed": "blue"}, "znanylekarz.pl": {"errorType": "status_code", "url": "https://www.znanylekarz.pl/{}", "urlMain": "https://znanylekarz.pl", "username_claimed": "janusz-nowak"}, "Platzi": {"errorType": "status_code", "errorCode": 404, "url": "https://platzi.com/p/{}/", "urlMain": "https://platzi.com/", "username_claimed": "freddier", "request_method": "GET"}, "BabyRu": {"url": "https://www.baby.ru/u/{}", "urlMain": "https://www.baby.ru/", "errorType": "message", "errorMsg": ["\\u0421\\u0442\\u0440\\u0430\\u043d\\u0438\\u0446\\u0430, \\u043a\\u043e\\u0442\\u043e\\u0440\\u0443\\u044e \\u0432\\u044b \\u0438\\u0441\\u043a\\u0430\\u043b\\u0438, \\u043d\\u0435 \\u043d\\u0430\\u0439\\u0434\\u0435\\u043d\\u0430", "\\u0414\\u043e\\u0441\\u0442\\u0443\\u043f \\u0441 \\u0432\\u0430\\u0448\\u0435\\u0433\\u043e IP-\\u0430\\u0434\\u0440\\u0435\\u0441\\u0430 \\u0432\\u0440\\u0435\\u043c\\u0435\\u043d\\u043d\\u043e \\u043e\\u0433\\u0440\\u0430\\u043d\\u0438\\u0447\\u0435\\u043d"], "username_claimed": "example"}, "Wowhead": {"url": "https://wowhead.com/user={}", "urlMain": "https://wowhead.com/", "errorType": "status_code", "errorCode": 404, "username_claimed": "blue"}, "addons.wago.io": {"url": "https://addons.wago.io/user/{}", "urlMain": "https://addons.wago.io/", "errorType": "status_code", "errorCode": 404, "username_claimed": "blue"}, "CurseForge": {"url": "https://www.curseforge.com/members/{}/projects", "urlMain": "https://www.curseforge.com.", "errorType": "status_code", "errorCode": 404, "username_claimed": "blue"}}')
BUNDLED_EXCLUSIONS = json.loads('["7Cups", "APClips", "Airliners", "Apple Developer", "Apple Discussions", "Archive.org", "Bandcamp", "Championat", "Chatujme.cz", "ChaturBate", "Codolio", "DeviantArt", "Discord.bio", "Envato Forum", "GeeksforGeeks", "Giphy", "Hashnode", "Houzz", "Hubski", "Instapaper", "Linktree", "ObservableHQ", "Odysee", "OurDJTalk", "PCGamer", "Pornhub", "Rarible", "Realmeye", "Reddit", "ReverbNation", "RocketTube", "RuneScape", "Scribd", "Shelf", "SlideShare", "Splice", "Spotify", "Trakt", "Trovo", "TryHackMe", "Velomania", "Weblate", "YandexMusic", "authorSTREAM", "dailykos", "fixya", "hunting", "igromania", "interpals", "mercadolivre", "opennet", "phpRU", "social.tchncs.de", "svidbook", "xHamster"]')
BUNDLED_ADAPTERS = json.loads('{"GitHub": {"root": ".js-profile-editable-area", "identity": "[itemprop=\'additionalName\']", "fields": {"avatar": {"selector": "img.avatar", "attribute": "src"}, "bio": {"selector": ".user-profile-bio"}, "followers": {"selector": "a[href$=\'tab=followers\'] .text-bold"}, "following": {"selector": "a[href$=\'tab=following\'] .text-bold"}}}, "Twitter": {"root": "main", "identity": "[data-testid=\'UserName\'] span", "fields": {"bio": {"selector": "[data-testid=\'UserDescription\']"}, "avatar": {"selector": "[data-testid^=\'UserAvatar-Container\'] img", "attribute": "src"}, "followers": {"selector": "a[href$=\'/verified_followers\'] span, a[href$=\'/followers\'] span"}, "following": {"selector": "a[href$=\'/following\'] span"}}}, "Instagram": {"root": "main header", "identity": "h1, h2", "fields": {"avatar": {"selector": "img", "attribute": "src"}, "followers": {"selector": "a[href$=\'/followers/\'] span"}, "following": {"selector": "a[href$=\'/following/\'] span"}}}, "YouTube": {"root": "ytd-page-header-renderer, ytd-c4-tabbed-header-renderer", "identity": "#channel-handle, .yt-content-metadata-view-model__metadata-text", "fields": {"avatar": {"selector": "img", "attribute": "src"}, "bio": {"selector": "#description, .ytDescriptionPreviewViewModelAttributedString"}, "subscribers": {"selector": "#subscriber-count"}}}, "GitLab": {"root": ".user-profile", "identity": ".username", "fields": {"avatar": {"selector": "img.avatar", "attribute": "src"}, "bio": {"selector": ".user-bio"}, "followers": {"selector": "a[href$=\'/followers\']"}, "following": {"selector": "a[href$=\'/following\']"}}}}')
DATA_PROVENANCE = json.loads('{"retrieved_utc": "2026-09-26", "catalog_source": "https://github.com/sherlock-project/sherlock/blob/master/sherlock_project/resources/data.json", "exclusions_source": "https://raw.githubusercontent.com/sherlock-project/sherlock/refs/heads/exclusions/false_positive_exclusions.txt", "catalog_sha256": "3fdfc6694c5cd99798881215554b09e617c6d5284a6219fae309882566a9fb30", "raw_sites": 481}')



import json
import re
import unicodedata
from dataclasses import dataclass, field, replace
from difflib import SequenceMatcher
from urllib.parse import unquote, urljoin, urlsplit, parse_qs, parse_qsl, urlencode, urlunsplit

from bs4 import BeautifulSoup


@dataclass
class Page:
    requested_url: str
    final_url: str
    status: int | None
    html: str = ""
    text: str = ""
    title: str = ""
    error: str = ""
    stable: bool = True
    native_data: dict = field(default_factory=dict)
    captcha_active: bool | None = None
    captcha_note: str = ""
    session_lost: bool = False
    visible_labels: list[str] | None = None
    profile_pending: bool = False


@dataclass
class Evidence:
    identity: list[str] = field(default_factory=list)
    fields: dict = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    @property
    def positive(self):
        meaningful = {"bio", "avatar", "followers", "following", "posts", "likes",
                      "repositories", "contributions", "subscribers", "statistics", "display_name"}
        return bool(self.identity) and any(key in meaningful and value is not None and str(value).strip()
                                           for key, value in self.fields.items())

    @property
    def strong(self):

        meaningful = {"bio", "avatar", "followers", "following", "posts", "likes",
                      "repositories", "contributions", "subscribers", "statistics"}
        present = meaningful.intersection(self.fields)
        return bool(self.identity) and len(present) >= 2


def fold(value):
    return unicodedata.normalize("NFKC", str(value)).strip().casefold()


def handle(value, nick):

    normalize = lambda s: unicodedata.normalize("NFC", str(s)).strip().removeprefix("@").casefold()
    return normalize(value) == normalize(nick)


def normalized_url(url):
    try:
        p = urlsplit(url)
        host = (p.hostname or "").lower().removeprefix("www.")
        port = p.port
        if port == (443 if p.scheme == "https" else 80):
            port = None
        return host, port, unquote(p.path).rstrip("/"), p.query
    except (ValueError, TypeError):
        return None


PROFILE_HOSTS = {"twitter.com": "x.com", "threads.net": "threads.com", "vk.com": "vk.ru"}
CASELESS_ROUTES = {
    "x.com": r"/[^/]+", "instagram.com": r"/[^/]+", "facebook.com": r"/[^/]+",
    "pinterest.com": r"/[^/]+", "twitch.tv": r"/[^/]+", "github.com": r"/[^/]+",
    "youtube.com": r"/@[^/]+", "tiktok.com": r"/@[^/]+", "threads.com": r"/@[^/]+",
    "reddit.com": r"/(?:user|u)/[^/]+(?:/about\.json)?", "snapchat.com": r"/(?:add/|@)[A-Za-z0-9_.-]+",
    "bsky.app": r"/profile/[A-Za-z0-9.-]+", "vk.ru": r"/[A-Za-z0-9_.]+",
    "t.me": r"/[^/]+", "steamcommunity.com": r"/id/[^/]+",
    "deviantart.com": r"/[A-Za-z0-9_-]+", "soundcloud.com": r"/[A-Za-z0-9_-]+",
    "imgur.com": r"/user/[A-Za-z0-9_-]+", "dailymotion.com": r"/(?:user/)?[A-Za-z0-9_-]+",
    "last.fm": r"/user/[A-Za-z0-9_-]+", "letterboxd.com": r"/[A-Za-z0-9_-]+",
    "myanimelist.net": r"/profile/[A-Za-z0-9_-]+", "scratch.mit.edu": r"/users/[A-Za-z0-9_-]+",
    "huggingface.co": r"/[A-Za-z0-9_-]+", "chess.com": r"/member/[A-Za-z0-9_-]+",
    "api.chess.com": r"/pub/player/[A-Za-z0-9_-]+",
    "osu.ppy.sh": r"/users/[A-Za-z0-9_-]+",
    "mastodon.social": r"/@[A-Za-z0-9_]+", "fosstodon.org": r"/@[A-Za-z0-9_]+",
    "dev.to": r"/[A-Za-z0-9_-]+", "hub.docker.com": r"/u/[A-Za-z0-9_-]+",
}


def profile_key(url):
    key = normalized_url(url)
    if key is None:
        return None
    host, port, path, query = key

    if host == "open.spotify.com":
        path = re.sub(r"^/intl-[a-z]{2}(?:-[A-Z]{2})?(?=/user/)", "", path)
        if re.fullmatch(r"/user/[^/]+", path):
            args = tuple(sorted((k, v) for k, v in parse_qsl(query, keep_blank_values=True)
                                if k not in {"si", "nd", "dlsi"} and not k.startswith("utm_")))
            return host, port, path, args
    original_host = host
    host = PROFILE_HOSTS.get(host, host)
    if host.endswith(".pinterest.com"):
        host = "pinterest.com"
    known_route = host in CASELESS_ROUTES and re.fullmatch(CASELESS_ROUTES[host], path, re.I)
    channel_route = host == "youtube.com" and re.fullmatch(r"/channel/UC[A-Za-z0-9_-]{22}", path)
    if not known_route and not channel_route:
        return original_host, port, path, query
    if known_route:
        path = path.casefold()
        if host == "snapchat.com" and path.startswith("/add/"):
            path = "/@" + path[5:]
        if host == "dailymotion.com" and not path.startswith("/user/") and path[1:] not in {"video", "playlist", "search", "login", "signup", "feed", "partner", "studio"}:
            path = "/user" + path

    args = sorted((k, v) for k, v in parse_qsl(query, keep_blank_values=True)
                  if not ((known_route or channel_route) and (k.casefold().startswith("utm_") or k.casefold() in
                  {"fbclid", "gclid", "igsh", "igshid", "si", "s", "t", "feature"})))
    return host, port, path, tuple(args)


def same_profile_url(a, b):
    first, second = normalized_url(a), normalized_url(b)
    if first is None or second is None:
        return False
    if first == second:
        return True
    return profile_key(a) == profile_key(b)


def web_url(value, base=""):
    if not isinstance(value, str) or not value.strip():
        return ""
    try:
        value = urljoin(base, value)
        p = urlsplit(value)
        return value if p.scheme in {"http", "https"} and p.hostname and not p.username else ""
    except ValueError:
        return ""


BLOCK_RE = re.compile(
    r"verify (?:that )?you(?:'re| are) (?:a )?human|checking your browser|"
    r"unusual traffic|access denied|too many requests|just a moment|"
    r"security verification|client challenge|enable javascript and cookies to continue|"
    r"you have been blocked|robot olmadığınızı|güvenlik doğrulaması|"
    r"sign in to confirm|log in to (?:continue|view)|login to (?:continue|view)|"
    r"account (?:is )?(?:temporarily restricted|suspended)|"
    r"not available in your (?:country|region)|unavailable in your (?:country|region)|"
    r"govt\. of india decided to block|devam etmek için giriş", re.I)
MISSING_RE = re.compile(
    r"^(?:404(?:\b.*)?|(?:oops[!,.]?\s*)?(?:page|user|profile|account) "
    r"(?:not found|does not exist|doesn't exist)|this (?:page|user|profile|account) "
    r"(?:does not|doesn't) exist|sayfa bulunamadı|kullanıcı bulunamadı)[.!\s]*$", re.I)
LOGIN_PROMPT_RE = re.compile(r"sign in to confirm|log in to (?:continue|view)|login to (?:continue|view)|devam etmek için giriş", re.I)


def visible_page_labels(page, soup):
    if page.visible_labels is not None:
        return page.visible_labels[:20]
    labels = []
    for node in soup.select('h1, h2, [role="alert"]'):
        hidden = False
        for ancestor in [node, *node.parents]:
            if (ancestor.name in {"template", "noscript"} or ancestor.has_attr("hidden")
                    or ancestor.get("aria-hidden") == "true"
                    or re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)", ancestor.get("style", ""), re.I)):
                hidden = True
                break
        if not hidden:
            labels.append(node.get_text(" ", strip=True))
        if len(labels) >= 20:
            break
    return labels


def gate(page, site, profile_positive=False):

    if page.error:
        return "UNKNOWN", page.error
    if urlsplit(page.final_url).scheme not in {"http", "https"}:
        return "UNKNOWN", "Site bağlantısı kurulamadı; tarayıcı hata sayfası açıldı"
    if page.status in {401, 403, 407, 429, 451}:
        return "UNKNOWN", f"Erişim engeli / giriş gerekli: HTTP {page.status}"
    soup = BeautifulSoup(page.html, "html.parser")
    labels = visible_page_labels(page, soup)
    heading = " ".join(labels[:5])
    block_text = page.title + " " + heading + " " + page.text[:1000]
    if profile_positive:
        block_text = LOGIN_PROMPT_RE.sub("", block_text)
    if BLOCK_RE.search(block_text):
        return "UNKNOWN", page.captcha_note or "Bot kontrolü / erişim engeli"

    widget = soup.select_one('iframe[src*="captcha"], .g-recaptcha, .h-captcha, #challenge-running')
    if page.captcha_active is True or (page.captcha_active is None and widget and not profile_positive):
        return "UNKNOWN", page.captcha_note or "CAPTCHA doğrulanamadı"
    path = urlsplit(page.final_url).path.casefold()
    if re.search(r"/(?:login|log-in|signin|sign-in|auth|authwall|accounts/login)(?:[/.]|$)", path):
        return "UNKNOWN", "Giriş sayfasına yönlendirme"
    if page.status is None and not profile_positive:
        return "UNKNOWN", "Ana belgenin HTTP durumu alınamadı"
    if not same_profile_url(page.requested_url, page.final_url):
        return "UNKNOWN", "Profil adresinden farklı bir adrese yönlendirildi"


    transient = r"(?:something went wrong(?: on [\w .-]+)?|temporarily unavailable|service unavailable|bir şeyler ters gitti)[.!\s]*"
    if any(re.fullmatch(transient, label.strip(), re.I) for label in [page.title, *labels[:5]]):
        return "UNKNOWN", "Site geçici hata ekranı gösterdi; profilin yokluğu doğrulanamadı"
    if page.profile_pending and not profile_positive:
        return "UNKNOWN", "Profil içeriği yüklenemedi; uygulama yükleme ekranında kaldı"
    if page.status in {404, 410}:
        if profile_positive:
            return "UNKNOWN", f"HTTP {page.status} ile profil verisi çelişiyor"
        return "NOT_FOUND", f"Profil adresi HTTP {page.status} döndürdü"
    if page.status is not None and not 200 <= page.status < 300:
        return "UNKNOWN", f"Beklenmeyen HTTP {page.status}"
    if not page.stable and not profile_positive:
        return "UNKNOWN", "DOM kararlı hale gelmedi"
    if not profile_positive and soup.select_one('input[type="password"]') and len(page.text) < 3000:
        return "UNKNOWN", "Giriş formu; doğrulanabilir profil alanı alınamadı"
    if ((urlsplit(page.final_url).hostname or "").removeprefix("www.") == "kick.com"
            and re.fullmatch(r"/[A-Za-z0-9_-]+/?", urlsplit(page.final_url).path)
            and fold(page.title) == "channel not found - kick streaming"):
        if profile_positive:
            return "UNKNOWN", "Bulunamadı başlığı ile profil verisi çelişiyor"
        return "NOT_FOUND", "Kick açıkça kanal bulunamadı yanıtı verdi"
    if ((urlsplit(page.final_url).hostname or "").removeprefix("www.") == "dailymotion.com"
            and re.fullmatch(r"/user/[A-Za-z0-9_-]+/?", urlsplit(page.final_url).path)
            and fold(page.title) == "not found"):
        return ("UNKNOWN", "Bulunamadı başlığı ile profil verisi çelişiyor") if profile_positive else ("NOT_FOUND", "DailyMotion açıkça profil bulunamadı yanıtı verdi")
    for label in [page.title, *labels[:5]]:
        if MISSING_RE.fullmatch(label.strip()):
            if profile_positive:
                return "UNKNOWN", "Bulunamadı başlığı ile profil verisi çelişiyor"
            return "NOT_FOUND", "Görünür bulunamadı başlığı (soft 404)"

    if not profile_positive and not site.get("urlProbe"):
        messages = site.get("errorMsg", [])
        if isinstance(messages, str):
            messages = [messages]
        for message in messages if isinstance(messages, list) else []:
            if not isinstance(message, str):
                continue


            plain = BeautifulSoup(message, "html.parser").get_text(" ", strip=True)
            missing_message = (MISSING_RE.fullmatch(plain.strip()) or
                               re.fullmatch(r"Sorry, nobody on Reddit goes by that name\.?", plain.strip(), re.I))
            error_labels = [page.title, page.text, *labels[:10]]
            if missing_message and any(fold(plain) == fold(label) for label in error_labels):
                return "NOT_FOUND", "Sitenin açık bulunamadı mesajı"
    return None, ""


def extract(page, nick, adapter=None):
    soup = BeautifulSoup(page.html, "html.parser")
    result = Evidence()
    def prefer(current, candidate):

        rank = lambda e: (e.positive, e.strong, len(e.fields), len(e.identity))
        return candidate if rank(candidate) > rank(current) else current

    if adapter:
        for scope in soup.select(adapter.get("root", "body"))[:10]:
            identities = scope.select(adapter["identity"])
            values = [x.get(adapter.get("identity_attribute", ""), "")
                      if adapter.get("identity_attribute") else x.get_text(" ", strip=True)
                      for x in identities]
            if not any(handle(v, nick) for v in values):
                continue
            result.identity.append("site_selector:exact_handle")
            for name, spec in adapter.get("fields", {}).items():
                node = scope.select_one(spec["selector"])
                if node is None:
                    continue
                value = node.get(spec["attribute"], "") if spec.get("attribute") else node.get_text(" ", strip=True)
                if name == "avatar":
                    value = web_url(value, page.final_url)
                elif name in {"followers", "following", "likes", "posts", "subscribers", "repositories"}:
                    if not re.search(r"\d", str(value)):
                        continue
                if str(value).strip():
                    result.fields[name] = str(value).strip()[:800]
            result.sources.append("site_adapter")
            break



    for script in soup.select('script[type="application/ld+json"]')[:30]:
        try:
            data = json.loads(script.string or script.get_text())
        except (ValueError, TypeError):
            continue
        roots = data if isinstance(data, list) else [data]
        expanded = []
        for root in roots:
            if isinstance(root, dict):
                expanded.append(root)
                if isinstance(root.get("@graph"), list):
                    expanded.extend(x for x in root["@graph"] if isinstance(x, dict))
        by_id = {x.get("@id"): x for x in expanded if isinstance(x.get("@id"), str)}
        for root in expanded:
            types = root.get("@type", [])
            types = [types] if isinstance(types, str) else types
            if not isinstance(types, list):
                continue
            person = None
            if "ProfilePage" in types:
                declared = web_url(root.get("url", ""), page.final_url)
                if declared and not same_profile_url(declared, page.final_url):
                    continue
                person = root.get("mainEntity")
                if isinstance(person, dict) and set(person) == {"@id"}:
                    person = by_id.get(person["@id"]) if isinstance(person["@id"], str) else None
            elif "Person" in types and same_profile_url(str(root.get("url", "")), page.final_url):
                person = root
            if not isinstance(person, dict):
                continue
            declared = web_url(person.get("url", ""), page.final_url)
            if declared and not same_profile_url(declared, page.final_url):
                continue
            values = [person.get("alternateName", ""), person.get("name", "")]
            values = [v for x in values for v in (x if isinstance(x, list) else [x])]
            exact = any(isinstance(v, str) and handle(v, nick) for v in values)


            bound = declared or (web_url(root.get("url", ""), page.final_url) if "ProfilePage" in types else "")
            alternate = person.get("alternateName", [])
            alternate = alternate if isinstance(alternate, list) else [alternate]
            conflicting = any(isinstance(v, str) and v.strip() and not handle(v, nick) for v in alternate)
            route_handle = unquote(urlsplit(bound).path).rstrip("/").rsplit("/", 1)[-1].removeprefix("@") if bound else ""
            if bound and not urlsplit(bound).path.strip("/"):
                route_handle = (urlsplit(bound).hostname or "").split(".")[0]
            bound_identity = bool(bound and same_profile_url(bound, page.final_url) and handle(route_handle, nick)
                                  and not conflicting and isinstance(person.get("name"), str) and person["name"].strip())
            if conflicting or (not exact and not bound_identity):
                continue
            candidate = Evidence(identity=["jsonld:exact_handle"])
            candidate.fields["username"] = nick
            if isinstance(person.get("name"), str) and person["name"].strip() and not handle(person["name"], nick):
                candidate.fields["display_name"] = person["name"][:200]
            if isinstance(person.get("description"), str) and person["description"].strip():
                candidate.fields["bio"] = person["description"][:800]
            image = person.get("image", "")
            if isinstance(image, dict):
                image = image.get("url", image.get("contentUrl", ""))
            avatar = web_url(image, page.final_url)
            if avatar:
                candidate.fields["avatar"] = avatar
            stats = person.get("interactionStatistic", root.get("interactionStatistic", []))
            stats = [stats] if isinstance(stats, dict) else stats
            for stat in stats if isinstance(stats, list) else []:
                if not isinstance(stat, dict):
                    continue
                value = stat.get("userInteractionCount")
                kind = str(stat.get("interactionType", ""))
                if isinstance(value, (str, int)) and re.fullmatch(r"\d[\d,.]*", str(value)):
                    key = ("followers" if "Follow" in kind else "likes" if "Like" in kind
                           else "posts" if "Write" in kind else "statistics")
                    candidate.fields.setdefault(key, str(value))
            candidate.sources.append("profile_jsonld")
            result = prefer(result, candidate)

    for scope in soup.select('[itemtype$="schema.org/Person"]')[:10]:
        identity = scope.select_one('[itemprop="alternateName"]')
        url = scope.select_one('[itemprop="url"]')
        if not identity or not handle(identity.get("content", identity.get_text(" ", strip=True)), nick):
            continue
        bound_url = web_url(url.get("href", url.get("content", "")), page.final_url) if url else ""
        if not bound_url or not same_profile_url(bound_url, page.final_url):
            continue
        candidate = Evidence(identity=["microdata:exact_handle"])
        for key, prop, attribute in [("bio", "description", "content"), ("avatar", "image", "src")]:
            node = scope.select_one(f'[itemprop="{prop}"]')
            if node:
                value = node.get(attribute, node.get("content", node.get_text(" ", strip=True)))
                value = web_url(value, page.final_url) if key == "avatar" else value
                if value:
                    candidate.fields.setdefault(key, str(value)[:800])
        candidate.sources.append("profile_microdata")
        result = prefer(result, candidate)

    result.fields["page_title"] = page.title[:500]
    description = soup.select_one('meta[name="description"], meta[property="og:description"]')
    if description:
        result.fields["page_description"] = description.get("content", "")[:800]
    return result


def object_json(text):
    if not isinstance(text, str) or len(text) > 3000000:
        return {}
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else {}
    except (ValueError, RecursionError):
        return {}


def embedded_json(page, name):
    value = page.native_data.get(name) if isinstance(page.native_data, dict) else None
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return object_json(value)
    decoder = json.JSONDecoder()
    for script in BeautifulSoup(page.html, "html.parser").select("script")[:120]:
        raw = script.string or script.get_text()
        if len(raw) > 3000000:
            continue
        match = re.search(r'(?:\b' + re.escape(name) + r'|window\["' + re.escape(name) + r'"\])\s*=\s*', raw)
        if match:
            try:
                value, _ = decoder.raw_decode(raw[match.end():].lstrip())
                return value if isinstance(value, dict) else {}
            except (ValueError, RecursionError):
                pass
    return {}


def metadata_evidence(page, nick):
    soup = BeautifulSoup(page.html, "html.parser")
    def meta(name):
        node = soup.select_one(f'meta[property="{name}"], meta[name="{name}"]')
        return node.get("content", "") if node else ""
    declared = meta("og:url")
    canonical = soup.select_one('link[rel="canonical"]')
    declared = declared or (canonical.get("href", "") if canonical else "")
    if declared and not same_profile_url(declared, page.final_url):
        return Evidence()
    username, title, description = meta("profile:username"), meta("og:title") or page.title, meta("og:description") or meta("description")
    if username and not handle(username, nick):
        return Evidence()
    host = (urlsplit(page.final_url).hostname or "").removeprefix("www.")
    host = PROFILE_HOSTS.get(host, host)
    if host.endswith(".pinterest.com"):
        host = "pinterest.com"
    path = unquote(urlsplit(page.final_url).path).rstrip("/")
    route_exact = host in CASELESS_ROUTES and re.fullmatch(CASELESS_ROUTES[host], path, re.I) and handle(path.rsplit("/", 1)[-1], nick)
    exact = bool(declared and username and handle(username, nick))
    display_name = ""
    if declared and meta("og:type").casefold() == "profile":


        route = unquote(urlsplit(declared).path).rstrip("/").rsplit("/", 1)[-1]
        if not urlsplit(declared).path.strip("/"):
            route = (urlsplit(declared).hostname or "").split(".")[0]
        exact = exact or handle(route, nick)
        display_name = " ".join(x for x in (meta("profile:first_name"), meta("profile:last_name")) if x).strip()
    patterns = {
        "instagram.com": r"^(.+?)\s*\(@([^()\s]+)\)\s*[•|\-].*Instagram",
        "facebook.com": r"^(.+?)\s*\(@([^()\s]+)\)\s*[•|\-].*Facebook",
        "threads.com": r"^(.+?)\s*\(@([^()\s]+)\)\s*[•|\-].*Threads",
        "pinterest.com": r"^(.+?)\s*\(([^()\s]+)\)\s*-\s*Profile\s*\|\s*Pinterest",
        "snapchat.com": r"^(.+?)\s*\(@([^()\s]+)\)\s*\|\s*Snapchat(?:\s|$)",
    }
    if host in patterns and route_exact:


        for label in (page.title, title):
            match = re.search(patterns[host], label, re.I)
            if match and handle(match[2], nick):
                exact, display_name = True, match[1].strip()
                break
    if host == "twitch.tv":
        exact = bool(route_exact and title.casefold().endswith(" - twitch") and handle(title[:-9], nick))

        if re.search(r"streams live on Twitch|Check out their videos|world.s leading video platform", description, re.I):
            description = ""
    if not exact:
        return Evidence()
    fields = {"username": username or nick}
    if display_name and not handle(display_name, nick):
        fields["display_name"] = display_name[:200]
    avatar = web_url(meta("og:image"))
    if any(part in avatar.casefold() for part in ("twitch_logo", "default_open_graph", "static-metadata", "/favicon", "404_user", "default_avatar")):
        avatar = ""
    if avatar:
        fields["avatar"] = avatar
    if description and host != "twitch.tv":
        fields["bio"] = description[:800]
    elif description and (declared or avatar):
        fields["bio"] = description[:800]
    return Evidence(["profile_metadata:exact_handle"], fields, ["profile_metadata"])


def telegram_evidence(page, nick):

    if not same_profile_url(page.final_url, "https://t.me/" + quote(nick, safe="")):
        return Evidence()
    soup = BeautifulSoup(page.html, "html.parser")
    scope = soup.select_one(".tgme_page")
    if scope is None:
        return Evidence()
    links = scope.select('.tgme_page_action a[href^="tg://resolve?"], '
                         'a.tgme_action_button_new[href^="tg://resolve?"], '
                         'a.tgme_action_button[href^="tg://resolve?"]')
    domains = [parse_qs(urlsplit(link.get("href", "")).query).get("domain", [""])[0] for link in links]
    if not domains or any(not handle(domain, nick) for domain in domains):
        return Evidence()

    title = scope.select_one(".tgme_page_title")
    if title is None or not title.get_text(" ", strip=True):
        return Evidence()
    fields = {"username": nick}
    name = title.get_text(" ", strip=True)
    if not handle(name, nick) and not re.search(r"^Telegram|^Contact\s+@", name, re.I):
        fields["display_name"] = name[:200]
    photo = scope.select_one("img.tgme_page_photo_image, .tgme_page_photo img")
    avatar = web_url(photo.get("src", ""), page.final_url) if photo else ""
    if avatar and not re.search(r"(?:telegram_logo|/img/t_logo|/favicon|default_avatar)", avatar, re.I):
        fields["avatar"] = avatar
    description = scope.select_one(".tgme_page_description")
    bio = description.get_text(" ", strip=True) if description else ""
    if bio and not re.search(r"you can contact|if you have Telegram|right away", bio, re.I):
        fields["bio"] = bio[:800]
    extra = scope.select_one(".tgme_page_extra")
    stats = extra.get_text(" ", strip=True) if extra else ""
    if re.search(r"\d[\d ,.]*[KMB]?\s*(?:subscribers|members|monthly users|üye|abone)\b", stats, re.I):
        fields["statistics"] = stats[:200]
    return Evidence(["telegram:exact_handle"], fields, ["telegram:public_profile"])


def bluesky_handle(nick):
    value = nick.removeprefix("@").casefold()
    return value if value.endswith(".bsky.social") else value + ".bsky.social"


def bluesky_api_url(nick):
    return "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=" + quote(bluesky_handle(nick), safe="")


def valid_did(value):
    return isinstance(value, str) and bool(re.fullmatch(r"did:plc:[a-z2-7]{24}|did:web:[a-zA-Z0-9.-]+(?:%3[Aa][0-9]+)?", value))


def bluesky_evidence(page, nick, api=False):
    username = bluesky_handle(nick)
    if api:
        data = object_json(page.text) or object_json(BeautifulSoup(page.html, "html.parser").get_text())
        if data.get("error") or not handle(data.get("handle", ""), username) or not valid_did(data.get("did")):
            return Evidence()
        fields = {"username": data["handle"], "account_id": data["did"]}
        for key, target in (("displayName", "display_name"), ("description", "bio"), ("avatar", "avatar")):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                value = web_url(value) if target == "avatar" else value[:800]
                if value:
                    fields[target] = value
        for key, target in (("followersCount", "followers"), ("followsCount", "following"), ("postsCount", "posts")):
            if type(data.get(key)) is int and data[key] >= 0:
                fields[target] = str(data[key])
        return Evidence(["bluesky:exact_handle", "native:account_id"], fields, ["bluesky:public_getProfile"])
    soup = BeautifulSoup(page.html, "html.parser")
    for node in soup.select('link[rel="canonical"], meta[property="og:url"]'):
        declared = node.get("href") or node.get("content")
        if declared and not same_profile_url(declared, page.final_url):
            return Evidence()
    for node in soup.select('meta[property="profile:username"], #bsky_handle'):
        if not handle(node.get("content", node.get_text(" ", strip=True)), username):
            return Evidence()
    result = extract(page, username)
    if not result.positive:
        result = metadata_evidence(page, username)
    if result.positive:
        result.fields["username"] = username

        node = soup.select_one('meta[name="twitter:value1"]')
        label = soup.select_one('meta[name="twitter:label1"]')
        if label and label.get("content") == "Account DID" and node and valid_did(node.get("content")):
            result.fields["account_id"] = node["content"]
        result.sources.append("bluesky:public_profile")
    return result


def roblox_route(url, nick=None):

    try:
        p = urlsplit(url)
        if p.scheme != "https" or p.username or p.port not in {None, 443}:
            return None, ""
        host = (p.hostname or "").removeprefix("www.")
        if host == "roblox.com" and p.path == "/user.aspx" and nick:
            args = parse_qsl(p.query, keep_blank_values=True)
            if len(args) == 1 and args[0][0] == "username" and handle(args[0][1], nick):
                return "lookup", ""
        if p.query:
            return None, ""
        pattern = r"/users/([1-9][0-9]{0,24})/profile/?" if host == "roblox.com" else r"/v1/users/([1-9][0-9]{0,24})/?" if host == "users.roblox.com" else ""
        match = re.fullmatch(pattern, p.path) if pattern else None
        if match:
            return ("profile" if host == "roblox.com" else "api"), match[1]
    except (ValueError, TypeError):
        pass
    return None, ""


def roblox_evidence(page, nick):
    before, before_id = roblox_route(page.requested_url, nick)
    after, identifier = roblox_route(page.final_url, nick)
    if before == after == "api" and before_id == identifier:
        data = object_json(page.text) or object_json(BeautifulSoup(page.html, "html.parser").get_text())
        if (data.get("errors") or type(data.get("id")) is not int or str(data["id"]) != identifier
                or not isinstance(data.get("name"), str) or not handle(data["name"], nick)):
            return Evidence()
        fields = {"username": data["name"], "account_id": identifier}
        for key, target in (("displayName", "display_name"), ("description", "bio")):
            if isinstance(data.get(key), str) and data[key].strip():
                fields[target] = data[key][:800]
        return Evidence(["roblox:exact_handle", "native:account_id"], fields, ["roblox:public_user_record"])
    if after != "profile" or not (before == "lookup" or before == "profile" and before_id == identifier):
        return Evidence()
    soup = BeautifulSoup(page.html, "html.parser")
    for node in soup.select('link[rel="canonical"], meta[property="og:url"]'):
        declared = node.get("href") or node.get("content")
        if declared and not same_profile_url(declared, page.final_url):
            return Evidence()
    title = re.fullmatch(r"(.+?)\s+-\s+Roblox", page.title.strip(), re.I)
    if not title or not handle(title[1], nick):
        return Evidence()

    pattern = (r"^" + re.escape(nick) + r" is one of the millions creating and exploring the endless possibilities of Roblox\. "
               r"Join " + re.escape(nick) + r" on Roblox and explore together!\s*(.+)$")
    for node in soup.select('meta[name="description"], meta[property="og:description"]'):
        match = re.fullmatch(pattern, node.get("content", "").strip(), re.I | re.S)
        if match and match[1].strip():
            return Evidence(["roblox:exact_handle", "native:account_id"],
                            {"username": title[1], "account_id": identifier, "bio": match[1].strip()[:800]},
                            ["roblox:profile_description"])
    return Evidence()


def account_page_evidence(page, nick):





    empty = (Evidence(), False)
    try:
        before, after = urlsplit(page.requested_url), urlsplit(page.final_url)
        if any(p.scheme != "https" or p.username or p.port not in {None, 443} for p in (before, after)):
            return empty
    except ValueError:
        return empty
    host = (after.hostname or "").removeprefix("www.")
    if (before.hostname or "").removeprefix("www.") != host:
        return empty
    routes = {
        "last.fm": "/user/", "letterboxd.com": "/", "myanimelist.net": "/profile/",
        "scratch.mit.edu": "/users/", "huggingface.co": "/", "soundcloud.com": "/",
        "mastodon.social": "/@", "fosstodon.org": "/@", "osu.ppy.sh": "/users/",
        "api.chess.com": "/pub/player/",
    }
    if host not in routes or before.query or after.query:
        return empty
    expected_path = routes[host] + nick
    if not handle(unquote(before.path).rstrip("/"), expected_path):
        return empty
    numeric_redirect = host == "osu.ppy.sh" and re.fullmatch(r"/users/[1-9][0-9]{0,24}/?", after.path)
    if not numeric_redirect and not same_profile_url(page.requested_url, page.final_url):
        return empty
    soup = BeautifulSoup(page.html, "html.parser")
    meta = lambda key: next((str(x.get("content", "")) for x in soup.select('meta[property], meta[name]')
                             if (x.get("property") or x.get("name")) == key), "")
    canonical = soup.select_one('link[rel="canonical"]')
    declared = [meta("og:url"), canonical.get("href", "") if canonical else ""]

    if any(not same_profile_url(web_url(url, page.final_url), page.final_url) for url in declared if url):
        return empty
    fields = {"username": nick}
    identity = [host + ":exact_handle"]
    source = host + ":profile_container"
    proven_redirect = False
    title = re.sub(r"[\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", page.title).strip()

    def text_field(key, value):
        if isinstance(value, str) and value.strip():
            fields[key] = value.strip()[:800]

    def image_field(value):
        value = web_url(value, page.final_url)
        if value:
            fields["avatar"] = value

    def count_field(key, value):
        if type(value) is int and value >= 0:
            fields[key] = str(value)

    def read_nodes(root, mapping):
        for key, selector in mapping.items():
            node = root.select_one(selector)
            if node is None:
                continue
            if key == "avatar":
                image_field(node.get("src") or node.get("data-src"))
            else:
                value = node.get_text(" ", strip=True)
                if key not in {"statistics", "followers", "following", "posts"} or re.search(r"\d", value):
                    text_field(key, value)

    if host == "huggingface.co":
        root = soup.select_one('[data-target="UserProfile"][data-props]')
        data = object_json(root["data-props"]) if root else {}
        user = data.get("u", {})
        if not isinstance(user, dict) or user.get("type") != "user" or not handle(user.get("user", ""), nick):
            return empty
        text_field("display_name", user.get("fullname"))
        image_field(user.get("avatarUrl"))
        for key, target in (("numFollowers", "followers"), ("numFollowingUsers", "following"),
                            ("numModels", "repositories"), ("totalPosts", "posts"), ("numberLikes", "likes")):
            count_field(target, data.get(key))
        source = "huggingface:UserProfile.u"
    elif host == "osu.ppy.sh":
        root = soup.select_one('[data-react="profile-page"][data-initial-data]')
        data = object_json(root["data-initial-data"]) if root else {}
        user = data.get("user", {})
        if (not isinstance(user, dict) or not handle(user.get("username", ""), nick)
                or type(user.get("id")) is not int or user["id"] <= 0
                or user.get("is_deleted") is True or user.get("is_restricted") is True):
            return empty
        if numeric_redirect and after.path.rstrip("/") != "/users/" + str(user["id"]):
            return empty
        fields["account_id"] = str(user["id"])
        image_field(user.get("avatar_url"))
        count_field("followers", user.get("follower_count"))
        count_field("posts", user.get("post_count"))
        profile = user.get("page")
        if isinstance(profile, dict):
            text_field("bio", profile.get("raw"))
        source = "osu:profile-page.user"
        proven_redirect = bool(numeric_redirect)
    elif host == "api.chess.com":
        data = object_json(page.text) or object_json(soup.get_text())
        identifier = data.get("player_id")
        profile = "https://www.chess.com/member/" + nick
        if (type(identifier) is not int or identifier <= 0 or not handle(data.get("username", ""), nick)
                or not same_profile_url(data.get("url", ""), profile) or data.get("error")):
            return empty
        fields["account_id"] = str(identifier)
        image_field(data.get("avatar"))
        text_field("display_name", data.get("name"))
        count_field("followers", data.get("followers"))

        if type(data.get("joined")) is int and data["joined"] > 0:
            fields["statistics"] = "Kayıt zamanı (Unix): " + str(data["joined"])
        source = "chess:public_player_record"
    elif host in {"mastodon.social", "fosstodon.org"}:
        username = meta("profile:username")
        if (not handle(username, nick + "@" + host) or meta("og:type") != "profile"
                or not any(same_profile_url(url, page.final_url) for url in declared if url)):
            return empty

        description = meta("og:description")
        match = re.match(r"^([\d,.]+) Posts?, ([\d,.]+) Following, ([\d,.]+) Followers?\s*·\s*(.*)$", description, re.I | re.S)
        if match:
            fields.update(posts=match[1], following=match[2], followers=match[3])
            text_field("bio", match[4])
        image_field(meta("og:image"))
        source = "mastodon:qualified_profile_metadata"
    elif host == "soundcloud.com":
        data = None
        for script in soup.select("script:not([src])"):
            match = re.search(r"(?:window\.)?__sc_hydration\s*=\s*", script.string or "")
            if match:
                try:
                    data, _ = json.JSONDecoder().raw_decode((script.string or "")[match.end():].lstrip())
                except (ValueError, TypeError, RecursionError):
                    continue
                break
        for item in data if isinstance(data, list) else []:
            user = item.get("data") if isinstance(item, dict) and item.get("hydratable") == "user" else None
            if (not isinstance(user, dict) or user.get("kind") != "user" or type(user.get("id")) is not int
                    or user["id"] <= 0 or not handle(user.get("permalink", ""), nick)
                    or not same_profile_url(user.get("permalink_url", ""), page.final_url)):
                continue
            fields["account_id"] = str(user["id"])
            text_field("display_name", user.get("username"))
            text_field("bio", user.get("description"))
            image_field(user.get("avatar_url"))
            for key, target in (("followers_count", "followers"), ("followings_count", "following"), ("track_count", "posts")):
                count_field(target, user.get(key))
            break
        source = "soundcloud:hydration.user"
    elif host == "scratch.mit.edu":
        root = soup.select_one("#profile-data")
        name = root.select_one(".header-text h2") if root else None
        if name is None or not handle(name.get_text(" ", strip=True), nick):
            return empty
        read_nodes(root, {"avatar": "#profile-avatar img", "bio": "#bio-readonly .overview"})

        match = re.search(r"/get_image/user/([1-9][0-9]*)_", fields.get("avatar", ""))
        if match:
            fields["account_id"] = match[1]
    elif host == "last.fm":
        root = soup.select_one(".header-new, .header--user, .header-user")
        if root is None:
            return empty
        labels = [x.get_text(" ", strip=True) for x in root.select(".header-title, .header-new-title, .header-new-username")]
        titled = re.fullmatch(re.escape(nick) + r"[’']s (?:Music |music )?[Pp]rofile\s*[|–-]\s*Last\.fm", title, re.I)
        if not any(handle(value, nick) for value in labels) and not titled:
            return empty
        read_nodes(root, {"avatar": ".header-new-avatar img, .header-avatar img",
                          "statistics": ".header-metadata, .header-new-metadata",
                          "bio": ".header-new-bio, .user-bio"})
    elif host == "letterboxd.com":
        root = soup.select_one("#profile-header, .profile-header")
        if root is None:
            return empty
        body = soup.body
        owner = root.get("data-person") or (body.get("data-person") if body else "")
        if owner and not handle(owner, nick):
            return empty
        owner_link = any(same_profile_url(web_url(a.get("href"), page.final_url), page.final_url)
                         for a in root.select(".profile-person h1 a, .profile-person-info h1 a, a.avatar"))
        titled = re.fullmatch(re.escape(nick) + r"[’']s profile\s*[•|–-]\s*Letterboxd", title, re.I)
        names = root.select(".profile-person h1, .profile-person-info h1")
        exact_name = any(handle(x.get_text(" ", strip=True), nick) for x in names)
        if not (handle(owner or "", nick) or owner_link or titled or exact_name):
            return empty
        read_nodes(root, {"avatar": ".profile-person .avatar img, .profile-person-info .avatar img, a.avatar img",
                          "statistics": ".profile-stats, .stats", "bio": ".profile-bio, .bio"})

        if any(key in fields for key in ("avatar", "statistics", "bio")):
            read_nodes(root, {"display_name": ".profile-person h1, .profile-person-info h1"})
    elif host == "myanimelist.net":
        root = soup.select_one(".user-profile")
        titled = re.fullmatch(re.escape(nick) + r"[’']s Profile\s*-\s*MyAnimeList\.net", title, re.I)
        if root is None or not titled:
            return empty
        read_nodes(root, {"avatar": ".user-image img", "bio": ".user-about",
                          "statistics": 'a[data-ga-click-type="profile-leftside-reviews"]'})
    evidence = Evidence(identity, fields, [source])
    if fields.get("account_id"):
        evidence.identity.append("native:account_id")
    return (evidence, proven_redirect) if evidence.positive else empty


def spotify_user_route(url):
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname != "open.spotify.com" or parsed.username or parsed.port not in {None, 443}:
            return ""
        path = profile_key(url)[2]
        match = re.fullmatch(r"/user/([^/]+)", path)
        return match[1] if match else ""
    except (ValueError, TypeError):
        return ""


def spotify_response_kind(url, nick, post_data=""):

    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.username or parsed.port not in {None, 443}:
            return ""
        if parsed.hostname == "api.spotify.com" and unquote(parsed.path).rstrip("/") == "/v1/users/" + nick:
            return "web_api"
        if (parsed.hostname == "spclient.wg.spotify.com"
                and unquote(parsed.path).rstrip("/") == "/user-profile-view/v3/profile/" + nick):
            return "profile_view"
        if parsed.hostname != "api-partner.spotify.com" or parsed.path not in {"/pathfinder/v1/query", "/pathfinder/v2/query"}:
            return ""
        args = dict(parse_qsl(parsed.query)) if parsed.query else object_json(post_data)
        variables = args.get("variables", {})
        variables = object_json(variables) if isinstance(variables, str) else variables
        if (args.get("operationName") == "getUser" and isinstance(variables, dict)
                and variables.get("uri") == "spotify:user:" + nick):
            return "graphql"
    except (ValueError, TypeError):
        pass
    return ""


def spotify_evidence(page, nick):
    if not handle(spotify_user_route(page.requested_url), nick) or not handle(spotify_user_route(page.final_url), nick):
        return Evidence()
    soup = BeautifulSoup(page.html, "html.parser")
    for node in soup.select('link[rel="canonical"], meta[property="og:url"]'):
        declared = node.get("href") or node.get("content")
        if declared and not same_profile_url(web_url(declared, page.final_url), page.final_url):
            return Evidence()
    candidates = []
    records = page.native_data.get("spotify_profiles", [])
    for record in records if isinstance(records, list) else []:
        if not isinstance(record, dict):
            continue
        kind = spotify_response_kind(record.get("url", ""), spotify_user_route(page.requested_url), record.get("post_data", ""))
        payload = record.get("payload")
        if not kind or not isinstance(payload, dict) or payload.get("error") or payload.get("errors"):
            continue
        user = payload
        if kind == "graphql":
            data = payload.get("data", {})
            if not isinstance(data, dict):
                continue
            user = data.get("user") or data.get("userV2")
        if not isinstance(user, dict):
            continue
        ids = [user[key] for key in ("id", "username") if isinstance(user.get(key), str) and user[key]]
        uri = user.get("uri")
        if uri is not None:
            if not isinstance(uri, str) or not uri.startswith("spotify:user:"):
                continue
            ids.append(unquote(uri[len("spotify:user:"):]))

        if kind != "profile_view" and not ids:
            continue
        if any(not handle(value, nick) for value in ids):
            continue
        if kind == "profile_view" and not ids and not any(type(user.get(key)) is int and user[key] >= 0
                                                         for key in ("followers_count", "following_count")):
            continue
        if kind == "web_api" and user.get("type") != "user":
            continue
        if kind == "graphql" and user.get("__typename") not in {None, "User"}:
            continue
        external = user.get("external_urls", {})
        if isinstance(external, dict) and external.get("spotify") and not same_profile_url(external["spotify"], page.final_url):
            continue
        fields = {"username": nick, "account_id": ids[0] if ids else spotify_user_route(page.requested_url)}
        for key in ("display_name", "name", "displayName"):
            value = user.get(key)
            if isinstance(value, str) and value.strip():
                fields["display_name"] = value.strip()[:200]
                break
        followers = user.get("followers")
        for key, value in (("followers", user.get("followers_count")), ("following", user.get("following_count")),
                           ("followers", followers.get("total", followers.get("totalCount")) if isinstance(followers, dict) else followers)):
            if type(value) is int and value >= 0:
                fields[key] = str(value)
        images = user.get("images", [])
        avatar = user.get("avatar")
        values = [user.get("image_url"), user.get("avatarUrl")]
        if isinstance(images, list):
            values.extend(item.get("url") for item in images if isinstance(item, dict))
        if isinstance(avatar, dict):
            sources = avatar.get("sources", [])
            if isinstance(sources, list):
                values.extend(item.get("url") for item in sources if isinstance(item, dict))
        for value in values:
            if web_url(value):
                fields["avatar"] = web_url(value)
                break
        candidate = Evidence(["spotify:exact_handle", "native:account_id"], fields, ["spotify:" + kind])
        if candidate.positive:
            candidates.append(candidate)
    if candidates:
        return max(candidates, key=lambda candidate: len(candidate.fields))


    root = soup.select_one('[data-testid="user-profile"], [data-testid="user-page"]')
    if root:
        title = root.select_one('[data-testid="entityTitle"] h1, h1[data-testid="entityTitle"]')
        avatar = root.select_one('[data-testid="user-avatar"] img, [data-testid="entity-image"] img')
        if (title and avatar and web_url(avatar.get("src"))
                and title.get_text(" ", strip=True) in visible_page_labels(page, soup)):
            return Evidence(["spotify:exact_handle"], {"username": nick, "display_name": title.get_text(" ", strip=True),
                            "avatar": web_url(avatar.get("src"))}, ["spotify:owner_header"])
    return Evidence()


def platform_evidence(page, nick, apply_gate=True):
    result = Evidence()
    host = (urlsplit(page.final_url).hostname or "").removeprefix("www.")
    if host == "t.me":
        result = telegram_evidence(page, nick)
    elif host == "youtube.com":
        data = embedded_json(page, "ytInitialData")
        metadata = data.get("metadata", {})
        channel = metadata.get("channelMetadataRenderer", {}) if isinstance(metadata, dict) else {}
        if isinstance(channel, dict):
            urls = [channel.get("vanityChannelUrl", "")]
            if isinstance(channel.get("ownerUrls"), list):
                urls.extend(channel["ownerUrls"])
            expected = "https://www.youtube.com/@" + quote(nick, safe="")
            exact = any(isinstance(url, str) and same_profile_url(url, expected) for url in urls)
            account_id = channel.get("externalId", "")
            by_id = account_id == nick and urlsplit(page.final_url).path.rstrip("/") == "/channel/" + nick
            exact = exact or by_id
            if exact and isinstance(account_id, str) and re.fullmatch(r"UC[A-Za-z0-9_-]{22}", account_id):
                username = nick
                if by_id:
                    for url in urls:
                        if isinstance(url, str) and (urlsplit(url).hostname or "").removeprefix("www.") == "youtube.com" and urlsplit(url).path.startswith("/@"):
                            username = unquote(urlsplit(url).path[2:]).rstrip("/")
                            break
                fields = {"username": username, "account_id": account_id, "display_name": str(channel.get("title", ""))[:200]}
                if isinstance(channel.get("description"), str) and channel["description"].strip():
                    fields["bio"] = channel["description"][:800]
                avatar = channel.get("avatar", {})
                images = avatar.get("thumbnails", []) if isinstance(avatar, dict) else []
                for item in reversed(images if isinstance(images, list) else []):
                    if isinstance(item, dict) and web_url(item.get("url")):
                        fields["avatar"] = web_url(item["url"])
                        break
                result = Evidence(["youtube:exact_handle", "native:account_id"], fields, ["youtube:channelMetadataRenderer"])
    elif host in {"x.com", "twitter.com"}:
        payload = page.native_data.get("twitter_user", {})
        payload = object_json(payload) if isinstance(payload, str) else payload
        data = payload.get("data", {}) if isinstance(payload, dict) else {}
        wrapper = data.get("user", {}) if isinstance(data, dict) else {}
        user = wrapper.get("result", {}) if isinstance(wrapper, dict) else {}
        if isinstance(user, dict) and user.get("__typename") == "User":
            legacy = user.get("legacy") or {}
            core = user.get("core") or {}
            avatar = user.get("avatar") or {}
            if all(isinstance(x, dict) for x in (legacy, core, avatar)):
                username = core.get("screen_name") or legacy.get("screen_name")
                account_id = user.get("rest_id", "")
                if isinstance(username, str) and handle(username, nick) and isinstance(account_id, str) and re.fullmatch(r"[1-9][0-9]{0,24}", account_id):
                    fields = {"username": username, "account_id": account_id}
                    display_name = core.get("name") or legacy.get("name")
                    if isinstance(display_name, str) and display_name.strip():
                        fields["display_name"] = display_name.strip()[:200]
                    image = web_url(avatar.get("image_url") or legacy.get("profile_image_url_https"))
                    if image:
                        fields["avatar"] = image
                    for key, target in {"followers_count": "followers", "friends_count": "following", "statuses_count": "posts"}.items():
                        if type(legacy.get(key)) is int and legacy[key] >= 0:
                            fields[target] = str(legacy[key])
                    bio = user.get("profile_bio") or {}
                    description = legacy.get("description") or (bio.get("description", "") if isinstance(bio, dict) else "")
                    if isinstance(description, str) and description.strip():
                        fields["bio"] = description[:800]
                    result = Evidence(["twitter:exact_handle", "native:account_id"], fields, ["twitter:UserByScreenName"])
    elif host == "twitch.tv":

        responses = page.native_data.get("twitch_users", [])
        for payload in responses if isinstance(responses, list) else []:
            data = payload.get("data", {}) if isinstance(payload, dict) else {}
            user = data.get("user", {}) if isinstance(data, dict) else {}
            if not isinstance(user, dict) or not handle(user.get("login", ""), nick):
                continue
            identifier = user.get("id", "")
            if not isinstance(identifier, str) or not re.fullmatch(r"[1-9][0-9]{0,24}", identifier):
                continue
            fields = {"username": user["login"], "account_id": identifier}
            for source, target in (("displayName", "display_name"), ("description", "bio"), ("profileImageURL", "avatar")):
                value = user.get(source)
                if isinstance(value, str) and value.strip():
                    value = web_url(value) if target == "avatar" else value[:800]
                    if value:
                        fields[target] = value
            count = user.get("followers", {})
            if isinstance(count, dict) and type(count.get("totalCount")) is int and count["totalCount"] >= 0:
                fields["followers"] = str(count["totalCount"])
            candidate = Evidence(["twitch:exact_handle", "native:account_id"], fields, ["twitch:public_user_response"])
            if candidate.positive:
                result = candidate
                break
    if not result.positive:
        result = metadata_evidence(page, nick)
    if not result.positive or (apply_gate and gate(page, {}, profile_positive=True)[0]):
        return Evidence()
    return result


def native_profile_kind(url, nick):

    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.username or parsed.port not in {None, 443}:
            return None
        host, path = parsed.hostname, unquote(parsed.path).rstrip("/")
        if host == "public.api.bsky.app" and path == "/xrpc/app.bsky.actor.getProfile":
            if parse_qsl(parsed.query, keep_blank_values=True) == [("actor", bluesky_handle(nick))]:
                return "Bluesky API"
        if parsed.query:
            return None
        if host == "bsky.app" and handle(path, "/profile/" + bluesky_handle(nick)):
            return "Bluesky"
        if host in {"www.tiktok.com", "tiktok.com"} and path.startswith("/@") and handle(path[2:], nick):
            return "TikTok"
        if host in {"www.reddit.com", "reddit.com"} and path.startswith("/user/"):
            username = path[6:].removesuffix("/about.json")
            if handle(username, nick):
                return "Reddit"
    except ValueError:
        pass
    return None


def native_evidence(page, nick, apply_gate=True):
    result = _native_evidence_raw(page, nick)
    if apply_gate and gate(replace(page, stable=True), {})[0]:
        return Evidence()
    return result


def _native_evidence_raw(page, nick):

    kind = native_profile_kind(page.requested_url, nick)
    result = Evidence()
    if not kind or native_profile_kind(page.final_url, nick) != kind:
        return result
    if kind == "Reddit" and (urlsplit(page.requested_url).path.rstrip("/").endswith("/about.json")
                             != urlsplit(page.final_url).path.rstrip("/").endswith("/about.json")):
        return result



    soup = BeautifulSoup(page.html, "html.parser")
    if kind in {"Bluesky", "Bluesky API"}:
        result = bluesky_evidence(page, nick, api=kind == "Bluesky API")
        if not result.positive:
            return Evidence()
        return result
    if kind == "TikTok":
        candidates = []
        scripts = {s.get("id"): s.string or s.get_text() for s in
                   soup.select('script#__UNIVERSAL_DATA_FOR_REHYDRATION__, script#SIGI_STATE')[:4]}
        for key in ("__UNIVERSAL_DATA_FOR_REHYDRATION__", "SIGI_STATE"):
            if isinstance(page.native_data, dict) and isinstance(page.native_data.get(key), str):
                scripts[key] = page.native_data[key]
        for key, raw in scripts.items():
            data = object_json(raw) or object_json(html.unescape(raw))
            if key == "__UNIVERSAL_DATA_FOR_REHYDRATION__":
                scope = data.get("__DEFAULT_SCOPE__", {})
                detail = scope.get("webapp.user-detail", {}) if isinstance(scope, dict) else {}
                if not isinstance(detail, dict) or ("statusCode" in detail and
                        (type(detail["statusCode"]) is not int or detail["statusCode"] != 0)):
                    continue
                info = detail.get("userInfo", {})
                candidates.append((info, "tiktok:user-detail"))
            else:
                user_page, module = data.get("UserPage", {}), data.get("UserModule", {})
                if not isinstance(user_page, dict) or type(user_page.get("statusCode")) is not int or user_page["statusCode"] != 0 or not isinstance(module, dict):
                    continue
                users, stats = module.get("users", {}), module.get("stats", {})
                if not isinstance(users, dict) or not isinstance(stats, dict):
                    continue
                for key, user in users.items():
                    if handle(key, nick):
                        candidates.append(({"user": user, "stats": stats.get(key, {})}, "tiktok:UserModule"))
        valid = []
        for info, source in candidates:
            if not isinstance(info, dict):
                continue
            user, stats = info.get("user", {}), info.get("stats", {})
            stats_v2 = info.get("statsV2", {})
            if not isinstance(user, dict) or not isinstance(stats, dict):
                continue
            account_id = str(user.get("id", ""))
            if (not isinstance(user.get("uniqueId"), str) or not handle(user["uniqueId"], nick)
                    or not re.fullmatch(r"[1-9][0-9]{0,24}", account_id)):
                continue
            fields = {"account_id": account_id, "username": user["uniqueId"]}
            if isinstance(user.get("nickname"), str) and user["nickname"].strip():
                fields["display_name"] = user["nickname"].strip()[:200]
            for key, name in {"followerCount": "followers", "followingCount": "following",
                              "videoCount": "posts", "heartCount": "likes"}.items():
                value = stats.get(key)
                if value is None and isinstance(stats_v2, dict):
                    value = stats_v2.get(key)
                if isinstance(value, str) and re.fullmatch(r"[0-9]{1,16}", value):
                    value = int(value)
                if type(value) is int and 0 <= value <= 10**15:
                    fields[name] = str(value)
            avatar = web_url(user.get("avatarLarger") or user.get("avatarMedium") or user.get("avatarThumb"))
            if avatar:
                fields["avatar"] = avatar
            if isinstance(user.get("signature"), str) and user["signature"].strip():
                fields["bio"] = user["signature"].strip()[:800]
            if type(user.get("privateAccount")) is bool:
                fields["private_account"] = user["privateAccount"]
            evidence = Evidence(["native:exact_handle", "native:account_id"], fields, [source])
            if evidence.positive:
                valid.append(evidence)
        if valid and len({e.fields["account_id"] for e in valid}) == 1:
            return max(valid, key=lambda e: len(e.fields))
    elif kind == "Reddit" and urlsplit(page.requested_url).path.rstrip("/").endswith("/about.json"):
        data = object_json(page.text)
        if not data:
            nodes = soup.select("pre")
            if len(nodes) == 1:
                data = object_json(nodes[0].get_text())
        user = data.get("data", {})
        if (data.get("kind") != "t2" or not isinstance(user, dict)
                or not isinstance(user.get("name"), str) or not handle(user["name"], nick)
                or not isinstance(user.get("id"), str) or not re.fullmatch(r"[0-9a-z]{1,20}", user["id"])
                or int(user["id"], 36) == 0 or user.get("is_suspended") is True):
            return result

        if not all(type(user.get(k)) is int and abs(user[k]) <= 10**15 for k in ("link_karma", "comment_karma")):
            return result
        created = user.get("created_utc")
        if type(created) not in {int, float} or not 0 < created <= time.time() + 86400:
            return result
        fields = {"account_id": user["id"], "username": user["name"],
                  "link_karma": user["link_karma"], "comment_karma": user["comment_karma"],
                  "created_utc": created}
        avatar = web_url(user.get("icon_img"))
        if avatar:
            fields["avatar"] = avatar
        profile = user.get("subreddit", {})
        if isinstance(profile, dict) and isinstance(profile.get("public_description"), str) and profile["public_description"].strip():
            fields["bio"] = profile["public_description"].strip()[:800]
        return Evidence(["native:exact_handle", "native:account_id"], fields, ["reddit:user-about"])
    return result


def fingerprint(page, names):
    soup = BeautifulSoup(page.html, "html.parser")
    for node in soup.select("script, style, nav, header, footer, noscript"):
        node.decompose()
    text = fold(soup.get_text(" ", strip=True))
    for name in sorted(names, key=len, reverse=True):
        text = re.sub(re.escape(fold(name)), "<handle>", text)
    text = re.sub(r"\b\d+\b", "<n>", text)
    return re.sub(r"\s+", " ", text)[:20000]


def decide(page, site, nick, evidence, controls=()):

    state, reason = gate(page, site, profile_positive=evidence.positive)
    if state:
        return state, reason
    if not evidence.positive:
        return "UNKNOWN", "Tam nickname ve en az bir profil alanı alınamadı"
    return "VERIFIED", "Tam nickname ve en az bir profil alanı bulundu"




import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import urldefrag



def parse_chrome_major(text):
    match = re.search(r"\b(\d{2,3})\.\d+\.\d+\.\d+\b", str(text))
    return int(match.group(1)) if match else None


def windows_file_major(path):

    import ctypes
    from ctypes import wintypes

    class FixedFileInfo(ctypes.Structure):
        _fields_ = [(name, wintypes.DWORD) for name in (
            "signature", "struct_version", "file_ms", "file_ls", "product_ms",
            "product_ls", "flags_mask", "flags", "os", "type", "subtype",
            "date_ms", "date_ls")]

    dll = ctypes.WinDLL("version", use_last_error=True)
    dll.GetFileVersionInfoSizeW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
    dll.GetFileVersionInfoSizeW.restype = wintypes.DWORD
    dll.GetFileVersionInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p]
    dll.GetFileVersionInfoW.restype = wintypes.BOOL
    dll.VerQueryValueW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR,
                                 ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.UINT)]
    dll.VerQueryValueW.restype = wintypes.BOOL
    size = dll.GetFileVersionInfoSizeW(str(path), None)
    if not size:
        return None
    data = ctypes.create_string_buffer(size)
    if not dll.GetFileVersionInfoW(str(path), 0, size, data):
        return None
    ptr, length = ctypes.c_void_p(), wintypes.UINT()
    if not dll.VerQueryValueW(data, "\\", ctypes.byref(ptr), ctypes.byref(length)):
        return None
    if length.value < ctypes.sizeof(FixedFileInfo):
        return None
    info = ctypes.cast(ptr, ctypes.POINTER(FixedFileInfo)).contents
    if info.signature != 0xFEEF04BD:
        return None
    return info.file_ms >> 16 or None


def detect_chrome_major(path):
    if os.name == "nt":
        try:
            return windows_file_major(path)
        except (OSError, AttributeError, ValueError):
            return None
    try:
        result = subprocess.run([str(path), "--version"], capture_output=True,
                                text=True, timeout=5, check=False)
        return parse_chrome_major(result.stdout + result.stderr)
    except (OSError, subprocess.SubprocessError):
        return None


CHROME_START_LOCK = threading.Lock()


class ChromeStartupError(RuntimeError):
    pass


class ChromeProcess:

    def __init__(self, profile):
        self.profile = Path(profile)
        self.process = None
        self.log = None
        self.windows = os.name == "nt"
        self.endpoint = None
        self.command = []
        self.last_pid = None
        self.last_code = None

    def launch(self, args, **kwargs):
        if self.process is not None:
            raise RuntimeError("Bu işçinin Chrome işlemi zaten başlatıldı")
        self.log = (self.profile / "browser-process.log").open("ab", buffering=0)
        kwargs.update(stdin=subprocess.DEVNULL, stdout=self.log, stderr=subprocess.STDOUT,
                      close_fds=True)
        env = dict(kwargs.get("env", os.environ))
        env["CHROME_LOG_FILE"] = str(self.profile / "chrome_debug.log")
        kwargs["env"] = env
        self.command = list(args)
        if self.windows:
            kwargs["creationflags"] = kwargs.get("creationflags", 0) | subprocess.CREATE_NO_WINDOW
        else:
            kwargs["start_new_session"] = True
        try:
            self.process = subprocess.Popen(args, **kwargs)
            self.last_pid = self.process.pid
            return self.process
        except BaseException:
            self.log.close()
            self.log = None
            raise

    def close(self):
        process = self.process
        try:
            if process is not None:


                if process.poll() == 0 and self.endpoint:
                    try:
                        from websocket import create_connection
                        with create_connection(self.endpoint, timeout=2, suppress_origin=True,
                                               http_no_proxy=["127.0.0.1", "localhost", "::1"]) as connection:
                            connection.send(json.dumps({"id": 1, "method": "Browser.close"}))
                            try:
                                connection.recv()
                            except Exception:
                                pass  
                    except Exception:
                        pass
                if process.poll() is None:
                    if self.windows:

                        taskkill = str(Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "taskkill.exe")
                        try:
                            subprocess.run([taskkill, "/PID", str(process.pid), "/T", "/F"],
                                           stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL, timeout=8, check=False,
                                           creationflags=subprocess.CREATE_NO_WINDOW)
                        except (OSError, subprocess.SubprocessError):
                            pass
                    else:
                        try:
                            import signal
                            os.killpg(process.pid, signal.SIGTERM)
                        except (ProcessLookupError, PermissionError):
                            pass
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        if not self.windows:
                            try:
                                import signal
                                os.killpg(process.pid, signal.SIGKILL)
                            except (ProcessLookupError, PermissionError):
                                pass
                        process.kill()
                        process.wait(timeout=3)
                else:
                    process.wait(timeout=1)
                self.last_code = process.returncode
                self.process = None
        finally:
            if self.log is not None:
                self.log.close()
                self.log = None


@contextmanager
def managed_uc_launch(uc, owner):



    original = uc.subprocess
    class ProcessFacade:
        def __getattr__(self, name):
            return getattr(original, name)
        def Popen(self, args, **kwargs):
            return owner.launch(args, **kwargs)
    uc.subprocess = ProcessFacade()
    try:
        yield
    finally:
        uc.subprocess = original


def wait_for_chrome(address, timeout=45, stop=None, owner=None):

    parsed = urlsplit("http://" + str(address))
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"} or (not parsed.port and owner is None):
        raise ValueError("Chrome hata ayıklama adresi yerel olmalı")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + timeout
    clean_exit_at = None
    while time.monotonic() < deadline:
        check_cancel(stop)
        expected_path = None
        if owner is not None:
            process = owner.process
            if process is None:
                raise ChromeStartupError("Chrome işlemi oluşturulamadı")
            code = process.poll()
            if code not in (None, 0):
                raise ChromeStartupError(f"Chrome bağlantı kurulmadan kapandı (çıkış kodu: {code})")
            if code == 0:
                if clean_exit_at is None:
                    clean_exit_at = time.monotonic()
                elif time.monotonic() - clean_exit_at >= min(8, timeout):
                    raise ChromeStartupError("Chrome 0 koduyla kapandı; bu profile ait çalışan tarayıcı bağlantısı bulunamadı")
            try:

                with (owner.profile / "DevToolsActivePort").open(encoding="utf-8") as stream:
                    lines = stream.read(4096).splitlines()
                port = int(lines[0])
                if not 0 < port < 65536 or not lines[1].startswith("/devtools/browser/"):
                    raise ValueError("invalid DevToolsActivePort")
                expected_path = lines[1]
                address = f"127.0.0.1:{port}"
            except (OSError, ValueError, IndexError):
                pause(.25, stop)
                continue
        try:
            with opener.open(f"http://{address}/json/version", timeout=min(2, max(.1, deadline - time.monotonic()))) as response:
                data = json.loads(response.read(65536))
            websocket = urlsplit(str(data.get("webSocketDebuggerUrl", ""))) if isinstance(data, dict) else None
            target = urlsplit("http://" + address)
            if (websocket and websocket.scheme == "ws"
                    and websocket.hostname in {"127.0.0.1", "localhost", "::1"}
                    and websocket.port == target.port
                    and (expected_path is None or websocket.path == expected_path)):
                if owner is not None:
                    owner.endpoint = str(data["webSocketDebuggerUrl"])
                return address
        except (OSError, ValueError):
            pass
        pause(.25, stop)
    raise TimeoutError(f"Chrome {timeout:g} saniyede hazır olmadı (chrome not reachable)")


def short_error(exc):
    return str(exc).split("Stacktrace:", 1)[0].split("; For documentation", 1)[0].strip()[:1200]


def dead_session(exc):
    from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException
    from urllib3.exceptions import HTTPError
    return isinstance(exc, (InvalidSessionIdException, NoSuchWindowException, HTTPError)) or bool(re.search(
        r"invalid session id|chrome not reachable|disconnected|tab crashed|session deleted|not connected to DevTools|target window already closed",
        str(exc), re.I))


def safe_chrome_class(base):
    class SafeChrome(base):
        def __init__(self, *args, **kwargs):

            self.debug = False
            self._nickscan_closed = False
            self._nickscan_stop = kwargs.pop("nickscan_stop", None)
            self._nickscan_timeout = kwargs.pop("nickscan_timeout", 45)
            self._nickscan_owner = kwargs.pop("nickscan_owner", None)
            try:
                super().__init__(*args, **kwargs)
            except BaseException:
                try:
                    self.quit()
                except Exception:
                    pass
                raise

        def start_session(self, capabilities=None, browser_profile=None):

            if self._nickscan_owner is None:
                wait_for_chrome(self.options.debugger_address, self._nickscan_timeout, self._nickscan_stop)
            else:
                address = wait_for_chrome(self.options.debugger_address, self._nickscan_timeout,
                                          self._nickscan_stop, owner=self._nickscan_owner)
                self.options.debugger_address = address
                if capabilities is not None:
                    capabilities.setdefault("goog:chromeOptions", {})["debuggerAddress"] = address
            return super().start_session(capabilities, browser_profile)

        def quit(self):
            if getattr(self, "_nickscan_closed", False):
                return
            self._nickscan_closed = True
            owner = getattr(self, "_nickscan_owner", None)
            service_process = getattr(getattr(self, "service", None), "process", None)
            try:
                if owner is not None:
                    owner.close()

                    self.__dict__.pop("browser_pid", None)
                super().quit()
            except OSError as exc:
                if getattr(exc, "winerror", None) != 6:
                    raise
            finally:
                if service_process is not None:
                    try:
                        if service_process.poll() is None:
                            service_process.kill()
                        service_process.wait(timeout=3)
                    except (OSError, subprocess.SubprocessError):
                        pass
                executor = getattr(self, "command_executor", None)
                if executor is not None:
                    try:
                        executor.close()
                    except Exception:
                        pass

        def __del__(self):

            try:
                self.quit()
            except Exception:
                pass

        @classmethod
        def _ensure_close(cls, instance):
            try:
                instance.quit()
            except Exception:
                pass

    return SafeChrome


def document_status(events, frame_id, final_url, loader_id=None):

    found = None
    for entry in events:
        try:
            msg = json.loads(entry["message"])["message"]
            p = msg["params"]
            if (msg["method"] == "Network.responseReceived"
                    and p.get("type") == "Document"
                    and p.get("frameId") == frame_id
                    and (not loader_id or p.get("loaderId") == loader_id)
                    and urldefrag(p["response"]["url"])[0] == urldefrag(final_url)[0]):
                found = int(p["response"]["status"])
        except (KeyError, TypeError, ValueError):
            continue
    return found


class CancelledScan(Exception):
    pass


def check_cancel(stop):
    if stop is not None and stop.is_set():
        raise CancelledScan()


def pause(seconds, stop=None):
    if stop is None:
        time.sleep(seconds)
    elif stop.wait(seconds):
        raise CancelledScan()


@contextmanager
def interruptible_lock(lock, stop):
    while not lock.acquire(timeout=0.2):
        check_cancel(stop)
    try:
        check_cancel(stop)
        yield
    finally:
        lock.release()


class HostLimiter:

    def __init__(self, delay, stop):
        self.delay, self.stop = delay, stop
        self.guard = threading.Lock()
        self.hosts = {}

    @contextmanager
    def slot(self, url):
        host = (urlsplit(url).hostname or "").lower().removeprefix("www.")
        with self.guard:
            state = self.hosts.setdefault(host, [threading.Lock(), 0.0])
        with interruptible_lock(state[0], self.stop):
            pause(max(0, state[1] - time.monotonic()), self.stop)
            try:
                yield
            finally:
                state[1] = time.monotonic() + self.delay


class DriverPool:

    def __init__(self, stop, source=None):
        self.stop, self.source = stop, source
        self.directory = tempfile.TemporaryDirectory(prefix="nickscan_drivers_")
        self.root = Path(self.directory.name)
        self.lock = threading.Lock()
        self.templates = {}
        self.copies = {}

    def _read_url(self, url, max_bytes):
        check_cancel(self.stop)
        deadline = time.monotonic() + 90
        data = bytearray()
        with urllib.request.urlopen(url, timeout=30) as response:
            while True:
                check_cancel(self.stop)
                if time.monotonic() > deadline:
                    raise TimeoutError("Sürücü indirme toplam süresi aşıldı")
                chunk = response.read(65536)
                if not chunk:
                    break
                data.extend(chunk)
                if len(data) > max_bytes:
                    raise ValueError("Sürücü indirme boyutu sınırı aşıldı")
        return bytes(data)

    def _prepare(self, major):
        destination = self.root / f"template_{major}{'.exe' if os.name == 'nt' else ''}"
        if self.source:
            shutil.copy2(self.source, destination)
            return destination
        if major < 115:
            raise ValueError("Chrome 115 veya daha yeni bir sürüm gerekli")
        machine = platform.machine().lower()
        if os.name == "nt":
            target = "win64" if machine in {"amd64", "x86_64", "arm64"} else "win32"
        elif sys.platform == "darwin":
            target = "mac-arm64" if machine in {"arm64", "aarch64"} else "mac-x64"
        else:
            target = "linux-arm64" if machine in {"arm64", "aarch64"} else "linux64"
        manifest_url = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"
        manifest = json.loads(self._read_url(manifest_url, 4000000))
        release = manifest.get("milestones", {}).get(str(major))
        if not release or parse_chrome_major(release.get("version")) != major:
            raise RuntimeError(f"Chrome {major} için resmi sürücü bulunamadı")
        entries = release.get("downloads", {}).get("chromedriver", [])
        download = next((x["url"] for x in entries if x.get("platform") == target), None)
        parsed = urlsplit(download or "")
        if (parsed.scheme != "https" or parsed.hostname != "storage.googleapis.com"
                or not parsed.path.startswith("/chrome-for-testing-public/") or parsed.username):
            raise RuntimeError("Geçerli resmi ChromeDriver indirme adresi bulunamadı")
        blob = self._read_url(download, 60000000)
        binary = "chromedriver.exe" if os.name == "nt" else "chromedriver"
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            entry = next((i for i in archive.infolist() if i.filename.split("/")[-1] == binary), None)
            if entry is None or entry.file_size > 100000000:
                raise RuntimeError("ChromeDriver arşivi geçersiz")
            destination.write_bytes(archive.read(entry))
        destination.chmod(0o755)
        return destination

    def get(self, major, worker):
        with interruptible_lock(self.lock, self.stop):
            key = (major, worker)
            if key not in self.copies or not Path(self.copies[key]).is_file():
                if major not in self.templates or not self.templates[major].is_file():
                    self.templates[major] = self._prepare(major)
                path = self.root / f"worker_{worker}_{major}{'.exe' if os.name == 'nt' else ''}"
                shutil.copy2(self.templates[major], path)
                self.copies[key] = str(path)
            return self.copies[key]

    def close(self):
        try:
            self.directory.cleanup()
        except OSError:

            pass


class BrowserRuntime:

    MANIFEST = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

    def __init__(self, stop, mode="auto", notify=None, cache=None):
        self.stop, self.mode, self.notify = stop, mode, notify
        parent = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".cache")
        self.cache = Path(cache) if cache is not None else parent / "NicknameOSINT" / "browser"
        self.lock = threading.Lock()
        self.config = None
        self.pool = None
        self.failure = None

    @staticmethod
    def target():
        machine = platform.machine().lower()
        if os.name == "nt":
            return "win64" if machine in {"amd64", "x86_64", "arm64", "aarch64"} else "win32"
        if sys.platform.startswith("linux") and machine in {"amd64", "x86_64"}:
            return "linux64"
        raise ChromeStartupError("Otomatik Chrome paketi bu platformda desteklenmiyor; --chrome ile kurulu tarayıcıyı seç")

    def cached(self):
        try:
            marker = self.cache / "current.json"
            if marker.stat().st_size > 4096:
                return None
            data = json.loads(marker.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return None
            target = self.target()
            if (data.get("platform") != target or not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", data.get("version", ""))
                    or not re.fullmatch(r"[0-9a-zA-Z_.-]+", data.get("directory", ""))):
                return None
            root = (self.cache / data["directory"]).resolve()
            if root.parent != self.cache.resolve():
                return None
            ext = ".exe" if target.startswith("win") else ""
            chrome = root / f"chrome-{target}" / ("chrome" + ext)
            driver = root / f"chromedriver-{target}" / ("chromedriver" + ext)
            if not chrome.is_file() or not driver.is_file() or not chrome.stat().st_size or not driver.stat().st_size:
                return None
            return dict(chrome=str(chrome), driver=str(driver), version=data["version"])
        except (OSError, TypeError, ValueError, ChromeStartupError):
            return None

    def preferred(self):
        return self.mode == "managed" or self.config is not None or self.cached() is not None

    def say(self, message):
        if self.notify:
            self.notify(message)

    def _download(self, url, destination, max_bytes):
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        total, announced = 0, 0
        deadline = time.monotonic() + 600
        check_cancel(self.stop)
        with opener.open(url, timeout=30) as response, Path(destination).open("wb") as stream:
            while True:
                check_cancel(self.stop)
                if time.monotonic() >= deadline:
                    raise TimeoutError("Chrome indirme süresi aşıldı")
                data = response.read(1024 * 1024)
                if not data:
                    break
                total += len(data)
                if total > max_bytes:
                    raise ValueError("Resmi tarayıcı indirmesi boyut sınırını aştı")
                stream.write(data)
                if total - announced >= 32 * 1024 * 1024:
                    announced = total
                    self.say(f"Tarayıcı paketi indiriliyor: {total // (1024 * 1024)} MB")

    def _unpack(self, archive_path, root, prefix):
        with zipfile.ZipFile(archive_path) as archive:
            entries = archive.infolist()
            if len(entries) > 10000 or sum(x.file_size for x in entries) > 1500000000:
                raise ValueError("Tarayıcı arşivi boyut sınırını aştı")
            for entry in entries:
                check_cancel(self.stop)
                name = entry.filename
                parts = name.rstrip("/").split("/")
                if (not parts or parts[0] != prefix or any(p in {"", ".", ".."} for p in parts)
                        or "\\" in name or ":" in name or (entry.external_attr >> 16) & 0o170000 == 0o120000):
                    raise ValueError("Tarayıcı arşivinde geçersiz dosya yolu")
                destination = Path(root).joinpath(*parts)
                if entry.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(entry) as src, destination.open("wb") as out:
                        shutil.copyfileobj(src, out, length=1024 * 1024)
                    if entry.external_attr >> 16 & 0o111:
                        destination.chmod(0o755)

    def get(self):
        with interruptible_lock(self.lock, self.stop):
            if self.config is not None:
                return self.config
            if self.failure:
                raise ChromeStartupError(self.failure)
            try:
                config = self.cached()
                if config is None:
                    self.say("Resmi Chrome for Testing ve aynı sürümde ChromeDriver hazırlanıyor; ilk indirme yaklaşık 200–300 MB olabilir.")
                    self.cache.mkdir(parents=True, exist_ok=True)
                    with tempfile.TemporaryDirectory(prefix="download_", dir=self.cache) as work:
                        staging = Path(work)
                        manifest = staging / "manifest.json"
                        self._download(self.MANIFEST, manifest, 4000000)
                        release = json.loads(manifest.read_text(encoding="utf-8"))["channels"]["Stable"]
                        version, target = release["version"], self.target()
                        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", version):
                            raise ValueError("Resmi tarayıcı sürüm bilgisi geçersiz")
                        bundle = staging / "bundle"
                        bundle.mkdir()
                        for kind in ("chrome", "chromedriver"):
                            check_cancel(self.stop)
                            expected = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/{target}/{kind}-{target}.zip"
                            entry = next((x for x in release["downloads"][kind] if x.get("platform") == target), None)
                            if not entry or entry.get("url") != expected:
                                raise ValueError("Geçerli resmi tarayıcı indirme adresi bulunamadı")
                            archive = staging / (kind + ".zip")
                            self._download(expected, archive, 400000000 if kind == "chrome" else 60000000)
                            self._unpack(archive, bundle, kind + "-" + target)
                        ext = ".exe" if target.startswith("win") else ""
                        for kind in ("chrome", "chromedriver"):
                            executable = bundle / f"{kind}-{target}" / (kind + ext)
                            if not executable.is_file() or not executable.stat().st_size:
                                raise ValueError("Tarayıcı paketi eksik")
                            executable.chmod(0o755)
                        for helper in ("chrome_crashpad_handler", "chrome_sandbox"):
                            executable = bundle / f"chrome-{target}" / helper
                            if executable.is_file():
                                executable.chmod(0o755)
                        check_cancel(self.stop)
                        name = version + "-" + target + "-" + secrets.token_hex(4)
                        os.replace(bundle, self.cache / name)
                        marker = staging / "current.json"
                        marker.write_text(json.dumps(dict(version=version, platform=target, directory=name)), encoding="utf-8")
                        os.replace(marker, self.cache / "current.json")
                        config = self.cached()
                        if config is None:
                            raise ValueError("İndirilen tarayıcı paketi doğrulanamadı")
                self.pool = DriverPool(self.stop, config["driver"])
                self.config = config
                self.say(f"Programın Chrome for Testing {config['version']} tarayıcısı hazır.")
                return config
            except CancelledScan:
                raise
            except Exception as exc:
                self.failure = "Programın ayrı Chrome paketi hazırlanamadı: " + short_error(exc)
                raise ChromeStartupError(self.failure) from exc

    def close(self):
        if self.pool is not None:
            self.pool.close()


CAPTCHA_HOOK = r"""
(() => {
  window.__nickscanWidgets = [];
  let ticks = 0;
  const timer = setInterval(() => {
    for (const [name, type] of [['turnstile','TurnstileTaskProxyless'], ['grecaptcha','RecaptchaV2TaskProxyless']]) {
      const api = window[name];
      if (!api || typeof api.render !== 'function' || api.render.__nickscanWrapped) continue;
      const original = api.render;
      function wrapped(container, options) {
        if (options && options.sitekey) {
          window.__nickscanWidgets.push({type, websiteKey: options.sitekey,
            action: options.action, data: options.cData, pagedata: options.chlPageData,
            callback: options.callback, container});
        }
        return Reflect.apply(original, this, arguments);
      }
      wrapped.__nickscanWrapped = true;
      api.render = wrapped;
    }
    if (++ticks >= 800) clearInterval(timer);
  }, 25);
})();
"""

CAPTCHA_DETECT = r"""
const visible = node => { if (!node) return false; const r = node.getBoundingClientRect();
  const s = getComputedStyle(node); return r.width > 20 && r.height > 20 && s.display !== 'none' && s.visibility !== 'hidden'; };
const text = (document.body?.innerText || '').slice(0,2000);
const challenge = /verify.*human|security verification|just a moment|checking your browser|robot olmad|güvenlik doğrulaması/i.test(document.title+' '+text);
const solved = Array.from(document.querySelectorAll('[name="g-recaptcha-response"], [name="cf-turnstile-response"]')).some(n => n.value);
if (solved) return {active:challenge, task:null};
const widgets = window.__nickscanWidgets || [];
let task = null;
for (const node of document.querySelectorAll('.g-recaptcha[data-sitekey], .cf-turnstile[data-sitekey]')) {
  if (!visible(node) && !challenge) continue;
  const key = node.getAttribute('data-sitekey');
  const type = node.classList.contains('cf-turnstile') ? 'TurnstileTaskProxyless' : 'RecaptchaV2TaskProxyless';
  const captured = widgets.find(w => w.websiteKey === key);
  task = {type, websiteKey:key, websiteURL:location.href};
  if (captured) for (const key of ['action','data','pagedata']) if (captured[key]) task[key] = captured[key];
  if (type === 'RecaptchaV2TaskProxyless' && node.getAttribute('data-size') === 'invisible') task.isInvisible = true;
  break;
}
if (!task && challenge && widgets.length) {
  const w = widgets[widgets.length-1];
  task = {type:w.type, websiteKey:w.websiteKey, websiteURL:location.href};
  for (const key of ['action','data','pagedata']) if (w[key]) task[key] = w[key];
}
if (!task) for (const frame of document.querySelectorAll('iframe[src]')) {
  if (!visible(frame)) continue;
  try { const u = new URL(frame.src);
    if ((u.hostname.endsWith('.google.com') || u.hostname === 'www.recaptcha.net') && /\/recaptcha\/api2\/anchor/.test(u.pathname) && u.searchParams.get('k')) {
      task = {type:'RecaptchaV2TaskProxyless', websiteKey:u.searchParams.get('k'), websiteURL:location.href}; break;
    }
  } catch (_) {}
}
const active = challenge || !!task || Array.from(document.querySelectorAll('iframe[src*="captcha"], .h-captcha, #challenge-running'))
  .some(node => visible(node) && node.getBoundingClientRect().height > 80);
return {active, task};
"""

CAPTCHA_APPLY = r"""
const [token, key] = arguments;
const widgets = (window.__nickscanWidgets || []).filter(w => w.websiteKey === key);
let callbacks = 0;
for (const name of ['g-recaptcha-response','cf-turnstile-response']) {
  for (const field of document.querySelectorAll('[name="'+name+'"]')) {
    field.value = token; field.dispatchEvent(new Event('input',{bubbles:true}));
    field.dispatchEvent(new Event('change',{bubbles:true}));
  }
}
for (const widget of widgets) if (typeof widget.callback === 'function') { widget.callback(token); callbacks++; }
if (!callbacks) for (const node of document.querySelectorAll('[data-sitekey][data-callback]')) {
  if (node.getAttribute('data-sitekey') !== key) continue;
  const name = node.getAttribute('data-callback');
  if (!/^[A-Za-z_$][\w$]*(\.[A-Za-z_$][\w$]*)*$/.test(name)) continue;
  let fn = window; for (const part of name.split('.')) fn = fn && fn[part];
  if (typeof fn === 'function') { fn(token); callbacks++; }
}

return callbacks;
"""


class CaptchaSolver:

    def __init__(self, key="", limit=10, stop=None):
        self.key, self.limit, self.stop = key.strip(), limit, stop
        self.used, self.seen, self.disabled = 0, set(), False
        self.lock = threading.Lock()

    def _post(self, method, payload):
        check_cancel(self.stop)
        request = urllib.request.Request("https://api.2captcha.com/" + method,
            data=json.dumps({"clientKey": self.key, **payload}).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request, timeout=20) as response:
            data = response.read(262145)
        if len(data) > 262144:
            raise ValueError("Çözüm servisi yanıtı çok büyük")
        data = json.loads(data)
        if not isinstance(data, dict):
            raise ValueError("Çözüm servisi yanıtı geçersiz")
        return data

    def solve(self, task):
        if not self.key:
            return None, "CAPTCHA için NICKSCAN_2CAPTCHA_KEY ve servis bakiyesi gerekli"
        if not isinstance(task, dict) or task.get("type") not in {"RecaptchaV2TaskProxyless", "TurnstileTaskProxyless"}:
            return None, "Bu CAPTCHA türü otomatik çözüm bağlantısında desteklenmiyor"
        if not web_url(task.get("websiteURL")) or not isinstance(task.get("websiteKey"), str) or not task["websiteKey"]:
            return None, "CAPTCHA parametreleri alınamadı"
        key = (task["websiteURL"], task["websiteKey"])
        with self.lock:
            if self.disabled:
                return None, "CAPTCHA servisi anahtar veya bakiye hatası nedeniyle durduruldu"
            if key in self.seen:
                return None, "Bu sayfanın CAPTCHA çözümü daha önce denendi"
            if self.used >= self.limit:
                return None, "Tarama için CAPTCHA çözüm sınırına ulaşıldı"
            self.used += 1
            self.seen.add(key)
        try:
            data = self._post("createTask", {"task": task})
            task_id = data.get("taskId")
            deadline = time.monotonic() + 120
            while not data.get("errorId"):
                if data.get("status") == "ready":
                    solution = data.get("solution", {})
                    if isinstance(solution, dict) and (solution.get("gRecaptchaResponse") or solution.get("token")):
                        return solution, "CAPTCHA çözümü alındı"
                    return None, "CAPTCHA servisi geçerli çözüm döndürmedi"
                if type(task_id) is not int or time.monotonic() >= deadline:
                    return None, "CAPTCHA çözümü zamanında tamamlanamadı"
                pause(5, self.stop)
                data = self._post("getTaskResult", {"taskId": task_id})
            code = str(data.get("errorCode", "ERROR_UNKNOWN"))
            if code in {"ERROR_KEY_DOES_NOT_EXIST", "ERROR_KEY_INVALID", "ERROR_ZERO_BALANCE", "ERROR_WRONG_USER_KEY"}:
                with self.lock:
                    self.disabled = True
            return None, "CAPTCHA servisi: " + (code if re.fullmatch(r"[A-Z0-9_]{1,80}", code) else "Hata")
        except CancelledScan:
            raise
        except (OSError, ValueError, KeyError):
            return None, "CAPTCHA çözüm servisine bağlanılamadı"


PAGE_SNAPSHOT = r"""
    const visible = e => {
        if (!e || !e.getClientRects().length || e.closest('[hidden], [aria-hidden="true"]')) return false;
        const s = getComputedStyle(e);
        return s.display !== 'none' && s.visibility !== 'hidden';
    };
    const labels = [...document.querySelectorAll('h1,h2,[role="alert"]')]
        .filter(visible).slice(0,20).map(e => e.innerText.trim());
    const terminal = labels.some(s => /^(?:404\b|(?:page|user|profile|account) not found|something went wrong|access denied|just a moment)/i.test(s));
    const busy = [...document.querySelectorAll('[aria-busy="true"],[role="progressbar"]:not([aria-valuenow]):not([aria-valuetext]),[data-testid="loading-spinner"],[data-testid="loading-indicator"]')].some(visible);
    const spotifyShell = location.hostname === 'open.spotify.com' && /\/(?:user)\/[^/]+\/?$/.test(location.pathname)
        && ![...document.querySelectorAll('[data-testid="entityTitle"], [data-testid="user-profile"] h1, [data-testid="user-page"] h1')].some(visible)
        && /spotify.*web player/i.test(document.title);
    return {url: location.href, title: document.title,
        text: document.body ? document.body.innerText.slice(0,300000) : '',
        ready: document.readyState, visibleLabels: labels,
        profilePending: !terminal && (busy || spotifyShell)};
"""


class Browser:
    def __init__(self, timeout=30, settle=4, chrome=None, version=None,
                 visible=False, driver=None, pool=None, worker=0, limiter=None, stop=None,
                 startup_timeout=45, diagnostics=None, captcha_solver=None,
                 other_accounts=True, other_limit=5, runtime=None, web_search_budget=None):
        self.timeout = timeout
        self.settle = settle
        self.chrome = chrome
        self.version = version
        self.visible = visible
        self.driver_path = driver
        self.driver = None
        self.visits = 0
        self.pool, self.worker, self.limiter, self.stop = pool, worker, limiter, stop
        self.startup_timeout, self.diagnostics = startup_timeout, diagnostics
        self._profile = None
        self._process = None
        self._executable = None
        self._major = None
        self.runtime = runtime
        self._managed = False
        self.captcha_solver = captcha_solver
        self.other_accounts, self.other_limit = other_accounts, other_limit
        self.web_search_budget = web_search_budget

    def start(self):
        if self.driver is not None:
            return

        with interruptible_lock(CHROME_START_LOCK, self.stop):
            try:
                if self._process is not None:
                    self.close()
                    if self._process is not None:
                        raise ChromeStartupError("Önceki Chrome işlemi kapatılamadı; yeni işlem başlatılmadı")
                if self.runtime is not None and self.runtime.preferred():
                    self._select_runtime()
                try:
                    self._start()
                except ChromeStartupError:
                    if self.runtime is None or self._managed:
                        raise
                    self.close()
                    if self._process is not None:
                        raise
                    self.runtime.say("Kurulu Chrome açılamadı; programın ayrı Chrome paketine geçiliyor.")
                    self._select_runtime()
                    self._start()
            except BaseException:
                self.close()
                raise

    def _select_runtime(self):
        config = self.runtime.get()
        self._executable = config["chrome"]
        self.pool = self.runtime.pool
        self._managed = True

    def _start(self):
        check_cancel(self.stop)
        import undetected_chromedriver as uc
        from selenium.common.exceptions import WebDriverException
        from urllib3.exceptions import HTTPError

        executable = self._executable or self.chrome or uc.find_chrome_executable()
        if not executable or not Path(executable).is_file():
            raise ChromeStartupError("Chrome bulunamadı. Chrome kur veya --chrome ile chrome.exe yolunu belirt.")
        executable = str(Path(executable).resolve())
        self._executable = executable
        detected = detect_chrome_major(executable)
        if self._managed:
            managed_major = parse_chrome_major(self.runtime.config["version"])
            if detected and detected != managed_major:
                raise ChromeStartupError("Programın önbellekteki Chrome sürümü kayıtla uyuşmuyor")
            detected = detected or managed_major
        if self.version and detected and self.version != detected:
            raise ValueError(f"--chrome-version {self.version}, seçili Chrome {detected} ile uyuşmuyor. Parametreyi kaldır.")
        major = self.version or detected
        if not major:
            raise ChromeStartupError("Chrome sürümü okunamadı. chrome://version değerine göre --chrome-version 153 gibi belirt.")
        driver_class = safe_chrome_class(uc.Chrome)
        for attempt in range(2):
            check_cancel(self.stop)
            self._major = major
            self._profile = Path(tempfile.mkdtemp(prefix=f"nickscan_T{self.worker}_"))
            self._process = ChromeProcess(self._profile)
            options = self._options(uc)
            options.add_argument("--enable-logging")
            options.add_argument(f"--log-file={self._profile / 'chrome_debug.log'}")
            if attempt and not self.visible:
                options.add_argument("--disable-gpu")
            kwargs = dict(options=options, headless=not self.visible,
                          use_subprocess=True, version_main=major,
                          browser_executable_path=executable,
                          user_data_dir=str(self._profile),
                          nickscan_stop=self.stop, nickscan_timeout=self.startup_timeout,
                          nickscan_owner=self._process,
                          no_sandbox=bool(hasattr(os, "geteuid") and os.geteuid() == 0))
            if self.pool:
                kwargs["driver_executable_path"] = self.pool.get(major, self.worker)
            elif self.driver_path:
                kwargs["driver_executable_path"] = self.driver_path
            try:
                with managed_uc_launch(uc, self._process):
                    self.driver = driver_class(**kwargs)
                break
            except (WebDriverException, ChromeStartupError, OSError, HTTPError) as exc:
                self._startup_diagnostic(executable, major, attempt, exc)
                self.close()
                if self._process is not None:
                    raise ChromeStartupError("Önceki Chrome işlemi kapatılamadı; yeniden başlatma durduruldu") from exc
                message = str(exc)
                current = re.search(r"Current browser version is\s+(\d+)", message, re.I)

                if (attempt == 0 and not self.version and not self.driver_path
                        and not self._managed and current and int(current.group(1)) != major):
                    major = int(current.group(1))
                    continue
                if self.driver_path and current:
                    raise RuntimeError("Elle seçilen ChromeDriver tarayıcıya uymuyor. --driver parametresini kaldır.") from exc
                transient = (isinstance(exc, (ChromeStartupError, TimeoutError, HTTPError)) or
                             re.search(r"cannot connect to chrome|chrome not reachable|DevToolsActivePort|Chrome.*hazır olmadı|disconnected|failed to start", message, re.I))
                if attempt == 0 and transient:
                    pause(1, self.stop)
                    continue
                detail = (" Ayrıntı: index.html içindeki Tarayıcı günlüğü" if callable(self.diagnostics) else f" Ayrıntı: {self.diagnostics}") if self.diagnostics else ""
                hint = (" --show-browser ile açılışı görebilir, --startup-timeout 90 ile süreyi artırabilirsin."
                        if isinstance(exc, TimeoutError) else " Ayrıntılı hata için index.html dosyasını paylaş.")
                raise ChromeStartupError("Chrome oturumu başlatılamadı: " + short_error(exc) + detail + hint) from exc
        try:
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.set_script_timeout(self.timeout)
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
            self.driver.execute_cdp_cmd("Network.setBypassServiceWorker", {"bypass": True})
            self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
                "headers": {"Accept-Language": "en-US,en;q=0.9"}})
            self.driver.execute_cdp_cmd("Browser.setDownloadBehavior", {"behavior": "deny"})
            if self.captcha_solver and self.captcha_solver.key:
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": CAPTCHA_HOOK})
            self.visits = 0
        except BaseException:
            self.close()
            raise

    def _startup_diagnostic(self, executable, major, attempt, exc, phase="açılış"):
        if not self.diagnostics:
            return
        try:
            detail = []
            for name in ("chrome_debug.log", "browser-process.log"):
                log = self._profile / name if self._profile else None
                if log and log.is_file():
                    with log.open("rb") as stream:
                        stream.seek(max(0, log.stat().st_size - 8000))
                        detail.append(name + ":\n" + stream.read(8000).decode("utf-8", errors="replace"))
            process = self._process.process if self._process else None
            process_info = (f"PID={process.pid} çıkış={process.poll()}" if process else
                            f"PID={self._process.last_pid} çıkış={self._process.last_code}" if self._process else "işlem bilgisi yok")
            command = subprocess.list2cmdline(self._process.command) if self._process else ""
            message = (f"\n{stamp()} T{self.worker} Chrome={major} headless={not self.visible} aşama={phase} deneme={attempt + 1}\n"
                       f"Dosya: {executable}\nBaşlatma: {command}\n{process_info}\n{type(exc).__name__}: {short_error(exc)}\nChrome günlüğü:\n"
                       + ("\n".join(detail) or "(günlük üretilemedi)") + "\n")
            if callable(self.diagnostics):
                self.diagnostics(message)
            else:
                with Path(self.diagnostics).open("a", encoding="utf-8") as stream:
                    stream.write(message)
        except OSError:
            pass  

    def _options(self, uc):
        options = uc.ChromeOptions()

        options.debugger_address = "127.0.0.1:0"


        options._ignore_local_proxy = True
        options.page_load_strategy = "eager"
        options.add_argument("--no-proxy-server")
        options.add_argument("--lang=en-US")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-mode")
        if sys.platform.startswith("linux"):
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-quic")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("about:blank")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "download_restrictions": 3,
        })
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        return options

    def visit(self, url):
        check_cancel(self.stop)
        if self.limiter:
            with self.limiter.slot(url):
                return self._visit_recovering(url)
        return self._visit_recovering(url)

    def _visit_recovering(self, url):
        page = self._visit_with_captcha(url)
        if page.session_lost:

            check_cancel(self.stop)
            self.close()
            pause(1, self.stop)
            return self._visit_with_captcha(url)
        return page

    def _visit_with_captcha(self, url):
        page = self._visit(url)
        if not page.captcha_active or not self.captcha_solver or self.driver is None:
            return page
        try:
            detected = self.driver.execute_script(CAPTCHA_DETECT) or {}
            task = detected.get("task")
            solution, note = self.captcha_solver.solve(task)
            page.captcha_note = note
            if not solution:
                return page

            if self.driver.current_url != task["websiteURL"]:
                page.captcha_note = "CAPTCHA sayfası çözüm beklenirken değişti"
                return page
            if isinstance(solution.get("userAgent"), str) and task["type"] == "TurnstileTaskProxyless":
                self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": solution["userAgent"]})
            token = solution.get("gRecaptchaResponse") or solution.get("token")
            callbacks = self.driver.execute_script(CAPTCHA_APPLY, token, task["websiteKey"])
            pause(1, self.stop)
            page = self._visit(url, navigate=False)
            if page.captcha_active:
                page.captcha_note = ("CAPTCHA çözümü site tarafından kabul edilmedi" if callbacks
                                     else "CAPTCHA çözümü alındı; sitenin tamamlama işlevine erişilemedi")
            return page
        except CancelledScan:
            raise
        except Exception:
            page.captcha_note = "CAPTCHA çözümü sayfaya uygulanamadı"
            return page

    def _visit(self, url, navigate=True):
        from selenium.common.exceptions import TimeoutException, WebDriverException
        from urllib3.exceptions import HTTPError
        if self.driver is None:
            self.start()
        d = self.driver
        page = Page(url, url, None)
        self.visits += 1
        original = None
        try:
            original = d.current_window_handle

            events = []
            if navigate:
                d.get("about:blank")
                d.get_log("performance")
                d.get(url)
            start = time.monotonic()
            last = None
            unchanged_since = start
            page.stable = False
            deadline = max(self.settle + 5, 8)
            while time.monotonic() - start < deadline:
                check_cancel(self.stop)
                d.switch_to.window(original)
                snapshot = d.execute_script(PAGE_SNAPSHOT)
                if snapshot.get("profilePending"):
                    deadline = max(deadline, 15)
                try:
                    events.extend(d.get_log("performance"))
                    events = events[-5000:]
                except WebDriverException:
                    pass
                signature = hashlib.sha256((snapshot["url"] + snapshot["text"]).encode()).digest()
                now = time.monotonic()
                if signature != last:
                    unchanged_since = now
                    last = signature
                if (now - start >= self.settle and now - unchanged_since >= 1.5 and snapshot["ready"] == "complete"
                        and not snapshot.get("profilePending")):
                    page.stable = True
                    break
                pause(0.5, self.stop)

            final = d.execute_script("const snapshot = (() => {" + PAGE_SNAPSHOT + "})();" + """
                const native = Object.fromEntries(['__UNIVERSAL_DATA_FOR_REHYDRATION__', 'SIGI_STATE']
                    .map(id => [id, document.getElementById(id)])
                    .filter(([id, node]) => node)
                    .map(([id, node]) => [id, node.textContent.slice(0,3000000)]));
                if (window.ytInitialData) { try { native.ytInitialData = JSON.stringify(window.ytInitialData).slice(0,3000000); } catch (_) {} }
                return {...snapshot,
                  html: document.documentElement.outerHTML.slice(0,3000000),
                  navigationStatus: performance.getEntriesByType('navigation')[0]?.responseStatus || null,
                  native};
            """)
            page.native_data = final.get("native", {})
            page.visible_labels = final.get("visibleLabels")
            page.profile_pending = bool(final.get("profilePending"))
            if final["url"] != snapshot["url"] or final["text"] != snapshot["text"]:
                page.stable = False
            page.final_url, page.title = final["url"], final["title"]
            page.text, page.html = final["text"], final["html"]
            try:
                frame = d.execute_cdp_cmd("Page.getFrameTree", {})["frameTree"]["frame"]
                events.extend(d.get_log("performance"))
                page.status = document_status(events, frame["id"], page.final_url, frame.get("loaderId"))
            except WebDriverException:
                pass
            navigation_status = final.get("navigationStatus")
            if page.status is None and type(navigation_status) is int and 100 <= navigation_status <= 599:
                page.status = navigation_status
            if urlsplit(page.final_url).scheme not in {"http", "https"}:
                code = re.search(r"(?:net::)?ERR_[A-Z_0-9]+", page.text)
                page.error = "Site bağlantısı kurulamadı" + (f" ({code.group(0)})" if code else "; tarayıcı hata sayfası açıldı")
            self._capture_public_responses(page, events)
            detected = d.execute_script(CAPTCHA_DETECT)
            if isinstance(detected, dict):
                page.captcha_active = bool(detected.get("active"))

        except TimeoutException:
            page.error = "Sayfa yükleme zaman aşımı (yok olarak yorumlanmadı)"
            try:
                d.execute_script("window.stop()")
                if navigate:
                    return self._visit(url, navigate=False)
            except (WebDriverException, HTTPError) as exc:
                if dead_session(exc):
                    page.session_lost = True
                    self._startup_diagnostic(self._executable, self._major, 0, exc, phase="oturum")
                    self.close()
        except WebDriverException as exc:
            code = re.search(r"net::ERR_[A-Z_0-9]+", str(exc))
            page.error = f"Site bağlantısı kurulamadı ({code.group(0)})" if code else f"Tarayıcı hatası: {short_error(exc)}"

            if dead_session(exc):
                page.session_lost = True
                self._startup_diagnostic(self._executable, self._major, 0, exc, phase="oturum")
                self.close()
        except HTTPError as exc:
            page.error = f"Tarayıcı bağlantısı koptu: {type(exc).__name__}"
            page.session_lost = True
            self._startup_diagnostic(self._executable, self._major, 0, exc, phase="oturum")
            self.close()
        finally:
            if self.driver is not None and original is not None:
                try:
                    for tab in d.window_handles:
                        if tab != original:
                            d.switch_to.window(tab)
                            d.close()
                    d.switch_to.window(original)
                except (WebDriverException, HTTPError):
                    if page.error:
                        page.session_lost = True
                    self.close()
        return page

    def _capture_public_responses(self, page, events):
        host = (urlsplit(page.final_url).hostname or "").removeprefix("www.")
        if host not in {"x.com", "twitter.com", "twitch.tv", "open.spotify.com"}:
            return
        spotify_nick = spotify_user_route(page.requested_url) if host == "open.spotify.com" else ""
        requests = {}
        if spotify_nick:
            for entry in events:
                try:
                    message = json.loads(entry["message"])["message"]
                    if message.get("method") == "Network.requestWillBeSent":
                        params = message["params"]
                        body = params.get("request", {}).get("postData", "")
                        if (isinstance(body, str) and len(body) <= 30000
                                and spotify_response_kind(params.get("request", {}).get("url", ""), spotify_nick, body)):
                            requests[params["requestId"]] = body
                except (ValueError, KeyError, TypeError):
                    continue
        captured = set()
        for entry in reversed(events):
            try:
                message = json.loads(entry["message"])["message"]
                params = message["params"]
                response = params.get("response", {})
                parsed = urlsplit(response.get("url", ""))
                twitter = (host in {"x.com", "twitter.com"} and parsed.hostname in
                           {"x.com", "api.x.com", "twitter.com", "api.twitter.com"} and parsed.path.endswith("/UserByScreenName"))
                twitch = host == "twitch.tv" and parsed.hostname == "gql.twitch.tv" and parsed.path == "/gql"
                post_data = requests.get(params.get("requestId"), "")
                spotify = spotify_nick and spotify_response_kind(response.get("url", ""), spotify_nick, post_data)
                if (message["method"] != "Network.responseReceived" or response.get("status") != 200
                        or not (twitter or twitch or spotify) or params.get("requestId") in captured):
                    continue
                if len(captured) >= 30:
                    return
                captured.add(params["requestId"])
                body = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": params["requestId"]})
                if body.get("base64Encoded") and len(body.get("body", "")) <= 700000:
                    import base64
                    body = {"body": base64.b64decode(body["body"], validate=True).decode("utf-8")}
                if not body.get("base64Encoded") and len(body.get("body", "")) <= 500000:
                    if spotify:
                        payload = object_json(body["body"])
                        if payload:
                            page.native_data.setdefault("spotify_profiles", []).append(
                                {"url": response["url"], "post_data": post_data, "payload": payload})
                        if len(captured) >= 20:
                            return
                        continue
                    if twitter:
                        page.native_data["twitter_user"] = object_json(body["body"])
                        return
                    payload = json.loads(body["body"])
                    for item in payload if isinstance(payload, list) else [payload]:
                        if isinstance(item, dict):
                            data = item.get("data", {})
                            if isinstance(data, dict) and isinstance(data.get("user"), dict):
                                page.native_data.setdefault("twitch_users", []).append({"data": {"user": data["user"]}})
                    if len(page.native_data.get("twitch_users", [])) >= 20 or len(captured) >= 30:
                        return
            except Exception:
                continue

    def close(self):
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
        if self._process is not None:
            try:
                self._process.close()
            except (OSError, subprocess.SubprocessError) as exc:
                self._startup_diagnostic(self._executable, self.version, 0, exc)
                return  
            self._process = None
        if self._profile is not None:
            for attempt in range(5):
                try:
                    shutil.rmtree(self._profile)
                    break
                except FileNotFoundError:
                    break
                except OSError:

                    if attempt < 4:
                        time.sleep(.1)
            self._profile = None




import argparse
import csv
import hashlib
import html
import json
import re
import secrets
import string
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parent
VERSION = "1.15.0"
DEFAULT_WORKERS = 5
MAX_SITES = 200


POPULAR_SITE_ORDER = (
    "YouTube", "Twitter", "Instagram", "Facebook", "TikTok", "Reddit",
    "Twitch", "LinkedIn", "Pinterest", "Snapchat", "Telegram", "threads",
    "Bluesky", "GitHub", "Steam Community (User)", "Roblox", "Spotify",
    "VK", "tumblr", "Kick", "SoundCloud", "Medium", "Patreon",
    "Linktree", "GitLab", "Vimeo", "DailyMotion", "Rumble", "Flickr",
    "Imgur", "DeviantArt", "Behance", "ArtStation", "Dribbble", "Wattpad",
    "Substack", "WordPress", "Blogger", "mastodon.social", "Gravatar",
    "BuyMeACoffee", "kofi", "Bandcamp", "last.fm", "MyAnimeList", "Anilist",
    "Letterboxd", "GoodReads", "Trakt", "TheMovieDB", "Fandom",
    "Wikipedia", "Archive.org", "9GAG", "Chess", "Lichess", "Duolingo",
    "Strava", "TradingView", "Hugging Face", "Kaggle", "HackerRank",
    "LeetCode", "Codeforces", "Codewars", "Codechef", "Atcoder", "DEV Community",
    "HackerNews", "Replit.com", "Codepen", "CodeSandbox",
    "freecodecamp", "Codecademy", "Docker Hub", "npm", "PyPi", "BitBucket",
    "SourceForge", "Codeberg", "Gitea", "Gitee", "GitBook", "HackMD",
    "Hashnode", "ProductHunt", "Open Collective", "OpenStreetMap",
    "Unsplash", "VSCO", "Sketchfab", "Newgrounds", "Itch.io",
    "Scratch", "osu!", "Speedrun.com", "Xbox Gamertag", "PSNProfiles.com",
    "FortniteTracker", "Minecraft", "CurseForge",
    "Wowhead", "Steam Community (Group)", "GameFAQs", "Gamespot", "Giant Bomb",
    "Kongregate", "Ninja Kiwi", "NintendoLife", "Pokemon Showdown", "TETR.IO",
    "Warframe Market", "Star Citizen", "Nightbot", "BoardGameGeek", "Sporcle",
    "HackTheBox", "TryHackMe", "HackerOne", "BugCrowd", "Intigriti",
    "HackenProof (Hackers)", "CyberDefenders", "PentesterLab", "CryptoHack",
    "VirusTotal", "Pastebin", "Keybase", "About.me", "AllMyLinks", "Carrd",
    "Gumroad", "Redbubble", "Cults3D", "MyMiniFactory", "CGTrader", "BOOTH",
    "Instructables", "Hackaday", "hackster", "Arduino Forum", "Freelancer",
    "ResearchGate", "Academia.edu", "Credly", "Launchpad", "Packagist",
    "RubyGems", "WordPressOrg", "Python.org Discussions", "CloudflareCommunity",
    "BraveCommunity", "Jupyter Community Forum", "n8n Community", "Nextcloud Forum",
    "Joplin Forum", "Caddy Community", "Cryptomator Forum", "Bitwarden Forum",
    "Wakatime", "Topcoder", "HackerEarth", "Coders Rank", "Coderwall", "Asciinema",
    "CSSBattle", "DMOJ", "Vjudge", "devRant", "LessWrong", "Lobsters", "habr",
    "LemmyWorld", "programming.dev", "Fosstodon", "pixelfed.social", "minds",
    "SpaceHey", "Myspace", "LiveJournal", "Plurk", "Clubhouse", "Vero",
    "YouNow", "Smule", "MixCloud", "Discogs", "Freesound", "MuseScore",
    "Ultimate-Guitar", "Rate Your Music", "Fanpop", "Mydramalist", "LibraryThing",
    "Archive of Our Own", "SmugMug", "EyeEm", "Exposure", "YouPic",
    "LottieFiles", "Tenor", "Giphy", "Genius (Users)", "Genius (Artists)",
    "Issuu", "SpeakerDeck", "Slides", "SlideShare", "Trello", "Disqus",
    "Flipboard", "BuzzFeed", "HubPages", "Naver", "note", "Velog", "tistory",
    "Wix", "Weebly", "Jimdo", "WebNode", "Wikidot", "write.as", "Listed",
    "Untappd", "geocaching", "Polarsteps", "couchsurfing", "Pronouns.page",
    "Tellonym.me", "F3.cool", "Clapper", "Kik", "furaffinity",
)
POPULAR_RANK = {name.casefold(): index for index, name in enumerate(POPULAR_SITE_ORDER)}


POPULAR_RECHECKS = {"Reddit", "Spotify", "Linktree", "DeviantArt", "Bandcamp",
                    "Trakt", "Archive.org", "Hashnode", "TryHackMe", "Giphy", "SlideShare"}
EXTRA_SITES = {
    "last.fm": {
        "url": "https://www.last.fm/user/{}", "urlMain": "https://www.last.fm/",
        "errorType": "status_code",
    },
    "Letterboxd": {
        "url": "https://letterboxd.com/{}/", "urlMain": "https://letterboxd.com/",
        "errorType": "message", "errorMsg": "Sorry, we can’t find the page you’ve requested.",
    },
    "Snapchat": {
        "url": "https://www.snapchat.com/@{}", "urlMain": "https://www.snapchat.com/",
        "regexCheck": r"^[A-Za-z][A-Za-z0-9_.-]{1,13}[A-Za-z0-9]$", "errorType": "status_code",
    },
    "threads": {
        "url": "https://www.threads.com/@{}", "urlMain": "https://www.threads.com/", "errorType": "status_code",
    },
    "Facebook": {
        "url": "https://www.facebook.com/{}",
        "urlMain": "https://www.facebook.com/",
        "regexCheck": r"^[A-Za-z0-9.]+$",
        "errorType": "status_code",
        "source": "https://www.facebook.com/help/162586890471598",
    },
}
SITE_ALIASES = {"x": "twitter", "x.com": "twitter", "fb": "facebook",
                "steam": "steam community (user)"}
LABELS = {"VERIFIED": "POZİTİF", "NOT_FOUND": "BULUNAMADI",
          "UNKNOWN": "BELİRSİZ", "SKIPPED": "ATLANDI"}


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def valid_nick(nick):
    if not nick or len(nick) > 64:
        raise ValueError("Nickname 1–64 karakter olmalı.")
    if not all(c.isalnum() or c in "_.-" for c in nick):
        raise ValueError("Yalnızca harf, rakam, alt çizgi, nokta ve tire kullan.")
    if nick in {".", ".."}:
        raise ValueError("Geçersiz nickname.")
    return nick


def accepted(nick, site):
    pattern = site.get("regexCheck")
    return not pattern or re.fullmatch(pattern, nick) is not None


def control_names(nick, site):
    names = []

    for length in [16, 12, 10, 8]:
        for alphabet in [string.ascii_lowercase, string.ascii_lowercase + string.digits, string.digits]:
            for _ in range(8):
                candidate = "".join(secrets.choice(alphabet) for _ in range(length))
                if candidate != nick and candidate not in names and accepted(candidate, site):
                    names.append(candidate)
                    if len(names) == 2:
                        return names
    return []


def profile_url(site, nick):
    template = site["url"]
    if template.count("{}") != 1:
        raise ValueError("Desteklenmeyen profil URL şablonu")
    if template == "https://bsky.app/profile/{}.bsky.social":
        return "https://bsky.app/profile/" + quote(bluesky_handle(nick), safe="")
    url = template.replace("{}", quote(nick, safe=""))
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Geçersiz profil URL adresi")
    return url


def load_catalog(path, include_nsfw=False, include_excluded=False):
    data = json.loads(path.read_text(encoding="utf-8")) if path else {**BUNDLED_SITES, **EXTRA_SITES}
    if not isinstance(data, dict):
        raise ValueError("Site listesi bir JSON nesnesi olmalı")
    exclusions = set(BUNDLED_EXCLUSIONS)
    sites = {}
    omitted = Counter()
    for name, site in data.items():
        if not isinstance(site, dict) or "url" not in site:
            continue
        if site.get("isNSFW") and not include_nsfw:
            omitted["NSFW"] += 1
            continue
        if name in exclusions and name not in POPULAR_RECHECKS and not include_excluded:
            omitted["kaynak listenin sorunlu siteleri"] += 1
            continue
        try:
            profile_url(site, "sampleuser")
            if site.get("regexCheck"):
                re.compile(site["regexCheck"])
        except (ValueError, TypeError, re.error, AttributeError):
            omitted["desteklenmeyen şablon"] += 1
            continue
        sites[name] = site
    return dict(sorted(sites.items(), key=lambda x: (
        POPULAR_RANK.get(x[0].casefold(), len(POPULAR_SITE_ORDER)), x[0].casefold()))), dict(omitted)


def select_sites(catalog, requested=None, limit=MAX_SITES):
    if not 1 <= limit <= MAX_SITES:
        raise ValueError(f"--limit 1 ile {MAX_SITES} arasında olmalı")
    if requested:
        lookup = {name.casefold(): name for name in catalog}
        wanted = set()
        for name in requested:
            key = SITE_ALIASES.get(name.casefold(), name.casefold())
            if key not in lookup:
                raise ValueError(f"Site bulunamadı veya dışlandı: {name}. --list-sites kullan.")
            wanted.add(lookup[key])
        catalog = {name: site for name, site in catalog.items() if name in wanted}

    return dict(list(catalog.items())[:limit])


def read_checkpoint(out, nickname, signature, sites):

    try:
        report = out / "index.html"
        if report.stat().st_size > 25000000:
            raise ValueError("Devam raporu çok büyük")
        node = BeautifulSoup(report.read_text(encoding="utf-8"), "html.parser").select_one('script#nickscan-state[type="application/json"]')
        if node is None:
            raise ValueError("HTML içinde devam bilgisi bulunamadı; yeni tarama başlat")
        old = json.loads(node.string or node.get_text())
        if not isinstance(old, dict) or not isinstance(old.get("metadata"), dict):
            raise ValueError("Raporun yapısı geçersiz")
        if old.get("nickname") != nickname or old["metadata"].get("catalog_sha256") != signature:
            raise ValueError("Devam etmek için nickname, sürüm, site seçimi ve öncelik sırası aynı olmalı")
        now = datetime.now(timezone.utc)
        def age(value):
            date = datetime.fromisoformat(value)
            if date.tzinfo is None:
                raise ValueError("Rapor zaman dilimi içermiyor")
            elapsed = (now - date).total_seconds()
            if elapsed < 0:
                raise ValueError("Rapor geleceğe ait; sistem saatini kontrol et")
            return elapsed
        if age(old["saved_at"]) > 86400:
            raise ValueError("Rapor 24 saatten eski; yeni tarama başlat")
        age(old["metadata"]["started_at"])
        if not isinstance(old.get("results"), list):
            raise ValueError("Rapor sonuç listesi geçersiz")
        results, seen = {}, set()
        for row in old["results"]:
            if not isinstance(row, dict):
                raise ValueError("Rapor satırı geçersiz")
            name = row["site"]
            if name not in sites or name in seen or row["status"] not in LABELS:
                raise ValueError("Raporda farklı, tekrar eden veya geçersiz bir site var")
            seen.add(name)
            if (not isinstance(row.get("fields"), dict) or not isinstance(row.get("controls"), list)
                    or not isinstance(row.get("reason"), str)
                    or row.get("url") != profile_url(sites[name], nickname)):
                raise ValueError("Rapor satırındaki profil adresi veya alanlar geçersiz")
            if (row.get("discovery_status") is not None and row["discovery_status"] not in
                    {"pending", "running", "interrupted", "complete", "disabled"}):
                raise ValueError("Raporda geçersiz diğer hesap arama durumu var")
            elapsed = age(row["checked_at"])
            if row["status"] != "UNKNOWN" and elapsed <= 86400:
                results[name] = row
        return results, old["metadata"]["started_at"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Devam raporu bozuk veya eksik; yeni tarama başlat") from exc


def observe_profile(page, site, nick, adapter=None, native_only=False):

    evidence, owner_redirect = account_page_evidence(page, nick)
    if spotify_user_route(page.requested_url):
        evidence, owner_redirect = spotify_evidence(page, nick), False
    if evidence.positive:
        checked = replace(page, requested_url=page.final_url) if owner_redirect else page
        state, reason = decide(checked, {}, nick, evidence)
        if state == "VERIFIED":
            reason = ("Tam nickname, hesap kimliği ve platform profil verisi bulundu" if evidence.fields.get("account_id")
                      else "Tam nickname ve en az bir profil alanı bulundu")
        return dict(status=state, reason=reason, verification="single_native",
                    http_status=page.status, final_url=page.final_url,
                    source_url=page.requested_url, fields=evidence.fields,
                    evidence=evidence.identity + evidence.sources)
    roblox_kind, _ = roblox_route(page.requested_url, nick)
    if roblox_kind:
        evidence = roblox_evidence(page, nick)
        checked = page
        if evidence.positive and roblox_kind == "lookup":


            checked = replace(page, requested_url=page.final_url)
        state, reason = decide(checked, {}, nick, evidence)
        if state == "VERIFIED":
            reason = "Tam nickname, hesap kimliği ve platform profil verisi bulundu"
        return dict(status=state, reason=reason, verification="single_native",
                    http_status=page.status, final_url=page.final_url,
                    source_url=page.requested_url, fields=evidence.fields,
                    evidence=evidence.identity + evidence.sources)
    kind = native_profile_kind(page.requested_url, nick)
    if kind in {"Bluesky", "Bluesky API"}:
        evidence = (bluesky_evidence(page, nick, api=kind == "Bluesky API")
                    if native_profile_kind(page.final_url, nick) == kind else Evidence())
        state, reason = decide(page, {}, nick, evidence)
        if state == "VERIFIED" and evidence.fields.get("account_id"):
            reason = "Tam nickname, hesap kimliği ve platform profil verisi bulundu"
        return dict(status=state, reason=reason, verification="single_native",
                    http_status=page.status, final_url=page.final_url,
                    source_url=page.requested_url, fields=evidence.fields,
                    evidence=evidence.identity + evidence.sources)
    evidence = native_evidence(page, nick, apply_gate=False)
    native_block, native_reason = gate(replace(page, stable=True), {}) if evidence.identity else (None, "")
    if not evidence.identity and not native_only:
        evidence = platform_evidence(page, nick, apply_gate=False)
    if evidence.identity:
        state, method = "VERIFIED", "single_native"
        reason = ("Tam nickname, hesap kimliği ve platform profil verisi bulundu" if evidence.fields.get("account_id")
                  else "Tam nickname ve en az bir profil alanı bulundu")
        blocked, blocked_reason = gate(page, {}, profile_positive=True)
        if native_block == "UNKNOWN":
            blocked, blocked_reason = native_block, native_reason
        if blocked:
            state, reason = blocked, blocked_reason
    else:
        evidence = Evidence() if native_only else extract(page, nick, adapter)
        state, reason = decide(page, {} if native_only else site, nick, evidence)
        method = "single_profile"
        if (state == "UNKNOWN" and not gate(page, site)[0]
                and same_profile_url(page.final_url, "https://t.me/" + quote(nick, safe=""))
                and re.search(r"Telegram: Contact @|You can contact @", page.title + " " + page.text, re.I)):
            reason = "Telegram yalnızca genel iletişim sayfası gösterdi; herkese açık profil alanı alınamadı. Bu, hesabın bulunmadığı anlamına gelmez"
    return dict(status=state, reason=reason, verification=method,
                http_status=page.status, final_url=page.final_url,
                source_url=page.requested_url, fields=evidence.fields,
                evidence=evidence.identity + evidence.sources)


def unwrap_search_link(url):
    import base64
    for _ in range(3):
        if not web_url(url):
            return ""
        p = urlsplit(url)
        host = (p.hostname or "").removeprefix("www.")
        args = parse_qs(p.query)
        target = ""
        if host == "bing.com" and p.path.startswith("/ck/"):
            encoded = args.get("u", [""])[0]
            if encoded.startswith("a1"):
                try:
                    target = base64.urlsafe_b64decode(encoded[2:] + "=" * (-len(encoded[2:]) % 4)).decode("utf-8")
                except (ValueError, UnicodeError):
                    return ""
        elif host in {"duckduckgo.com", "html.duckduckgo.com"}:
            target = args.get("uddg", [""])[0]
        elif host == "google.com" and p.path == "/url":
            target = args.get("q", args.get("url", [""]))[0]
        if not target:
            return url
        url = target
    return web_url(url)


def profile_candidate(url, site):

    url = unwrap_search_link(url)
    if not url:
        return None
    p = urlsplit(url)
    root = urlsplit(profile_url(site, "NICKSCANHANDLE"))
    host = (p.hostname or "").removeprefix("www.")
    original = (root.hostname or "").removeprefix("www.")
    path = unquote(p.path).rstrip("/")
    try:
        if p.port not in {None, 443, 80}:
            return None
    except ValueError:
        return None


    args = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
            if not k.casefold().startswith("utm_") and k.casefold() not in
            {"fbclid", "gclid", "igsh", "igshid", "si", "s", "t", "feature"}]
    if args:
        return None
    url = urlunsplit((p.scheme, p.netloc, p.path.rstrip("/"), "", ""))
    original, host = PROFILE_HOSTS.get(original, original), PROFILE_HOSTS.get(host, host)
    if original == "pinterest.com" and host.endswith(".pinterest.com"):
        host = "pinterest.com"
    if original == "x.com" and host == "x.com":
        match = re.fullmatch(r"/([A-Za-z0-9_]{1,15})", path)
        if not match or match[1].casefold() in {"home", "explore", "search", "i", "login", "signup", "settings", "intent", "share", "messages", "notifications", "compose"}:
            return None
        return "https://x.com/" + match[1], match[1]
    if original == "youtube.com" and host == original:
        match = re.fullmatch(r"/(?:@([^/]+)|channel/(UC[A-Za-z0-9_-]{22}))", path)
        if match:
            username = match[1] or match[2]
            return "https://www.youtube.com" + p.path.rstrip("/"), username
        return None
    if original == "snapchat.com" and host == original:
        match = re.fullmatch(r"/(?:add/|@)([A-Za-z][A-Za-z0-9_.-]{1,13}[A-Za-z0-9])", path)
        return ("https://www.snapchat.com/@" + match[1], match[1]) if match else None
    if original == "bsky.app" and host == original:
        match = re.fullmatch(r"/profile/([A-Za-z0-9][A-Za-z0-9.-]*\.bsky\.social)", path, re.I)
        return ("https://bsky.app/profile/" + match[1], match[1]) if match else None
    if "nickscanhandle" in original:
        match = re.fullmatch(re.escape(original).replace("nickscanhandle", r"(?P<user>[^.]+)"), host)
        if not match or path != unquote(root.path).rstrip("/"):
            return None
        return url, match["user"]
    if host != original:
        return None
    pattern = re.escape(unquote(root.path).rstrip("/")).replace("NICKSCANHANDLE", r"(?P<user>[^/]+)")
    match = re.fullmatch(pattern, path)
    if not match or "user" not in match.groupdict():
        return None
    username = match["user"]
    if username.casefold() in {"login", "signup", "explore", "search", "accounts", "about", "settings", "privacy", "terms", "help", "directory", "watch", "videos", "p", "reel", "reels", "pin"}:
        return None
    if not accepted(username.removeprefix("@"), site):
        return None
    return url, username


def search_gate(page):


    state, reason = gate(replace(page, requested_url=page.final_url, stable=True), {})
    if state:
        return state, reason
    a, b = normalized_url(page.requested_url), normalized_url(page.final_url)
    if not a or not b or PROFILE_HOSTS.get(a[0], a[0]) != PROFILE_HOSTS.get(b[0], b[0]) or a[1] != b[1] or a[2] != b[2]:
        return "UNKNOWN", "Arama başka bir sayfaya yönlendirildi"
    first, second = parse_qs(a[3]), parse_qs(b[3])
    for key in ("q", "search_query"):
        if key in first and first[key] != second.get(key):
            return "UNKNOWN", "Arama terimi yönlendirmede kayboldu veya değişti"
    return None, ""


def related_candidates(page, site, nick, primary_url, search_page=None):
    if search_page is None:
        search_page = urlsplit(page.requested_url).path.rstrip("/") in {"/search", "/search/user", "/results"}
    state = search_gate(page)[0] if search_page else gate(replace(page, stable=True), {})[0]
    if page.error or state:
        return []
    soup = BeautifulSoup(page.html, "html.parser")
    found = {}
    def consider(link, label):
        candidate = profile_candidate(urljoin(page.final_url, link), site)
        if not candidate:
            return
        url, username = candidate
        if same_profile_url(url, primary_url):
            return
        label = " ".join(label.split())[:250]
        if handle(username, nick):
            kind = "Tam kullanıcı adı"
        elif handle(label, nick) or re.search(r"(?<!\w)" + re.escape(fold(nick)) + r"(?!\w)", fold(label)):
            kind = "Görünen ad eşleşmesi"
        elif len(nick) >= 3 and fold(nick) in fold(username):
            kind = "Benzer kullanıcı adı"
        else:
            return
        found.setdefault(profile_key(url), dict(url=url, username=username, display_name=label or username,
                         match=kind, source_url=page.final_url, status="UNKNOWN", reason="Arama eşleşmesi; profil henüz doğrulanmadı"))
    for node in soup.select('[data-testid="UserCell"], ytd-channel-renderer')[:40]:
        for anchor in node.select("a[href]")[:15]:
            consider(anchor["href"], node.get_text(" ", strip=True))
    web_search = (urlsplit(page.final_url).hostname or "").removeprefix("www.") in {"bing.com", "duckduckgo.com", "html.duckduckgo.com"}
    anchors = soup.select("li.b_algo h2 a[href], .result__a[href], [data-testid='result-title-a'][href]") if web_search else soup.select("a[href]")
    for anchor in anchors[:1200]:
        consider(anchor["href"], anchor.get_text(" ", strip=True))

    pending = [embedded_json(page, "ytInitialData")]
    for _ in range(4000):
        if not pending:
            break
        value = pending.pop()
        if isinstance(value, dict):
            card = value.get("channelRenderer")
            if isinstance(card, dict):
                identifier = card.get("channelId", "")
                title = card.get("title", {})
                name = title.get("simpleText", "") if isinstance(title, dict) else ""
                if isinstance(title, dict) and not name:
                    name = "".join(x.get("text", "") for x in title.get("runs", []) if isinstance(x, dict))
                if isinstance(identifier, str) and re.fullmatch(r"UC[A-Za-z0-9_-]{22}", identifier):
                    navigation = card.get("navigationEndpoint", {})
                    endpoint = navigation.get("browseEndpoint", {}) if isinstance(navigation, dict) else {}
                    route = endpoint.get("canonicalBaseUrl", "") if isinstance(endpoint, dict) else ""
                    consider(urljoin("https://www.youtube.com", route) if isinstance(route, str) and route.startswith("/@") else "https://www.youtube.com/channel/" + identifier, name)
            card = value.get("lockupViewModel")
            if isinstance(card, dict) and card.get("contentType") == "LOCKUP_CONTENT_TYPE_CHANNEL":
                identifier = card.get("contentId", "")
                metadata = card.get("metadata", {})
                metadata = metadata.get("lockupMetadataViewModel", {}) if isinstance(metadata, dict) else {}
                title = metadata.get("title", {}) if isinstance(metadata, dict) else {}
                label = title.get("content", "") if isinstance(title, dict) else ""
                if isinstance(identifier, str) and re.fullmatch(r"UC[A-Za-z0-9_-]{22}", identifier):
                    consider("https://www.youtube.com/channel/" + identifier, label)
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value[:200])
    return list(found.values())[:40]


def discovery_url(name, nick):
    term = quote(nick, safe="")
    templates = {"Twitter": f"https://x.com/search?q={term}&src=typed_query&f=user",
        "YouTube": f"https://www.youtube.com/results?search_query={term}&sp=EgIQAg%3D%3D",
        "GitHub": f"https://github.com/search?q={term}&type=users",
        "Reddit": f"https://www.reddit.com/search/?q={term}&type=users",
        "TikTok": f"https://www.tiktok.com/search/user?q={term}"}
    return templates.get(name)


class SearchBudget:

    def __init__(self, limit=30):
        self.remaining = limit
        self.lock = threading.Lock()

    def take(self):
        with self.lock:
            if self.remaining <= 0:
                return False
            self.remaining -= 1
            return True


def web_discovery_urls(site, nick):
    root = urlsplit(site.get("urlMain") or profile_url(site, "NICKSCANHANDLE"))
    host = (root.hostname or "").removeprefix("www.")
    if not host:
        return []
    query = quote(f'site:{host} "{nick}"', safe="")
    return [("Web araması · Bing", f"https://www.bing.com/search?q={query}&count=10"),
            ("Web araması · DuckDuckGo", f"https://duckduckgo.com/?q={query}&ia=web")]


def discover_accounts(browser, row, name, site, nick, adapter, stop):
    candidates = row.pop("_related_seed", []) + copy.deepcopy(row.get("other_accounts", []))
    row["other_accounts"], row["other_accounts_note"] = [], ""
    row["discovery"] = []
    if row["status"] == "SKIPPED" or not getattr(browser, "other_accounts", False):
        row["other_accounts_note"] = "Ek hesap araması yapılmadı"
        return
    limit = getattr(browser, "other_limit", 5)
    search = discovery_url(name, nick)
    primary_id = row.get("fields", {}).get("account_id")
    selected, duplicates = None, set()
    def unique_candidates():
        unique = {}
        for candidate in candidates:
            if same_profile_url(candidate["url"], row["url"]):
                continue
            if primary_id and urlsplit(candidate["url"]).path.rstrip("/") == "/channel/" + primary_id:
                continue
            unique.setdefault(profile_key(candidate["url"]), candidate)
        return list(unique.values())
    def publish(note=None):
        visible = unique_candidates()[:limit] if selected is None else selected
        row["other_accounts"] = [item for item in visible if profile_key(item["url"]) not in duplicates]
        for item in row["other_accounts"]:
            item.setdefault("check_state", "complete" if item.get("status") == "VERIFIED" else "pending")
        if note is not None:
            row["other_accounts_note"] = note
        callback = getattr(browser, "discovery_progress", None)
        if callback:
            callback()
    def search_once(label, url):
        check_cancel(stop)
        record = dict(source=label, url=url, status="UNKNOWN", reason="Arama tamamlanmadı", candidates=0)
        row["discovery"].append(record)
        publish(label + " sürüyor")
        try:
            page = browser.visit(url)
            state, reason = search_gate(page)
            found = related_candidates(page, site, nick, row["url"], search_page=True)
            record.update(status="BLOCKED" if state else "SEARCHED", reason=reason or "Arama sayfası okundu",
                          candidates=len(found), final_url=page.final_url, http_status=page.status)
            candidates.extend(found)
            publish(label + (": " + reason if state else f": {len(found)} aday bulundu; profil kontrolleri sırada"))
            return len(found)
        except CancelledScan:
            raise
        except Exception as exc:
            record.update(reason="Arama sayfası okunamadı: " + type(exc).__name__)
            publish(record["reason"])
            return 0
    try:
        publish("Diğer hesaplar aranıyor")
        if search:
            search_once("Platform araması", search)
        budget = getattr(browser, "web_search_budget", None)
        if len(unique_candidates()) < limit and budget is not None:
            for label, target in web_discovery_urls(site, nick):
                if not budget.take():
                    row["discovery"].append(dict(source=label, url=target, status="SKIPPED", candidates=0,
                                                 reason="Tarama için belirlenen web arama sınırına ulaşıldı"))
                    break
                if search_once(label, target):
                    break
        seen_ids = {row.get("fields", {}).get("account_id")} - {None, ""}
        unique = unique_candidates()
        selected = unique[:limit]
        publish("Bulunan adayların profilleri kontrol ediliyor" if selected else "Arama kaynakları kontrol edildi")
        for candidate in selected:
            check_cancel(stop)
            candidate["check_state"] = "running"
            publish("Aday profil kontrol ediliyor: @" + candidate["username"])
            try:
                page = browser.visit(candidate["url"])
                observation = observe_profile(page, site, candidate["username"], adapter)
            except CancelledScan:
                raise
            except Exception as exc:
                candidate["reason"] = "Aday bulundu; profil okunamadı: " + type(exc).__name__
                candidate["check_state"] = "complete"
                publish()
                continue
            candidate.update(status=observation["status"], reason=observation["reason"], fields=observation["fields"])
            candidate["check_state"] = "complete"
            candidate["username"] = observation["fields"].get("username", candidate["username"])
            candidate["display_name"] = observation["fields"].get("display_name", candidate.get("display_name", candidate["username"]))
            account_id = observation["fields"].get("account_id")
            if observation["status"] == "VERIFIED" and account_id:
                if account_id in seen_ids:
                    duplicates.add(profile_key(candidate["url"]))
                else:
                    seen_ids.add(account_id)
            publish()
        notes = []
        for record in row["discovery"]:
            notes.append(record["source"] + ": " + (f'{record["candidates"]} aday' if record["status"] == "SEARCHED" else record["reason"]))
        if len(unique) > limit:
            notes.append(f"{len(unique)} farklı adaydan ilk {limit} profil incelendi; --other-limit ile artırılabilir")
        if not row["other_accounts"]:
            notes.append("Erişilebilen kaynaklarda ek eşleşme bulunamadı" if any(r["status"] == "SEARCHED" for r in row["discovery"])
                         else "Ek hesap araması tamamlanamadı; bu platformda başka hesap olmadığı anlamına gelmez")
        row["other_accounts_note"] = " · ".join(notes)
        publish()
    except CancelledScan:
        raise
    except Exception:
        row["other_accounts_note"] = "Diğer hesaplar aranırken sayfaya erişilemedi"
        raise


def scan_site(browser, name, site, nick, adapter, delay, stop=None):
    row = _scan_primary(browser, name, site, nick, adapter, delay, stop)
    try:
        discover_accounts(browser, row, name, site, nick, adapter, stop)
    except CancelledScan:

        row.pop("_related_seed", None)
        row.setdefault("other_accounts", [])
        row["other_accounts_note"] = "Diğer hesap araması durduruldu"
    return row


def _scan_primary(browser, name, site, nick, adapter, delay, stop=None):
    check_cancel(stop)
    url = profile_url(site, nick)
    row = dict(site=name, url=url, checked_at=stamp(), status="UNKNOWN", reason="",
               http_status=None, final_url=url, fields={}, evidence=[], controls=[], checks=[],
               verification_policy="any_one_positive")
    if not accepted(nick, site):
        row.update(status="SKIPPED", reason="Nickname sitenin karakter/uzunluk kuralına uymuyor")
        return row


    targets = [(url, False), (url, False)]
    if native_profile_kind(url, nick) == "Reddit":
        api_url = url.rstrip("/") if urlsplit(url).path.rstrip("/").endswith("/about.json") else url.rstrip("/") + "/about.json"
        targets[1] = (api_url, True)
    elif native_profile_kind(url, nick) == "Bluesky":
        targets[1] = (bluesky_api_url(nick), True)
    elif same_profile_url(url, "https://www.chess.com/member/" + quote(nick, safe="")):
        targets[1] = ("https://api.chess.com/pub/player/" + quote(nick, safe=""), True)
    for number, (target, native_only) in enumerate(targets, 1):
        check_cancel(stop)
        if number > 1:
            pause(delay, stop)
        page = browser.visit(target)
        if number == 1 and roblox_route(url, nick)[0] == "lookup":
            route, identifier = roblox_route(page.final_url, nick)
            if route == "profile" and not page.error and page.status == 200:
                targets[1] = ("https://users.roblox.com/v1/users/" + identifier, True)
        if getattr(browser, "other_accounts", False):
            row.setdefault("_related_seed", []).extend(related_candidates(page, site, nick, url))
        observation = observe_profile(page, site, nick, adapter, native_only)
        record = dict(attempt=number, checked_at=stamp(), **{key: observation[key] for key in
                      ("status", "reason", "verification", "source_url", "http_status", "final_url")})
        record["page_title"] = page.title[:500]
        record["evidence"] = observation["evidence"][:20]
        row["checks"].append(record)
        row.update(observation)
        if number > 1:
            row["recheck"] = record.copy()
        if observation["status"] == "VERIFIED":
            return row

    if all(check["status"] == "NOT_FOUND" for check in row["checks"]):
        row.update(status="NOT_FOUND", reason="Profil bulunamadı yanıtı alındı")
    else:
        details = " · ".join(dict.fromkeys(check["reason"] for check in row["checks"]))
        row.update(status="UNKNOWN", reason=details)
    return row


def discovery_pending(row):
    return row.get("discovery_status") in {"pending", "running", "interrupted"}


class ScanQueue:

    def __init__(self, stop):
        self.stop = stop
        self.condition = threading.Condition()
        self.queues = [[], []]
        self.active = [0, 0]
        self.unfinished = 0
        self.last_phase = 1

    def put(self, job):
        with self.condition:
            heapq.heappush(self.queues[job[0]], job)
            self.unfinished += 1
            self.condition.notify_all()

    def qsize(self):
        with self.condition:
            return sum(map(len, self.queues))

    def get(self):
        with self.condition:
            while not self.stop.is_set():
                primary, discovery = self.queues
                if discovery and (not primary or self.active[1] == 0 and self.last_phase == 0):
                    phase = 1
                elif primary:
                    phase = 0
                else:
                    if self.unfinished == 0:
                        return None
                    self.condition.wait(.2)
                    continue
                job = heapq.heappop(self.queues[phase])
                self.active[phase] += 1
                self.last_phase = phase
                return job
        return None

    def task_done(self, job):
        with self.condition:
            self.active[job[0]] -= 1
            self.unfinished -= 1
            self.condition.notify_all()


def parallel_scan(sites, nick, adapters, results, workers, browser_factory,
                  on_result=None, on_event=None, stop=None):





    if len(sites) > MAX_SITES:
        raise ValueError(f"Bir tarama en fazla {MAX_SITES} site içerebilir")
    stop = stop if stop is not None else threading.Event()
    jobs, events = ScanQueue(stop), queue.Queue()
    for priority, (name, site) in enumerate(sites.items()):
        if name not in results:
            jobs.put((0, priority, name, site, None))
        elif discovery_pending(results[name]):
            jobs.put((1, priority, name, site, copy.deepcopy(results[name])))
    count = min(workers, jobs.qsize())
    if not count:
        return {"interrupted": False, "worker_errors": [], "discovery_pending": 0}

    def failed_primary(name, site, exc):
        return dict(site=name, url=profile_url(site, nick), checked_at=stamp(),
                    status="UNKNOWN", reason=f"Site işleme hatası: {type(exc).__name__}: {str(exc)[:250]}",
                    http_status=None, final_url="", fields={}, evidence=[], controls=[],
                    discovery_status="disabled", other_accounts=[], other_accounts_note="Profil işleme hatası nedeniyle ek arama yapılmadı")

    def worker(number):
        browser = None
        try:
            browser = browser_factory(number, stop)
            while not stop.is_set():
                job = jobs.get()
                if job is None:
                    break
                phase, priority, name, site, row = job
                started = time.monotonic()
                saved_seed = copy.deepcopy(row.get("_related_seed", [])) if row is not None else []
                try:


                    if accepted(nick, site) and browser.driver is None:
                        try:
                            events.put(("starting", number, name))
                            browser.start()
                        except CancelledScan:
                            raise
                        except Exception as exc:
                            jobs.put(job)
                            events.put(("worker_error", number, f"{type(exc).__name__}: {exc}"))
                            break
                        events.put(("ready", number, name))
                    started = time.monotonic()
                    if phase == 0:
                        events.put(("checking", number, name))
                        row = _scan_primary(browser, name, site, nick, adapters.get(name), 0, stop)
                        row["primary_seconds"] = round(time.monotonic() - started, 3)
                        enabled = row["status"] != "SKIPPED" and getattr(browser, "other_accounts", False)
                        row.update(discovery_status="pending" if enabled else "disabled", other_accounts=[],
                                   other_accounts_note="Ana profil kaydedildi; diğer hesaplar araması sırada" if enabled else "Ek hesap araması yapılmadı")
                        events.put(("row", number, copy.deepcopy(row)))
                        if enabled:
                            jobs.put((1, priority, name, site, row))
                    else:
                        events.put(("discovering", number, name))
                        row["discovery_status"] = "running"
                        row["other_accounts_note"] = "Diğer hesaplar aranıyor"
                        browser.discovery_progress = lambda: events.put(("updated", number, copy.deepcopy(row)))
                        browser.discovery_progress()
                        discover_accounts(browser, row, name, site, nick, adapters.get(name), stop)
                        row["discovery_status"] = "complete" if getattr(browser, "other_accounts", False) else "disabled"
                        row["discovery_seconds"] = round(time.monotonic() - started, 3)
                        events.put(("updated", number, copy.deepcopy(row)))
                except CancelledScan:
                    if phase == 1 and row is not None:
                        row.update(discovery_status="interrupted", other_accounts_note="Diğer hesap araması durduruldu; ana profil sonucu korundu")
                        row["_related_seed"] = saved_seed + copy.deepcopy(row.get("other_accounts", []))
                        events.put(("updated", number, copy.deepcopy(row)))
                    break
                except Exception as exc:
                    if phase == 0:
                        row = failed_primary(name, site, exc)
                    else:
                        row.update(discovery_status="interrupted", other_accounts_note=f"Ek arama tamamlanamadı: {type(exc).__name__}; ana profil sonucu korundu")
                        row["_related_seed"] = saved_seed + copy.deepcopy(row.get("other_accounts", []))
                    events.put(("row" if phase == 0 else "updated", number, copy.deepcopy(row)))
                    browser.close()
                finally:
                    browser.discovery_progress = None
                    jobs.task_done(job)
                    events.put(("idle", number, None))
                if browser.visits >= 35:
                    browser.close()
        except CancelledScan:
            pass
        except Exception as exc:
            events.put(("worker_error", number, f"{type(exc).__name__}: {exc}"))
        finally:
            try:
                if browser is not None:
                    browser.close()
            finally:
                events.put(("done", number, None))

    executor = ThreadPoolExecutor(max_workers=count, thread_name_prefix="nickscan")
    futures = [executor.submit(worker, i + 1) for i in range(count)]
    done, interrupted, errors, callback_error = 0, False, [], None
    last_heartbeat = time.monotonic()
    try:
        while done < count:
            try:
                try:
                    kind, number, value = events.get(timeout=0.2)
                except queue.Empty:
                    if on_event and callback_error is None and time.monotonic() - last_heartbeat >= 5:
                        on_event("heartbeat", 0, None)
                        last_heartbeat = time.monotonic()
                    continue
                if kind == "done":
                    done += 1
                elif kind in {"row", "updated"}:
                    results[value["site"]] = value
                    if on_result and callback_error is None:
                        on_result(value, number)
                elif kind == "worker_error":
                    errors.append({"worker": number, "error": value})
                if on_event and callback_error is None:
                    on_event(kind, number, value)
            except KeyboardInterrupt:
                interrupted = True
                stop.set()
                print("\nDurduruluyor: yeni site alınmayacak; çalışan tarayıcılar kapanıyor.", flush=True)
            except Exception as exc:

                callback_error = exc
                stop.set()
    finally:
        interrupted = interrupted or (stop.is_set() and callback_error is None)
        stop.set()
        executor.shutdown(wait=True, cancel_futures=True)
    if callback_error:
        raise callback_error
    for future in futures:
        future.result()
    return {"interrupted": interrupted, "worker_errors": errors,
            "discovery_pending": sum(discovery_pending(row) for row in results.values())}


def atomic_text(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def csv_cell(value):
    value = str(value if value is not None else "")
    return "'" + value if value.lstrip().startswith(("=", "+", "-", "@")) else value


def report_payload(path):
    node = BeautifulSoup(Path(path).read_text(encoding="utf-8"), "html.parser").select_one("script#nickscan-state")
    return json.loads(node.string or node.get_text()) if node else {}


def write_reports(out, nick, results, metadata, full=True):

    out.mkdir(parents=True, exist_ok=True)
    order = {name: index for index, name in enumerate(metadata.get("site_order", []))}
    rows = sorted(results.values(), key=lambda r: (order.get(r["site"], MAX_SITES), r["site"].casefold()))
    totals = dict(Counter(x["status"] for x in rows))
    payload = dict(version=VERSION, nickname=nick, saved_at=stamp(), metadata=metadata,
                   totals=totals, results=rows)
    esc = lambda value: html.escape(str(value), quote=True)
    def link(url, label):
        safe = web_url(url)
        return f'<a href="{esc(safe)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>' if safe else esc(label)
    names = {"username": "Kullanıcı adı", "account_id": "Hesap kimliği", "display_name": "Görünen ad",
             "bio": "Açıklama", "avatar": "Profil resmi", "followers": "Takipçi", "following": "Takip edilen",
             "posts": "Gönderi", "likes": "Beğeni", "subscribers": "Abone", "repositories": "Depolar",
             "link_karma": "Gönderi karması", "comment_karma": "Yorum karması", "created_utc": "Hesap oluşturma zamanı",
             "private_account": "Gizli hesap", "page_title": "Sayfa başlığı", "page_description": "Sayfa açıklaması"}
    table = []
    for row in sorted(rows, key=lambda r: ({"VERIFIED": 0, "UNKNOWN": 1, "NOT_FOUND": 2, "SKIPPED": 3}[r["status"]], order.get(r["site"], MAX_SITES), r["site"])):
        fields = []
        for key, value in row.get("fields", {}).items():
            shown = link(value, "Görüntüle") if key == "avatar" else esc(value)
            fields.append(f'<dt>{esc(names.get(key, key))}</dt><dd>{shown}</dd>')
        if row.get("source_url"):
            fields.append('<dt>Kaynak</dt><dd>' + link(row["source_url"], "Kaynağı aç") + '</dd>')
        fields.append('<dt>Tarama zamanı</dt><dd>' + esc(row.get("checked_at", "")) + '</dd>')
        if "primary_seconds" in row:
            fields.append('<dt>Ana profil süresi</dt><dd>' + esc(row["primary_seconds"]) + ' sn</dd>')
        proof = '<details><summary>Kanıt / alanlar</summary><dl>' + ''.join(fields) + '</dl></details>'
        related = row.get("other_accounts", [])
        extra = []
        for account in related:
            extra.append('<tr><td>' + esc(account.get("display_name", "")) + '</td><td>@' +
                         esc(account.get("username", "")) + '</td><td>' + esc(account.get("match", "")) +
                         '</td><td>' + esc("KONTROL EDİLİYOR" if account.get("check_state") == "running" else "ADAY" if account.get("check_state") == "pending" else LABELS.get(account.get("status"), "BELİRSİZ")) +
                         '<small>' + esc(account.get("reason", "")) + '</small></td><td>' +
                         link(account.get("url", ""), "Profil") +
                         ('<small>' + link(account["source_url"], "Arama kaynağı") + '</small>' if account.get("source_url") else '') + '</td></tr>')
        content = ('<div class="related-scroll"><table class="related"><thead><tr><th>Görünen ad</th><th>Kullanıcı adı</th><th>Eşleşme</th><th>Durum</th><th>Adres</th></tr></thead><tbody>' +
                   ''.join(extra) + '</tbody></table></div>') if extra else ''
        note = row.get("other_accounts_note", "")
        searches = ''.join('<li>' + link(record.get("url", ""), record.get("source", "Arama")) + ': ' +
                           esc(str(record.get("candidates", 0)) + ' aday' if record.get("status") == "SEARCHED" else record.get("reason", "")) + '</li>'
                           for record in row.get("discovery", []))
        phase_label = {"pending": "Sırada", "running": "Aranıyor", "interrupted": "Yarım kaldı", "disabled": "Kapalı"}.get(row.get("discovery_status"), "")
        summary = "Diğer hesaplar (" + (str(len(related)) + " aday · " if related and phase_label else str(len(related)) if not phase_label else "") + phase_label + ")"
        others = '<details><summary>' + esc(summary) + '</summary>' + content + ('<small>'+esc(note)+'</small>' if note else '') + ('<ul class="searches">' + searches + '</ul>' if searches else '') + '</details>'
        table.append(f'<tr class="{esc(row["status"])}"><td>{esc(row["site"])}</td><td class="status">{esc(LABELS[row["status"]])}</td>'
                     + '<td>' + link(row["url"], "Profil") + '</td><td>' + esc(row["reason"]) + '</td><td>' + proof + '</td><td>' + others + '</td></tr>')
    state = "Tamamlandı" if metadata.get("complete") else "Sürüyor / tamamlanmadı"
    completed_extra = sum(row.get("discovery_status") == "complete" for row in rows)
    running_extra = sum(row.get("discovery_status") == "running" for row in rows)
    pending_extra = sum(row.get("discovery_status") in {"pending", "interrupted"} for row in rows)
    progress = f'Ana profiller: {len(rows)}/{metadata.get("site_count", len(rows))} · Diğer hesaplar: {completed_extra} tamamlandı, {running_extra} aranıyor, {pending_extra} sırada'
    phases = {"starting": "Başlatılıyor", "primary": "Ana profil", "discovery": "Diğer hesaplar", "idle": "Bekliyor", "closed": "Kapandı"}
    activity = metadata.get("worker_activity", {})
    worker_info = ''.join('<span>T' + esc(number) + ' · ' + esc(phases.get(item.get("phase"), "Bekliyor")) +
                          (' · ' + esc(item["site"]) if item.get("site") else '') + '</span>'
                          for number, item in sorted(activity.items()))
    worker_panel = ('<div class="workers">' + worker_info + '</div><small>En yüksek eşzamanlı ana profil: ' +
                    esc(metadata.get("peak_active_primary", 0)) + '</small>') if worker_info else ''
    chips = ''.join(f'<span>{esc(LABELS[key])}: <b>{totals.get(key, 0)}</b></span>' for key in LABELS)
    diagnostics = metadata.get("diagnostics", []) + metadata.get("worker_errors", [])
    errors = ('<details class="logs"><summary>Tarayıcı günlüğü</summary><pre>' + esc('\n'.join(str(x) for x in diagnostics)) + '</pre></details>') if diagnostics else ''
    serialized = json.dumps(payload, ensure_ascii=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    doc = ('''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Nickname OSINT</title><style>
*{box-sizing:border-box}body{font:14px system-ui,sans-serif;background:#101827;color:#e8eef8;margin:32px auto;padding:0 24px;max-width:1600px}
h1{font-size:28px;margin-bottom:8px}.meta,small{color:#aebdd0}small{display:block;margin-top:8px}.totals,.workers{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.totals span,.workers span{background:#1b283c;border-radius:8px;padding:10px 14px}.workers{margin:12px 0;font-size:12px}
.table-scroll,.related-scroll{overflow-x:auto}table{width:100%;border-collapse:collapse}th{text-align:left;color:#aebdd0;font-size:12px}td,th{padding:15px 12px;border-bottom:1px solid #314155;vertical-align:top}td:nth-child(1),td.status{white-space:nowrap}td:nth-child(4){min-width:220px}
a{color:#8ac9ff}summary{cursor:pointer;white-space:nowrap}details[open]{min-width:210px}.VERIFIED>.status{color:#6ee7b7}.UNKNOWN>.status{color:#fcd34d}.NOT_FOUND>.status{color:#d5dfeb}.SKIPPED>.status{color:#94a3b8}
dl{margin:14px 0;font-size:12px}dt{color:#9bacc3;margin-top:10px}dd{margin:3px 0;max-width:320px;overflow-wrap:anywhere}.related{font-size:12px;min-width:520px}.related td{white-space:normal;min-width:0}.related small{max-width:230px}.logs{margin-top:24px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}
</style></head><body>''' + '<h1>Nickname: ' + esc(nick) + '</h1><div class="meta">Nickname OSINT ' + esc(VERSION) + ' · ' + esc(state) + ' · ' + esc(progress) + '</div>' + worker_panel + '<div class="totals">' + chips + '</div><div class="table-scroll"><table><thead><tr><th>Site</th><th>Durum</th><th>Adres</th><th>Gerekçe</th><th>Kanıt / alanlar</th><th>Diğer hesaplar</th></tr></thead><tbody>' + ''.join(table) + '</tbody></table></div>' + errors + '<script id="nickscan-state" type="application/json">' + serialized + '</script></body></html>')
    atomic_text(out / "index.html", doc)


def parser():
    p = argparse.ArgumentParser(description="Proxyless Chromium nickname tarayıcısı")
    p.add_argument("--version", action="version", version="Nickname OSINT " + VERSION)
    p.add_argument("nickname", nargs="?", help="Boş bırakırsan program sorar")
    p.add_argument("--sites", nargs="+", help="Tam site isimleri; boşsa tüm uygun siteler")
    p.add_argument("--limit", type=int, default=MAX_SITES, help="Öncelik sırasındaki ilk N site (1–200, varsayılan 200)")
    p.add_argument("--workers", "--threads", type=int, default=DEFAULT_WORKERS,
                   help="Paralel Chromium sayısı (1–6, varsayılan 5)")
    p.add_argument("--list-sites", action="store_true")
    p.add_argument("--catalog", type=Path, default=None)
    p.add_argument("--nsfw", action="store_true", help="NSFW sitelerini de ekle")
    p.add_argument("--include-excluded", action="store_true", help="Kaynak listenin sorunlu sitelerini de dene")
    p.add_argument("--timeout", type=float, default=30)
    p.add_argument("--startup-timeout", type=float, default=45, help="Chrome hazır olma süresi (5–180 saniye)")
    p.add_argument("--settle", type=float, default=4, help="JS sonrası en az bekleme (saniye)")
    p.add_argument("--delay", type=float, default=2, help="Aynı siteye ziyaretler arasında bekleme (saniye)")
    p.add_argument("--chrome", help="Chrome/Chromium tam dosya yolu")
    p.add_argument("--browser-mode", choices=("auto", "installed", "managed"), default="auto",
                   help="auto: kurulu Chrome açılmazsa ayrı resmi Chrome indir; managed: ayrı Chrome; installed: yalnızca kurulu")
    p.add_argument("--chrome-version", type=int, help="Gerekirse Chrome ana sürüm numarası")
    p.add_argument("--driver", help="İsteğe bağlı mevcut chromedriver tam yolu")
    p.add_argument("--show-browser", action="store_true", help="Tanılama için pencereyi göster")
    p.add_argument("--captcha-limit", type=int, default=10, help="2Captcha görev sınırı; NICKSCAN_2CAPTCHA_KEY gerekir (0–100)")
    p.add_argument("--other-limit", type=int, default=5, help="Site başına diğer hesap sınırı (1–20)")
    p.add_argument("--web-search-limit", type=int, default=30, help="Ek hesaplar için ortak web arama bütçesi (0–100, varsayılan 30)")
    p.add_argument("--no-other-accounts", action="store_true", help="Ek hesap aramasını kapat")
    p.add_argument("--output", type=Path, help="Yeni rapor klasörü")
    p.add_argument("--resume", type=Path, help="Son 24 saatte oluşturulan rapor klasörünü devam ettir")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    import math
    if (not all(math.isfinite(v) for v in [args.timeout, args.delay, args.settle, args.startup_timeout])
            or args.timeout < 5 or args.delay < 1 or args.settle < 2
            or not 5 <= args.startup_timeout <= 180
            or not 0 <= args.captcha_limit <= 100 or not 1 <= args.other_limit <= 20
            or not 0 <= args.web_search_limit <= 100
            or not 1 <= args.workers <= 6 or not 1 <= args.limit <= MAX_SITES):
        raise ValueError("workers: 1–6; limit: 1–200; other-limit: 1–20; web-search-limit ve captcha-limit: 0–100; timeout >= 5; startup-timeout: 5–180; delay >= 1, settle >= 2 olmalı; NaN/sonsuz değer kullanma")
    if args.output and args.resume:
        raise ValueError("--output ve --resume birlikte kullanılamaz")
    if args.browser_mode == "managed" and (args.chrome or args.chrome_version or args.driver):
        raise ValueError("--browser-mode managed ile --chrome, --chrome-version veya --driver birlikte kullanılmaz")
    sites, omitted = load_catalog(args.catalog, args.nsfw, args.include_excluded)
    sites = select_sites(sites, args.sites, args.limit)
    if args.list_sites:
        for index, name in enumerate(sites, 1):
            print(f"{index:3}. {name}")
        print(f"\n{len(sites)} site. Dışarıda: {omitted}")
        return 0
    nick = valid_nick((args.nickname or input("Aranacak nickname: ")).strip().removeprefix("@"))
    if not sites:
        raise ValueError("Taranacak site kalmadı")
    adapters = BUNDLED_ADAPTERS
    fingerprint = hashlib.sha256((json.dumps(sites, sort_keys=True) + json.dumps(list(sites))
                                  + json.dumps(adapters, sort_keys=True) + VERSION
                                  + str((args.no_other_accounts, args.other_limit, args.web_search_limit))).encode()).hexdigest()
    metadata = dict(catalog_sha256=fingerprint, site_count=len(sites), excluded=omitted,
                    engine="undetected-chromedriver", proxy=False, started_at=stamp(),
                    workers=args.workers, max_sites=MAX_SITES, site_order=list(sites), complete=False,
                    policy="any one positive; exact handle plus one profile field OR native account object; retry only on no positive; no negative controls; no identity attribution")
    metadata.update(worker_activity={}, peak_active_primary=0)
    results = {}
    if args.resume:
        out = args.resume.resolve()
        results, metadata["started_at"] = read_checkpoint(out, nick, fingerprint, sites)
    else:
        safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", nick)
        out = (args.output or ROOT / "reports" / f"{safe_name}_{datetime.now():%Y%m%d_%H%M%S}_{secrets.token_hex(2)}").resolve()
        if out.exists() and any(out.iterdir()):
            raise ValueError("Çıktı klasörü boş değil; yeni klasör veya --resume kullan")
    print(f"\nNickname OSINT {VERSION} | {len(sites)} site | {args.workers} paralel tarayıcı | proxyless")
    print("Tek başarılı kontrol = POZİTİF. İlkinde kanıt yoksa ikinci şans verilir. Giriş/CAPTCHA/erişim engeli = BELİRSİZ.")
    print(f"Rapor: {out}\n")
    stop = threading.Event()
    solver = CaptchaSolver(os.environ.get("NICKSCAN_2CAPTCHA_KEY", ""), args.captcha_limit, stop)
    diagnostics, diagnostics_lock = [], threading.Lock()
    def diagnostic(message):
        with diagnostics_lock:
            diagnostics.append(message if len(message) <= 12000 else message[:2000] + "\n...\n" + message[-9800:])
            del diagnostics[:-30]
    def sync_diagnostics():
        with diagnostics_lock:
            metadata["diagnostics"] = list(diagnostics)
    pool = DriverPool(stop, args.driver)
    def runtime_progress(message):
        print(message, flush=True)
        diagnostic(message)
    runtime = (BrowserRuntime(stop, args.browser_mode, runtime_progress)
               if args.browser_mode != "installed" and not (args.chrome or args.chrome_version or args.driver) else None)
    limiter = HostLimiter(args.delay, stop)
    web_search_budget = SearchBudget(args.web_search_limit)
    def factory(number, event):
        return Browser(timeout=args.timeout, settle=args.settle, chrome=args.chrome,
                       version=args.chrome_version, visible=args.show_browser, driver=args.driver,
                       pool=pool, worker=number, limiter=limiter, stop=event,
                       startup_timeout=args.startup_timeout, diagnostics=diagnostic,
                       captcha_solver=solver, other_accounts=not args.no_other_accounts, other_limit=args.other_limit,
                       runtime=runtime, web_search_budget=web_search_budget)
    reported_primary = set(results)
    def received(row, number):
        active_discovery = row.get("discovery_status") == "running"
        metadata["worker_activity"][str(number)] = dict(phase="discovery" if active_discovery else "idle", site=row["site"] if active_discovery else "")
        if row["site"] not in reported_primary:
            reported_primary.add(row["site"])
            print(f"[{len(results)}/{len(sites)} ana profil] [T{number}] {row['site']}: {LABELS[row['status']]} — {row['reason']}", flush=True)
        else:
            print(f"[T{number}] {row['site']}: diğer hesaplar güncellendi ({len(row.get('other_accounts', []))} aday)", flush=True)
        sync_diagnostics()
        write_reports(out, nick, results, metadata)
    def event(kind, number, value):
        mapping = {"starting": "starting", "ready": "idle", "checking": "primary", "discovering": "discovery", "idle": "idle", "done": "closed"}
        if kind in mapping:
            metadata["worker_activity"][str(number)] = dict(phase=mapping[kind], site=value if kind in {"starting", "checking", "discovering"} else "")
            active_primary = sum(x["phase"] == "primary" for x in metadata["worker_activity"].values())
            metadata["peak_active_primary"] = max(metadata["peak_active_primary"], active_primary)
        if kind == "starting":
            print(f"[T{number}] Chromium açılış sırasında...", flush=True)
        elif kind == "ready":
            print(f"[T{number}] Chromium hazır.", flush=True)
        elif kind == "checking":
            print(f"[T{number}] {value} — ana profil kontrol ediliyor...", flush=True)
        elif kind == "discovering":
            print(f"[T{number}] {value} — diğer hesaplar aranıyor...", flush=True)
        elif kind == "heartbeat":
            active = ", ".join(f"T{k}: {v['site']} ({'ana profil' if v['phase'] == 'primary' else 'diğer hesaplar'})"
                               for k, v in metadata["worker_activity"].items() if v["phase"] in {"primary", "discovery"})
            print(f"[Durum] Ana profiller {len(results)}/{len(sites)} | {active or 'Tarayıcı açılışı / bekleme'}", flush=True)
            sync_diagnostics()
            write_reports(out, nick, results, metadata)
        elif kind == "worker_error":
            print(f"[T{number}] Tarayıcı durdu: {value}", file=sys.stderr, flush=True)
    interrupted = False
    failure = None
    try:
        write_reports(out, nick, results, metadata)
        outcome = parallel_scan(sites, nick, adapters, results, args.workers, factory, received, event, stop)
        interrupted = outcome["interrupted"]
        metadata["worker_errors"] = outcome["worker_errors"]
        if len(results) < len(sites) and not interrupted:
            failure = "Çalışan tarayıcı kalmadı; tamamlanmamış siteler raporda yok. Hata nedenini düzeltip --resume kullan."
        elif outcome.get("discovery_pending", 0) and not interrupted:
            failure = "Ana profiller kaydedildi; bazı diğer hesap aramaları tamamlanamadı. --resume ile devam edebilirsin."
    except KeyboardInterrupt:
        interrupted = True
        print("\nDurduruldu; tamamlanan sonuçlar kaydediliyor.")
    except Exception as exc:
        failure = f"{type(exc).__name__}: {exc}"
        print(f"\nTarama durdu: {failure}", file=sys.stderr)
        print("Chrome kurulumunu/sürümünü kontrol et. Mevcut sonuçlar korunuyor.", file=sys.stderr)
    finally:
        stop.set()
        pool.close()
        if runtime is not None:
            runtime.close()
        metadata["complete"] = len(results) == len(sites) and not failure and not interrupted
        if failure:
            metadata["error"] = failure
        sync_diagnostics()
        try:
            write_reports(out, nick, results, metadata)
        except OSError as exc:
            failure = f"Rapor kaydedilemedi: {exc}"
            print(failure, file=sys.stderr)
    if failure:
        print(failure, file=sys.stderr)
    print("\n" + " | ".join(f"{LABELS[k]}: {v}" for k, v in Counter(r["status"] for r in results.values()).items()))
    if (out / "index.html").exists():
        print(f"Raporu aç: {out / 'index.html'}")
    return 1 if failure else 130 if interrupted else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        raise SystemExit(2)
