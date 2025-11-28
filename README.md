Este repositório documenta e analisa um keylogger **desenvolvido por mim**, com finalidade **estritamente educacional**, para estudo de comportamento de malware, análise ofensiva, defensiva e compreensão de técnicas utilizadas por ameaças reais.

O foco deste material é **ensinar estudantes e profissionais de cibersegurança** a identificar, analisar e mitigar esse tipo de código, entendendo sua estrutura e funcionamento interno.

> ⚠️ **Aviso Ético e Legal**
> O código aqui apresentado deve ser usado **apenas em ambientes controlados**, autorizados e isolados.  
> Qualquer uso fora desse contexto é ilegal.

---

## 🧩 Arquitetura Geral do Código

O keylogger que desenvolvi possui quatro pilares principais:

1. **Captura de teclas**  
2. **Armazenamento em buffer e gravação periódica**  
3. **Criptografia dos registros**  
4. **Envio do arquivo criptografado por e-mail**  

Abaixo está a explicação completa **função por função**.

---

# 🛠️ Explicação do Código — Parte por Parte

## 📌 Importações
O script importa módulos essenciais para:

- capturar teclas  
- lidar com threads  
- gerenciar buffers  
- criptografar arquivos  
- enviar e-mails  
- registrar logs  
- manipular arquivos  

Cada importação reflete uma parte da estrutura típica de malware estudado em laboratórios.

---

## 📌 Configuração inicial e caminhos de arquivos
O script define os caminhos:

- `log.txt` — log das teclas  
- `log_encrypted.txt` — arquivo criptografado  
- `chave.key` — chave criptográfica  

Isso permite rastrear indicadores de comprometimento em análises defensivas.

---

## 📌 Função `capturar_tecla(evento)`
**O que faz:**  
Intercepta cada tecla pressionada no sistema.

**Como funciona:**  
- Converte teclas em símbolos inteligíveis  
- Trata teclas especiais como Enter, Tab, Backspace  
- Adiciona tudo a uma fila (`Queue`) usada como buffer  

**Relevância na análise de malware:**  
Captura de eventos de teclado é um comportamento clássico de keyloggers.

---

## 📌 Função `gravar_buffer()`
**O que faz:**  
Grava periodicamente o conteúdo da fila no arquivo `log.txt`.

**Como funciona:**  
- Loop infinito em thread separada  
- Consome a fila e escreve no log  
- Evita perda de dados caso o programa pare  

**Importância defensiva:**  
Criação de arquivos recorrentes é um padrão detectável por EDR/antivírus.

---

## 📌 Funções de criptografia

### `gerar_chave()`
Gera automaticamente uma chave simétrica Fernet caso não exista.

### `carregar_chave()`
Carrega a chave armazenada no disco.

### `criptografar_log()`
Criptografa `log.txt` e salva em `log_encrypted.txt`.

### `descriptografar_log()`
Descriptografa o arquivo criptografado.

**Por que isso importa na análise?**  
Malwares modernos frequentemente criptografam exfiltrações para evitar detecção por inspeção.

---

## 📌 Função `enviar_email()`
**O que faz:**  
Envia o arquivo criptografado para o e-mail configurado.

**Como funciona:**  
- Cria mensagem SMTP  
- Adiciona o arquivo criptografado como anexo  
- Usa TLS para transmissão segura  

**Comportamento observado em ameaças reais:**  
Keyloggers e stealers simples frequentemente usam SMTP para exfiltração.

---

## 📌 Função `enviar_email_periodico()`
**O que faz:**  
Envia automaticamente relatórios a cada intervalo determinado.

**Por que isso é relevante?**  
Gera tráfego periódico — algo monitorável por firewalls e EDR.

---

## 📌 Execução principal (`if __name__ == "__main__":`)
O script:

1. Gera/Carrega chave  
2. Inicia thread de gravação  
3. Inicia thread de envio periódico  
4. Começa captura de teclado  
5. Envia relatório final ao encerrar  

Essa estrutura modular é típica em malware organizado.

---

# 🔍 Indicadores de Comprometimento (IoCs)

- Arquivos criados no sistema  
- Processos capturando teclado  
- Conexões SMTP recorrentes  
- Geração automática de chaves criptográficas  
- Threads executando loops infinitos  

---

# 🛡️ Como Defender Sistemas Contra Esse Tipo de Código

- Bloquear scripts Python não assinados  
- Restringir bibliotecas de captura de teclado  
- Inspecionar tráfego SMTP  
- Monitorar criação de arquivos suspeitos  
- Usar EDR com heurística comportamental  
- Executar scripts desconhecidos apenas em sandbox  

---

# 📚 Conclusão

Este projeto demonstra:

- Entendimento técnico sobre captura de teclas  
- Compreensão de criptografia simétrica  
- Capacidade de estruturar programas com múltiplas threads  
- Conhecimento de técnicas utilizadas em keyloggers reais  
- Habilidade de documentar e analisar comportamento de malware  

Este repositório serve como estudo avançado para quem busca atuar em:

- SOC (Blue Team)  
- DFIR  
- Análise de malware  
- Segurança ofensiva ética (Red Team)



This repository documents a keylogger **developed by me**, created strictly for **educational purposes**, malware analysis training, and security research inside controlled environments.

> ⚠️ Ethical Notice  
> This code must **only** be executed in isolated, authorized labs.  
> Unauthorized use is illegal.

---

## 🧩 Global Architecture

The keylogger implements:

1. Keystroke monitoring  
2. Buffered logging  
3. Symmetric encryption  
4. Data transmission via email  

Below is the full breakdown, function by function.

---

# 🛠️ Code Walkthrough — Function by Function

## `capturar_tecla(event)`
Captures keyboard events and formats special keys.  
Adds captured characters to a buffer queue.

## `gravar_buffer()`
Background thread that writes queued keystrokes into `log.txt`.  
This simulates typical behavior seen in keylogging malware.

## Encryption functions
- `gerar_chave()` — generates encryption key if missing  
- `carregar_chave()` — loads encryption key  
- `criptografar_log()` — encrypts log file (Fernet)  
- `descriptografar_log()` — decrypts the encrypted file  

This mirrors real malware that encrypts stolen data.

## `enviar_email()`
Prepares an SMTP message and sends the encrypted log as an attachment.  
Reflects exfiltration techniques used by simple stealers and RATs.

## `enviar_email_periodico()`
Sends encrypted logs periodically in a background loop.

## Main execution block
Initializes all components, starts threads and begins capturing keystrokes.

---

# 🔍 Indicators of Compromise (IoCs)

- Files: `log.txt`, `log_encrypted.txt`, `chave.key`  
- Keyboard hooks active on the system  
- Recurring SMTP connections  
- Continuous background threads  
- Cryptographic key generation  

---

# 🛡️ Defensive Recommendations

- Block unauthorized Python execution  
- Restrict keyboard hook libraries  
- Monitor SMTP traffic  
- Detect suspicious file creation patterns  
- Use EDR behavioral detection  

---

# 📚 Conclusion

This project demonstrates:

- Understanding of keylogging mechanics  
- Cryptographic handling with Fernet  
- Multithreaded architecture  
- Practical malware behavior patterns  
- Professional documentation and analysis  

It is suitable for portfolios related to:

- SOC / Blue Team  
- Malware Analysis  
- DFIR  
- Ethical Offensive Security / Red Team
