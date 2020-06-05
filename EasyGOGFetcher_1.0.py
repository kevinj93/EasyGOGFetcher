import os
import re
import shutil
import html

print('Easy GOG Fetcher for gog-games.com')
print('Version 1.0 \n')
print('By kevinj93 \n')

for folder in os.listdir():
    if 'GOG_HTML' in folder:
        shutil.rmtree('GOG_HTML')

os.mkdir('GOG_HTML')

shutil.copy('wget.exe', './GOG_HTML/wget.exe')

os.chdir('GOG_HTML')


def gen_any_pages(no_pages):
    page_links = []
    page_fetch_format_prefix = 'https://gog-games.com/search/all/'
    page_fetch_format_suffix = '/date/desc/any'

    for i in range(1, no_pages + 1):
        page_links.append(page_fetch_format_prefix + str(i) + page_fetch_format_suffix)
    return page_links


def ren_dl_pages():  # rename download pages
    page_suffix = 1
    for file in os.listdir():
        if 'any' in file:
            os.rename(file, 'any_' + str(page_suffix) + '.html')
            page_suffix += 1


def get_game_pages():
    game_pages = []

    for file in os.listdir():
        if 'any' in file:
            pagehandle = open(file, 'r', encoding='utf8')
            pagereader = pagehandle.readlines()
            for line in pagereader:
                indices = [m.start() for m in re.finditer('/game/', line)]
                for index in indices:
                    current_game_start = line[index:]
                    current_game_end = current_game_start.index("\"")
                    game_pages.append('https://gog-games.com' + current_game_start[:current_game_end])
    return game_pages


def rename_game_pages():
    for file in os.listdir():  # rename game files
        if not os.path.isdir(file) and '.' not in file:
            os.rename(file, file + '.html')


def get_dl_links_gamepage(gn=False):
    gamelinks = []
    multifilemirrorlinks = []
    for filename in os.listdir():

        if '.txt' not in filename and '.exe' not in filename and 'wget' not in filename:
            file = open(filename, 'r', encoding='utf8')
            freader = file.read().splitlines()
            if gn == True:
                starttag = ('<title>')
                endtag = (' - GOG Games</title>')
                for line in freader:
                    if'<title>' in line:
                        gamename = html.unescape(line.lstrip()[len(starttag):len(line)-len(endtag)-2])
                        gamelinks.append('\n\n' + gamename + '\n\n')
                        multifilemirrorlinks.append('\n\n' + gamename + '\n\n')
            for line in freader:
                if 'zippyshare' in line and 'game' in line and 'Open all Links' not in line and 'extras-' not in line:
                    start = line.index('href=\"')
                    end = line.index(" target")
                    gamelinks.append(line[start + 6:end - 1] + '\n')
                if 'multifilemirror' in line and 'game' in line and 'Open all Links' not in line and 'extras-' not in line:
                    start = line.index('href=\"')
                    end = line.index(" target")
                    multifilemirrorlinks.append(line[start + 6:end - 1] + '\n')
    return gamelinks, multifilemirrorlinks


print('Please Specify the number of pages to fetch.')
user_answered = False
while not user_answered:
    try:
        userchoice = int(input(''))
        user_answered = True
    except:
        print('Invalid value, please try again')

print('General Cleanup ...')
for junk in os.listdir():
    if 'wget' not in junk:
        os.remove(junk)

for index, link in enumerate(gen_any_pages(userchoice)):  # generate game pages
    print('Fetching "any" pages ...')
    print(str(index + 1) + '/' + str(userchoice))
    os.system('wget ' + link + ' >nul 2> nul')
    os.system('cls')

print('Fixing "any" Page names ...')
ren_dl_pages()

print('Getting game links from "any" pages...')
game_links = get_game_pages()  # game links from each page

for index, game in enumerate(game_links):  # get games html pages
    print('Fetching game pages ...')
    print(str(index + 1) + '/' + str(len(game_links)))
    os.system('wget ' + game + ' >nul 2> nul')
    os.system('cls')


print('Cleaning up "any" pages...')
for file in os.listdir():  # any_pages cleanup
    if 'any_' in file:
        os.remove(file)

print('Fixing game page names...')
rename_game_pages()  # rename game pages to proper html files

glinks = open('zippyshare_links.txt', 'w')
glinks_raw = open('zippyshare_links_raw.txt', 'w')

glinks_mfm = open('multifilemirror_links.txt', 'w')
glinks_mfm_raw = open('multifilemirror_links_raw.txt', 'w')

glinks.write('Zippyshare links: \n')
glinks_raw.write('Zippyshare raw links: \n')

glinks_mfm.write('Multifilemirror links: \n')
glinks_mfm_raw.write('Multifilemirror raw links: \n')

print('Writing Links to file ...')
for gamelink in get_dl_links_gamepage(True)[0]:
    glinks.write(gamelink)
for gamelink in get_dl_links_gamepage()[0]:
    glinks_raw.write(gamelink)

for gamelink in get_dl_links_gamepage(True)[1]:
    glinks_mfm.write(gamelink)
for gamelink in get_dl_links_gamepage()[1]:
    glinks_mfm_raw.write(gamelink)

open_handles = [glinks, glinks_raw, glinks_mfm, glinks_mfm_raw]

for handle in open_handles:
    handle.close()

shutil.move('zippyshare_links.txt', '../zippyshare_links.txt')
shutil.move('zippyshare_links_raw.txt', '../zippyshare_links_raw.txt')
shutil.move('multifilemirror_links.txt', '../multifilemirror_links.txt')
shutil.move('multifilemirror_links_raw.txt', '../multifilemirror_links_raw.txt')

print('Cleaning up temporary files ...')

for file in os.listdir():
        os.remove(file)

os.chdir('../')
os.rmdir('GOG_HTML')

print('Zippyshare and Multifilemirror links saved in the same folder as the script.')

print('\n Done! Press any key to exit')
os.system('pause >nul')
