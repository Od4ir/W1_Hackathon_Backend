from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uuid
import PyPDF2
import io

load_dotenv()

app = Flask(__name__)
history = []

# 🔐 Configurar chave
genai.configure(api_key=os.getenv("LLM_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def extract_text_from_pdf(pdf_file):
    """Extrai texto de um arquivo PDF."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return None

def structure_document_text(text):
    """Envia o texto extraído para a LLM estruturar."""
    try:
        prompt = """
        Extraia as informações deste documento e retorne APENAS um JSON válido, 
        sem comentários ou markdown, com os seguintes campos:
        - Nome (string)
        - CPF (string, formato "XXX.XXX.XXX-XX")
        - Endereço (string)
        - Holding (string, se aplicável)

        Exemplo de saída esperada:
        {
            "Nome": "Odair Gonçalves",
            "CPF": "123.456.789-00",
            "Endereço": "Rua do IME, 123",
            "Holding": "Casa na Praia"
        }

        Documento para análise:
        """
        
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(f"{prompt}\n\nDocumento:\n{text}")
        return response.text
    except Exception as e:
        return None

@app.route('/processar-pdf', methods=['POST'])
def processar_pdf():
    """Endpoint para processar PDF e retornar texto estruturado."""
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({'erro': 'Nome de arquivo vazio'}), 400
    
    if not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({'erro': 'Formato de arquivo inválido. Envie um PDF.'}), 400
    
    # Extrai texto do PDF
    extracted_text = extract_text_from_pdf(pdf_file)
    if not extracted_text:
        return jsonify({'erro': 'Falha ao extrair texto do PDF'}), 500
    
    # Envia para a LLM estruturar
    structured_text = structure_document_text(extracted_text)
    if not structured_text:
        return jsonify({'erro': 'Falha ao processar texto com a LLM'}), 500
    
    return jsonify({
        'texto_extraido': extracted_text,
        'texto_estruturado': structured_text
    }), 200


def get_investment_info():
    """Busca informações de investimentos do usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna informações de investimentos do usuário.
    """
    try:
        response = "Fale sobre o aplicativo sync onde ela consegue ver investimentos dela"
        # response = requests.get()
        return response.json()
    except:
        return "Não foi possível verificar as informações de investimentos no banco de dados :("
    
def get_doc_missing_by_user_id():
    """Busca documentos não apresentados pelo usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna um resumo dos produtos que a pessoa ainda não tem.
    """
    try:
        # No link abaixo mostrar informações de arquivos que faltam para concluir uma holding
        # response = requests.get(f"http://172.17.0.1:7296/api/ProdutosContratados/nao-contratados/usuario/{usuario_id}")
        response = "falta iptu"
        prompt = f"Resuma esse json que possui informações sobre os documentos que não foram encontrados para continuar com oa holding {response}"
        response_LLM = model.generate_content(prompt)
        return response_LLM.text
    except:
        return "Não foi possível verificar os documentos faltantes no banco de dados :("

# Processos de holding em aberto

def transfer_to_human():
    numero_protocolo = str(uuid.uuid4())[:8]  # algo tipo "a3f9c1e2"
    recado = "Encaminharemos sua questão a um de nossos especialistas humanos."
    resumo = "Resumo da conversa será construído pela LLM"
    return {
        "mensagem": recado,
        "protocolo": numero_protocolo,
        "resumo": resumo
    }



def get_products(produtos:str):
    """Informa o que a W1 oferece.
    Args:
        produtos: argumento aleatório
    Return: 
        Retorna todos os produtos oferecidos pelo Banco.
    """
    prompt = f"Resuma as funções de uma empresa de Consultoria Patrimonial"
    response_LLM = model.generate_content(prompt)
    return response_LLM.text


def comparar_estrategias_sucessorias(nome_bem: str, valor_estimado: float, tipo_bem: str) -> str:
    itcmd_percentual = 0.08
    custo_inventario = valor_estimado * itcmd_percentual
    custo_holding = 50000.00

    texto = f"""
🟥 Fora da W1:
Bem: {nome_bem} ({tipo_bem})
Valor total gasto com inventário:
💸 R$ {custo_inventario:,.2f} (exemplo: {int(itcmd_percentual * 100)}% de ITCMD sobre R$ {valor_estimado:,.2f})

Tempo estimado:
🕐 2 a 4 anos de inventário judicial

Riscos:
⚠️ Bloqueio de bens, brigas familiares, altos custos jurídicos

🟩 Com W1 Holding Patrimonial:
Custo da estruturação:
💼 R$ {custo_holding:,.2f} (ex: honorários advocatícios + abertura de empresa)

Tempo estimado:
⏱️ 2 a 3 meses

Vantagens:
✅ Economia de impostos
✅ Sucessão planejada
✅ Proteção dos bens
✅ Gestão profissional
""".strip()
    return texto


tool = [transfer_to_human, get_products, get_investment_info, get_doc_missing_by_user_id, comparar_estrategias_sucessorias]

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=generation_config,
    system_instruction="""
Você é W1ll, um assistente virtual da W1 Consultoria, uma empresa brasileira especializada em consultoria patrimonial. Sua missão é oferecer respostas claras, amigáveis e úteis para clientes adultos e idosos, de forma educada e profissional, mesmo diante de mensagens agressivas.

# 🎯 Objetivos:
- Caso o cliente mande apenas um oi, tudo bem ou algo do tipo:
    - Apresente-se no início da conversa
    - Explique brevemente o que pode fazer:
        - Tirar dúvidas sobre a W1
        - Informar sobre investimentos (chame: get_investment_info)
        - Informar documentos faltantes para abertura de holding (chame: get_doc_missing_by_user_id)
        - Informar os produtos oferecidos (chame: get_products)
        - Transferir para um atendente humano se necessário (chame: transfer_to_human)
- Caso o cliente faça uma pergunta direta, responda de forma clara e objetiva.
- Caso o cliente faça uma pergunta complexa, divida a resposta em partes e explique cada uma delas.
- Informar o número do protocolo e um resumo da conversa ao final de cada interação ou antes de transferir.
- Quando o usuário desejar fazer uma comparação de estratégias sucessórias, também conhecida como simulação do processo da holding, pergunte o nome do bem, valor estimado e tipo de bem. Em seguida, chamar a função comparar_estrategias_sucessorias(nome_bem, valor_estimado, tipo_bem) e apresentar o resultado.
- Se o usuário não fornecer informações suficientes, solicitar os dados necessários de forma educada.

# 🧭 Diretrizes:
- Só responda a assuntos relacionados a: W1, holding, documentos de abertura (ex: IPTU, valor venal), produtos e serviços da empresa.
- Se a pergunta for fora desse escopo, informe que será encaminhada a um atendente humano (chame: transfer_to_human).
- Mantenha mensagens curtas e objetivas, exceto quando a explicação exigir.
- Use uma linguagem acessível e calorosa.

# 🧱 Valores da empresa:
A W1 Consultoria busca orientar clientes de forma personalizada para alcançar suas metas financeiras com clareza, eficiência e empatia. Suas estratégias são desenvolvidas com base na situação atual e objetivos futuros do cliente.

# 🧰 Funções disponíveis:
- get_investment_info(): retorna informações de investimentos do usuário.
- get_doc_missing_by_user_id(): retorna documentos pendentes para abrir uma holding.
- get_products(produtos: str): retorna os produtos oferecidos pela empresa.
- transfer_to_human(): transfere para um atendente e gera número de protocolo.
- comparar_estrategias_sucessorias(nome_bem: str, valor_estimado: float, tipo_bem: str): compara estratégias sucessórias.

""",
    tools=tool
)


@app.route('/mensagem', methods=['POST'])
def enviar_mensagem():
    mensagem = request.json.get('mensagem')
    if mensagem:
        chat_session = model.start_chat(
            history=history,
            enable_automatic_function_calling=True
        )
        response = chat_session.send_message(mensagem)
        resposta_text = response.text
        history.append({"role":"user","parts":[mensagem]})
        history.append({"role":"model","parts":[resposta_text]})
        return jsonify({"resposta": resposta_text}), 200
    return jsonify({'erro': 'Mensagem não fornecida'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

from services.pdf_extractor import extract_text_from_pdf

@app.route('/extract', methods=['POST'])
def extract_from_pdf():
    try:
        data = request.json
        filepath = data.get("filepath")
        if not filepath:
            return jsonify({"erro": "Arquivo não especificado"}), 400

        # 🗂️ Extrair texto do PDF
        texto = extract_text_from_pdf(filepath)

        # ✨ Prompt para LLM
        prompt = f"""
        Você receberá abaixo o conteúdo extraído de um documento PDF. Seu papel é identificar e estruturar as informações mais relevantes em formato JSON. Seja preciso e organizado.

        Conteúdo do PDF:
        \"\"\"
        {texto}
        \"\"\"

        Retorne um JSON com as informações encontradas.
        """

        # 🤖 Chamar o modelo
        chat = model.start_chat(history=[], enable_automatic_function_calling=False)
        resposta = chat.send_message(prompt)

        return jsonify({"resultado": resposta.text}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
