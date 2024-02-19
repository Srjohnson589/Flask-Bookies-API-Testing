import requests

def find_book(searchstr):
    url = f'https://www.googleapis.com/books/v1/volumes?q={searchstr}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        top_five_books = []
        for i in range(0, 5):
            info_dict = {
                'id' : data['items'][i]['id'],
                'title': data['items'][i]['volumeInfo']['title'],
                'authors': data['items'][i]['volumeInfo']['authors'],
                'smallThumbnail': data['items'][i]['volumeInfo']['imageLinks']['smallThumbnail'],
                'thumbnail': data['items'][i]['volumeInfo']['imageLinks']['thumbnail']
            }
            top_five_books.append(info_dict)
        return top_five_books
    return "No books found."
