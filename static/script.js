const BASE_URL = "https://pokeapi.co/api/v2/"

async function getPokemon(term) {
    const response = await axios({
        url: `${BASE_URL}/pokemon/${term}`,
        method: "GET"
    })
    const pokemon = response.data;
    return pokemon;
}