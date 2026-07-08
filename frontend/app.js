async function normalizar() {
    try {
        console.log("FUNÇÃO NORMALIZAR");

        const smiles = document.getElementById("smiles").value;

        const response = await fetch("http://127.0.0.1:8000/molecules/normalize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ smiles })
        });
           console.log(response.status);
           console.log(response);

       console.log("Status:", response.status);

       const texto = await response.text();

       console.log("Resposta crua:");
       console.log(texto);

       const data = JSON.parse(texto);

       console.log(data);

        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);

        // imagem com SMILES canônico
        if (data.ok && data.smiles_canonico) {
            const url = `http://127.0.0.1:8000/molecules/image/${encodeURIComponent(data.smiles_canonico)}`;

            console.log("IMG URL:", url);

            document.getElementById("mol-img").src = url;
        }

    } catch (err) {
    console.error(err);

    alert(err.message);
    }
}


async function buscarSimilar() {
    try {
        console.log("FUNÇÃO SIMILAR");

        const smiles = document.getElementById("smiles").value;

        const response = await fetch("http://127.0.0.1:8000/molecules/search_similar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                smiles: smiles,
                top_k: 5
            })
        });
        
         console.log(response.status);
         console.log(response);

        const data = await response.json();

        console.log("RESPOSTA SIMILAR:", data);

        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);

    } catch (err) {
    console.error(err);

    alert(err.message);
    }
}


//  integração com Ketcher
async function obterSmilesDoDesenho() {

    const frame = document.getElementById("ketcher-frame");

    try {

        const ketcher = frame.contentWindow.ketcher;

        const smiles = await ketcher.getSmiles();

        document.getElementById("smiles").value = smiles;

        console.log("SMILES:", smiles);

        await normalizar();

    } catch (error) {

        console.error(error);

        alert("Erro ao obter SMILES");

    }

}
