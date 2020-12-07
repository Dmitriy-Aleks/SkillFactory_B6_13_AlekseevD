from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album

# Вывод результатов запроса альбомов исполнителя
@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено!".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "<h2>Список альбомов {}:</h2>".format(artist)
        result += "<br />".join(album_names)
        result += "<br /><br /><i>Количество альбомов <b>{}</b>: {}</i>".format(artist,len(album_names))
    return result

@route("/albums", method="POST")
def new_album():
    """
    POST-запрос для добавления данных об альбоме в БД.
    Если такой альбом уже есть в базе данных, то выводится ошибка 409
    Перед сохранением, данные валидируются.
    """

    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }

    for key, value in album_data.items():
        valid, message = album.album_validation(key, value)
        if not valid:
            return HTTPError(449, message)

    existing_album = album.find_album(album_data)
    if existing_album:
        return HTTPError(409, "Данный альбом уже существует в базе данных. Его id - {}.".format(existing_album.id))


    added_album = album.add_album(album_data)
    if added_album:
        
        return "Данные об альбоме успешно сохранены"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)