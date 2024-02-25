# WhatsApp-Clone Release Candidate

### Introdução

Cumpridos os requisitos da primeira versão do sistema de troca de mensagens, verificou-se a necessidade de um sistema confiável no qual há a distribuição igualitária de mensagens, de forma que se um usuário exibir uma mensagem em sua interface, todos os outros devem exibi-la também. Além disso, para fins de teste e avaliação, a interface deve ser compatível com comandos em shell script.

### Fundamentação Teórica

Para cumprir tais requisitos, vários algoritmos foram discutidos e apresentados durante as sessões, porém decidi utilizar o algoritmo de difusão confiável baseado em Nack. Esse algoritmo funciona da seguinte forma: uma sequência de mensagens é enviada para um grupo de nós, caso algum dos receptores note a falta de uma mensagem, ele envia um Nack para os outros receptores e para o transmissor solicitando a mensagem que está faltando. Um dos problemas dessa implementação é a explosão de retransmissões causada pelo envio das retransmissões por todos os nós do sistema, o problema pode ser resolvido através do uso de um buffer de mensagens onde ficam guardadas as mensagens recebidas e que podem ser retransmitidas através de um Nack caso algum nó solicite. Ao perceber que todos os outros nós possuem determinada mensagem, o nó a exclui do buffer. O problema também pode ser resolvido através de um contador de tempo nos nós que aguarda um tempo aleatório para enviar a mensagem solicitada, como o tempo aleatório vai ser diferente para cada nó, nenhum deles vai enviar simultaneamente e após o primeiro fazer o envio da mensagem os outros podem cancelá-lo.



### Metodologia

Para desenvolver a atividade e melhorar o sistema desenvolvido no problema anterior, primeiro foi desenvolvido um sistema de reconexão, de forma que caso um nó perca sua conexão com a internet ele se reconecte em seguida. Então foi desenvolvido o algoritmo de difusão confiável baseado em Nack para fazer isso, para o desenvolvimento do algoritmo foram criadas tags para o Nack (a solicitação de uma mensagem perdida), para a própria mensagem perdida e para o compartilhamento de IDs entre os nós. O compartilhamento de IDs é necessário para que todos os nós saibam quais mensagens os outros nós possuem e assim poderem compartilhá-las com eles, tal funcionalidade foi implementada com o uso de uma thread que compartilha os IDs com os outros nós a cada 30 segundos. Para utilização do código em shell script, foram implementadas funções separadas com parte do código que executam tarefas específicas como enviar uma mensagem e ver o histórico de mensagens.

### Resultados e Discussões

O sistema foi desenvolvido conforme descrito na seção metodologia, porém não obteve êxito na confiabilidade, sendo que mensagens podem ser perdidas pelo usuário ao desconectar-se da rede. Apesar de implementada a interface inicial do algoritmo com base em Nack, o programa não foi suficientemente testado devido a necessidade de presença física no laboratório para avaliar o funcionamento do programa durante uma falha de conexão.

### Conclusão

O processo de implementação do novo programa começou bem e, apesar de não atingir o resultado esperado, um sistema no qual as mensagens fossem as mesmas para cada um dos nós, no fim foi implementado um sistema melhor que o anterior onde os nós conseguem se reconectar após falhas na rede. Conclui-se a viabilidade de um sistema de troca de mensagens descentralizado e a necessidade de implementação de uma confiabilidade na troca de mensagens para um funcionamento adequado.

### Referências

Lamport, L. (1978). Time, clocks, and the ordering of events in a distributed system. Communications of the ACM, pages 558–565.
Lung, L. Comunicação de Grupo: Disfusão Confiável e Atômica.
