📌 Cadastro de Clientes no Sistema RPA Challenge e Cotação de Novos Pedidos no Correios e JadLog

📖 Descrição

Este projeto automatiza o cadastro de clientes no Sistema Challenge e realiza a cotação de novos pedidos utilizando diferentes serviços de transporte. O processo é realizado de forma automatizada, garantindo eficiência e redução de erros manuais.

🔧 Requisitos

Antes de executar o projeto, certifique-se de instalar as dependências necessárias:

pip install --upgrade -r requirements.txt

📂 Estrutura do Projeto

O projeto é estruturado com diferentes módulos para organização e separação de responsabilidades:

📌 src/setup.py - Configuração inicial do bot.

🌎 src/brasil_api.py - Integração com a Brasil API para consulta de dados.

📁 src/criar_diretorios.py - Cria os diretórios necessários para a execução do projeto.

📝 src/configurar_logs.py - Configuração dos logs do usuário e desenvolvedor.

📦 src/cotacao_correios.py - Realiza a cotação de fretes via Correios.

🚛 src/cotacao_jadlog.py - Realiza a cotação de fretes via Jadlog.

📧 src/emailf.py - Envio de e-mails automáticos com relatórios.

📊 src/excelf.py - Manipulação de arquivos Excel.

⚙️ src/utilidades.py - Funções auxiliares utilizadas no projeto.

🤖 src/rpa_challenge.py - Preenchimento automático do desafio RPA.

▶️ Como Executar

Para iniciar o processo automatizado, execute o arquivo principal:

python bot.py

O processo realiza as seguintes etapas:

🚀 Inicializa o bot e configura os diretórios.

📄 Cria a planilha de saída.

🔄 Preenche a planilha com dados existentes.

🌐 Obtém informações adicionais via Brasil API.

🏆 Realiza o preenchimento automático do desafio RPA.

📦 Consulta cotações de frete com Correios e Jadlog.

✅ Finaliza a planilha e envia o e-mail com os resultados.

⚠️ Tratamento de Erros

Caso ocorra algum erro durante o processo:

🛠️ Os detalhes do erro serão registrados nos logs.

🔍 O nome da função que gerou o erro será identificado e registrado.

📷 Um e-mail será enviado com a captura de tela do erro.
