import os, sys, json, re, time, urllib.request, base64
from concurrent.futures import ThreadPoolExecutor
import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

THEME_DIR = '/home/yorx/.icons/Liquid-Glass-Dark'
APPS_DIR = os.path.join(THEME_DIR, 'apps', 'scalable')
CACHE_DIR = '/tmp/liquid_glass_cache'
os.makedirs(CACHE_DIR, exist_ok=True)

with open('/tmp/macos_liquid_glass_complete.json') as f:
    hits = json.load(f)

print(f"Loaded {len(hits)} hits from local dataset")

# Build lookup catalogs
app_catalog = {}
slug_catalog = {}

for h in hits:
    name = h.get('appName', '').strip()
    dl = h.get('downloads', 0)
    if not name:
        continue
    key = name.lower()
    if key not in app_catalog or dl > app_catalog[key].get('downloads', 0):
        app_catalog[key] = h

    clean = re.sub(r'\(?liquid\s*glass\)?|\(dark\)|\(light\)|\-dark|\-light|dark|light|macos|ios|default|\bnew\b', '', name, flags=re.I)
    clean = clean.strip(' -_()')
    slug = re.sub(r'[^a-z0-9]', '', clean.lower())
    if len(slug) >= 3:
        if slug not in slug_catalog or dl > slug_catalog[slug].get('downloads', 0):
            slug_catalog[slug] = h

def find_best(pattern, preferred_users=['adrian', 'tochii', 'wonki', 'p1xelz', 'hectorlizard', 'designer_26.2', 'appmaker', 'kmiarthur']):
    candidates = []
    regex = re.compile(pattern, re.I)
    for k, h in app_catalog.items():
        if regex.search(k):
            score = h.get('downloads', 0)
            if h.get('usersName') in preferred_users:
                score *= 1.5
            candidates.append((score, h))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    return None

