# WhatsApp-Clone

### Introdução

Aplicativos modernos de troca de mensagens são ferramentas fundamentais para o uso pessoal, acadêmico e profissional, com a evolução dos dispositivos móveis e do acesso à internet, tais tecnologias se desenvolveram de modo que além da troca de mensagens de texto, incluem: envio de arquivos de voz, texto, imagem e vídeo, chamadas de voz e de vídeo, canais de notícia, etc. O rápido desenvolvimento dessa tecnologia mudou a forma como nos comunicamos e hoje influencia vários aspectos de nossa vida como relacionamentos, política e informação.

### Fundamentação Teórica

Para resolver o problema foi feito o uso do algoritmo de relógio de Lamport, um tipo de relógio lógico, que não está associado ao tempo físico mas sim associa um número ou tempo a cada evento ocorrido dentro do sistema e os ordena de forma que se considerarmos o relógio como uma função C, para cada evento evento a e b:
1. C(a) ≠ C(b)
2. Se a acontece antes de b no mesmo processo, então C(a) < C(b).
3. Se a é o envio de uma mensagem e b, o seu recebimento, então C(a) < C(b).

### Metodologia

O desenvolvimento da atividade iniciou-se com a criação de um sistema descentralizado de conversa entre diferentes usuários, feito através de uma dupla conexão peer to peer entre cada um dos usuários do chat,em um sistema descentralizado no qual através do compartilamento adequado dos endereços cada usuário consegue receber e enviar mensagens para cada um dos presente. Após desenvolvida essa parte, foi implementado um relógio lógico de Lamport para sincronização e ordenação das mensagens enviadas. A execução do algoritmo funciona da seguinte forma: cada máquina possui seu próprio relógio lógico, que é implementado a cada envio de mensagem e é compartilhado no pacote da mensagem, de forma que o destinatário ao receber uma mensagem com o tempo lógico maior que o do seu relógio, atualiza o relógio para assim seguir a segunda regra do algoritmo que define que a marca temporal relativa ao recebimento de uma mensagem não pode ser maior que a marca temporal do envio. Por fim, para solucionar empates, um número inteiro único é associado a cada 
Finalizada essa etapa, foi feita a criptografia, foi utilizada a biblioteca cryptography e seu módulo Fernet, que é um algoritmo de chave simétrica que utiliza chaves de 256 bits para criptografar e descriptografar cada mensagem enviada no chat. Para que não seja necessário o compartilhamento das chaves entre os usuários, assim comprometendo a segurança do aplicativo, cada versão do aplicativo possui a mesma chave depositada em um arquivo secreto .env que não é acessível ao usuário devido a execução do aplicativo através de um contâiner Dockerfile. Os pacotes trocados entre os usuários são do tipo json e são organizados da seguinte forma: o campo "tag" que é um identificador do tipo de pacote que está sendo enviado, podendo ser um pacote de entrada, de compartilhamento de histórico, de troca de contato, de pedido de sincronização e, de uma mensagem convencional.
Também foi desenvolvido um sistema de sincronização de mensagens, de forma que quando um novo usuário se conecta no chat, um usuário antigo se reconecta após ficar offline ou um usuário qualquer após passado certo tempo, regulado por uma thread que opera uma contagem e faz a sincronização após 3 minutos

### Resultados e Discussões

O sistema foi desenvolvido conforme solicitado, seguindo a metodologia descrita na seção anterior e apresenta êxito em sua funcionalidade de envio e recebimento de mensagens entre os diferentes usuários da aplicação, além da execução sem falhas da criptografia e decriptografia das mensagens e resolver possíveis problemas de concorrência através do desempate do relógio de Lamport. O sistema foi testado de diversas formas, inicialmente em dois processos na mesma máquina e depois em duas e três máquinas. Uma questão que apareceu durante a resolução do problema foi a questão da confiabilidade, que foi parcialmente resolvida através da constante sincronizaçõ de mensagens entre os usuários, porém sua resolução completa e ideal se daria através da confirmação de recebimento de cada mensagem.

### Conclusão

### Referências

Lamport, L. (1978). Time, clocks, and the ordering of events in a distributed system. Communications of the ACM, pages 558–565.
