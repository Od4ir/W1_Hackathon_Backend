from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

def get_investment_info_by_user_id(usuario_id: str):
    """Busca informações de investimentos do usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna informações de investimentos do usuário.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/Investimentos/usuario/{usuario_id}")
        return response.json()
    except:
        return "Não foi possível verificar as informações de investimentos no banco de dados :("
    
def get_uncontracted_products_by_user_id(usuario_id: str):
    """Busca produtos não contratados pelo usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna um resumo dos produtos que a pessoa ainda não tem.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/ProdutosContratados/nao-contratados/usuario/{usuario_id}")
        response = response.json()
        prompt = f"Resuma esse json que possui informações sobre os produtos não contratados pelo usuário {response}"
        response_LLM = model.generate_content(prompt)
        return response_LLM.text
    except:
        return "Não foi possível verificar os produtos não contratados no banco de dados :("

# Processos de holding em aberto

def transfer_to_human():
    """
    Args:
    return: 
        recado (string): recado de transferencia para um atendente humano
    """
    recado = "Deve transferir para um atendente humano"
    numero_protocolo = "123456"
    return recado, numero_protocolo

def get_user_id_by_email(email: str):
    """Busca o ID do usuário a partir do email.
    Args:
        email: Email do usuário.
    Return:
        str: Retorna o ID do usuário.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/Usuarios/email/{email}/id")
        return response.json()
    except:
        return "Não foi possível verificar o email no banco de dados :("

def get_user_details(email: str):
    """Busca informações do usuário a partir do email.
    Args:
        email: Email do usuário.
    Return:
        dict: Retorna informações como nome, email, telefone, idade, gênero apenas. Caso o usuário queira, ele pode solicitar informações sobre contas e investimentos posteriormente.
    """
    user_id = get_user_id_by_email(email)
    if user_id:
        response = requests.get(f"http://172.17.0.1:7296/api/Usuarios/{user_id}")
        return response.json()
    else:
        return "Não foi possível encontrar o usuário com o email fornecido."

def get_products(produtos:str):
    """Informa os produtos financeiros, de investimento ou bancários que o banco oferece.
    Args:
        produtos: argumento aleatório
    Return: 
        Retorna todos os produtos oferecidos pelo Banco.
    """
    response = requests.get("http://172.17.0.1:7296/api/ProdutosBancarios")
    response = response.json()
    prompt = f"Resuma as funções  {response}"
    response_LLM = model.generate_content(prompt)
    return response_LLM.text


tool = [transfer_to_human, get_user_id_by_email, get_user_details, get_products, get_investment_info_by_user_id, get_uncontracted_products_by_user_id]

genai.configure(api_key="AIzaSyCA8UFoADPrHVzFq26gFWtzqJ4IzyxfqRc")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    generation_config=generation_config,
    system_instruction="Seu nome é Agente Will e você é um assistente virtual de uma empresa de Consultoria Patrimonial. Suas tarefas é responder os clientes de forma mais amigavel possível para um público mais adulto e idoso. Você conseguir resolver questões sobre como abrir uma holding, serviços da W1, como encontrar os documentos para abrir holding como iptu e certificado de valor venal" 
    
    "A W1 Consultoria é uma empresa brasileira dedicada a fornecer orientação e planejamento financeiro personalizado. Nosso foco é ajudar você a alcançar suas metas financeiras por meio de estratégias cuidadosamente desenvolvidas, que consideram tanto sua situação atual quanto seus objetivos futuros."

    "Quando o usuário solicitar informações pessoais, você deve informar o nome, email, telefone, idade, gênero do usuário e também seu id, chamando a função get_user_info_by_email. Memorize o id da pessoa. A não ser que essas informações estejam no histórico da conversa. Porém, se a pessoa solicitar uma consulta nova, faça e informe os dados."

    "Quando o usuário solicitar informações sobre investimentos, você deve informar os investimentos do usuário, chamando a função get_investment_info_by_user_id. Caso não tenha o id, consiga o id pelo email do usuário."

    "Quando o usuário solicitar informações sobre produtos não contratados, você deve informar os produtos não contratados pelo usuário, chamando a função get_uncontracted_products_by_user_id. Caso não tenha o id, consiga o id pelo email do usuário."

    "Você não deve inventar produtos ou informações sobre o banco. Você deve sempre buscar informações reais no banco de dados."

    "Quando um usuário solicitar informações sobre produtos, você deve informar todos os produtos oferecidos, por meio da função get_products."

    "Caso não consiga resolver a questão do cliente, você deve transferir para um atendente humano chamando a função transfer_to_human. Como resposta para o usuário, além de informar que a questão será resolvida por um atendente humano, você deve informar o número do protocolo da conversa e um resumo da conversa até o momento",
    tools=tool 
)

# Buscar informações no bd
# Encontrar documentos iptu


app = Flask(__name__)
history = []

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
        return resposta_text, 200
    else:
        return jsonify({'erro': 'Mensagem não fornecida'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')