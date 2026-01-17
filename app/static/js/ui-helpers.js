// ui-helpers.js - UI utility functions

const UIHelpers = {
  /**
   * Format file size for display
   */
  formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  },

  /**
   * Format E-value for display
   */
  formatEValue(eValue) {
    if (eValue === 0) return '0.0';
    if (eValue < 0.0001) return eValue.toExponential(2);
    return eValue.toFixed(4);
  },

  /**
   * Escape HTML for safe insertion
   */
  escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, function (s) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[s];
    });
  },

  /**
   * Show error message
   */
  showError(message) {
    const elements = window.DOMElements;
    elements.errorContainer.style.display = 'block';
    elements.errorMessage.textContent = message;
    elements.errorContainer.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest'
    });
  },

  /**
   * Hide error message
   */
  hideError() {
    const elements = window.DOMElements;
    elements.errorContainer.style.display = 'none';
  },

  /**
   * Show progress container
   */
  showProgress() {
    const elements = window.DOMElements;
    elements.progressContainer.style.display = 'block';
  },

  /**
   * Hide progress container
   */
  hideProgress() {
    const elements = window.DOMElements;
    elements.progressContainer.style.display = 'none';
  },

  /**
   * Update progress bar
   */
  updateProgress(current, total, sequenceId) {
    const elements = window.DOMElements;
    const percent = (current / total) * 100;
    elements.progressBar.style.width = `${percent}%`;
    elements.progressBar.setAttribute('aria-valuenow', percent);

    // Ensure animation classes are present
    if (!elements.progressBar.classList.contains('progress-bar-striped')) {
      elements.progressBar.classList.add('progress-bar-striped', 'progress-bar-animated');
    }

    elements.progressText.textContent = `Processing sequence ${current} of ${total}`;
    elements.currentSequence.innerHTML = `
      <div class="d-flex align-items-center">
        <span class="spinner-border spinner-border-sm me-2" role="status"></span>
        <strong>Current:</strong>&nbsp;${sequenceId}
      </div>
    `;
  }
};

// Export for use in other modules
window.UIHelpers = UIHelpers;