// api.js - API communication layer

const BlastAPI = {
  /**
   * Validate and parse sequences
   */
  async validateSequences(fastaText) {
    const formData = new FormData();
    formData.append('fasta_text', fastaText);

    const response = await fetch('/blast', {
      method: 'POST',
      body: formData
    });

    return await response.json();
  },

  /**
   * Run BLAST for a single sequence
   */
  async blastSingleSequence(sequenceId, sequence) {
    const response = await fetch('/blast_single', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sequence_id: sequenceId,
        sequence: sequence
      })
    });

    return await response.json();
  },

  /**
   * Process multiple sequences with streaming results
   * Calls onResult callback as each result arrives
   */
  async processSequencesStreaming(sequences, onProgress, onResult, onComplete, onError) {
    const total = sequences.length;

    for (let i = 0; i < sequences.length; i++) {
      const seqObj = sequences[i];

      // Update progress (i+1 for 1-based counting)
      if (onProgress) {
        onProgress(i + 1, total, seqObj.id);
      }

      try {
        const data = await this.blastSingleSequence(seqObj.id, seqObj.sequence);

        if (data && data.success) {
          // Call result callback immediately when result arrives
          if (onResult) {
            onResult(data, i);
          }
        } else {
          if (onError) {
            onError(`BLAST failed for ${seqObj.id}: ${data.error || 'unknown error'}`, i);
          }
        }
      } catch (err) {
        if (onError) {
          onError(`Network error for ${seqObj.id}: ${err.message}`, i);
        }
      }
    }

    // All sequences processed
    if (onComplete) {
      onComplete();
    }
  }
};

// Export for use in other modules
window.BlastAPI = BlastAPI;