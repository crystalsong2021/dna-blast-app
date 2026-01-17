// results.js - Result rendering and table management

const ResultsRenderer = {
  /**
   * Format title for two-line display
   */
  formatTitle(title) {
    let cleanTitle = title.replace(/^gi\|\d+\|(?:gb|ref|emb|dbj)\|[^|]+\|\s*/, '');

    const patterns = [
      /^([A-Z][a-z]+\s+[a-z]+\s+(?:strain|isolate|chromosome)\s+[^\s,]+)/i,
      /^([A-Z][a-z]+\s+[a-z]+\s+strain\s+[A-Z0-9\-_]+)/i,
      /^([A-Z][a-z]+\s+[a-z]+\s+[A-Z0-9\-_]+)/,
      /^([A-Z][a-z]+\s+[a-z]+)/
    ];

    let line1 = '';
    let line2 = cleanTitle;

    for (const pattern of patterns) {
      const match = cleanTitle.match(pattern);
      if (match) {
        line1 = match[1];
        line2 = cleanTitle.substring(match[1].length).trim();
        line2 = line2.replace(/^[,\s]+/, '');
        break;
      }
    }

    if (!line1) {
      line1 = cleanTitle.substring(0, 40);
      line2 = cleanTitle.substring(40);
    }

    const maxLine2Length = 60;
    const line2Truncated = line2.length > maxLine2Length
      ? line2.substring(0, maxLine2Length) + '...'
      : line2;

    return { line1, line2: line2Truncated, full: cleanTitle };
  },

  /**
   * Create title cell HTML
   */
  createTitleCell(hit) {
    const formatted = this.formatTitle(hit.title);
    const cellId = `title-${Math.random().toString(36).substr(2, 9)}`;

    return `
      <td class="title-cell" id="${cellId}">
        <div class="title-text" data-full-title="${hit.title.replace(/"/g, '&quot;')}">
          <div class="title-line-1">${formatted.line1}</div>
          ${formatted.line2 ? `<div class="title-line-2">${formatted.line2}</div>` : ''}
        </div>
      </td>
    `;
  },

  /**
   * Add tooltip functionality to title cells
   */
  addTitleTooltips(container) {
    const titleCells = container.querySelectorAll('.title-text');
    let currentTooltip = null;

    titleCells.forEach(cell => {
      cell.addEventListener('mouseenter', () => {
        const fullTitle = cell.dataset.fullTitle;

        if (currentTooltip) currentTooltip.remove();

        const tooltip = document.createElement('div');
        tooltip.className = 'title-tooltip';
        tooltip.textContent = fullTitle;
        document.body.appendChild(tooltip);

        const rect = cell.getBoundingClientRect();
        tooltip.style.left = `${rect.left}px`;
        tooltip.style.top = `${rect.bottom + 10}px`;

        setTimeout(() => tooltip.classList.add('show'), 10);
        currentTooltip = tooltip;
      });

      cell.addEventListener('mouseleave', () => {
        if (currentTooltip) {
          currentTooltip.classList.remove('show');
          setTimeout(() => {
            if (currentTooltip) {
              currentTooltip.remove();
              currentTooltip = null;
            }
          }, 200);
        }
      });

      cell.addEventListener('click', () => {
        cell.classList.toggle('title-expanded');
      });
    });
  },

  /**
   * Create sortable table
   */
  createSortableTable(hits, tabId) {
    let sortColumn = null;
    let sortDirection = 'asc';
    let sortedHits = [...hits];

    const renderTable = () => {
      const tableHTML = `
        <table class="table table-striped table-hover results-table">
          <thead>
            <tr>
              <th class="sortable" data-column="index">#</th>
              <th class="sortable" data-column="title">Description</th>
              <th class="sortable" data-column="accession">Accession</th>
              <th class="sortable" data-column="alignment_length">Align Length</th>
              <th class="sortable" data-column="e_value">E-value</th>
              <th class="sortable" data-column="percent_identity">Identity %</th>
            </tr>
          </thead>
          <tbody>
            ${sortedHits.map((hit, idx) => `
              <tr>
                <td>${idx + 1}</td>
                ${this.createTitleCell(hit)}
                <td class="mono">${hit.accession}</td>
                <td>${hit.alignment_length}</td>
                <td class="mono">${window.UIHelpers.formatEValue(hit.e_value)}</td>
                <td>${hit.percent_identity}%</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      const container = document.querySelector(`#${tabId} .table-container`);
      container.innerHTML = tableHTML;

      this.addTitleTooltips(container);

      const headers = container.querySelectorAll('th.sortable');
      headers.forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        if (th.dataset.column === sortColumn) {
          th.classList.add(sortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
        }
      });

      headers.forEach(th => {
        th.addEventListener('click', () => {
          const column = th.dataset.column;

          if (sortColumn === column) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
          } else {
            sortColumn = column;
            sortDirection = 'asc';
          }

          sortedHits = [...hits].sort((a, b) => {
            let aVal, bVal;

            if (column === 'index') {
              aVal = hits.indexOf(a);
              bVal = hits.indexOf(b);
            } else if (column === 'title' || column === 'accession') {
              aVal = a[column].toLowerCase();
              bVal = b[column].toLowerCase();
            } else {
              aVal = parseFloat(a[column]);
              bVal = parseFloat(b[column]);
            }

            if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
            if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
            return 0;
          });

          renderTable();
        });
      });
    };

    renderTable();
  },

  /**
   * Add a result tab as soon as result arrives (streaming approach)
   */
  addResultTab(result, index) {
    const elements = window.DOMElements;
    elements.resultsContainer.style.display = 'block';

    const tabId = `result-tab-${index}`;
    const isActive = index === 0;

    // Create tab button
    const tabLi = document.createElement('li');
    tabLi.className = 'nav-item';
    tabLi.innerHTML = `
      <button class="nav-link ${isActive ? 'active' : ''}"
              data-bs-toggle="tab"
              data-bs-target="#${tabId}"
              type="button"
              role="tab">
        ${result.sequence_id}
      </button>
    `;
    elements.resultsTabs.appendChild(tabLi);

    // Create tab content
    const tabContent = document.createElement('div');
    tabContent.className = `tab-pane fade ${isActive ? 'show active' : ''}`;
    tabContent.id = tabId;
    tabContent.innerHTML = `
      <div class="query-info">
        <strong>Query ID:</strong> ${result.sequence_id} |
        <strong>Length:</strong> ${result.query_length}bp |
        <strong>Hits Found:</strong> ${result.hits.length}
      </div>
      ${result.hits.length === 0
        ? '<div class="no-hits">No BLAST hits found for this sequence</div>'
        : '<div class="table-container"></div>'
      }
    `;
    elements.resultsTabContent.appendChild(tabContent);

    // Create sortable table if there are hits
    if (result.hits.length > 0) {
      this.createSortableTable(result.hits, tabId);
    }

    // Scroll to results on first tab
    if (index === 0) {
      elements.resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};

// Export for use in other modules
window.ResultsRenderer = ResultsRenderer;