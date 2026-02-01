function renderActionButtons(id, options = {}) {
    let buttons = `<div class="btn-group btn-group-sm gap-1">`;

    if (options.show) {
        buttons += `
            <a href="${options.show.replace('{id}', id)}"
               class="btn btn-outline-info me-2">
                <i data-feather="eye"></i>
            </a>`;
    }

    if (options.edit) {
        buttons += `
           <button class="btn btn-primary edit-btn" data-title="${options.title}" data-id="${id}" data-url="${options.edit}" data-bs-toggle="modal" data-bs-target="${options.modal_id}">
            <i data-feather="edit"></i>
        </button>`;
    }

    if (options.delete) {
        buttons += `
            <button class="btn btn-outline-danger me-2"
                    data-id="${id}"
                    data-action="delete">
                <i data-feather="trash"></i>
            </button>`;
    }

    buttons += `</div>`;
    return buttons;
}
