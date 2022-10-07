const BASE_URL = "https://pokeapi.co/api/v2"
const $pokemonSearch = $("#pokemon-search")
const $term = $("#term")
const $pokemonDisplay = $("#pokemon-display")

async function getPokemon(term) {
    console.log("called")
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
        $pokemonDisplay.append($pokemon[0])
        console.log($pokemon[0])
        $pokemonDisplay.show()
    }
}

$pokemonSearch.on("submit", function (evt) {
    evt.preventDefault();
    const term = $term.val().toLowerCase();
    console.log("term:", term);
    getAndShowPokemon(term);
})