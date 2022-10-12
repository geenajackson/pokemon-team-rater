const BASE_URL = "https://pokeapi.co/api/v2"
const $pokemonSearch = $("#pokemon-search")
const $term = $("#autocomplete")
const $pokemonDisplay = $("#pokemon-display")
const $rateArea = $("#rate-area")
const $pathname = window.location.pathname


async function getPokemon(term) {
    try {
        const response = await axios({
            url: `${BASE_URL}/pokemon/${term}`,
            method: "GET"
        });
        const pokemon = response.data;
        return pokemon;
    }
    catch (error) {
        return undefined;
    }
}

function showPokemonMarkup(pokemon) {
    if (pokemon == undefined) {
        return $(`<p>Pokemon not found!</p>`)
    }
    else if ($pokemonDisplay.children().text().toLowerCase().includes(pokemon.name.toLowerCase()) == false) {
        return $(`
    <div>
    <input type="radio" id="${pokemon.name}" name="pokemon" value="${pokemon.name}">
    <label for="${pokemon.name}"><img src="${pokemon.sprites.front_default}">${pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1)}</label>
    </div>
    `)
    }
    else {
        return undefined;
    }
}

async function getAndShowPokemon(term) {
    const pokemon = await getPokemon(term)
    const $pokemon = showPokemonMarkup(pokemon)
    if ($pokemon != undefined) {
        $pokemonDisplay.prepend($pokemon[0])
        $pokemonDisplay.show()
    }
}

async function handleRating(rating) {
    try {
        await axios({
            url: $pathname + `/rating/${rating}/submit`,
            method: "POST"
        });
    }
    catch (error) {
        return undefined;
    }
}

$("input[type='radio']").click(function (evt) {
    evt.preventDefault();
    const rating = $("input[name='crating']:checked").val();
    handleRating(rating)
    location.reload()
})

$pokemonSearch.on("submit", function (evt) {
    evt.preventDefault();
    const term = $term.val().toLowerCase();
    getAndShowPokemon(term);
})