def direct_search(query):
    try:
        body = {
            'query': query,
            'searchOptions': {
                'hitsPerPage': 3,
                'page': 1,
                'sort': ['downloads:desc']
            }
        }
        req = urllib.request.Request(
            'https://macosicons.com/api/search',
            headers={
                'Content-Type': 'application/json',
                'Referer': 'https://macosicons.com/',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            },
            data=json.dumps(body).encode('utf-8')
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', [])
            return hits[0] if hits else None
    except Exception as e:
        print(f"Direct search error for {query}: {e}")
        return None

# Hand-curated mappings
curated = {
    # System & Core
    "file-manager.svg": (["system-file-manager.svg", "org.gnome.Nautilus.svg", "nautilus.svg", "org.xfce.thunar.svg", "thunar.svg", "org.kde.dolphin.svg", "dolphin.svg", "nemo.svg", "caja.svg", "pcmanfm.svg"], r"finder beta 2|finder"),
    "terminal.svg": (["utilities-terminal.svg", "org.gnome.Terminal.svg", "gnome-terminal.svg", "org.kde.konsole.svg", "konsole.svg", "xfce4-terminal.svg", "xterm.svg", "terminator.svg", "tilix.svg"], r"terminal app liquid glass|terminal"),
    "alacritty.svg": (["Alacritty.svg", "alacritty-term.svg"], "direct:alacritty"),
    "kitty.svg": ([], r"\bkitty\b"),
    "warp.svg": (["warp-terminal.svg"], r"\bwarp\b"),
    "preferences-system.svg": (["preferences_system.svg", "org.gnome.Settings.svg", "gnome-control-center.svg", "systemsettings.svg", "xfce-settings-manager.svg", "kcontrol.svg"], r"gnome settings|system settings|settings"),
    "softwarecenter.svg": (["gnome-software.svg", "org.gnome.Software.svg", "pamac-manager.svg", "org.kde.discover.svg", "software.svg", "muondiscover.svg"], r"app store.*tahoe|app store"),
    "calc.svg": (["accessories-calculator.svg", "org.gnome.Calculator.svg", "gnome-calculator.svg", "kcalc.svg", "galculator.svg"], r"calculator"),
    "calendar.svg": (["org.gnome.Calendar.svg", "gnome-calendar.svg", "korganizer.svg"], r"notion calendar|calendar"),
    "accessories-text-editor.svg": (["text-editor.svg", "org.gnome.TextEditor.svg", "gedit.svg", "org.gnome.gedit.svg", "org.xfce.mousepad.svg", "mousepad.svg", "kwrite.svg", "kate.svg"], r"\bnotes\b|text editor"),
    "accessories-document-viewer.svg": (["org.gnome.Evince.svg", "evince.svg", "okular.svg", "xreader.svg", "qpdfview.svg", "org.xfce.ristretto.svg"], r"preview ios 26|preview"),
    "file-roller.svg": (["accessories-archiver.svg", "org.gnome.ArchiveManager.svg", "org.kde.ark.svg", "ark.svg", "7zip.svg"], r"the unarchiver|7zip|archive"),
    "org.gnome.clocks.svg": (["gnome-clocks.svg", "alarm-clock.svg"], r"clock"),
    "gnome-weather.svg": (["org.gnome.Weather.svg", "weather.svg"], r"weather-liquid glass|weather"),
    "gnome-maps.svg": (["org.gnome.Maps.svg"], r"google maps|maps"),
    "gnome-contacts.svg": (["org.gnome.Contacts.svg", "x-office-address-book.svg"], r"gnome contacts|contacts"),
    "user-trash.svg": (["trash.svg", "user-trash-full.svg", "trashcan_full.svg", "trashcan_empty.svg"], r"trash-full|trash"),
    "applets-screenshooter.svg": (["org.gnome.Screenshot.svg", "spectacle.svg", "screen-recorder.svg"], r"tahoe camera|camera|screenshot"),
    
    # Browsers
    "firefox.svg": (["org.mozilla.firefox.svg", "firefox-bin.svg"], r"firefox \(liquid glass\)|firefox"),
    "google-chrome.svg": (["chrome.svg", "chromium.svg", "chromium-browser.svg"], r"google chrome \(liquid glass\)|chrome"),
    "brave.svg": (["brave-browser.svg", "brave-beta.svg", "brave-nightly.svg"], r"brave \(dark\)|brave"),
    "microsoft-edge.svg": (["ms-edge.svg"], r"edge"),
    "safari.svg": (["web-browser.svg", "browser.svg", "internet-web-browser.svg"], r"safari \(liquid glass\)|safari"),
    "arc.svg": (["arc-browser.svg"], r"arc liquid glass|arc"),
    "tor-browser.svg": (["tor.svg"], "direct:tor browser"),
    "librewolf.svg": ([], r"librewolf"),

    # Office & Productivity
    "libreoffice-writer.svg": (["libreoffice3-writer.svg", "org.libreoffice.LibreOffice.writer.svg", "ms-word.svg", "word.svg"], r"microsoft word|pages"),
    "libreoffice-calc.svg": (["libreoffice3-calc.svg", "org.libreoffice.LibreOffice.calc.svg", "ms-excel.svg", "excel.svg"], r"microsoft excel|numbers"),
    "libreoffice-impress.svg": (["org.libreoffice.LibreOffice.impress.svg", "ms-powerpoint.svg", "powerpoint.svg"], r"microsoft powerpoint|keynote"),
    "libreoffice-draw.svg": (["org.libreoffice.LibreOffice.draw.svg"], r"keynote|draw"),
    "notion.svg": (["notion-app.svg"], r"notion \| liquid glass|notion"),
    "obsidian.svg": (["md.obsidian.Obsidian.svg"], r"obsidian \(dark\)|obsidian"),
    "craft.svg": ([], "direct:craft"),
    "thunderbird.svg": (["org.mozilla.Thunderbird.svg", "emblem-mail.svg"], r"gmail|proton mail|mail"),
    "1password.svg": ([], r"1password"),
    "bitwarden.svg": ([], r"bitwarden"),

    # Developers
    "visual-studio-code.svg": (["vscode.svg", "code.svg", "code-oss.svg", "vscodium.svg", "com.visualstudio.code.svg"], r"visual studio code|vs code"),
    "sublime-text.svg": (["sublime.svg", "sublime_text.svg"], r"sublime text|code editor app"),
    "pycharm.svg": (["jetbrains-pycharm.svg", "pycharm-community.svg"], r"pycharm"),
    "idea.svg": (["jetbrains-idea.svg", "intellij.svg", "intellij-idea-community.svg"], r"intellij idea|idea"),
    "android-studio.svg": ([], r"android studio"),
    "docker.svg": (["docker-desktop.svg"], r"\bdocker\b"),
    "postman.svg": ([], r"postman"),
    "github.svg": (["github-desktop.svg"], r"\bgithub\b"),

    # Social & Chat
    "discord.svg": (["com.discordapp.Discord.svg"], r"discord \(dark\)|discord"),
    "telegram.svg": (["org.telegram.desktop.svg", "telegram-desktop.svg"], r"telegram dark mono|telegram"),
    "whatsapp.svg": (["whatsapp-desktop.svg"], r"whatsapp \(liquid glass\)|whatsapp"),
    "slack.svg": (["com.slack.Slack.svg"], r"\bslack\b"),
    "signal.svg": (["signal-desktop.svg", "org.thoughtcrime.securesms.Signal.svg"], r"signal"),
    "zoom.svg": (["zoom-desktop.svg", "us.zoom.Zoom.svg"], r"zoom \(liquid glass\)|zoom"),
    "teams.svg": (["microsoft-teams.svg", "ms-teams.svg"], r"teams \(dark\)|teams"),
    "skype.svg": (["skypeforlinux.svg"], "direct:skype"),
    "wechat.svg": (["electronic-wechat.svg"], r"wechat"),
    "instagram.svg": ([], r"instagram"),
    "tiktok.svg": ([], r"tiktok"),

    # Media & Audio
    "spotify-client.svg": (["spotify.svg", "spotify-launcher.svg", "com.spotify.Client.svg"], r"spotify \| liquid glass|spotify"),
    "vlc.svg": (["org.videolan.VLC.svg"], r"vlc \(liquid glass\)|vlc"),
    "mpv.svg": (["io.mpv.Mpv.svg", "media-player.svg", "org.xfce.parole.svg"], r"iina|mpv"),
    "audacity.svg": (["org.audacityteam.Audacity.svg"], r"audacity"),
    "youtube.svg": (["youtube-music.svg", "com.github.th_ch.youtube_music.svg", "app.ytmdesktop.ytmdesktop.svg"], r"youtube music|youtube"),
    "netflix.svg": ([], r"netflix \(liquid glass\)|netflix"),
    "stremio.svg": (["com.stremio.Stremio.svg"], r"stremio"),
    "obs.svg": (["obs-studio.svg", "com.obsproject.Studio.svg"], r"obs studio"),

    # Creative
    "blender.svg": (["org.blender.Blender.svg"], r"blender \(dark\)|blender"),
    "gimp.svg": (["org.gimp.GIMP.svg"], r"gimp"),
    "inkscape.svg": (["org.inkscape.Inkscape.svg"], r"inkscape"),
    "figma.svg": (["figma-linux.svg"], r"\bfigma\b"),
    "canva.svg": ([], r"\bcanva\b"),
    "photoshop.svg": ([], r"photoshop"),
    "illustrator.svg": ([], r"illustrator"),

    # Gaming & AI
    "steam.svg": (["steam-launcher.svg", "steam-native.svg"], r"steam \(liquid glass\)|steam"),
    "minecraft.svg": ([], "direct:minecraft"),
    "roblox.svg": ([], r"roblox"),
    "transmission.svg": (["transmission-gtk.svg", "transmission-qt.svg"], r"transmission"),
    "qbittorrent.svg": (["org.qbittorrent.qBittorrent.svg"], r"qbittorrent"),
    "chatgpt.svg": (["chat-gpt.svg", "openai.svg"], r"chatgpt \(dark\)|chatgpt"),
    "claude.svg": ([], r"claude \(dark\)|claude"),
    "gemini.svg": (["google-gemini.svg"], r"gemini"),
}

# Resolve all mappings
resolved_actions = [] # list of (primary_file, aliases, hit_dict)
used_primaries = set()

for primary, (aliases, pat) in curated.items():
    hit = None
    if isinstance(pat, str) and pat.startswith("direct:"):
        hit = direct_search(pat[7:])
    else:
        hit = find_best(pat)
    if hit:
        resolved_actions.append((primary, aliases, hit))
        used_primaries.add(primary)
        for a in aliases:
            used_primaries.add(a)
    else:
        print(f"Warning: Could not resolve curated app {primary}")

# Add slug matches from scalable apps that haven't been resolved
for f in os.listdir(APPS_DIR):
    if f in used_primaries:
        continue
    base = os.path.splitext(f)[0]
    base_slug = re.sub(r'[^a-z0-9]', '', base.lower())
    if base_slug in slug_catalog:
        hit = slug_catalog[base_slug]
        resolved_actions.append((f, [], hit))
        used_primaries.add(f)

print(f"Total applications planned for Liquid Glass replacement: {len(resolved_actions)}")

# Gather unique icons to download
unique_downloads = {}
for primary, aliases, hit in resolved_actions:
    oid = hit.get('objectID')
    url = hit.get('iOSUrl') or hit.get('icnsUrl')
    if oid and url and oid not in unique_downloads:
        unique_downloads[oid] = (url, hit.get('appName'))

print(f"Total unique PNGs to download: {len(unique_downloads)}")

def download_and_scale(item):
    oid, (url, app_name) = item
    cache_path = os.path.join(CACHE_DIR, f"{oid}.png")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        return oid, True

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()

        # Parse with GdkPixbuf and scale to 512x512
        loader = GdkPixbuf.PixbufLoader()
        loader.write(data)
        loader.close()
        pixbuf = loader.get_pixbuf()
        if not pixbuf:
            return oid, False

        # Scale
        scaled = pixbuf.scale_simple(512, 512, GdkPixbuf.InterpType.HYPER)
        scaled.savev(cache_path, 'png', [], [])
        return oid, True
    except Exception as e:
        print(f"Error downloading {app_name} ({url}): {e}")
        return oid, False

print("Starting concurrent downloads...")
start_t = time.time()
with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(download_and_scale, unique_downloads.items()))

