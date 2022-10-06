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
    else return $(`
    <p><img src="${pokemon.sprites.front_default}">Name: ${pokemon.name}</p>
    
    `)
}

async function getAndShowPokemon(term) {
    const pokemon = await getPokemon(term)
    const $pokemon = showPokemonMarkup(pokemon)
    $pokemonDisplay.append($pokemon[0])
    console.log($pokemon[0])
    $pokemonDisplay.show()
}

$pokemonSearch.on("submit", function (evt) {
    evt.preventDefault();
    const term = $term.val().toLowerCase();
    console.log("term:", term);
    getAndShowPokemon(term);
})