import { useEffect, useRef, useState } from "react";
import { Editor } from "ketcher-react";

function MoleculeEditor() {
  const ketcherRef = useRef(null);

  const [smiles, setSmiles] = useState("");
  const [resultado, setResultado] = useState(null);
  const [imagemUrl, setImagemUrl] = useState("");

  useEffect(() => {
    console.log("Ketcher carregado");
  }, []);

  async function obterSmiles() {
    if (!ketcherRef.current) return;

    try {
      const s = await ketcherRef.current.getSmiles();

      setSmiles(s);

      console.log("SMILES:", s);
    } catch (err) {
      console.error(err);
    }
  }

  async function normalizar() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/molecules/normalize",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            smiles,
          }),
        }
      );

      const data = await response.json();

      setResultado(data);

      if (data.ok && data.smiles_canonico) {
        setImagemUrl(
          `http://127.0.0.1:8000/molecules/image/${encodeURIComponent(
            data.smiles_canonico
          )}`
        );
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function buscarSimilares() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/molecules/search_similar",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            smiles,
            top_k: 5,
          }),
        }
      );

      const data = await response.json();

      setResultado(data);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          padding: "10px",
          background: "#20232a",
          color: "white",
        }}
      >
        <h2>MODiMOL</h2>

        <button onClick={obterSmiles}>
          Obter SMILES
        </button>

        <button onClick={normalizar}>
          Normalizar
        </button>

        <button onClick={buscarSimilares}>
          Buscar Similares
        </button>

        <br />
        <br />

        <input
          value={smiles}
          onChange={(e) => setSmiles(e.target.value)}
          placeholder="SMILES"
          style={{
            width: "100%",
            padding: "8px",
          }}
        />
      </div>

      <div style={{ flex: 1 }}>
        <Editor
          onInit={(ketcher) => {
            ketcherRef.current = ketcher;
          }}
        />
      </div>

      {imagemUrl && (
        <div style={{ padding: "10px" }}>
          <img
            src={imagemUrl}
            alt="Molécula"
            width="250"
          />
        </div>
      )}

      {resultado && (
        <pre
          style={{
            padding: "10px",
            overflow: "auto",
            maxHeight: "300px",
          }}
        >
          {JSON.stringify(resultado, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default MoleculeEditor;
