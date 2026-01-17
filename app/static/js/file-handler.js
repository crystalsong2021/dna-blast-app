// file-handler.js - File upload and management

const FileHandler = {
  /**
   * Handle file selection
   */
  handleFileSelect(file) {
    if (!file) return;

    const elements = window.DOMElements;
    const state = window.BlastState;

    // Validate file type
    const validExtensions = ['.fasta', '.fa', '.txt'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));

    if (!isValid) {
      window.UIHelpers.showError('Invalid file type. Please upload a FASTA file (.fasta, .fa, or .txt)');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      window.UIHelpers.showError('File is too large. Maximum size is 10MB');
      return;
    }

    // Read file content
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      state.setFile(file, content);

      // Update UI
      elements.uploadPrompt.style.display = 'none';
      elements.fileNameDisplay.style.display = 'block';
      elements.importFileBtn.style.display = 'block';

      elements.fileNameDisplay.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>Selected:</strong> ${file.name}
            <br>
            <small class="text-muted">${window.UIHelpers.formatFileSize(file.size)}</small>
          </div>
          <button type="button" class="btn btn-sm btn-danger" id="removeFile">
            Remove
          </button>
        </div>
      `;

      document.getElementById('removeFile').addEventListener('click', () => {
        this.clearFileSelection();
      });
    };
    reader.readAsText(file);
  },

  /**
   * Import file content to text box
   */
  importFileToTextBox() {
    const elements = window.DOMElements;
    const state = window.BlastState;

    if (state.fileContent) {
      elements.fastaText.value = state.fileContent;
      this.closeDrawer();

      // Show success message
      const originalPlaceholder = elements.fastaText.placeholder;
      elements.fastaText.placeholder = '✓ File imported successfully! Click "Run BLAST Search" to begin.';
      setTimeout(() => {
        elements.fastaText.placeholder = originalPlaceholder;
      }, 3000);
    }
  },

  /**
   * Clear file selection
   */
  clearFileSelection() {
    const elements = window.DOMElements;
    const state = window.BlastState;

    state.clearFile();
    elements.fastaFile.value = '';
    elements.uploadPrompt.style.display = 'block';
    elements.fileNameDisplay.style.display = 'none';
    elements.importFileBtn.style.display = 'none';
  },

  /**
   * Open file drawer
   */
  openDrawer() {
    const elements = window.DOMElements;
    elements.fileDrawer.classList.add('open');
    elements.fileDrawerBackdrop.classList.add('show');
  },

  /**
   * Close file drawer
   */
  closeDrawer() {
    const elements = window.DOMElements;
    elements.fileDrawer.classList.remove('open');
    elements.fileDrawerBackdrop.classList.remove('show');
  }
};

// Export for use in other modules
window.FileHandler = FileHandler;