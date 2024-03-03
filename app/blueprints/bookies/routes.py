from . import bookies
from flask import render_template, request, redirect, url_for, flash
from .forms import SearchInput, ChatInput
from flask_login import current_user, login_required, LoginManager
from app.models import db, User, Book 
import requests

from openai import OpenAI
client = OpenAI()


# Home route, greeting page
@bookies.route('/')
def home():
    return render_template('home.html')


# Google Books API function and route to get and return info
# Authors and sometimes Image breaking

def search(searchstr):
    url = f'https://www.googleapis.com/books/v1/volumes?q={searchstr}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        top_five_books = []
        i = 0
        while len(top_five_books) < 5:
            try:
                info_dict = {
                    'id' : data['items'][i]['id'],
                    'title': data['items'][i]['volumeInfo']['title'],
                    'authors': data['items'][i]['volumeInfo']['authors'],
                    'smallThumbnail': data['items'][i]['volumeInfo']['imageLinks']['smallThumbnail'],
                    'thumbnail': data['items'][i]['volumeInfo']['imageLinks']['thumbnail']
                }
                top_five_books.append(info_dict)
                i+=1
            except:
                i+=1
        return top_five_books
    return "No books found."

@bookies.route('/find', methods=['GET','POST'])
def find():
    find_form = SearchInput()
    chat_form = ChatInput()
    if request.method == 'POST' and find_form.validate_on_submit():
        user_input = find_form.search_str.data
        top_five_books = search(user_input)
        if find_form.submit_btn.data:
            return render_template('find.html', top_five_books=top_five_books, find_form=find_form)
        # if form.catch_btn.data:
        #     if not Pokemon.query.get(pokedata['name']):
        #         newpoke = Pokemon(pokedata['name'], pokedata['hp'], pokedata['attack'], pokedata['defense'], pokedata['sprite_img'])
        #         newpoke.save()
        #     if pokedata['name'] in current_user.caught_pokemon or len(current_user.caught_pokemon.all()) >= 6:
        #         flash(f'Pokemon already caught! Release one to catch another.', 'danger')
        #         return redirect(url_for('pokesearch.get_pokemon'))
        #     else:
        #         caughtpoke = Pokemon.query.get(pokedata['name'])
        #         current_user.caught_pokemon.append(caughtpoke)
        #         print(caughtpoke)
        #         db.session.commit()
        #         flash(f'{caughtpoke.name} caught!', 'success')
        #         return redirect(url_for('pokesearch.get_pokemon'))
    else:
        return render_template('find.html', find_form=find_form, chat_form=chat_form)


# @pokesearch.route('/release/<poke_name>')
# @login_required
# def release(poke_name):
#     releasepoke = Pokemon.query.filter(Pokemon.name==poke_name).first()
#     current_user.caught_pokemon.remove(releasepoke)
#     db.session.commit()
#     flash(f'{poke_name} has been released!', 'success')
#     return redirect(url_for('pokesearch.get_pokemon'))

# @pokesearch.route('/battlehome')
# @login_required
# def battlehome():
#     otherusers = User.query.filter(User.id != current_user.id)
#     users = []
#     for user in otherusers:
#         if len(user.caught_pokemon.all()) == 6:
#             users.append(user)
#     return render_template('battlehome.html', users=users)

# @pokesearch.route('/vs/<user_id>')
# @login_required
# def vs(user_id):
#         opponent = User.query.get(user_id)
#         return render_template('vs.html', opponent=opponent)

# @pokesearch.route('/finishedvs/<opponent>')
# @login_required
# def finishedvs(opponent):
#         opp = User.query.get(opponent)
#         o_p_list = opp.caught_pokemon.all()
#         opp_total_hp = 0
#         opp_total_defense = 0
#         opp_total_attack = 0
#         for p in o_p_list:
#             opp_total_hp += p.hp
#             opp_total_defense += p.defense
#             opp_total_attack += p.attack
#         cu_p_list = current_user.caught_pokemon.all()
#         cu_total_hp = 0
#         cu_total_defense = 0
#         cu_total_attack = 0
#         for p in cu_p_list:
#             cu_total_hp += p.hp
#             cu_total_defense += p.defense
#             cu_total_attack += p.attack

#         ## TOTAL HP - (TOTAL ATTACK undergone - TOTAL DEFENSE) = FINAL HP
#         cu_final_hp = cu_total_hp - (opp_total_attack - cu_total_defense)
#         opp_final_hp = opp_total_hp - (cu_total_attack - opp_total_defense)

#         ## GREATER FINAL HP WINS
#         if cu_final_hp > opp_final_hp:
#             flash(f'{current_user.username} won!', 'success')
#             return render_template('finishedvs.html', opponent=opp)
#         elif cu_final_hp == opp_final_hp:
#             flash("It's a tie!", 'success')
#             return render_template('finishedvs.html', opponent=opp)
#         else:
#             flash(f'{opp.username} won!', 'danger')
#             return render_template('finishedvs.html', opponent=opp)

    
@bookies.route('/chat', methods=['POST'])
def chat():
    find_form = SearchInput()
    chat_form = ChatInput()
    if request.method == 'POST' and chat_form.validate_on_submit():
        user_message = chat_form.chat_input.data
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful librarian, giving concise but descriptive responses"},
                {"role": "user", "content": user_message},
            ],
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        chat_response = completion.choices[0].message.content
    return render_template('find.html', find_form=find_form, chat_form=chat_form, chat_response=chat_response)