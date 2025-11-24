# 📧 Sistema de Envio de E-mails para Egressos - Fatec Zona Leste

Este projeto foi desenvolvido para facilitar o envio de e-mails personalizados aos egressos da Fatec Zona Leste.  
Ele permite selecionar um arquivo CSV com os dados dos ex-alunos, visualizar os registros, enviar mensagens em massa e manter um histórico dos envios realizados.

---

## 🚀 Funcionalidades

- **Splash Screen**: Tela inicial com a identidade visual da Fatec.
- **Tela Principal**:
  - Seleção de arquivo CSV com dados dos egressos.
  - Visualização do histórico de envios.
- **Modal de Gerenciamento**:
  - Visualização dos dados do CSV em tabela.
  - Envio de e-mails personalizados para cada egresso.
  - Exclusão do arquivo selecionado.
- **Histórico de Envios**:
  - Registro automático de cada envio (arquivo, data, quantidade e status).
- **Centralização de janelas**: Todas as telas e modais abrem centralizadas na tela.
- **Resumo automático**: Após cada envio, o remetente recebe um e-mail resumo.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (interface gráfica)
- [Pandas](https://pandas.pydata.org/) (manipulação de CSV)
- [Yagmail](https://github.com/kootenpv/yagmail) (envio de e-mails)
- [PyInstaller](https://pyinstaller.org/) (geração de executável)

---

## 📂 Estrutura do Projeto

