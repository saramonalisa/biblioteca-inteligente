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

$(".detalhar-livro").click(function () {
  const url = $(this).data("url");
  $.get(url,
    (resposta) => {
      $("#modal-livro .modal-body").html(resposta);
    }
  );
});