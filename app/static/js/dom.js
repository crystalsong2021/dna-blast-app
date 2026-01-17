// dom.js - Cached DOM element references

const DOMElements = {
  form: null,
  fastaText: null,
  fastaFile: null,
  fileUploadArea: null,
  uploadPrompt: null,
  fileNameDisplay: null,
  importFileBtn: null,
  submitBtn: null,
  loadExample: null,
  toggleFileUpload: null,
  fileDrawer: null,
  fileDrawerBackdrop: null,
  closeDrawer: null,
  progressContainer: null,
  currentSequence: null,
  progressBar: null,
  progressText: null,
  errorContainer: null,
  errorMessage: null,
  resultsContainer: null,
  resultsTabs: null,
  resultsTabContent: null,

  init() {
    this.form = document.getElementById('blastForm');
    this.fastaText = document.getElementById('fastaText');
    this.fastaFile = document.getElementById('fastaFile');
    this.fileUploadArea = document.getElementById('fileUploadArea');
    this.uploadPrompt = document.getElementById('uploadPrompt');
    this.fileNameDisplay = document.getElementById('fileNameDisplay');
    this.importFileBtn = document.getElementById('importFileBtn');
    this.submitBtn = document.getElementById('submitBtn');
    this.loadExample = document.getElementById('loadExample');
    this.toggleFileUpload = document.getElementById('toggleFileUpload');
    this.fileDrawer = document.getElementById('fileDrawer');
    this.fileDrawerBackdrop = document.getElementById('fileDrawerBackdrop');
    this.closeDrawer = document.getElementById('closeDrawer');
    this.progressContainer = document.getElementById('progressContainer');
    this.currentSequence = document.getElementById('currentSequence');
    this.progressBar = document.getElementById('progressBar');
    this.progressText = document.getElementById('progressText');
    this.errorContainer = document.getElementById('errorContainer');
    this.errorMessage = document.getElementById('errorMessage');
    this.resultsContainer = document.getElementById('resultsContainer');
    this.resultsTabs = document.getElementById('resultsTabs');
    this.resultsTabContent = document.getElementById('resultsTabContent');
  }
};

// Export for use in other modules
window.DOMElements = DOMElements;