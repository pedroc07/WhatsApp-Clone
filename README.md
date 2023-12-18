# WhatsApp-Clone

Introdução

Aplicativos modernos de troca de mensagens são ferramentas fundamentais para o uso pessoal, acadêmico e profissional, com a evolução dos dispositivos móveis e do acesso à internet, tais tecnologias se desenvolveram de modo que além da troca de mensagens de texto, incluem: envio de arquivos de voz, texto, imagem e vídeo, chamadas de voz e de vídeo, canais de notícia, etc. O rápido desenvolvimento dessa tecnologia mudou a forma como nos comunicamos e hoje influencia vários aspectos de nossa vida como relacionamentos, política e informação.

Fundamentação Teórica

Para resolver o problema foi feito o uso do algoritmo de relógio de Lamport, 

Metodologia

O desenvolvimento da atividade iniciou-se com a criação de um sistema descentralizado de conversa entre diferentes usuários, feito através de uma conexão peer to peer dupla entre cada um dos usuários do chat. Após desenvolvida essa parte, foi implementado um relógio lógico de Lamport para sincronização e ordenação das mensagens enviadas. A execução do algoritmo funciona da seguinte forma: cada máquina possui seu próprio relógio lógico, que é implementado a cada envio de mensagem e é compartilhado no pacote da mensagem, de forma que o destinatário ao receber uma mensagem com o tempo lógico maior que o do seu relógio, atualiza o relógio para que assim todas as máquinas estejam sincronizadas. Finalizada essa etapa, foi feita a criptografia, foi utilizada a biblioteca cryptography e seu módulo Fernet, que é um algoritmo de chave simétrica que utiliza chaves de 256 bits para criptografar e descriptografar cada mensagem enviada no chat. Para que não seja necessário o compartilhamento das chaves entre os usuários, assim comprometendo a segurança do aplicativo, cada versão do aplicativo possui a mesma chave depositada em um arquivo secreto .env que não é acessível ao usuário devido a execução do aplicativo através de um contâiner Dockerfile. Os pacotes trocados entre os usuários são do tipo json e são organizados da seguinte forma: o campo "tag" que é um identificador do tipo de pacote que está sendo enviado, podendo ser um pacote de entrada, de compartilhamento de histórico, de troca de contato, de pedido de sincronização e, de uma mensagem convencional. Também foi desenvolvido um sistema de sincronização de mensagens, de forma que quando um novo usuário se conecta no chat, um usuário antigo se reconecta após ficar offline ou um usuário qualquer após passado certo tempo, regulado por uma thread que opera uma contagem e faz a sincronização após 3 minutos
