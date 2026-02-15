$(document).on("click", function (e) {

  /* ===============================
     ADD ROW
  =============================== */
  const $addBtn = $(e.target).closest(".add-row");
  if ($addBtn.length) {

    const sectionName = $addBtn.data("section");
    const $section = $addBtn.closest(".dynamic-section");
    const $tbody = $section.find(".dynamic-rows");

    // Clone first row as template
    const $templateRow = $tbody.find(".dynamic-row").first();
    const $newRow = $templateRow.clone();

    const index = $tbody.children().length;

    cleanClonedSelect2($newRow);
    resetRowInputs($newRow, sectionName, index);
    $tbody.append($newRow);
    initializeRowSelects($newRow);

    return;
  }

  /* ===============================
     REMOVE ROW
  =============================== */
  const $removeBtn = $(e.target).closest(".remove-row");
  if ($removeBtn.length) {

    const $tbody = $removeBtn.closest("tbody");

    // Optional: prevent removing last row
    if ($tbody.children().length === 1) return;

    $removeBtn.closest(".dynamic-row").remove();
    reindexRows($tbody);

    return;
  }
});


/* ===============================
   HELPERS
=============================== */

function resetRowInputs($row, sectionName, index) {

  // Remove any calculated data attached to the row
  $row.removeAttr("data-total");

  $row.find("input, select, textarea").each(function () {
    const $el = $(this);

    /* ---- Update name [index] ---- */
    if ($el.attr("name")) {
      $el.attr(
        "name",
        $el.attr("name").replace(/\[\d+\]/g, `[${index}]`)
      );
    }

    /* ---- Reset value ---- */
    if ($el.is(":checkbox, :radio")) {
      $el.prop("checked", false);

    } else if ($el.is("select")) {
      $el.val("");          // HARD reset
      $el.find("option:selected").prop("selected", false);

    } else {
      $el.val("");          // clears readonly too
    }

    /* ---- Remove validation state ---- */
    $el.removeClass("is-valid is-invalid");
  });
}



function reindexRows($tbody) {
  $tbody.children(".dynamic-row").each(function (index) {
    $(this).find("input, select, textarea").each(function () {
      const $el = $(this);
      if ($el.attr("name")) {
        $el.attr(
          "name",
          $el.attr("name").replace(/\[\d+\]/, `[${index}]`)
        );
      }
    });
  });
}

function cleanClonedSelect2($row) {
  $row.find("span.select2").remove();

  $row.find("select").each(function () {
    const $select = $(this);
    $select.removeClass("select2-hidden-accessible");
    $select.removeAttr("data-select2-id tabindex aria-hidden");
    $select.find("option").removeAttr("data-select2-id");
  });
}

function initializeRowSelects($row) {
  if (!$.fn.select2) return;

  const $modal = $row.closest(".modal");

  $row.find("select").each(function () {
    const $select = $(this);
    const url = $select.data("url");
    const label = $select.data("field-name") || "option";
    const placeholder = $select.find("option:first").text() || `Select ${label}`;
    const config = {
      theme: "bootstrap-5",
      width: "100%",
      placeholder: placeholder,
      allowClear: !$select.prop("required"),
      dropdownParent: $modal.length ? $modal : undefined
    };

    if (url) {
      config.ajax = {
        url: url,
        dataType: "json",
        delay: 250,
        data: function (params) {
          return {
            q: params.term,
            page: params.page || 1
          };
        },
        processResults: function (data, params) {
          return {
            results: data.results || data,
            pagination: {
              more: (params.page || 1) < ((data.pagination && data.pagination.total_pages) || 1)
            }
          };
        },
        cache: true
      };
      config.minimumInputLength = 0;
    }

    $select.select2(config);
  });
}
