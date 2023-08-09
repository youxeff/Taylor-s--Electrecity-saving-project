function selectExportOption() {
    var exportOptions = {
      userlist: "Export User List",
      billinglist: "Export Billing List",
      cancel: "Cancel"
    };
  
    var exportButtons = Object.keys(exportOptions).map(function(option) {
      var button = document.createElement("button");
      button.className = "export-option";
      button.innerText = exportOptions[option];
      button.addEventListener("click", function() {
        if (option === "cancel") {
          window.location.href = "/dashboard";
        } else {
          window.location.href = "/export_data?option=" + option;
        }
      });
      return button;
    });
  
    var container = document.createElement("div");
    container.className = "export-options";
    exportButtons.forEach(function(button) {
      container.appendChild(button);
    });
  
    var modal = document.createElement("div");
    modal.className = "export-modal";
    modal.appendChild(container);
    document.body.appendChild(modal);
  
    container.addEventListener("click", function(event) {
      event.stopPropagation();
      document.body.removeChild(modal);
    });
  }
  