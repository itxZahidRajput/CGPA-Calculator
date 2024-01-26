function downloadPDF() {
    // Get the HTML content of the result section
    const resultSection = document.querySelector('.table');
    const resultHTML = resultSection.outerHTML;

    // Create a new jsPDF instance
    const pdf = new jsPDF();

    // Add HTML content to the PDF
    pdf.fromHTML(resultHTML, 15, 15);

    // Save the PDF file
    pdf.save('result.pdf');
}
