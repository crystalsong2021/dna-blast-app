// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Cache DOM elements
    const elements = {
        form: document.getElementById('blastForm'),
        fastaText: document.getElementById('fastaText'),
        loadTestBtn: document.getElementById('loadTestExample'),
        loadRealBtn: document.getElementById('loadRealExample'),
        results: document.getElementById('results'),
        queryInfo: document.getElementById('queryInfo'),
        resultsTable: document.getElementById('resultsTable'),
        error: document.getElementById('error')
    };

    // Constants
    const TEST_SEQUENCE = `>test
ATCGATCGATCG`;

    const REAL_EXAMPLE_SEQUENCE = `>NC_009085_A1S_r15
ATTGAACGCTGGCGGCAGGCTTAACACATGCAAGTCGAGCGGGGGAAGGTAGCTTGCTAC
TGGACCTAGCGGCGGACGGGTGAGTAATGCTTAGGAATCTGCCTATTAGTGGGGGACAAC
ATCTCGAAAGGGATGCTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGATCTTCGGA
CCTTGCGCTAATAGATGAGCCTAAGTCGGATTAGCTAGTTGGTGGGGTAAAGGCCTACCA
AGGCGACGATCTGTAGCGGGTCTGAGAGGATGATCCGCCACACTGGGACTGAGACACGGC
CCAGA`;

    /**
     * Load test sequence (0 hits) into textarea
     */
    const loadTestExample = () => {
        console.log('Load test example clicked');
        elements.fastaText.value = TEST_SEQUENCE;
        console.log('Test sequence loaded');
    };

    /**
     * Load real example sequence into textarea
     */
    const loadRealExample = () => {
        console.log('Load real example clicked');
        console.log('Textarea element:', elements.fastaText);
        elements.fastaText.value = REAL_EXAMPLE_SEQUENCE;
        console.log('Value set to:', elements.fastaText.value);
    };

    /**
     * Display results in the table
     * @param {Object} data - Response data from server
     */
    const showResults = (data) => {
        elements.results.style.display = 'block';
        elements.queryInfo.textContent = `Query: ${data.query_id} | Hits: ${data.hits.length}`;

        // Clear previous results
        elements.resultsTable.innerHTML = '';

        // Populate table with hits
        data.hits.forEach(hit => {
            const row = elements.resultsTable.insertRow();
            row.innerHTML = `
                <td>${hit.title.substring(0, 40)}</td>
                <td>${hit.accession}</td>
                <td>${hit.percent_identity}%</td>
            `;
        });
    };

    /**
     * Display error message
     * @param {string} message - Error message to display
     */
    const showError = (message) => {
        elements.error.style.display = 'block';
        elements.error.textContent = message;
    };

    /**
     * Hide all result and error displays
     */
    const clearDisplay = () => {
        elements.results.style.display = 'none';
        elements.error.style.display = 'none';
    };

    /**
     * Handle form submission
     * @param {Event} e - Submit event
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        clearDisplay();

        console.log('Form submitted');
        console.log('Textarea value:', elements.fastaText.value);

        try {
            const formData = new FormData(elements.form);
            console.log('FormData entries:');
            for (let pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }

            const response = await fetch('/blast', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            console.log('Response data:', data);

            if (data.success) {
                showResults(data);
            } else {
                showError(data.error || 'An error occurred during BLAST search');
            }
        } catch (err) {
            console.error('Fetch error:', err);
            showError(`Error: ${err.message}`);
        }
    };

    // Attach event listeners
    console.log('Attaching event listeners...');
    console.log('Elements found:', {
        form: !!elements.form,
        fastaText: !!elements.fastaText,
        loadTestBtn: !!elements.loadTestBtn,
        loadRealBtn: !!elements.loadRealBtn
    });

    elements.loadTestBtn.addEventListener('click', loadTestExample);
    elements.loadRealBtn.addEventListener('click', loadRealExample);
    elements.form.addEventListener('submit', handleSubmit);

    console.log('Event listeners attached successfully');
});