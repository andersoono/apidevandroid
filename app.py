import json
import os
from flask import Flask, jsonify

DATA_FOLDER = 'dados/GeoJSON'

FILE_MAP = {
    1: 'Biodigestores.geojson',
    2: 'Centro_de_Recondicionamento_Tecnologico.geojson',
    3: 'Ecopontos.geojson',
    4: 'Ilhas_Ecológicas.geojson',
    5: 'Retorna_Machine.geojson',
    6: 'Pontos_de_Coleta_Domiciliar.geojson',
    7: 'Lixeiras_Subterraneas.geojson'
}

app = Flask(__name__)

def get_geojson_by_id(id_arquivo):

    filename = FILE_MAP.get(id_arquivo)
    
    if not filename:
        return None, "ID não mapeado. Use um ID entre 1 e 7."

    file_path = os.path.join(DATA_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return None, f"Arquivo '{filename}' não encontrado no disco. Verifique a pasta '{DATA_FOLDER}'."
            
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data, None
            
    except json.JSONDecodeError:
        return None, f"Erro de JSON: O arquivo '{filename}' está mal formatado."
    except Exception as e:
        return None, f"Erro ao ler '{filename}': {e}"

@app.route('/dados/geojson/<int:id_arquivo>', methods=['GET'])
def get_specific_data(id_arquivo):
    
    data, error = get_geojson_by_id(id_arquivo)
    
    if data is None:
        return jsonify({"error": error}), 404
        
    return jsonify(data)


@app.route('/', methods=['GET'])
def home():
     
    return jsonify({
        "status": "API para a trabalho da faculdade funcionando normalmente."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
