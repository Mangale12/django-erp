class NestedFormManager {
    constructor(formSelector) {
      this.form = document.querySelector(formSelector);
      if (!this.form) return;
      
      this.initEventListeners();
      this.initExistingItems();
    }
  
    initEventListeners() {
      // Add item button
      this.form.addEventListener('click', (e) => {
        if (e.target.closest('.add-nested-item')) {
          const btn = e.target.closest('.add-nested-item');
          this.addItem(btn.dataset.section);
        }
      });
  
      // Remove item
      this.form.addEventListener('click', (e) => {
        if (e.target.closest('.remove-nested-item')) {
          e.target.closest('.nested-item-row').remove();
          this.validateMinItems();
        }
      });
  
      // Menu item selection → load price & modifiers
      this.form.addEventListener('change', (e) => {
        if (e.target.classList.contains('nested-menu-item-select')) {
          this.loadItemDetails(e.target);
        }
      });
  
      // Recalculate totals
      this.form.addEventListener('input', (e) => {
        if (e.target.classList.contains('quantity-input') || 
            e.target.classList.contains('unit-price-input')) {
          this.recalculateRow(e.target.closest('.nested-item-row'));
        }
      });
  
      // Form submit override for nested data
      this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }
  
    addItem(sectionName) {
      const container = document.getElementById(`${sectionName}-container`);
      const template = document.getElementById(`${sectionName}-template`);
      const clone = document.importNode(template.content, true);
      
      // Replace __INDEX__ with timestamp for unique names
      const index = Date.now();
      clone.querySelectorAll('[name]').forEach(el => {
        el.name = el.name.replace(/__INDEX__/g, index);
      });
      clone.querySelectorAll('[id]').forEach(el => {
        if (el.id.includes('__INDEX__')) el.id = el.id.replace(/__INDEX__/g, index);
      });
      
      container.appendChild(clone);
      this.initSelects(container.lastElementChild); // Re-init Select2 if used
      this.validateMinItems(sectionName);
    }
  
    async loadItemDetails(select) {
      const row = select.closest('.nested-item-row');
      const itemId = select.value;
      const modifierContainer = row.querySelector('.modifier-container');
      const priceInput = row.querySelector('.unit-price-input');
      
      if (!itemId) return;
      
      modifierContainer.innerHTML = '<div class="spinner-border spinner-border-sm"></div>';
      
      try {
        // REUSE YOUR EXISTING SELECT2 ENDPOINT! (Smart reuse)
        const response = await fetch(`${select.dataset.url}?term=${itemId}`);
        const data = await response.json();
        
        // Find selected item in results (your select endpoint returns "results" array)
        const item = data.results.find(i => i.id == itemId);
        if (item && item.price) {
          priceInput.value = item.price;
          this.recalculateRow(row);
        }
        
        // Load modifiers via dedicated endpoint (create this)
        const modsRes = await fetch(`/api/menu-items/${itemId}/modifiers/`);
        const mods = await modsRes.json();
        
        if (mods.length) {
          modifierContainer.innerHTML = mods.map(m => `
            <div class="form-check form-check-inline">
              <input class="form-check-input modifier-checkbox" type="checkbox" 
                     name="${select.name.replace('[menu_item]', '[modifiers][]')}" 
                     value="${m.id}">
              <label class="form-check-label">${m.name} ${m.price ? '(+'+m.price+')' : ''}</label>
            </div>
          `).join('');
        } else {
          modifierContainer.innerHTML = '<small class="text-muted">No modifiers available</small>';
        }
      } catch (err) {
        modifierContainer.innerHTML = '<small class="text-danger">Failed to load details</small>';
        console.error(err);
      }
    }
  
    recalculateRow(row) {
      const qty = parseFloat(row.querySelector('.quantity-input').value) || 0;
      const price = parseFloat(row.querySelector('.unit-price-input').value) || 0;
      row.querySelector('.total-price-input').value = (qty * price).toFixed(2);
    }
  
    validateMinItems(sectionName) {
      const container = document.getElementById(`${sectionName}-container`);
      const min = container.closest('[data-min-items]')?.dataset.minItems || 0;
      const count = container.querySelectorAll('.nested-item-row').length;
      
      if (count < min) {
        // Show visual warning (implement your UI pattern)
        alert(`At least ${min} item(s) required!`);
      }
    }
  
    initExistingItems() {
      // Auto-recalculate pre-rendered items on modal open
      this.form.querySelectorAll('.nested-item-row').forEach(row => {
        this.recalculateRow(row);
      });
    }
  
    initSelects(container) {
      // If using Select2: $(container).find('select').select2();
    }
  
    // CRITICAL: Transform nested form data into API-ready structure
    getNestedData() {
      const sections = {};
      this.form.querySelectorAll('.nested-items-container').forEach(container => {
        const sectionName = container.id.replace('-container', '');
        sections[sectionName] = [];
        
        container.querySelectorAll('.nested-item-row').forEach(row => {
          const itemData = {};
          row.querySelectorAll('[name]').forEach(input => {
            // Parse nested name: order_items[0][menu_item]
            const match = input.name.match(/(\w+)\[(\d+)\]\[(\w+)\]/);
            if (match && match[3] !== 'modifiers') {
              itemData[match[3]] = input.value;
            }
          });
          
          // Collect checked modifiers
          const modifiers = Array.from(row.querySelectorAll('.modifier-checkbox:checked'))
            .map(cb => cb.value);
          if (modifiers.length) itemData.modifiers = modifiers;
          
          sections[sectionName].push(itemData);
        });
      });
      return sections;
    }
  
    async handleSubmit(e) {
      e.preventDefault();
      if (!this.form.dataset.isOrderModal) return; // Skip for simple forms
      
      // Validate top-level fields first
      if (!this.form.checkValidity()) {
        this.form.reportValidity();
        return;
      }
  
      // Build payload matching your create_order endpoint
      const payload = {
        ...Object.fromEntries(new FormData(this.form).entries()),
        ...this.getNestedData()
      };
      
      // Remove empty top-level fields that shouldn't be sent
      ['id', 'csrfmiddlewaretoken'].forEach(key => delete payload[key]);
      
      try {
        const response = await fetch(this.form.dataset.submitUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken()
          },
          body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        if (data.success) {
          bootstrap.Modal.getInstance(this.form.closest('.modal')).hide();
          // Show toast notification (implement your pattern)
          location.reload(); // Or redirect per data.redirect_url
        } else {
          alert(`Error: ${data.error}`);
        }
      } catch (err) {
        alert('Submission failed. Check console for details.');
        console.error(err);
      }
    }
  
    getCSRFToken() {
      return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
             document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    }
  }
  
  // AUTO-INIT on modal show (works with Bootstrap 5)
  document.addEventListener('DOMContentLoaded', () => {
    const orderModal = document.getElementById('orderModal');
    if (orderModal) {
      orderModal.addEventListener('shown.bs.modal', () => {
        new NestedFormManager('#orderForm');
      });
    }
    
    // Also init if modal is already open (for SPA scenarios)
    if (document.querySelector('#orderModal.show')) {
      new NestedFormManager('#orderForm');
    }
  });