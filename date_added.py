
from plexapi import *
from plexapi.myplex import MyPlexAccount
from simple_term_menu import TerminalMenu
import sqlite3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"{bcolors.HEADER}Hello and welcome to this awesome date added editor{bcolors.ENDC}")

def spacer():
    print("")
    print("------------")
    print("")

def menuPicker(list):
    listStrings= []
    for item in list:
        listStrings.append(item.title)

    terminal_menu = TerminalMenu(listStrings)
    index = terminal_menu.show()
    print(f"{bcolors.OKGREEN}You selected {listStrings[index]}!{bcolors.ENDC}")
    return listStrings[index]

username = input("Enter your username: (slattery.75@osu.edu)") or "slattery.75@osu.edu"
password = input("Enter your password: (jacksfriendswatchmovies)") or "jacksfriendswatchmovies"
serverip = input("Enter your server ip: (CRUCIAL_CONTROL_WARD)") or "CRUCIAL_CONTROL_WARD"

print('Logging you in..')

spacer()

account = MyPlexAccount(username, password)
plex = account.resource(serverip).connect()

if(plex != None):
    print(f"{bcolors.OKGREEN}Successfully logged in.{bcolors.ENDC}")

spacer()

chosenLibraryTitle = menuPicker(plex.library.sections())
chosenLibraryKey = str(plex.library.section(chosenLibraryTitle).key)

spacer()

methodIndex = TerminalMenu(["Pick from list of movies (ordered by date added)","Search for a movie(exact name)"]).show()

if(methodIndex == 0):
    chosenMovieTitle = menuPicker(plex.library.section(chosenLibraryTitle).search(sort="addedAt:desc"))
else:
    print("search")

con = sqlite3.connect('/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db')
cursor = con.cursor()
cursor.execute("SELECT added_at FROM metadata_items WHERE title = \""+chosenMovieTitle+"\" and library_section_id = "+chosenLibraryKey)
print(chosenMovieTitle+"\'s current added date is: "+ cursor.fetchone()[0])

print("Does this look like the correct date?")
methodIndex = TerminalMenu(["Yes","No"]).show()

if(methodIndex == 0):
    # cursor.execute("select * from sqlite_master where type = 'trigger';")
    # triggers = cursor.fetchall()
    # for trig in triggers:
    #     print(trig)
    print("Enter a new DateTime value: ")
    newDateTime = input()
    cursor.execute("DROP TRIGGER fts4_metadata_titles_before_update_icu;")
    cursor.execute("DROP TRIGGER fts4_metadata_titles_after_update_icu;")
    cursor.execute("UPDATE metadata_items SET added_at = \""+newDateTime+"\" WHERE title = \""+chosenMovieTitle+"\" and library_section_id = "+chosenLibraryKey)
    cursor.execute("UPDATE metadata_items SET added_at = \""+newDateTime+"\" WHERE title = \""+chosenMovieTitle+"\" and metadata_type = 12 and media_item_count = 3")
    cursor.execute("SELECT added_at FROM metadata_items WHERE title = \""+chosenMovieTitle+"\" and metadata_type = 12 and media_item_count = 3")
    print(chosenMovieTitle+"\'s added date is NOW: "+ cursor.fetchone()[0])
    cursor.execute("CREATE TRIGGER fts4_metadata_titles_before_update_icu BEFORE UPDATE ON metadata_items BEGIN DELETE FROM fts4_metadata_titles_icu WHERE docid=old.rowid; END")
    cursor.execute("CREATE TRIGGER fts4_metadata_titles_after_update_icu AFTER UPDATE ON metadata_items BEGIN INSERT INTO fts4_metadata_titles_icu(docid, title, title_sort, original_title) VALUES(new.rowid, new.title, new.title_sort, new.original_title); END")
    con.commit()
    con.close()
else:
    cursor.execute("SELECT added_at FROM metadata_items WHERE title = \""+chosenMovieTitle+"\" AND metadata_type = 12 AND media_item_count = 3")
    print(chosenMovieTitle+"\'s added date is NOW: "+ cursor.fetchone()[0])
    print("Bye")
