document.addEventListener("DOMContentLoaded", function () {
  var fileUpload = document.getElementById("file-upload");
  var parseBtn = document.getElementById("parse-btn");
  var select_article_fields = document.getElementById("select-article-fields");
  var inputFields = document.getElementById("input-fields");
  var submitBtn = document.getElementById("submit-btn");
  var result = document.getElementById("result");

  // 全局变量
  var article_index = 0;
  var JSON_data = null;

  fileUpload.addEventListener("change", function (event) {
    var file = event.target.files[0];

    if (file && file.type === "application/json") {
      parseBtn.removeAttribute("disabled");
      select_article_btn.removeAttribute("disabled");
    } else {
      parseBtn.setAttribute("disabled", "true");
      inputFields.innerHTML = "";
      submitBtn.setAttribute("disabled", "true");
      result.innerHTML = "";
      alert("请选择一个 JSON 文件");
    }
  });

  parseBtn.addEventListener("click", function () {
    var file = fileUpload.files[0];
    var reader = new FileReader();

    reader.onload = function (event) {
      var json = JSON.parse(event.target.result);
      JSON_data = json;

      select_article_fields.innerHTML = "";
      inputFields.innerHTML = "";
      result.innerHTML = "";

      // 创建一个下拉列表框
      var dropdown = document.createElement("select");
      dropdown.id = "options";
      select_article_fields.appendChild(dropdown);

      var option = document.createElement("option");
      option.value = "";                  // 默认选项值为空字符串
      option.textContent = "请选择文章";   // 默认显示文字 "请选择文章"
      dropdown.appendChild(option);

      for (var i = 0; i < json.length; i++) {
        var title = json[i]["title"];
        option = document.createElement("option");
        option.value = i;             // 选项的值为文章的索引
        option.textContent = title;   // 选项的显示文本为文章的标题
        dropdown.appendChild(option);
      }

      dropdown.addEventListener("change", function () {
        var articleIndex = parseInt(dropdown.value); // 获取选中的文章索引
        article_index = articleIndex;
        inputFields.innerHTML = ""; // 清空输入框区域

        if (!isNaN(articleIndex)) {
          var article = json[articleIndex];

          for (var i = 0; i < article.hints.length; i++) {
            var inputWrapper = document.createElement("div");
            inputWrapper.className = "input-wrapper";

            var label = document.createElement("label");
            label.textContent = "请输入一个" + article.hints[i] + ": ";

            var inputField = document.createElement("input");
            inputField.type = "text";

            inputWrapper.appendChild(label);
            inputWrapper.appendChild(inputField);
            inputFields.appendChild(inputWrapper);
          }

          submitBtn.removeAttribute("disabled");
        } else {
          submitBtn.setAttribute("disabled", "true");
        }
      });
    };

    reader.readAsText(file);
  });

  submitBtn.addEventListener("click", function () {
    var inputs = inputFields.getElementsByTagName("input");
    var article = JSON_data[article_index];
    var text = article["article"];

    // 文本替换
    for (var i = 0; i < inputs.length; i++) {
      text = text.replace("<" + (i + 1) + ">", inputs[i].value);
    }

    result.innerHTML = text;
  });
});