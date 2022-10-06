const BASE_URL = "https://pokeapi.co/api/v2"
const $pokemonSearch = $("#pokemon-search")
const $term = $("#term")
const $pokemonDisplay = $("pokemon-display")

async function getPokemon(term) {
    console.log("called")
    const response = await axios({
        url: `${BASE_URL}/pokemon/${term}`,
        method: "GET"
    });
    const pokemon = response.data;
    console.log("get pokemon:", pokemon)
    return pokemon;
}

function showPokemon(pokemon) {
    return $(`
    <p>Name: ${pokemon.name}</p>
    `)
}

$pokemonSearch.on("submit", function (evt) {
    evt.preventDefault();
    const term = $term.val();
    console.log("term:", term)
    const pokemon = getPokemon(term);
    console.log(pokemon)
    const markup = showPokemon(pokemon)
    $pokemonDisplay.append(markup)
    $pokemonDisplay.show();
    return false;
})