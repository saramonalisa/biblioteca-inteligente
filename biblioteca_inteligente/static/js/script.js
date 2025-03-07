const spinner = `
<div class="d-flex justify-content-center align-items-center" style="height: 200px;">
    <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
</div>`

function buscarMensagens() {
  $.get(mensagensUrl,
    (resposta) => {
      $("#div-mensagens").html(resposta);
    }
  );
}

function criarEventoPaginacao() {
  $(".page-link").click(function(evento) {
    evento.preventDefault();
    const url = $(this).data("url");
    $(".album").html(spinner);
    $.get(
      url,
      (resposta) => {
        $(".album").html(resposta);
        criarEventoPaginacao();
      }
    );
  });
}
criarEventoPaginacao();