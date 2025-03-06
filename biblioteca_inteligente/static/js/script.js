function buscarMensagens() {
    $.get(mensagensUrl,
      (resposta) => {
        $("#div-mensagens").html(resposta);
      }
    );
  }