success_count = sum(1 for _, s in results if s)
print(f"Downloaded and scaled {success_count}/{len(unique_downloads)} icons in {time.time() - start_t:.1f}s")

# Helper to create SVG from cached PNG
def make_svg(png_path):
    with open(png_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" width="100%" height="100%">
  <image width="512" height="512" href="data:image/png;base64,{b64}"/>
</svg>'''

installed_count = 0
symlinks_count = 0

for primary, aliases, hit in resolved_actions:
    oid = hit.get('objectID')
    cache_path = os.path.join(CACHE_DIR, f"{oid}.png")
    if not os.path.exists(cache_path):
        continue

    svg_content = make_svg(cache_path)
    primary_path = os.path.join(APPS_DIR, primary)

    # If it was a symlink, remove it so we can write real file
    if os.path.islink(primary_path):
        os.unlink(primary_path)

    with open(primary_path, 'w') as f:
        f.write(svg_content)
    installed_count += 1

    # Now create/update all aliases as symlinks pointing to primary
    for alias in aliases:
        alias_path = os.path.join(APPS_DIR, alias)
        if os.path.islink(alias_path) or os.path.exists(alias_path):
            os.unlink(alias_path)
        os.symlink(primary, alias_path)
        symlinks_count += 1

print(f"Successfully installed {installed_count} primary Liquid Glass icons and created {symlinks_count} symlinks!")
