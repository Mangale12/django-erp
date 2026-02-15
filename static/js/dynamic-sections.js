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

    resetRowInputs($newRow, sectionName, index);
    $tbody.append($newRow);

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
