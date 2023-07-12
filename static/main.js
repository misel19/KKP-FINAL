$(document).ready(function () {
  // Init
  $(".image-section").hide();
  $(".loader").hide();
  $("#result").hide();

  // Upload Preview
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#uploaded-image").attr("src", e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#image").change(function () {
    $(".image-section").show();
    $("#submit-btn").show();
    $("#result").text("");
    $("#result").hide();
    readURL(this);
  });

  // Predict
  $("#upload-form").submit(function (event) {
    event.preventDefault();
    var form_data = new FormData($(this)[0]);

    // tampilan loading animation
    $("#submit-btn").hide();
    $(".loader").show();

    // Membuat prediction by calling API /predict
    $.ajax({
      type: "POST",
      url: "/result",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Handle success response
        if (data.success) {
          // Redirect ke halaman result
          window.location.href = "/result";
        }
      },
      error: function (xhr, status, error) {
        // Tampilan error
        alert("Deteksi Gagal, silahkan upload gambar yang baik");
        $("#submit-btn").show();
        $(".loader").hide();
      },
    });
  });
});