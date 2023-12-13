# WhatsApp-Clone

Introdução

Aplicativos modernos de troca de mensagens são ferramentas fundamentais para o uso pessoal, acadêmico e profissional, com a evolução dos dispositivos móveis e do acesso à internet, tais tecnologias se desenvolveram de modo que além da troca de mensagens de texto, incluem: envio de arquivos de voz, texto, imagem e vídeo, chamadas de voz e de vídeo, canais de notícia, etc. O rápido desenvolvimento dessa tecnologia mudou a forma como nos comunicamos e hoje influencia vários aspectos de nossa vida como relacionamentos, política e informação.

Fundamentação Teórica

Metodologia

O desenvolvimento da atividade iniciou-se com a criação de um sistema descentralizado de conversa entre diferentes usuários, após feita essa parte, foi implementado um relógio lógico de Lamport para sincronização e ordenação das mensagens enviadas.
A execução do algoritmo funciona da seguinte forma: cada máquina possui seu próprio relógio lógico, que é implementado a cada envio de mensagem e é compartilhado no pacote da mensagem, de forma que o destinatário ao receber uma mensagem com o tempo lógico maior que o do seu relógio, atualiza o relógio para que assim todas as máquinas estejam sincronizadas.
