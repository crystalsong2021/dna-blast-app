// Main application controller
// Dependencies: state.js, dom.js, ui-helpers.js, results.js, api.js, file-handler.js

document.addEventListener('DOMContentLoaded', () => {
  // Initialize modules
  DOMElements.init();
  const elements = DOMElements;
  const state = BlastState;

  // Example sequence
  const EXAMPLE_SEQUENCE = `>NC_009085.1 Acinetobacter baumannii 16S ribosomal RNA
ATTGAACGCTGGCGGCAGGCTTAACACATGCAAGTCGAGCGGGGGAAGGTAGCTTGCTAC
TGGACCTAGCGGCGGACGGGTGAGTAATGCTTAGGAATCTGCCTATTAGTGGGGGACAAC
ATCTCGAAAGGGATGCTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGATCTTCGGA
CCTTGCGCTAATAGATGAGCCTAAGTCGGATTAGCTAGTTGGTGGGGTAAAGGCCTACCA
AGGCGACGATCTGTAGCGGGTCTGAGAGGATGATCCGCCACACTGGGACTGAGACACGGC
CCAGA`;

  /**
   * Load example sequence
   */
  const loadExampleSequence = () => {
    resetUI();
    elements.fastaText.value = EXAMPLE_SEQUENCE;
    FileHandler.clearFileSelection();
  };

  /**
   * Reset UI to initial state
   */
  const resetUI = () => {
    elements.resultsTabs.innerHTML = '';
    elements.resultsTabContent.innerHTML = '';
    elements.resultsContainer.style.display = 'none';
    UIHelpers.hideProgress();
    UIHelpers.hideError();
  };

  /**
   * Reset form after successful submission
   */
  const resetForm = () => {
    elements.fastaText.value = '';
    FileHandler.clearFileSelection();
    FileHandler.closeDrawer();
  };

  /**
   * Main BLAST submission handler with streaming results
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    UIHelpers.hideError();

    // Validate input
    const hasText = elements.fastaText.value.trim().length > 0;
    if (!hasText) {
      UIHelpers.showError('Please enter a sequence or upload a file');
      return;
    }

    // Reset UI for new search
    resetUI();
    state.reset();

    elements.submitBtn.disabled = true;

    try {
      // Step 1: Validate and parse sequences
      const data = await BlastAPI.validateSequences(elements.fastaText.value);

      if (!data.success) {
        UIHelpers.showError(data.error);
        elements.submitBtn.disabled = false;
        return;
      }

      state.setSequences(data.sequences);
      const sequences = data.sequences;

      // Step 2: Show progress
      UIHelpers.showProgress();

      // Step 3: Process sequences with streaming results
      await BlastAPI.processSequencesStreaming(
        sequences,
        // onProgress callback
        (current, total, seqId) => {
          UIHelpers.updateProgress(current, total, seqId);
        },
        // onResult callback - called immediately when each result arrives
        (result, index) => {
          state.addResult(result);
          ResultsRenderer.addResultTab(result, index);
        },
        // onComplete callback
        () => {
          UIHelpers.hideProgress();
          resetForm();
          console.log('All BLAST searches completed');
        },
        // onError callback
        (errorMsg, index) => {
          UIHelpers.showError(errorMsg);
          // Still add an empty result tab for failed sequence
          ResultsRenderer.addResultTab({
            sequence_id: sequences[index].id,
            query_length: sequences[index].sequence.length,
            hits: []
          }, index);
        }
      );

    } catch (error) {
      UIHelpers.showError(`Error: ${error.message}`);
      UIHelpers.hideProgress();
    } finally {
      elements.submitBtn.disabled = false;
    }
  };

  // ==================== Event Listeners ====================

  // Load example
  elements.loadExample.addEventListener('click', loadExampleSequence);

  // Form submission
  elements.form.addEventListener('submit', handleSubmit);

  // File drawer controls
  elements.toggleFileUpload.addEventListener('click', () => {
    resetUI();
    FileHandler.openDrawer();
  });
  elements.closeDrawer.addEventListener('click', () => FileHandler.closeDrawer());
  elements.fileDrawerBackdrop.addEventListener('click', () => FileHandler.closeDrawer());
  elements.importFileBtn.addEventListener('click', () => FileHandler.importFileToTextBox());

  // File upload area
  elements.fileUploadArea.addEventListener('click', (e) => {
    if (!e.target.closest('#removeFile')) {
      elements.fastaFile.click();
    }
  });

  elements.fastaFile.addEventListener('change', (e) => {
    FileHandler.handleFileSelect(e.target.files[0]);
  });

  // Drag and drop
  elements.fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.fileUploadArea.classList.add('drag-over');
  });

  elements.fileUploadArea.addEventListener('dragleave', () => {
    elements.fileUploadArea.classList.remove('drag-over');
  });

  elements.fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.fileUploadArea.classList.remove('drag-over');

    const file = e.dataTransfer.files[0];
    if (file) {
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      elements.fastaFile.files = dataTransfer.files;
      FileHandler.handleFileSelect(file);
    }
  });

  console.log('DNA BLAST Search application initialized (Refactored)');
});