# Conversor de Máquina de Turing
Este programa converte programas de Máquina de Turing entre dois modelos:
- **;S**: Modelo de Sipser (fita com início à esquerda).
- **;I**: Modelo de fita duplamente infinita.

As entradas e saídas podem ser executadas com o simulador online <https://morphett.info/turing/turing.html>.

## Formato do arquivo de entrada
- É **necessário** que o arquivo de entrada tenha extensão **".txt"** e esteja no mesmo diretório do programa.
  - ex: ``arquivoEntrada.txt``
- A primeira linha do arquivo especifica o tipo de máquina (`;S` ou `;I`).
- Cada linha seguinte segue o formato `<estado atual> <símbolo lido> <símbolo escrito> <direção> <novo estado>`.

## Como usar
1. **Clone o repositório**
   
   ```
   git clone https://github.com/kapfw/conversorMT
   ```
    **OU** Baixe o projeto comprimido `conversorMT.zip` e extraia na sua máquina.
  
2. **Execute o programa**
   
    Navegue até o diretório do arquivo e execute a aplicação com
    ```
     python3 conversor.py arquivoEntrada.txt
    ```

3. **Arquivo de saída**
   
     Após a execução, o arquivo de saída será gerado com o mesmo nome do arquivo de entrada, agora com a extensão "**.out**".


