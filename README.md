## Backupy

Este projeto consiste em utilizar a api do google drive através do módulo python [pydrive2](https://pypi.org/project/PyDrive2/), para efetuar backups de seus arquivos preferidos...


## Como instalar???

```shell
git clone https://github.com/cleitonleonel/backupy.git
cd backupy
python3 main.py
```

## OBS:

Para utilizar a api do google drive você precisa antes obter suas credenciais, para isso precisa seguir alguns passos.

Este tutorial mostra como habilitar a API Google Drive para uma conta específica Google, e obter as credenciais de acesso a ser usado a partir do Iperius para fazer backups na nuvem. Na verdade, para fazer um backup online para o Google Drive primeiro é preciso habilitar algumas opções específicas, então devendo criar uma conta no Iperius usando as credenciais fornecidas pelo Google (ID do cliente e cliente secreto).

Faça login com sua conta do Google na área reservada onde permite configurar APIs do Google, a partir deste URL: https://console.developers.google.com/apis/library

Crie um projeto a partir de "Selecione um Projeto":
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive3_por.png" alt="" width="450"/>
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive4_por.png" alt="" width="450"/>

Uma vez que o projeto é criado, vá em "Biblioteca de APIs" e habilite a "API do Google drive":
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive1_por.png" alt="" width="450"/>
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive2_por.png" alt="" width="450"/>

No menu à esquerda ("API & Services"), clique em "OAuth consent screen".
<img src="https://www.iperiusbackup.net/wp-content/uploads/2014/11/googledrive6_eng1.png" alt="" width="450"/>

Selecione "Externo" e insira seu endereço de e-mail e o nome do aplicativo. Este é o nome que será mostrado na "Tela de consentimento" ao fazer a autenticação.
<img src="https://www.iperiusbackup.net/wp-content/uploads/2014/11/googledrive6_2eng.png" alt="" width="450"/>
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive6_3eng.png" alt="" width="450"/>

Deixe todas as outras opções com os valores padrão e clique em "SAVE AND CONTINUE".
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive6_4.eng_.png" alt="" width="450"/>
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive6_5.eng_.png" alt="" width="450"/>

Na última etapa vá no menu à esquerda na "OAuth consent screen" e clique em "Publish App", a seguir clique em "Confirm" na tela.
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/publish_app.png" alt="" width="450"/>
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/publish_app2.png" alt="" width="450"/>

No menu esquerdo ("APIs e Services"), clique em "Credentials" e escolha OAuth Client ID no menu  "Create credentials" menu:
<img src="https://www.iperiusbackup.net/wp-content/uploads/2014/11/googledrive5_eng1.png" alt="" width="450"/>

Selecione a opção "App para computador", digite o nome e clique em "Criar":
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/googledrive7_por1.png" alt="" width="450"/>

Imediatamente, ID do cliente e Chave secreta do cliente serão mostrados à direita. Copie esta página para Autenticação no Gerenciador de Contas do Google Drive.
<img src="https://www.iperiusbackup.net/wp-content/uploads/2015/04/abilitare-le-api-google-drive-eng10.png" alt="" width="450"/>

Se chegou até aqui suas credenciais já devem existir, então basta voltar ao painel e em "API & Services" selecionar "Credenciais" e no lado direito em "IDs do cliente OAuth 2.0" baixar o arquivo json com suas credenciais,
após efetuar o download desse arquivo renomeie para "clients_secrets.json" e salve esse arquivo em um local bem sugestivo de preferência na mesma pasta do projeto, ele será o meio de acesso ao gdrive.

## Editando o settings:

A essa altura você já deve ter notado um arquivo settings.py dentro da pasta do projeto, pois bem configure-o de acordo com suas preferências e caminhos de arquivos.
Fique atento ao caminho do arquivo "client_secrets.json", ele deve ser real, ao executar o programa pela primeira vez será necessário aceitar o acesso a sua conta gdrive, é impressindível que já tenha liberado nas configurações de sua conta o "Acesso a apps menos Seguros", se não o fez é bom que o faça, pois poderam ocorrer erros de permissões sem isso.

## Author

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com