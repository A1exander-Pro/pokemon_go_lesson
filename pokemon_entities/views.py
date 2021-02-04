import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import *

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],

        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_entity = PokemonEntity.objects.all()
    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        try:
            pokemons_on_page.append({
                "pokemon_id": pokemon.id,
                "img_url": pokemon.image.url,
                "title_ru": pokemon.title,
            })
        except:
            pass

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon.objects.all(), id=pokemon_id)
    pokemon_attributes = {}
    requested_pokemon = pokemon
    entity = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": pokemon.image.url,

    }
    pokemon_attributes.update(entity)

    if pokemon.previous_evolution:
        previous_evolution = {"previous_evolution": {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": pokemon.previous_evolution.image.url,
        }}
        pokemon_attributes.update(previous_evolution)
    else:
        pass

    try:
        pokemon_evolution = requested_pokemon.evolution.get()
    except Pokemon.DoesNotExist:
        pokemon_evolution = None

    if pokemon_evolution:
        next_evolution = {"next_evolution": {
            "title_ru": pokemon_evolution.title,
            "pokemon_id": pokemon_evolution.id,
            "img_url": pokemon_evolution.image.url,
        }}
        pokemon_attributes.update(next_evolution)
    else:
        pass

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_entity = pokemon.entities.all()
    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_attributes})
