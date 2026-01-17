// state.js - Centralized state management

const BlastState = {
  selectedFile: null,
  fileContent: null,
  sequences: [],
  allResults: [],
  currentSequenceIndex: 0,

  reset() {
    this.selectedFile = null;
    this.fileContent = null;
    this.sequences = [];
    this.allResults = [];
    this.currentSequenceIndex = 0;
  },

  setFile(file, content) {
    this.selectedFile = file;
    this.fileContent = content;
  },

  clearFile() {
    this.selectedFile = null;
    this.fileContent = null;
  },

  setSequences(sequences) {
    this.sequences = sequences;
  },

  addResult(result) {
    this.allResults.push(result);
  },

  getResultCount() {
    return this.allResults.length;
  },

  getTotalSequences() {
    return this.sequences.length;
  }
};

// Export for use in other modules
window.BlastState = BlastState;