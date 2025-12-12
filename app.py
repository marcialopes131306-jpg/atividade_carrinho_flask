from flask import Flask, render_template, request, redirect, url_for, session, flash

# Criar a aplicação Flask
app = Flask(__name__)

# Chave secreta para sessões (em produção, use uma chave mais segura)
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração dos produtos (simulando um banco de dados)
app.config['PRODUTOS'] = {
    1: {
        'id': 1, 
        'nome': 'Produto 1', 
        'preco': 2.198, 
        'categoria': 'Eletrônicos',
        'imagem_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_994262-MLA100066473675_122025-F.webp'
    },
    2: {
        'id': 2, 
        'nome': 'Produto 2', 
        'preco': 1.499, 
        'categoria': 'Eletrônicos',
        'imagem_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_934018-MLA99576753908_122025-F.webp'
    },
    3: {
        'id': 3, 
        'nome': 'Produto 3', 
        'preco': 1.240, 
        'categoria': 'Eletrônicos',
        'imagem_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_875505-MLA99456385122_112025-F.webp'
    },
    4: {
        'id': 4, 
        'nome': 'Produto 4', 
        'preco': 5.994, 
        'categoria': 'Celulares e Telefones',
        'imagem_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_740306-MLA94919264998_102025-F.webp'
    },
    5: {
        'id': 5, 
        'nome': 'Produto 5', 
        'preco': 4.729,
        'categoria': 'Celulares e Telefones',
        'imagem_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_673808-MLA99443133132_112025-F.webp'
    },
    6: {
        'id': 6, 
        'nome': 'Produto 6', 
        'preco': 2.249, 
        'categoria': 'Celulares e Telefones',
        'imagem_url': 'https://http2.mlstatic.com/D_NQ_NP_2X_763543-MLA99919842737_112025-F.webp'
    },
}

# Rota principal - Lista de produtos
@app.route('/')
def index():
    produtos = app.config['PRODUTOS']

    categorias_selecionadas = request.args.get('categoria')

    produtos_para_exibir = {}
    if categorias_selecionadas:
        for id, produto in produtos.items():
            if produto.get('categoria') in categorias_selecionadas:
                produtos_para_exibir[id] = produto
    else:
        produtos_para_exibir = produtos
    return render_template('index.html', produtos=produtos_para_exibir)

# Rota para adicionar produto ao carrinho
@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    produtos = app.config['PRODUTOS']
    produto_a_adicionar = produtos.get(produto_id)
    quantidade = int(request.form.get('quantidade', 1))

    if not produto_a_adicionar:
        flash('Produto não encontrado.')
        return redirect(url_for('index'))
    
    # Recuperar carrinho da sessão (ou criar lista vazia)
    carrinho = session.get('carrinho', [])
    
    # Tentar encontrar o produto no carrinho
    encontrado = False
    for item in carrinho:
        if item['id'] == produto_id:
            item['quantidade'] += quantidade
            encontrado = True
            break
    # Se não encontrado, adicionar novo item
    if not encontrado:
        carrinho.append({
            'produto': produto_a_adicionar,
            'quantidade': quantidade
        })

    # Salvar carrinho na sessão
    session['carrinho'] = carrinho
    
    # Mensagem de feedback
    flash(f'{produto_a_adicionar["nome"]},{quantidade} Produtos adicionados ao carrinho!')
    return redirect(url_for('index'))

# Rota para visualizar o carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    
    # Calcular total
    total = sum(item['produto']['preco'] * item['quantidade']for item in carrinho)
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Rota para remover produto do carrinho
@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    
    # Procurar e remover produto
    for produto in carrinho:
        if produto['id'] == produto_id:
            carrinho.remove(produto)
            session['carrinho'] = carrinho
            flash('Produto removido do carrinho!')
            break
    else:
        flash('Produto não encontrado no carrinho.')
    
    return redirect(url_for('carrinho'))

# Rota para limpar o carrinho
@app.route('/limpar_compra', methods=['POST'])
def limpar_compra():
    session['carrinho'] = []
    flash('Carrinho limpo com sucesso!')
    return redirect(url_for('carrinho'))

# Sobre a loja 
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)