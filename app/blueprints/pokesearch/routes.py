from . import pokesearch
from flask import render_template, request, redirect, url_for, flash
from .forms import PokemonInput
from flask_login import current_user, login_required, LoginManager
from app.models import db, Pokemon, User, user_pokemon
import requests


# Home route, greeting page
@pokesearch.route('/')
def home():
    return render_template('home.html')


# Google Books API function and route to get and return info
def search(searchstr):
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

@pokesearch.route('/find', methods=['GET','POST'])
def find():
    form = SearchInput()
    if request.method == 'POST' and form.validate_on_submit():
        user_input = form.search_str.data
        top_five_books = search(pokemon)
        if form.submit_btn.data:
            return render_template('find.html', top_five_books=top_five_books, form=form)
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
        return render_template('find.html', form=form)


@pokesearch.route('/release/<poke_name>')
@login_required
def release(poke_name):
    releasepoke = Pokemon.query.filter(Pokemon.name==poke_name).first()
    current_user.caught_pokemon.remove(releasepoke)
    db.session.commit()
    flash(f'{poke_name} has been released!', 'success')
    return redirect(url_for('pokesearch.get_pokemon'))

@pokesearch.route('/battlehome')
@login_required
def battlehome():
    otherusers = User.query.filter(User.id != current_user.id)
    users = []
    for user in otherusers:
        if len(user.caught_pokemon.all()) == 6:
            users.append(user)
    return render_template('battlehome.html', users=users)

@pokesearch.route('/vs/<user_id>')
@login_required
def vs(user_id):
        opponent = User.query.get(user_id)
        return render_template('vs.html', opponent=opponent)

@pokesearch.route('/finishedvs/<opponent>')
@login_required
def finishedvs(opponent):
        opp = User.query.get(opponent)
        o_p_list = opp.caught_pokemon.all()
        opp_total_hp = 0
        opp_total_defense = 0
        opp_total_attack = 0
        for p in o_p_list:
            opp_total_hp += p.hp
            opp_total_defense += p.defense
            opp_total_attack += p.attack
        cu_p_list = current_user.caught_pokemon.all()
        cu_total_hp = 0
        cu_total_defense = 0
        cu_total_attack = 0
        for p in cu_p_list:
            cu_total_hp += p.hp
            cu_total_defense += p.defense
            cu_total_attack += p.attack

        ## TOTAL HP - (TOTAL ATTACK undergone - TOTAL DEFENSE) = FINAL HP
        cu_final_hp = cu_total_hp - (opp_total_attack - cu_total_defense)
        opp_final_hp = opp_total_hp - (cu_total_attack - opp_total_defense)

        ## GREATER FINAL HP WINS
        if cu_final_hp > opp_final_hp:
            flash(f'{current_user.username} won!', 'success')
            return render_template('finishedvs.html', opponent=opp)
        elif cu_final_hp == opp_final_hp:
            flash("It's a tie!", 'success')
            return render_template('finishedvs.html', opponent=opp)
        else:
            flash(f'{opp.username} won!', 'danger')
            return render_template('finishedvs.html', opponent=opp)

    
